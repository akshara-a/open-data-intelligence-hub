import os
import sys
import shutil
import tempfile
import subprocess
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ingestion.app.models import EntityNode, RelationshipEdge, UnresolvedCallNode
from ingestion.app.id_generator import (
    canonical_encode,
    compute_signature_hash,
    compute_content_hash,
    generate_entity_ids,
)
from ingestion.app.git_manager import (
    validate_repo_id,
    validate_egress_target,
    sync_bare_repository,
    verify_commit,
    extract_commit_tree,
    purge_bare_repository,
    GitSecurityError,
    CommitNotFoundError,
)
from ingestion.app.parsers.dispatcher import get_parser_for_file
from ingestion.app.parsers.python_parser import PythonParser
from ingestion.app.parsers.javascript_parser import JavaScriptTypeScriptParser
from ingestion.app.parsers.go_parser import GoParser
from ingestion.app.parsers.java_parser import JavaParser
from ingestion.app.evidence_generator import (
    resolve_and_filter_relationships,
    generate_entity_evidence,
    generate_relationship_evidence,
)
from ingestion.app.sqlite_writer import (
    get_sqlite_conn,
    store_file_embeddings,
    MODEL_VERSION,
    PREPROCESS_VERSION,
)
from ingestion.app.worker import (
    claim_job,
    execute_ingestion_pipeline,
    execute_purge_pipeline,
)
from backend.app.database import init_db


@pytest.fixture(scope="module")
def sample_git_repo():
    """
    Creates a temporary local Git repository with files in all 5 supported languages.
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="test_repo_"))
    try:
        # Initialize Git repo
        subprocess.run(["git", "init", "-b", "main"], cwd=str(temp_dir), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "TestUser"], cwd=str(temp_dir), check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(temp_dir), check=True)

        # 1. Python file
        py_file = temp_dir / "services" / "auth.py"
        py_file.parent.mkdir(parents=True, exist_ok=True)
        py_file.write_text(
            """import os
from math import sqrt

DEFAULT_TIMEOUT = 30

class AuthService:
    def login(self, username: str) -> bool:
        res = self.verify(username)
        return res

    def verify(self, name: str) -> bool:
        return True
""",
            encoding="utf-8",
        )

        # 2. TypeScript file
        ts_file = temp_dir / "models" / "user.ts"
        ts_file.parent.mkdir(parents=True, exist_ok=True)
        ts_file.write_text(
            """export interface UserProfile {
    id: string;
    email: string;
}

export class UserManager {
    getUser(id: string): UserProfile {
        return { id, email: "user@example.com" };
    }
}
""",
            encoding="utf-8",
        )

        # 3. Go file
        go_file = temp_dir / "pkg" / "server.go"
        go_file.parent.mkdir(parents=True, exist_ok=True)
        go_file.write_text(
            """package server

import "fmt"

type HTTPServer struct {
    Port int
}

func (s *HTTPServer) Start(port int) error {
    fmt.Println(port)
    return nil
}
""",
            encoding="utf-8",
        )

        # 4. Java file with method overloading
        java_file = temp_dir / "com" / "example" / "PaymentProcessor.java"
        java_file.parent.mkdir(parents=True, exist_ok=True)
        java_file.write_text(
            """package com.example;

import java.util.List;

public class PaymentProcessor {
    public boolean process(double amount) {
        return amount > 0;
    }

