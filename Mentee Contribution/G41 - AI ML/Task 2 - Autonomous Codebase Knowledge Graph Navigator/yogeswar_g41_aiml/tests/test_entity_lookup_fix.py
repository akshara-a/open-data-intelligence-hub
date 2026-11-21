import asyncio
import pytest
from unittest.mock import MagicMock, patch
from fastapi import Request

from mcp.app.cgg_engine import (
    ControlledGraphGatewayEngine,
    ResultLimitExceededException,
    MemoryLimitExceededException,
    QueryCancelledException,
)
from mcp.app.mcp_server import execute_tool


def test_no_double_rollback_on_result_limit():
    """Verify that ResultLimitExceededException triggers rollback exactly once without TransactionError."""
    engine = ControlledGraphGatewayEngine()
    mock_tx = MagicMock()
    mock_session = MagicMock()
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    dummy_records = [MagicMock(data=lambda i=i: {"id": i, "name": f"ent_{i}"}) for i in range(501)]
    mock_tx.run.return_value = dummy_records

    with patch.object(engine, "get_driver", return_value=mock_driver):
        with pytest.raises(ResultLimitExceededException):
            engine.execute_cgg_query("qry_limit_test", "MATCH (n:Entity) RETURN n", {})

        # Ensure rollback was called once
        assert mock_tx.rollback.call_count == 1
        assert mock_tx.commit.call_count == 0


def test_entity_lookup_pagination_parameters():
    """Verify entity_lookup tool sets limit and skip parameters correctly."""
    engine = ControlledGraphGatewayEngine()
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_tx = MagicMock()
    mock_tx.run.return_value = [MagicMock(data=lambda: {"entity_id": "e1", "name": "foo"})]
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver.session.return_value.__enter__.return_value = mock_session

    claims = {
        "iss": "cgg_internal_service",
        "aud": "cgg_mcp_service",
        "authorized_repo_id": "test_repo",
        "authorized_commit_sha": "test_sha",
    }

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=engine), \
         patch.object(engine, "get_driver", return_value=mock_driver):
        res = execute_tool(
            "cgg.entity_lookup",
            {"name": "foo", "limit": 25, "skip": 50},
            claims,
        )

        assert res["count"] == 1
        assert res["limit"] == 25
        assert res["skip"] == 50

        # Verify bound params passed to tx.run
        call_args = mock_tx.run.call_args
        params = call_args[0][1]
        assert params["limit"] == 25
        assert params["skip"] == 50
        assert params["repo_id"] == "test_repo"
        assert params["commit_sha"] == "test_sha"


def test_entity_lookup_default_and_clamped_limit():
    """Verify limit defaults to 500 and is clamped to at most 500."""
    engine = ControlledGraphGatewayEngine()
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_tx = MagicMock()
    mock_tx.run.return_value = []
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver.session.return_value.__enter__.return_value = mock_session

    claims = {
        "iss": "cgg_internal_service",
        "aud": "cgg_mcp_service",
        "authorized_repo_id": "test_repo",
        "authorized_commit_sha": "test_sha",
    }

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=engine), \
         patch.object(engine, "get_driver", return_value=mock_driver):
        # 1. Test limit exceeding 500 is clamped
        res = execute_tool("cgg.entity_lookup", {"limit": 999}, claims)
        assert res["limit"] == 500

        # 2. Test negative limit is clamped to 1
        res = execute_tool("cgg.entity_lookup", {"limit": -10}, claims)
        assert res["limit"] == 1

        # 3. Test negative skip is clamped to 0
        res = execute_tool("cgg.entity_lookup", {"skip": -5}, claims)
        assert res["skip"] == 0


def test_auto_pagination_algorithm():
    """Verify pagination chunking algorithm aggregates multiple pages when results exceed 500."""
    page_1 = [{"entity_id": f"e_{i}"} for i in range(500)]
    page_2 = [{"entity_id": f"e_{500+i}"} for i in range(471)]

    calls = []

    def mock_fetch_page(skip, limit):
        calls.append({"skip": skip, "limit": limit})
        if skip == 0:
            return page_1
        elif skip == 500:
            return page_2
        return []

    # Emulate backend pagination loop
    all_entities = []
    current_skip = 0
    page_limit = 500
    max_total_entities = 5000

    while len(all_entities) < max_total_entities:
        entities = mock_fetch_page(current_skip, page_limit)
        all_entities.extend(entities)
        if len(entities) < page_limit:
            break
        current_skip += page_limit

    assert len(all_entities) == 971
    assert len(calls) == 2
    assert calls[0]["skip"] == 0
    assert calls[0]["limit"] == 500
    assert calls[1]["skip"] == 500
    assert calls[1]["limit"] == 500


def test_snapshot_relationships_tool_execution():
    """Verify cgg.snapshot_relationships tool dispatches with pagination."""
    engine = ControlledGraphGatewayEngine()
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_tx = MagicMock()
    mock_tx.run.return_value = [
        MagicMock(data=lambda: {
            "id": "rel_1",
            "source_id": "s1",
            "source_name": "src",
            "target_id": "t1",
            "target_name": "tgt",
            "relationship": "CALLS",
            "direction": "OUTGOING",
        })
    ]
    mock_session.begin_transaction.return_value = mock_tx
    mock_driver.session.return_value.__enter__.return_value = mock_session

    claims = {
        "iss": "cgg_internal_service",
        "aud": "cgg_mcp_service",
        "authorized_repo_id": "test_repo",
        "authorized_commit_sha": "test_sha",
    }

    with patch("mcp.app.mcp_server.get_cgg_engine", return_value=engine), \
         patch.object(engine, "get_driver", return_value=mock_driver):
        res = execute_tool(
            "cgg.snapshot_relationships",
            {"relationship_type": "CALLS", "limit": 100, "skip": 0},
            claims,
        )

        assert res["count"] == 1
        assert res["limit"] == 100
        assert res["skip"] == 0
        assert len(res["relationships"]) == 1
        assert res["relationships"][0]["relationship"] == "CALLS"
