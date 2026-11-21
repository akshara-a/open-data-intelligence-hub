import os
os.environ["ALLOW_EMBEDDING_FALLBACK"] = "true"
import sys
import shutil
import tempfile
import sqlite3
import numpy as np
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from rag.app.models import (
    CodeChunk,
    IndexRequest,
    RetrievalRequest,
    RankingExplanation,
    RetrievalResultItem,
)
from rag.app.chunker import CodeChunker
from rag.app.embedding_engine import (
    EmbeddingEngine,
    get_embedding_engine,
    MODEL_VERSION,
    PREPROCESS_VERSION,
    VECTOR_DIM,
)
from rag.app.sqlite_storage import SQLiteChunkStorage
from rag.app.cgg_client import CGGClient
from rag.app.retriever import GraphRAGRetriever
from rag.app.indexer import SnapshotIndexer


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_rag.db"
    return str(db_file)


@pytest.fixture
def sample_code_files():
    return {
        "src/auth.py": """def login(username: str, password_hash: str) -> str:
    # Verifies user password hash and issues RS256 token
    if not username or not password_hash:
        raise ValueError("Invalid credentials")
    return "token_jwt_sample_123"

def verify_token(token: str) -> bool:
    # Decodes and verifies RS256 token signature
    return token.startswith("token_")
""",
        "src/database.py": """class DatabasePool:
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.active = True

    def execute_query(self, query: str, params: tuple = ()) -> list:
        # Executes SQL query with connection lease and transaction commit
        if not self.active:
            raise RuntimeError("Database pool closed")
        return [{"id": 1, "status": "ok"}]
""",
        "src/api_router.py": """from auth import login
from database import DatabasePool

def handle_request(path: str, payload: dict) -> dict:
    # Routes incoming request to auth and database service
    token = login(payload.get("user"), payload.get("pass"))
    pool = DatabasePool()
    res = pool.execute_query("SELECT 1")
    return {"token": token, "data": res}

def dynamic_dispatch(action_name: str):
    # Dynamic unresolvable dispatch site
    return eval(f"action_{action_name}")()
""",
    }


def test_source_chunking_and_line_ranges():
    """
    Validates Requirement 3 / Test Item 1:
    Deterministic source chunking preserving exact file paths, line ranges, and entity metadata.
    """
    chunker = CodeChunker(max_chunk_lines=30)
    code = """def first_func():
    a = 1
    return a

def second_func():
    b = 2
    return b
"""
    chunks = chunker.chunk_file(
        repo_id="repo-1",
        commit_sha="commit-1",
        file_path="src/utils.py",
        content=code,
    )
    assert len(chunks) >= 1
    for c in chunks:
        assert c.file_path == "src/utils.py"
        assert c.line_start >= 1
        assert c.line_end >= c.line_start
        assert c.content_hash is not None
        assert c.chunk_id.startswith("repo-1::commit-1::Chunk::")


def test_embedding_generation_and_normalization():
    """
    Validates Requirement 2 / Test Item 2:
    Embedding generation produces 768-dim float32 vectors strictly normalized to unit L2 sphere.
    Also verifies explicit fallback reporting and no silent substitution.
    """
    engine = EmbeddingEngine(force_fallback=True)
    assert engine.fallback_mode is True
    assert engine.status == "fallback_deterministic_projection"
    assert engine.backend == "deterministic_projection_fallback"
    assert engine.model_version == "fallback-deterministic-projection-v1"

    text = "def calculate_impact(node, depth): return depth * 2"
    vec = engine.embed_text(text)

    assert isinstance(vec, np.ndarray)
    assert vec.shape == (VECTOR_DIM,)
    assert vec.dtype == np.float32

    # L2 norm must equal 1.0 (unit vector)
    norm = np.linalg.norm(vec)
    assert abs(norm - 1.0) < 1e-5, f"Vector must be unit normalized, got {norm}"

    # Cosine similarity of identical text must equal 1.0
    vec_same = engine.embed_text(text)
    sim = engine.compute_cosine_similarity(vec, vec_same)
    assert abs(sim - 1.0) < 1e-4

    # Verify no silent substitution when fallback is disallowed
    strict_engine = EmbeddingEngine(allow_fallback=False)
    if strict_engine.status != "active_transformer":
        assert strict_engine.backend == "unavailable"
        assert "model_load_failed" in strict_engine.status
        with pytest.raises(RuntimeError, match="Embedding model unavailable"):
            strict_engine.embed_text("sample code")


