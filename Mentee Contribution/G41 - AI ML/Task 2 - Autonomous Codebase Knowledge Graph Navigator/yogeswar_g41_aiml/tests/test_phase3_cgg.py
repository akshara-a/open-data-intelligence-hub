import os
import sys
import json
import uuid
import time
import threading
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mcp.app.cgg_engine import (
    ControlledGraphGatewayEngine,
    get_cgg_engine,
    cancel_query,
    validate_read_only_cypher,
    ResultLimitExceededException,
    MemoryLimitExceededException,
    QueryCancelledException,
    InvalidQueryException,
)
from mcp.app.templates import get_template, QUERY_TEMPLATES
from mcp.app.git_reader import read_file_from_git
from mcp.app.auth import (
    verify_internal_service_token,
    enforce_scope,
)
from mcp.app.mcp_server import list_tools, execute_tool, handle_json_rpc
from backend.app.auth import create_internal_service_token
from fastapi import HTTPException


@pytest.fixture
def auth_scope_tokens():
    repo_id = "test-repo-uuid-1234"
    commit_sha = "a1b2c3d4e5f67890abcdef1234567890abcdef12"
    token = create_internal_service_token(repo_id=repo_id, commit_sha=commit_sha)
    claims = verify_internal_service_token(token)
    return {
        "repo_id": repo_id,
        "commit_sha": commit_sha,
        "token": token,
        "claims": claims,
    }


def test_schema_initialization_and_idempotency():
    """
    Validates AC-3.1 / Requirement 2:
    Neo4j schema constraints and indexes can be initialized idempotently without error.
    """
    engine = ControlledGraphGatewayEngine()
    mock_session = MagicMock()
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    with patch.object(engine, "get_driver", return_value=mock_driver):
        # 1. First initialization
        engine.ensure_schema()
        assert mock_session.run.call_count >= 10, "Expected all constraints and indexes to be registered"

        # Verify statements contain IF NOT EXISTS
        for call_args in mock_session.run.call_args_list:
            stmt = call_args[0][0]
            assert "IF NOT EXISTS" in stmt, f"Statement must be idempotent: {stmt}"

        # 2. Repeated initialization (idempotency check)
        engine.ensure_schema()
        assert mock_session.run.call_count >= 20, "Repeated schema execution must run idempotently"


def test_template_catalog_coverage():
    """
    Validates Section 3 / Section 6.4:
    Predefined templates exist for all 8 mandatory CGG operations.
    """
    expected_ops = [
        "snapshot_info",
        "entity_lookup",
        "entity_details",
        "direct_neighbors",
        "impact_downstream_1hop",
        "impact_downstream_2hop",
        "impact_downstream_3hop",
        "dependencies_upstream_1hop",
        "dependencies_upstream_2hop",
        "dependencies_upstream_3hop",
        "get_evidence",
        "evidence_for_entities",
        "relationship_evidence_lookup",
        "unresolved_calls",
        "graph_statistics",
    ]
    for op in expected_ops:
        template = get_template(op)
        assert template is not None, f"Missing template for operation: {op}"
        assert "$repo_id" in template, f"Template '{op}' must be scoped to $repo_id"
        assert "$commit_sha" in template, f"Template '{op}' must be scoped to $commit_sha"


def test_read_only_cypher_ast_validation():
    """
    Validates Section 10.2 / Requirement 4:
    CGG strictly rejects write and mutation clauses.
    """
    # Safe queries
    validate_read_only_cypher("MATCH (e:Entity {repo_id: $repo_id}) RETURN e LIMIT 10;")
    validate_read_only_cypher("MATCH (e:Entity)-[:CALLS]->(tgt:Entity) RETURN count(*);")

    # Forbidden write operations
    forbidden_queries = [
        "CREATE (n:Entity {name: 'evil'});",
        "MATCH (n:Entity) SET n.name = 'compromised';",
        "MATCH (n:Entity) DELETE n;",
        "MATCH (n:Entity) DETACH DELETE n;",
        "MERGE (n:Entity {id: '123'});",
        "DROP CONSTRAINT entity_pk;",
        "ALTER CURRENT USER SET PASSWORD FROM 'a' TO 'b';",
    ]
    for q in forbidden_queries:
        with pytest.raises(InvalidQueryException):
            validate_read_only_cypher(q)


def test_hard_500_row_limit_rollback():
    """
    Validates AC-3.2 / Section 6.3:
    When query results reach 501 records, CGG immediately rolls back and raises ResultLimitExceededException.
    """
    engine = ControlledGraphGatewayEngine()
    mock_tx = MagicMock()
    mock_session = MagicMock()
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    # Generate 501 records
    dummy_records = [MagicMock(data=lambda i=i: {"id": i, "name": f"entity_{i}"}) for i in range(501)]
    mock_tx.run.return_value = dummy_records

    with patch.object(engine, "get_driver", return_value=mock_driver):
        with pytest.raises(ResultLimitExceededException):
            engine.execute_cgg_query("qry_test_limit", "MATCH (n:Entity) RETURN n", {})

        # Verify transaction was immediately rolled back
        mock_tx.rollback.assert_called()
        mock_tx.commit.assert_not_called()