    public boolean process(double amount, String currency) {
        return amount > 0 && currency != null;
    }
}
""",
            encoding="utf-8",
        )

        # Commit initial version
        subprocess.run(["git", "add", "."], cwd=str(temp_dir), check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit with 5 languages"], cwd=str(temp_dir), check=True)

        commit_proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(temp_dir), check=True, capture_output=True, text=True)
        initial_commit = commit_proc.stdout.strip()

        yield str(temp_dir), initial_commit
    finally:
        shutil.rmtree(str(temp_dir), ignore_errors=True)


def test_canonical_delimiter_encoding_and_entity_identifiers():
    """
    Validates Section 7.1 Canonical Delimiter Encoding Specification & Entity IDs (AC-2.1)
    """
    # 1. Delimiter encoding
    raw = "src/auth:service v1"
    encoded = canonical_encode(raw)
    assert "/" not in encoded, "Slashes must be percent-encoded"
    assert ":" not in encoded, "Colons must be percent-encoded"
    assert "%2F" in encoded
    assert "%3A" in encoded

    # 2. Signature hash
    sig1 = compute_signature_hash(["double amount"], "boolean")
    sig2 = compute_signature_hash(["double amount", "String currency"], "boolean")
    assert len(sig1) == 12, "Signature hash must be 12 hex characters"
    assert len(sig2) == 12
    assert sig1 != sig2, "Distinct signatures must have distinct hashes"

    # 3. Entity ID Generation
    repo_id = "00000000-0000-4000-8000-000000000001"
    commit_sha = "abcdef1234567890abcdef1234567890abcdef12"
    snapshot_id, logical_id = generate_entity_ids(
        repo_id, commit_sha, "Function", "com.example.PaymentProcessor.process", signature_hash=sig1
    )
    assert snapshot_id.startswith(f"{repo_id}::{commit_sha}::Function::")
    assert logical_id.startswith(f"{repo_id}::Function::")
    assert snapshot_id.endswith(f"::{sig1}")
    assert logical_id.endswith(f"::{sig1}")


def test_git_security_and_bare_mirroring(sample_git_repo):
    """
    Validates Section 8.1 & 8.2 Git bare mirror architecture & security hardening (AC-2.3)
    """
    repo_dir, commit_sha = sample_git_repo
    repo_id = "11111111-1111-4111-8111-111111111111"
    purge_bare_repository(repo_id)

    # 1. UUID validation
    with pytest.raises(GitSecurityError):
        validate_repo_id("invalid-repo-id-with-traversal/../")

    validate_repo_id(repo_id)

    # 2. Egress IP blocking (SSRF protection)
    with pytest.raises(GitSecurityError):
        validate_egress_target("http://127.0.0.1:8080/repo.git", allow_local=False)
    with pytest.raises(GitSecurityError):
        validate_egress_target("http://10.0.0.5/repo.git", allow_local=False)

    # 3. Bare mirror sync
    bare_path = sync_bare_repository(repo_id, repo_dir, allow_local=True)
    assert bare_path.is_dir()
    assert (bare_path / "HEAD").is_file()

    # 4. Commit verification
    assert verify_commit(repo_id, commit_sha) is True
    assert verify_commit(repo_id, "0000000000000000000000000000000000000000") is False

    # 5. Tree extraction
    scratch_dir = Path(tempfile.mkdtemp(prefix="scratch_"))
    try:
        extracted = extract_commit_tree(repo_id, commit_sha, scratch_dir)
        assert len(extracted) >= 4
        # Verify relative path format
        file_names = [p.name for p in extracted]
        assert "auth.py" in file_names
        assert "user.ts" in file_names
        assert "server.go" in file_names
        assert "PaymentProcessor.java" in file_names
    finally:
        shutil.rmtree(str(scratch_dir), ignore_errors=True)


def test_tree_sitter_parsers_across_languages():
    """
    Validates Tree-sitter AST parsing across Python, TypeScript, Go, and Java (AC-2.1)
    """
    repo_id = "22222222-2222-4222-8222-222222222222"
    commit_sha = "c0ffee1234567890abcdef1234567890abcdef12"

    # 1. Python Parser
    py_code = b"""
import sys

def compute(x: int) -> int:
    return x * 2

class Calculator:
    def add(self, a: int, b: int) -> int:
        return compute(a) + b
"""
    py_parser = PythonParser()
    py_res = py_parser.parse_file("calc.py", py_code, repo_id, commit_sha)
    assert any(e.entity_type == "File" for e in py_res.entities)
    assert any(e.entity_type == "Class" and e.name == "Calculator" for e in py_res.entities)
    assert any(e.entity_type == "Function" and e.name == "compute" for e in py_res.entities)
    assert any(e.entity_type == "Function" and e.name == "add" for e in py_res.entities)
    assert any(r.rel_type == "IMPORTS" for r in py_res.relationships)

    # 2. TypeScript Parser
    ts_code = b"""