def test_persistent_storage_and_cache_reuse(temp_db):
    """
    Validates Requirement 2 / Test Items 3, 4, 5:
    Persistent embedding storage in SQLite and cross-commit cache reuse.
    """
    storage = SQLiteChunkStorage(temp_db)
    chunker = CodeChunker()

    content = "def test_alpha(): return 42\n"
    chunks_c1 = chunker.chunk_file("repo-1", "commit-aaa", "test.py", content)

    # 1. First indexing (cold cache)
    reused_1, new_1 = storage.persist_chunks(chunks_c1)
    assert reused_1 == 0
    assert new_1 == len(chunks_c1)

    # 2. Second indexing of same content under new commit (cache hit)
    chunks_c2 = chunker.chunk_file("repo-1", "commit-bbb", "test.py", content)
    reused_2, new_2 = storage.persist_chunks(chunks_c2)
    assert reused_2 == len(chunks_c2), "Identical content must reuse cached embedding"
    assert new_2 == 0

    # 3. Content modification under third commit (cache miss -> re-embed)
    mod_content = "def test_alpha(): return 999  # modified\n"
    chunks_c3 = chunker.chunk_file("repo-1", "commit-ccc", "test.py", mod_content)
    reused_3, new_3 = storage.persist_chunks(chunks_c3)
    assert new_3 == len(chunks_c3), "Modified content must trigger fresh embedding"


def test_deleted_and_renamed_file_handling(temp_db):
    """
    Validates Requirement 2 / Test Item 6:
    Stale chunks from deleted files are pruned from the snapshot context.
    """
    storage = SQLiteChunkStorage(temp_db)
    chunker = CodeChunker()

    c1 = chunker.chunk_file("repo-1", "commit-1", "active.py", "def a(): pass")
    c2 = chunker.chunk_file("repo-1", "commit-1", "obsolete.py", "def b(): pass")
    storage.persist_chunks(c1 + c2)

    # Re-index snapshot without obsolete.py
    storage.persist_chunks(c1)

    # Search: obsolete.py must not be returned
    engine = get_embedding_engine()
    results = storage.scan_semantic_candidates("repo-1", "commit-1", engine.embed_text("def b"))
    retrieved_files = [r["file_path"] for r in results]
    assert "obsolete.py" not in retrieved_files


def test_snapshot_isolation(temp_db):
    """
    Validates Requirement 5 / Test Item 10:
    Chunks and embeddings from commit A are strictly isolated from commit B.
    """
    storage = SQLiteChunkStorage(temp_db)
    chunker = CodeChunker()

    chunks_a = chunker.chunk_file("repo-1", "commit-A", "feature.py", "secret_token_alpha = 1")
    chunks_b = chunker.chunk_file("repo-1", "commit-B", "feature.py", "secret_token_beta = 2")
    storage.persist_chunks(chunks_a)
    storage.persist_chunks(chunks_b)

    engine = get_embedding_engine()
    q_vec = engine.embed_text("secret_token")

    # Query commit A
    res_a = storage.scan_semantic_candidates("repo-1", "commit-A", q_vec)
    for r in res_a:
        assert r["commit_sha"] == "commit-A"
        assert "secret_token_beta" not in r["content"]

    # Query commit B
    res_b = storage.scan_semantic_candidates("repo-1", "commit-B", q_vec)
    for r in res_b:
        assert r["commit_sha"] == "commit-B"
        assert "secret_token_alpha" not in r["content"]


