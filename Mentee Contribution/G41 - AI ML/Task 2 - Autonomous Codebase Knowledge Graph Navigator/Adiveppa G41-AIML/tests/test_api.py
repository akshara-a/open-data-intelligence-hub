"""Unit and integration tests for the FastAPI REST API interface."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client() -> TestClient:
    """Fixture providing a FastAPI TestClient."""
    return TestClient(app)


def test_health_endpoint(client: TestClient):
    """Test GET /health returns service health and graph summary."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["engine"] == "mock-networkx"
    assert data["graph_nodes"] == 22
    assert data["graph_edges"] == 35


def test_schema_endpoint(client: TestClient):
    """Test GET /schema returns graph structural schema."""
    response = client.get("/schema")
    assert response.status_code == 200
    data = response.json()
    assert data["total_nodes"] == 22
    assert data["total_edges"] == 35
    assert "Microservice" in data["node_types"]
    assert "CALLS" in data["relationship_types"]


def test_list_nodes_and_filtering(client: TestClient):
    """Test GET /nodes with and without category query filter."""
    # All nodes
    res_all = client.get("/nodes")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 22

    # Filtered by category
    res_filtered = client.get("/nodes?category=Microservice")
    assert res_filtered.status_code == 200
    services = res_filtered.json()
    assert len(services) == 6
    for s in services:
        assert s["type"] == "Microservice"


def test_node_details_endpoint(client: TestClient):
    """Test GET /nodes/{node_id} for existing and missing components."""
    # Existing component
    res = client.get("/nodes/legacy-auth-module")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "legacy-auth-module"
    assert "direct_dependencies" in data
    assert "direct_dependents" in data
    assert len(data["direct_dependents"]) == 5

    # Missing component (404)
    res_missing = client.get("/nodes/nonexistent-service")
    assert res_missing.status_code == 404
    assert "not found" in res_missing.json()["detail"].lower()


def test_cycles_endpoint(client: TestClient):
    """Test GET /cycles returns circular dependencies."""
    response = client.get("/cycles")
    assert response.status_code == 200
    data = response.json()
    assert data["has_architectural_debt"] is True
    assert data["total_cycles"] >= 1


def test_blast_radius_endpoint(client: TestClient):
    """Test POST /blast-radius calculates downstream affected components."""
    payload = {"node_id": "legacy-auth-module"}
    response = client.post("/blast-radius", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_id"] == "legacy-auth-module"
    assert data["total_affected_count"] == 15
    assert data["starting_node_included"] is False
    assert len(data["affected_services"]) == 5

    # 404 for missing component
    missing_res = client.post("/blast-radius", json={"node_id": "ghost-node"})
    assert missing_res.status_code == 404


def test_navigate_endpoint(client: TestClient):
    """Test POST /navigate executes autonomous end-to-end multi-step flow."""
    query = "If I deprecate the legacy authentication module, which downstream API routes and frontend components will break?"
    response = client.post("/navigate", json={"query": query})
    assert response.status_code == 200
    data = response.json()

    assert data["user_query"] == query
    assert data["parsed_intent"]["intent"] == "blast_radius"
    assert data["cypher_result"]["is_valid"] is True
    assert data["cypher_result"]["is_safe"] is True
    assert data["tool_executed"] == "analyze_blast_radius"
    assert "Architectural Impact" in data["report_markdown"]
    assert "```mermaid" in data["report_markdown"]


def test_navigate_empty_query_error(client: TestClient):
    """Test POST /navigate rejects empty query with 400 error."""
    response = client.post("/navigate", json={"query": "   "})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