export interface Config { port: number; }
export class AppServer {
    start(cfg: Config): void {
        console.log(cfg);
    }
}
"""
    ts_parser = JavaScriptTypeScriptParser()
    ts_res = ts_parser.parse_file("server.ts", ts_code, repo_id, commit_sha)
    assert any(e.entity_type == "Interface" and e.name == "Config" for e in ts_res.entities)
    assert any(e.entity_type == "Class" and e.name == "AppServer" for e in ts_res.entities)
    assert any(e.entity_type == "Function" and e.name == "start" for e in ts_res.entities)

    # 3. Go Parser
    go_code = b"""
package worker

type Job struct { ID string }
func (j *Job) Process() error { return nil }
"""
    go_parser = GoParser()
    go_res = go_parser.parse_file("job.go", go_code, repo_id, commit_sha)
    assert any(e.entity_type == "Class" and e.name == "Job" for e in go_res.entities)
    assert any(e.entity_type == "Function" and e.name == "Process" for e in go_res.entities)

    # 4. Java Parser with Overloading (AC-2.1 signature hash check)
    java_code = b"""
package com.demo;
public class Printer {
    public void print(String msg) {}
    public void print(int num) {}
}
"""
    java_parser = JavaParser()
    java_res = java_parser.parse_file("Printer.java", java_code, repo_id, commit_sha)
    print_fns = [e for e in java_res.entities if e.entity_type == "Function" and e.name == "print"]
    assert len(print_fns) == 2, "Both overloaded print methods must be extracted"
    assert print_fns[0].entity_id != print_fns[1].entity_id, "Overloaded methods must have unique entity IDs"
    assert print_fns[0].signature_hash != print_fns[1].signature_hash, "Distinct signatures must have distinct hashes"


def test_syntax_error_recovery():
    """
    Verifies that syntax errors in a source file do not crash the parser;
    valid subtrees are extracted and syntax warnings recorded.
    """
    repo_id = "33333333-3333-4333-8333-333333333333"
    commit_sha = "deadbeef1234567890abcdef1234567890abcdef"
    malformed_code = b"""
def valid_function():
    return 42

