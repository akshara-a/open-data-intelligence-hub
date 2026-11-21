import os
import time
import shutil
import tempfile
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List

from .models import EntityNode, RelationshipEdge, UnresolvedCallNode
from .git_manager import (
    sync_bare_repository,
    verify_commit,
    extract_commit_tree,
    purge_bare_repository,
    CommitNotFoundError,
    GitSecurityError,
)
from .parsers.dispatcher import get_parser_for_file
from .evidence_generator import resolve_and_filter_relationships
from .graph_writer import Neo4jGraphWriter
from .sqlite_writer import get_sqlite_conn, store_file_embeddings

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/app_state.db")
WORKER_ID = f"worker_{os.getpid()}_{int(time.time())}"


def update_job_progress(
    job_id: str,
    status: str,
    progress: int,
    log_output: Optional[str] = None,
    db_path: Optional[str] = None,
):
    conn = get_sqlite_conn(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE jobs
            SET status = :status,
                progress = :progress,
                log_output = COALESCE(:log_output, log_output),
                lease_expires_at = datetime('now', '+5 minutes')
            WHERE id = :id
            """,
            {"status": status, "progress": progress, "log_output": log_output, "id": job_id},
        )


def claim_job(db_path: Optional[str] = None):
    """
    Implements Atomic Job Claiming with Worker Leases per Section 15.1
    """
    try:
        conn = get_sqlite_conn(db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute(
                """
                UPDATE jobs
                SET status = 'RUNNING',
                    worker_id = :worker_id,
                    claimed_at = CURRENT_TIMESTAMP,
                    lease_expires_at = datetime('now', '+5 minutes')
                WHERE id = (
                    SELECT id FROM jobs
                    WHERE status = 'PENDING'
                       OR (status = 'RUNNING' AND lease_expires_at < CURRENT_TIMESTAMP)
                    ORDER BY created_at ASC
                    LIMIT 1
                )
                RETURNING *;
                """,
                {"worker_id": WORKER_ID},
            )
            job = cursor.fetchone()
            return job
    except Exception as e:
        return None


def execute_ingestion_pipeline(
    job: Any,
    db_path: Optional[str] = None,
    graph_writer: Optional[Neo4jGraphWriter] = None,
    allow_local_git: bool = False,
) -> Dict[str, Any]:
    job_id = job["id"]
    repo_id = job["repo_id"]
    commit_sha = job["commit_sha"]

    scratch_base = Path(tempfile.gettempdir()) / "scratch"
    scratch_dir = scratch_base / str(job_id)

    try:
        # Retrieve git_url from repositories table
        conn = get_sqlite_conn(db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT git_url FROM repositories WHERE repo_id = ?", (repo_id,))
            repo_row = cursor.fetchone()
            if not repo_row:
                raise ValueError(f"Repository {repo_id} not found in database")
            git_url = repo_row["git_url"]

        # Stage 1: Bare repo sync and commit verification (10%)
        update_job_progress(job_id, "RUNNING", 10, f"Synchronizing bare repository from {git_url}", db_path=db_path)
        sync_bare_repository(repo_id, git_url, allow_local=allow_local_git)
        if not verify_commit(repo_id, commit_sha):
            raise CommitNotFoundError(f"Commit SHA {commit_sha} could not be verified in repository {repo_id}")

        # Stage 2: Safe scratch extraction (30%)
        update_job_progress(job_id, "RUNNING", 30, f"Extracting tree for commit {commit_sha}", db_path=db_path)
        extracted_rel_files = extract_commit_tree(repo_id, commit_sha, scratch_dir)

        # Stage 3: Static parsing across supported languages (60%)
        update_job_progress(job_id, "RUNNING", 60, f"Parsing {len(extracted_rel_files)} source files with Tree-sitter", db_path=db_path)
        all_entities: List[EntityNode] = []
        all_relationships: List[RelationshipEdge] = []
        all_unresolved: List[UnresolvedCallNode] = []
        file_contents: Dict[str, str] = {}
        syntax_warnings: List[str] = []

        for rel_path in extracted_rel_files:
            str_path = str(rel_path).replace("\\", "/")
            full_path = scratch_dir / rel_path
            parser = get_parser_for_file(str_path)
            if not parser:
                continue

            try:
                code_bytes = full_path.read_bytes()
                file_contents[str_path] = code_bytes.decode("utf-8", errors="replace")
                parse_res = parser.parse_file(str_path, code_bytes, repo_id, commit_sha)
                all_entities.extend(parse_res.entities)
                all_relationships.extend(parse_res.relationships)
                all_unresolved.extend(parse_res.unresolved_calls)
                if parse_res.syntax_errors:
                    syntax_warnings.extend(parse_res.syntax_errors)
            except Exception as fe:
                syntax_warnings.append(f"Error parsing file {str_path}: {fe}")

        # Stage 4: Relationship resolution, evidence generation & isolation (80%)
        update_job_progress(job_id, "RUNNING", 80, "Resolving snapshot relationships and generating evidence provenance", db_path=db_path)
        valid_rels, ent_evidences, rel_evidences, final_unresolved = resolve_and_filter_relationships(
            all_entities, all_relationships, all_unresolved, repo_id, commit_sha
        )

        # Stage 5: Persistence to Neo4j graph & SQLite embeddings (90%)
        update_job_progress(job_id, "RUNNING", 90, "Writing graph entities and vector embeddings", db_path=db_path)
        if graph_writer is not None:
            try:
                graph_writer.ensure_schema_constraints()
                graph_writer.persist_snapshot(
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                    entities=all_entities,
                    relationships=valid_rels,
                    entity_evidences=ent_evidences,
                    relationship_evidences=rel_evidences,
                    unresolved_calls=final_unresolved,
                )
            except Exception as ge:
                syntax_warnings.append(f"Neo4j graph write warning: {ge}")

        # Store file embeddings in SQLite
        store_file_embeddings(repo_id, commit_sha, file_contents, db_path=db_path)

        # Stage 6: Finalize job (100%)
        log_summary = (
            f"Ingested {len(all_entities)} entities, {len(valid_rels)} verified relationships, "
            f"{len(ent_evidences) + len(rel_evidences)} evidences, {len(final_unresolved)} unresolved calls."
        )
        if syntax_warnings:
            log_summary += f" Warnings: {'; '.join(syntax_warnings[:5])}"

        update_job_progress(job_id, "COMPLETED", 100, log_summary, db_path=db_path)
        return {
            "entities_count": len(all_entities),
            "relationships_count": len(valid_rels),
            "evidence_count": len(ent_evidences) + len(rel_evidences),
            "unresolved_calls_count": len(final_unresolved),
            "status": "COMPLETED",
        }

    except Exception as e:
        err_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        retries = job["retry_count"] if "retry_count" in job.keys() else 0
        if retries < 2:
            conn = get_sqlite_conn(db_path)
            with conn:
                conn.execute(
                    "UPDATE jobs SET status = 'PENDING', retry_count = retry_count + 1, log_output = ? WHERE id = ?",
                    (f"Retry triggered: {err_msg}", job_id),
                )
        else:
            update_job_progress(job_id, "FAILED", job["progress"], f"Fatal error: {err_msg}", db_path=db_path)
        raise
    finally:
        # Cleanup ephemeral scratch workspace per Section 8.3
        if scratch_dir.exists():
            shutil.rmtree(str(scratch_dir), ignore_errors=True)


def execute_purge_pipeline(
    job: Any,
    db_path: Optional[str] = None,
    graph_writer: Optional[Neo4jGraphWriter] = None,
):
    """
    Executes privileged repository deletion per Section 8.1 / AC-5.3
    """
    job_id = job["id"]
    repo_id = job["repo_id"]

    try:
        update_job_progress(job_id, "RUNNING", 10, f"Purging repository {repo_id}", db_path=db_path)

        # 1. Purge Neo4j graph nodes
        if graph_writer is not None:
            try:
                graph_writer.purge_repository(repo_id)
            except Exception as ge:
                pass

        # 2. Purge bare Git mirror
        purge_bare_repository(repo_id)

        # 3. Purge SQLite tables in atomic transaction
        conn = get_sqlite_conn(db_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("DELETE FROM embeddings WHERE repo_id = ?", (repo_id,))
            cursor.execute("DELETE FROM reports WHERE repo_id = ?", (repo_id,))
            cursor.execute("DELETE FROM repo_memberships WHERE repo_id = ?", (repo_id,))
            cursor.execute("DELETE FROM repositories WHERE repo_id = ?", (repo_id,))

        update_job_progress(job_id, "COMPLETED", 100, f"Successfully purged repository {repo_id}", db_path=db_path)
    except Exception as e:
        err_msg = f"Purge failure: {e}\n{traceback.format_exc()}"
        update_job_progress(job_id, "FAILED", 0, err_msg, db_path=db_path)
        raise


def run_worker_loop(
    single_run: bool = False,
    db_path: Optional[str] = None,
    graph_writer: Optional[Neo4jGraphWriter] = None,
    allow_local_git: bool = False,
):
    actual_writer = graph_writer or Neo4jGraphWriter()
    allow_local = allow_local_git or os.getenv("ALLOW_LOCAL_GIT", "0") == "1"
    print(f"Ingestion worker {WORKER_ID} active. Monitoring queue at {db_path or SQLITE_DB_PATH}...", flush=True)
    while True:
        job = claim_job(db_path=db_path)
        if job:
            job_type = job["job_type"]
            print(f"Claimed job {job['id']} (type: {job_type}) for repo {job['repo_id']}", flush=True)
            try:
                if job_type in ("INGEST", "COMMIT_INGEST"):
                    execute_ingestion_pipeline(job, db_path=db_path, graph_writer=actual_writer, allow_local_git=allow_local)
                elif job_type == "REPO_PURGE":
                    execute_purge_pipeline(job, db_path=db_path, graph_writer=actual_writer)
            except Exception as e:
                print(f"Worker job error: {e}", flush=True)
        if single_run:
            break
        time.sleep(2)


if __name__ == "__main__":
    run_worker_loop()