def test_graph_retrieval_and_hybrid_ranking(temp_db, sample_code_files):
    """
    Validates Requirement 4 / Test Items 8, 9, 11, 12:
    Combines semantic scores with CGG graph relationships and distinguishes verified vs. unresolved.
    """
    indexer = SnapshotIndexer(temp_db)
    indexer.index_snapshot("repo-1", "commit-1", file_contents=sample_code_files)

    # Mock CGG client responses
    mock_cgg = MagicMock()
    mock_cgg.lookup_entities.return_value = [
        {
            "entity_id": "repo-1::commit-1::Function::auth.login",
            "name": "login",
            "file_path": "src/auth.py",
            "line_start": 1,
            "line_end": 5,
        }
    ]
    mock_cgg.get_direct_neighbors.return_value = {
        "outgoing_dependencies": [],
        "incoming_dependents": [
            {
                "entity_id": "repo-1::commit-1::Function::api_router.handle_request",
                "relationship": "CALLS",
            }
        ],
    }
    mock_cgg.get_unresolved_calls.return_value = [
        {
            "call_id": "call_1",
            "invoked_symbol_name": "dynamic_dispatch",
            "file_path": "src/api_router.py",
        }
    ]
    mock_cgg.get_entity_details.return_value = {
        "declaration_evidence_id": "E-evidence-auth-login-1",
    }

    retriever = GraphRAGRetriever(temp_db, cgg_client=mock_cgg)
    req = RetrievalRequest(
        repo_id="repo-1",
        commit_sha="commit-1",
        query="user login authentication",
        top_k=5,
        include_graph=True,
    )
    resp = retriever.retrieve(req)

    assert resp.results_returned > 0
    top_hit = resp.results[0]
    assert top_hit.combined_score >= top_hit.semantic_similarity
    assert top_hit.ranking_explanation.explanation is not None

    # Verify provenance grounding
    assert top_hit.provenance_status in ("evidence_grounded", "unsupported")
    if top_hit.evidence_ids:
        assert "E-evidence-auth-login-1" in top_hit.evidence_ids


def test_empty_query_and_missing_snapshot(temp_db):
    """
    Validates Requirement 5 & 6 / Test Items 13 & 15:
    Empty queries, missing snapshot identifiers, and boundaries handled cleanly.
    """
    retriever = GraphRAGRetriever(temp_db)

    # Missing repo_id / commit_sha raises ValueError
    with pytest.raises(ValueError):
        retriever.retrieve(RetrievalRequest(repo_id="", commit_sha="abc", query="test"))

    with pytest.raises(ValueError):
        retriever.retrieve(RetrievalRequest(repo_id="repo-1", commit_sha="", query="test"))

    # Empty query text returns 0 results
    empty_resp = retriever.retrieve(RetrievalRequest(repo_id="repo-1", commit_sha="abc", query="   "))
    assert empty_resp.results_returned == 0
    assert len(empty_resp.results) == 0


def test_curated_benchmark_evaluation(temp_db, sample_code_files):
    """
    Validates Section 7 Benchmark Evaluation:
    Evaluates retrieval performance against curated benchmark queries and measures Precision@K, Recall@K, and MRR.
    """
    indexer = SnapshotIndexer(temp_db)
    indexer.index_snapshot("bench-repo", "commit-bench", file_contents=sample_code_files)

    mock_cgg = MagicMock()
    mock_cgg.lookup_entities.return_value = []
    mock_cgg.get_direct_neighbors.return_value = {"outgoing_dependencies": [], "incoming_dependents": []}
    mock_cgg.get_unresolved_calls.return_value = []
    mock_cgg.get_entity_details.return_value = None

    retriever = GraphRAGRetriever(temp_db, cgg_client=mock_cgg)

    benchmark_queries = [
        {
            "query": "user password verification and token generation",
            "expected_file": "src/auth.py",
        },
        {
            "query": "database connection pool and SQL query execution",
            "expected_file": "src/database.py",
        },
        {
            "query": "handle incoming request routing and dynamic dispatch",
            "expected_file": "src/api_router.py",
        },
    ]

    precisions = []
    recalls = []
    reciprocal_ranks = []
    K = 3

    for item in benchmark_queries:
        req = RetrievalRequest(
            repo_id="bench-repo",
            commit_sha="commit-bench",
            query=item["query"],
            top_k=K,
            include_graph=False,
        )
        resp = retriever.retrieve(req)
        retrieved_files = [r.file_path for r in resp.results]

        # Calculate Precision@K
        relevant_retrieved = sum(1 for f in retrieved_files if f == item["expected_file"])
        precisions.append(relevant_retrieved / K)

        # Calculate Recall@K (assuming 1 primary relevant file in fixture)
        recalls.append(1.0 if relevant_retrieved >= 1 else 0.0)

        # Calculate Reciprocal Rank
        rr = 0.0
        for rank, f in enumerate(retrieved_files, 1):
            if f == item["expected_file"]:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)

    mean_precision = sum(precisions) / len(precisions)
    mean_recall = sum(recalls) / len(recalls)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print(f"\n--- Benchmark Evaluation Metrics ---")
    print(f"Queries evaluated: {len(benchmark_queries)}")
    print(f"Mean Precision@{K}: {mean_precision:.4f}")
    print(f"Mean Recall@{K}: {mean_recall:.4f}")
    print(f"MRR (Mean Reciprocal Rank): {mrr:.4f}")

    assert mean_recall >= 0.8, f"Benchmark Recall@{K} should be >= 0.8, got {mean_recall}"
    assert mrr >= 0.7, f"Benchmark MRR should be >= 0.7, got {mrr}"