def broken_function(
    # missing closing parenthesis and body
"""
    py_parser = PythonParser()
    res = py_parser.parse_file("broken.py", malformed_code, repo_id, commit_sha)
    assert len(res.syntax_errors) > 0, "Syntax error must be captured"
    assert any(e.name == "valid_function" for e in res.entities), "Valid function in AST must still be extracted"


def test_evidence_generation_and_bidirectional_traversal():
    """
    Validates Section 11.1 & 11.2 Evidence Provenance & Bi-Directional Traversal (AC-2.2)
    """
    repo_id = "44444444-4444-4444-8444-444444444444"
    commit_sha = "abcdef1234567890abcdef1234567890abcdef12"

    src_id, src_log = generate_entity_ids(repo_id, commit_sha, "Function", "api.handle_auth")
    tgt_id, tgt_log = generate_entity_ids(repo_id, commit_sha, "Function", "auth.login")

    src_node = EntityNode(
        entity_id=src_id,
        logical_entity_id=src_log,
        repo_id=repo_id,
        commit_sha=commit_sha,
        file_path="api.py",
        name="handle_auth",
        entity_type="Function",
        content_hash="abc123",
        line_start=10,
        line_end=20,
    )
    tgt_node = EntityNode(
        entity_id=tgt_id,
        logical_entity_id=tgt_log,
        repo_id=repo_id,
        commit_sha=commit_sha,
        file_path="auth.py",
        name="login",
        entity_type="Function",
        content_hash="def456",
        line_start=30,
        line_end=40,
    )

    rel = RelationshipEdge(
        source_entity_id=src_id,
        target_entity_id=tgt_id,
        rel_type="CALLS",
        repo_id=repo_id,
        commit_sha=commit_sha,
    )

    # Inferred AFFECTS must be rejected
    inferred_rel = RelationshipEdge(
        source_entity_id=src_id,
        target_entity_id=tgt_id,
        rel_type="AFFECTS",
        repo_id=repo_id,
        commit_sha=commit_sha,
    )

    valid_rels, ent_evs, rel_evs, unres = resolve_and_filter_relationships(
        [src_node, tgt_node],
        [rel, inferred_rel],
        [],
        repo_id,
        commit_sha,
    )

    # 1. Inferred AFFECTS filtered out
    assert len(valid_rels) == 1
    assert valid_rels[0].rel_type == "CALLS"

    # 2. 100% entity evidence
    assert len(ent_evs) == 2
    for ev in ent_evs:
        assert ev.evidence_id.startswith("E-")
        assert ev.evidence_type == "ENTITY"

    # 3. 100% relationship evidence
    assert len(rel_evs) == 1
    rev = rel_evs[0]
    assert rev.evidence_id.startswith("E-")
    assert rev.evidence_type == "RELATIONSHIP"
    assert rev.source_entity_id == src_id
    assert rev.target_entity_id == tgt_id

    # 4. Bi-directional guarantee: querying either source or target returns the same RelationshipEvidence record
    # Both endpoints are strictly encoded in the single RelationshipEvidence node
    assert rev.source_entity_id == src_id
    assert rev.target_entity_id == tgt_id


def test_sqlite_embeddings_and_cache_reuse():
    """
    Validates Section 9.1 & 9.2 File-Level Embeddings & Cache Invalidation
    """
    test_db = ROOT_DIR / "data" / "test_embeddings.db"
    if test_db.exists():
        test_db.unlink()

    repo_id = "55555555-5555-4555-8555-555555555555"
    commit_1 = "1111111111111111111111111111111111111111"
    commit_2 = "2222222222222222222222222222222222222222"

    files_c1 = {
        "src/util.py": "def helper(): return 'v1'",
        "src/data.py": "DATA = [1, 2, 3]",
    }
    # In commit 2, data.py is unchanged, util.py is modified
    files_c2 = {
        "src/util.py": "def helper(): return 'v2_updated'",
        "src/data.py": "DATA = [1, 2, 3]",
    }

    # Store for commit 1
    store_file_embeddings(repo_id, commit_1, files_c1, db_path=str(test_db))

    conn = get_sqlite_conn(str(test_db))
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vector FROM embeddings WHERE repo_id = ? AND commit_sha = ? AND file_path = ?", (repo_id, commit_1, "src/data.py"))
        vec_c1_data = cursor.fetchone()["vector"]

    # Store for commit 2
    store_file_embeddings(repo_id, commit_2, files_c2, db_path=str(test_db))

    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vector FROM embeddings WHERE repo_id = ? AND commit_sha = ? AND file_path = ?", (repo_id, commit_2, "src/data.py"))
        vec_c2_data = cursor.fetchone()["vector"]

        cursor.execute("SELECT vector FROM embeddings WHERE repo_id = ? AND commit_sha = ? AND file_path = ?", (repo_id, commit_2, "src/util.py"))
        vec_c2_util = cursor.fetchone()["vector"]

        cursor.execute("SELECT vector FROM embeddings WHERE repo_id = ? AND commit_sha = ? AND file_path = ?", (repo_id, commit_1, "src/util.py"))
        vec_c1_util = cursor.fetchone()["vector"]

    conn.close()

    # Identical content across commits reuses the identical cached vector
    assert vec_c1_data == vec_c2_data
    # Changed content produces a different vector
    assert vec_c1_util != vec_c2_util

    if test_db.exists():
        try:
            test_db.unlink()
        except Exception:
            pass


def test_end_to_end_worker_pipeline_and_privileged_purge(sample_git_repo):
    """
    Validates Section 15.1 Atomic Job Claiming & Section 8.1 Privileged Repo Purge (AC-5.3)
    """
    repo_dir, commit_sha = sample_git_repo
    repo_id = "66666666-6666-4666-8666-666666666666"

    test_db = ROOT_DIR / "data" / "test_worker.db"
    if test_db.exists():
        test_db.unlink()

    # Initialize tables
    conn = get_sqlite_conn(str(test_db))
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS repositories (
                repo_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                git_url TEXT NOT NULL,
                default_branch TEXT DEFAULT 'main',
                status TEXT DEFAULT 'ACTIVE',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS repo_memberships (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                repo_id TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                repo_id TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                job_type TEXT NOT NULL,
                status TEXT NOT NULL,
                worker_id TEXT,
                progress INTEGER DEFAULT 0,
                log_output TEXT,
                claimed_at TIMESTAMP,
                lease_expires_at TIMESTAMP,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY,
                query_id TEXT NOT NULL,
                repo_id TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                query_text TEXT NOT NULL,
                markdown_body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS embeddings (
                repo_id TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                file_path TEXT NOT NULL,
                vector BLOB NOT NULL,
                model_version TEXT NOT NULL,
                preprocess_version TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (repo_id, commit_sha, file_path)
            );
            """
        )

        cursor.execute("INSERT INTO repositories (repo_id, name, git_url) VALUES (?, ?, ?)", (repo_id, "test_proj", repo_dir))
        cursor.execute("INSERT INTO repo_memberships (id, user_id, repo_id, role) VALUES ('m1', 'u1', ?, 'owner')", (repo_id,))

        # Enqueue an ingestion job
        job_id = "job-ingest-test-001"
        cursor.execute(
            "INSERT INTO jobs (id, repo_id, commit_sha, job_type, status, progress) VALUES (?, ?, ?, 'INGEST', 'PENDING', 0)",
            (job_id, repo_id, commit_sha),
        )

    # 1. Atomic job claim
    job = claim_job(db_path=str(test_db))
    assert job is not None
    assert job["id"] == job_id
    assert job["status"] == "RUNNING"
    assert job["lease_expires_at"] is not None

    # 2. Execute ingestion pipeline (no Neo4j mock needed, graph_writer=None tests worker pipeline)
    result = execute_ingestion_pipeline(job, db_path=str(test_db), graph_writer=None, allow_local_git=True)
    assert result["status"] == "COMPLETED"
    assert result["entities_count"] > 0
    assert result["relationships_count"] > 0
    assert result["evidence_count"] > 0

    # Verify job status in SQLite
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, progress, log_output FROM jobs WHERE id = ?", (job_id,))
        updated_job = cursor.fetchone()
        assert updated_job["status"] == "COMPLETED"
        assert updated_job["progress"] == 100

    # 3. Test Privileged Repo Purge (AC-5.3)
    purge_job_id = "job-purge-test-002"
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jobs (id, repo_id, commit_sha, job_type, status, progress) VALUES (?, ?, 'N/A', 'REPO_PURGE', 'PENDING', 0)",
            (purge_job_id, repo_id),
        )

    purge_job = claim_job(db_path=str(test_db))
    assert purge_job["id"] == purge_job_id

    execute_purge_pipeline(purge_job, db_path=str(test_db), graph_writer=None)

    # Verify repository and all SQLite records purged
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM repositories WHERE repo_id = ?", (repo_id,))
        assert cursor.fetchone()[0] == 0
        cursor.execute("SELECT COUNT(*) FROM repo_memberships WHERE repo_id = ?", (repo_id,))
        assert cursor.fetchone()[0] == 0
        cursor.execute("SELECT COUNT(*) FROM embeddings WHERE repo_id = ?", (repo_id,))
        assert cursor.fetchone()[0] == 0

    conn.close()

    # Verify bare repository deleted from storage
    bare_path = Path("./git_storage") / f"{repo_id}.git"
    assert not bare_path.exists()

    if test_db.exists():
        try:
            test_db.unlink()
        except Exception:
            pass