def test_memory_limit_exceeded_rollback():
    """
    Validates Section 6.3:
    Result payload exceeding 64 MiB triggers immediate transaction rollback.
    """
    engine = ControlledGraphGatewayEngine()
    mock_tx = MagicMock()
    mock_session = MagicMock()
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    # 10 records of 7 MB each > 64 MB
    huge_data = {"data": "x" * (7 * 1024 * 1024)}
    dummy_records = [MagicMock(data=lambda: huge_data) for _ in range(10)]
    mock_tx.run.return_value = dummy_records

    with patch.object(engine, "get_driver", return_value=mock_driver):
        with pytest.raises(MemoryLimitExceededException):
            engine.execute_cgg_query("qry_test_mem", "MATCH (n:Entity) RETURN n", {})

        mock_tx.rollback.assert_called()
        mock_tx.commit.assert_not_called()


def test_cooperative_thread_safe_cancellation():
    """
    Validates Section 6.3 / AC-3.5:
    Thread-safe cooperative cancellation safely aborts running query and rolls back transaction.
    """
    engine = ControlledGraphGatewayEngine()
    mock_tx = MagicMock()
    mock_session = MagicMock()
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    query_id = "qry_cancel_target"

    def slow_generator():
        for i in range(100):
            if i == 5:
                # Trigger cancellation from outside thread
                cancel_query(query_id)
            mock_rec = MagicMock()
            mock_rec.data.return_value = {"index": i}
            yield mock_rec

    mock_tx.run.return_value = slow_generator()

    with patch.object(engine, "get_driver", return_value=mock_driver):
        with pytest.raises(QueryCancelledException):
            engine.execute_cgg_query(query_id, "MATCH (n:Entity) RETURN n", {})

        mock_tx.rollback.assert_called()
        mock_tx.commit.assert_not_called()


def test_scope_enforcement_and_mismatch_rejection(auth_scope_tokens):
    """
    Validates Section 6.2 / AC-3.4:
    Token claims bind authorized_repo_id and authorized_commit_sha.
    Requests with mismatched scope return HTTP 403 SCOPE_MISMATCH.
    """
    claims = auth_scope_tokens["claims"]
    repo_id = auth_scope_tokens["repo_id"]
    commit_sha = auth_scope_tokens["commit_sha"]

    # 1. Matching scope passes cleanly
    enforce_scope(claims, repo_id=repo_id, commit_sha=commit_sha)

    # 2. Mismatched repo_id fails
    with pytest.raises(HTTPException) as exc_info:
        enforce_scope(claims, repo_id="other-repo-uuid", commit_sha=commit_sha)
    assert exc_info.value.status_code == 403
    assert "SCOPE_MISMATCH" in exc_info.value.detail

    # 3. Mismatched commit_sha fails
    with pytest.raises(HTTPException) as exc_info:
        enforce_scope(claims, repo_id=repo_id, commit_sha="other_sha_1234567890abcdef")
    assert exc_info.value.status_code == 403
    assert "SCOPE_MISMATCH" in exc_info.value.detail


def test_entity_lookup_and_details_execution(auth_scope_tokens):
    """
    Validates named operations: cgg.entity_lookup and cgg.entity_details.
    """
    claims = auth_scope_tokens["claims"]
    mock_engine = MagicMock()
    mock_engine.execute_cgg_query.return_value = [
        {
            "entity_id": f"{claims['authorized_repo_id']}::{claims['authorized_commit_sha']}::Function::test_fn::123",
            "name": "test_fn",
            "file_path": "src/main.py",
            "line_start": 10,
            "line_end": 20,
            "entity_types": ["Function"],
        }
    ]

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=mock_engine):
        # 1. Entity Lookup
        res = execute_tool("cgg.entity_lookup", {"name": "test_fn"}, claims)
        assert res["count"] == 1
        assert res["entities"][0]["name"] == "test_fn"

        # 2. Entity Details
        mock_engine.execute_cgg_query.return_value = [
            {
                "entity_id": "ent_123",
                "name": "test_fn",
                "declaration_evidence_id": "E-12345",
                "declaration_line_range": "10-20",
                "extraction_rule": "tree_sitter_function",
            }
        ]
        res = execute_tool("cgg.entity_details", {"entity_id": "ent_123"}, claims)
        assert res["entity"]["declaration_evidence_id"] == "E-12345"


def test_direct_neighbors_and_bounded_multihop(auth_scope_tokens):
    """
    Validates Section 10.1:
    Direct neighbors retrieval and bounded multi-hop traversal with max depth clamping.
    """
    claims = auth_scope_tokens["claims"]
    mock_engine = MagicMock()

    # Direct Neighbors
    mock_engine.execute_cgg_query.return_value = [
        {
            "outgoing_dependencies": [{"entity_id": "ent_b", "relationship": "CALLS"}],
            "incoming_dependents": [{"entity_id": "ent_c", "relationship": "IMPORTS"}],
        }
    ]

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=mock_engine):
        res = execute_tool("cgg.direct_neighbors", {"entity_id": "ent_a"}, claims)
        assert len(res["outgoing_dependencies"]) == 1
        assert len(res["incoming_dependents"]) == 1

        # Multi-hop Traversal with depth clamping (depth=5 clamped to 3)
        mock_engine.execute_cgg_query.return_value = [
            {"entity_id": "ent_d", "hop_distance": 2, "relationship_types": ["CALLS", "CALLS"]}
        ]
        res = execute_tool("cgg.multi_hop_dependencies", {"start_entity_id": "ent_a", "max_depth": 5}, claims)
        assert res["max_depth"] == 3
        assert res["count"] == 1