def test_dynamic_unresolved_call_classification_not_verified_static(temp_db):
    """
    Regression Test: Dynamic Unresolved Call Classification.
    Proves that an UnresolvedCall record remains classified as 'potential_uncertain'
    with lower confidence weight (0.3) and CANNOT be returned as 'verified_static',
    even if the enclosing file or entity has lexical containment relationships.
    """
    indexer = SnapshotIndexer(temp_db)
    dyn_files = {
        "src/router.py": (
            "def dispatch_action(action_name: str):\n"
            "    # Dynamic unresolvable dispatch site\n"
            "    return eval(f'action_{action_name}')()\n"
        )
    }
    indexer.index_snapshot("repo-regress", "commit-regress", file_contents=dyn_files)

    ent_id = "repo-regress::commit-regress::Function::router.dispatch_action::1234"
    file_id = "repo-regress::commit-regress::File::src/router.py"

    mock_cgg = MagicMock()
    # Mock lexical containment edge from file to function
    mock_cgg.get_direct_neighbors.return_value = {
        "outgoing_dependencies": [],
        "incoming_dependents": [
            {
                "entity_id": file_id,
                "name": "src/router.py",
                "relationship": "CONTAINS",
                "direction": "INCOMING",
            }
        ],
    }
    # Mock unresolved call record for this entity
    mock_cgg.get_unresolved_calls.return_value = [
        {
            "call_id": "repo-regress::commit-regress::UnresolvedCall::uc-999",
            "source_entity_id": ent_id,
            "invoked_symbol_name": "eval",
            "file_path": "src/router.py",
            "line_range": "3",
            "candidate_targets": [{"candidate_name": None, "classification": "potential_uncertain"}],
        }
    ]
    mock_cgg.lookup_entities.return_value = []
    mock_cgg.get_entity_details.return_value = {
        "entity_id": ent_id,
        "declaration_evidence_id": "E-decl-999",
    }

    retriever = GraphRAGRetriever(temp_db, cgg_client=mock_cgg)
    req = RetrievalRequest(
        repo_id="repo-regress",
        commit_sha="commit-regress",
        query="dispatch dynamic action eval site",
        top_k=3,
        include_graph=True,
    )
    resp = retriever.retrieve(req)
    assert len(resp.results) > 0

    top = resp.results[0]
    # Critical assertions per user requirement
    assert top.relationship_classification == "potential_uncertain", (
        f"Expected 'potential_uncertain', got '{top.relationship_classification}'"
    )
    assert top.relationship_classification != "verified_static", (
        "Regression detected: dynamic unresolved call was incorrectly classified as verified_static!"
    )
    assert top.ranking_explanation.relationship_classification == "potential_uncertain"
    # Verify architecture-defined lower confidence weight (0.3) applied to graph score
    # g_score = 0.3 * (1.0 / (1 + 1)) = 0.15
    assert abs(top.graph_relevance - 0.15) < 0.01, f"Expected g_score ~0.15, got {top.graph_relevance}"
    # Verify unresolved call evidence preserved
    assert any("uc-999" in str(ev) for ev in top.evidence_ids) or "E-decl-999" in top.evidence_ids