def test_evidence_and_unresolved_calls_lookup(auth_scope_tokens):
    """
    Validates Section 11 & 12:
    Evidence retrieval and unresolved dynamic calls with candidate match classification.
    """
    claims = auth_scope_tokens["claims"]
    mock_engine = MagicMock()

    # Evidence Lookup
    mock_engine.execute_cgg_query.return_value = [
        {
            "evidence_id": "E-55555",
            "file_path": "src/utils.py",
            "line_range": "30-35",
            "relationship_type": "CALLS",
        }
    ]

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=mock_engine):
        res = execute_tool("graph.get_evidence", {"evidence_id": "E-55555"}, claims)
        assert res["evidence"]["evidence_id"] == "E-55555"

        # Unresolved Calls with candidate target
        mock_engine.execute_cgg_query.return_value = [
            {
                "call_id": "call_1",
                "invoked_symbol_name": "dynamic_proc",
                "file_path": "src/app.py",
                "candidate_targets": [
                    {
                        "candidate_entity_id": "cand_1",
                        "candidate_name": "dynamic_proc",
                        "classification": "potential_uncertain",
                    }
                ],
            }
        ]
        res = execute_tool("cgg.unresolved_calls", {}, claims)
        assert res["count"] == 1
        assert res["unresolved_calls"][0]["candidate_targets"][0]["classification"] == "potential_uncertain"


def test_repo_read_file_from_git(tmp_path):
    """
    Validates AC-3.3 / Section 6.4:
    repo.read_file extracts exact lines from bare Git mirror.
    """
    import subprocess
    repo_id = "test-repo-git"
    bare_dir = tmp_path / f"{repo_id}.git"

    # Create a small Git repository and make it bare
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=str(work_dir), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=str(work_dir), check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(work_dir), check=True)

    test_file = work_dir / "service.py"
    test_file.write_text("line 1\nline 2\nline 3\nline 4\nline 5\n", encoding="utf-8")
    subprocess.run(["git", "add", "service.py"], cwd=str(work_dir), check=True)
    subprocess.run(["git", "commit", "-m", "add service.py"], cwd=str(work_dir), check=True)

    commit_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(work_dir), check=True, capture_output=True, text=True
    ).stdout.strip()

    # Mirror bare Git directory
    import shutil
    shutil.copytree(work_dir / ".git", bare_dir)
    subprocess.run(["git", "config", "--bool", "core.bare", "true"], cwd=str(bare_dir), check=True, capture_output=True)

    with patch("mcp.app.git_reader.get_git_repo_path", return_value=bare_dir):
        # Extract lines 2 to 4
        result = read_file_from_git(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path="service.py",
            start_line=2,
            end_line=4,
        )
        assert result["lines"] == ["line 2", "line 3", "line 4"]
        assert result["total_file_lines"] == 5
        assert result["start_line"] == 2
        assert result["end_line"] == 4

        # Path traversal rejection
        with pytest.raises(HTTPException) as exc_info:
            read_file_from_git(
                repo_id=repo_id,
                commit_sha=commit_sha,
                file_path="../../etc/passwd",
                start_line=1,
                end_line=5,
            )
        assert exc_info.value.status_code == 400


def test_mcp_json_rpc_handler(auth_scope_tokens):
    """
    Validates Section 6.1 / Section 6.4:
    MCP JSON-RPC 2.0 protocol handling for tools/list and tools/call.
    """
    claims = auth_scope_tokens["claims"]

    # 1. tools/list
    list_req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    resp = handle_json_rpc(list_req, claims)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 1
    tool_names = [t["name"] for t in resp["result"]["tools"]]
    assert "graph.run_query" in tool_names
    assert "graph.get_evidence" in tool_names
    assert "graph.get_evidence_for_entities" in tool_names
    assert "repo.read_file" in tool_names
    assert "cgg.entity_lookup" in tool_names

    # 2. tools/call dispatch
    mock_engine = MagicMock()
    mock_engine.execute_cgg_query.return_value = [{"status": "ok"}]

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=mock_engine):
        call_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "graph.run_query",
                "arguments": {
                    "operation": "snapshot_info",
                    "parameters": {},
                },
            },
        }
        call_resp = handle_json_rpc(call_req, claims)
        assert call_resp["jsonrpc"] == "2.0"
        assert call_resp["id"] == 2
        content = call_resp["result"]["content"]
        assert len(content) == 1
        data = json.loads(content[0]["text"])
        assert data["operation"] == "snapshot_info"
