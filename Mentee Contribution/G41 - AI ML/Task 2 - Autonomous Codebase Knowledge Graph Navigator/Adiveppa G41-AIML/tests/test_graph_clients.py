"""Unit tests for codebase knowledge graph engine and analysis functions."""

import json
import pytest
from pathlib import Path

from src.graph.mock_graph_client import MockGraphClient
from src.graph.schema import extract_graph_schema


@pytest.fixture
def graph_client() -> MockGraphClient:
    """Fixture providing a freshly loaded MockGraphClient instance."""
    return MockGraphClient()


def test_json_loading_and_schema(graph_client: MockGraphClient):
    """Test JSON loading, total node/edge counts, and schema categories."""
    schema = graph_client.get_schema()

    assert schema["total_nodes"] == 22
    assert schema["total_edges"] == 35

    expected_categories = {
        "Frontend component",
        "API gateway",
        "API route",
        "Microservice",
        "Shared module",
        "Database",
        "Cache",
    }
    assert set(schema["node_types"]) == expected_categories

    expected_relationships = {
        "CALLS",
        "DEPENDS_ON",
        "USES",
        "CONNECTS_TO",
        "AUTHENTICATES_WITH",
    }
    assert set(schema["relationship_types"]) == expected_relationships

    # Verify filtering by category
    microservices = graph_client.get_nodes(category="Microservice")
    assert len(microservices) == 6
    service_names = {s["id"] for s in microservices}
    assert "auth-service" in service_names
    assert "order-service" in service_names
    assert "payment-service" in service_names

    # Verify filtering by relationship type
    db_connections = graph_client.get_relationships(relationship_type="CONNECTS_TO")
    assert len(db_connections) == 6


def test_unique_node_ids_and_valid_references(tmp_path: Path):
    """Test validation errors for duplicate node IDs and broken edge references."""
    # Case 1: Duplicate node IDs
    dup_data = {
        "nodes": [
            {"id": "node-1", "type": "Microservice", "name": "Node 1"},
            {"id": "node-1", "type": "Microservice", "name": "Node 1 Dup"},
        ],
        "edges": [],
    }
    dup_file = tmp_path / "dup.json"
    dup_file.write_text(json.dumps(dup_data), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate node ID detected"):
        MockGraphClient(seed_path=dup_file)

    # Case 2: Broken edge source reference
    broken_source_data = {
        "nodes": [{"id": "node-1", "type": "Microservice", "name": "Node 1"}],
        "edges": [{"source": "missing-node", "target": "node-1", "type": "CALLS"}],
    }
    broken_source_file = tmp_path / "broken_src.json"
    broken_source_file.write_text(json.dumps(broken_source_data), encoding="utf-8")

    with pytest.raises(ValueError, match="nonexistent source node"):
        MockGraphClient(seed_path=broken_source_file)

    # Case 3: Broken edge target reference
    broken_target_data = {
        "nodes": [{"id": "node-1", "type": "Microservice", "name": "Node 1"}],
        "edges": [{"source": "node-1", "target": "missing-target", "type": "CALLS"}],
    }
    broken_target_file = tmp_path / "broken_target.json"
    broken_target_file.write_text(json.dumps(broken_target_data), encoding="utf-8")

    with pytest.raises(ValueError, match="nonexistent target node"):
        MockGraphClient(seed_path=broken_target_file)


def test_direct_dependency_traversal(graph_client: MockGraphClient):
    """Test direct dependency (outgoing) and dependent (incoming) lookups."""
    # web-portal directly calls route-orders-checkout and route-auth-login
    web_deps = graph_client.get_direct_dependencies("web-portal")
    assert web_deps == ["route-auth-login", "route-orders-checkout"]

    # legacy-auth-module is directly used/authenticated by 5 components
    auth_dependents = graph_client.get_direct_dependents("legacy-auth-module")
    assert auth_dependents == [
        "auth-service",
        "edge-api-gateway",
        "order-service",
        "payment-service",
        "user-service",
    ]


def test_transitive_dependency_traversal(graph_client: MockGraphClient):
    """Test transitive downstream dependency tracing and starting-node exclusion."""
    transitive = graph_client.get_transitive_dependents("legacy-auth-module")

    # Starting node itself MUST be excluded
    assert "legacy-auth-module" not in transitive

    # Total affected transitive dependents
    assert len(transitive) == 15

    # Should include services, routes, and edge/frontend components
    assert "auth-service" in transitive
    assert "order-service" in transitive
    assert "payment-service" in transitive
    assert "inventory-service" in transitive
    assert "user-service" in transitive
    assert "edge-api-gateway" in transitive
    assert "web-portal" in transitive
    assert "mobile-app" in transitive
    assert "admin-console" in transitive


def test_cycle_detection(graph_client: MockGraphClient):
    """Test detection of circular architectural dependencies."""
    cycles = graph_client.detect_cycles()

    # Verify cycles between order-service and inventory-service are detected
    assert len(cycles) >= 1
    found_order_inventory_cycle = False
    for c in cycles:
        if "order-service" in c and "inventory-service" in c:
            found_order_inventory_cycle = True
            break
    assert found_order_inventory_cycle, "Expected cycle between order-service and inventory-service."


def test_blast_radius_calculation(graph_client: MockGraphClient):
    """Test comprehensive blast-radius evaluation for legacy-auth-module deprecation."""
    br = graph_client.calculate_blast_radius("legacy-auth-module")

    assert br["target_id"] == "legacy-auth-module"
    assert br["target_name"] == "Legacy Auth Module"
    assert br["target_type"] == "Shared module"
    assert br["starting_node_included"] is False
    assert br["total_affected_count"] == 15

    # Check breakdown by category
    assert len(br["affected_services"]) == 5
    assert len(br["affected_api_routes"]) == 6
    assert len(br["affected_frontend_components"]) == 3

    # Check direct vs indirect dependents
    assert len(br["direct_dependents"]) == 5
    assert len(br["indirect_dependents"]) == 10
    assert len(br["direct_dependents"]) + len(br["indirect_dependents"]) == 15

    # Check traversal paths exist from affected nodes to target
    assert len(br["traversal_paths"]) == 15
    for path in br["traversal_paths"]:
        assert path[-1] == "legacy-auth-module"


def test_coupling_metrics(graph_client: MockGraphClient):
    """Test calculation of afferent coupling (Ca), efferent coupling (Ce), and instability (I)."""
    # legacy-auth-module: Ca = 5 (incoming), Ce = 0 (outgoing) -> I = 0.0 (Highly stable / SPOF)
    m_auth = graph_client.calculate_coupling_metrics("legacy-auth-module")
    assert m_auth["afferent_coupling"] == 5
    assert m_auth["efferent_coupling"] == 0
    assert m_auth["instability"] == 0.0
    assert m_auth["is_single_point_of_failure"] is True

    # order-service: Ca = 2, Ce = 8 -> I = 8 / (2 + 8) = 0.8 (Instable / Depends on many)
    m_order = graph_client.calculate_coupling_metrics("order-service")
    assert m_order["afferent_coupling"] == 2
    assert m_order["efferent_coupling"] == 8
    assert m_order["instability"] == 0.8
    assert m_order["is_single_point_of_failure"] is False

    # web-portal: Ca = 0, Ce = 2 -> I = 1.0 (Leaf / Maximum instability)
    m_portal = graph_client.calculate_coupling_metrics("web-portal")
    assert m_portal["afferent_coupling"] == 0
    assert m_portal["efferent_coupling"] == 2
    assert m_portal["instability"] == 1.0


def test_error_handling_unknown_node(graph_client: MockGraphClient):
    """Test that querying nonexistent nodes raises KeyError."""
    with pytest.raises(KeyError, match="not found in knowledge graph"):
        graph_client.get_direct_dependencies("nonexistent-service")

    with pytest.raises(KeyError, match="not found in knowledge graph"):
        graph_client.get_direct_dependents("nonexistent-service")

    with pytest.raises(KeyError, match="not found in knowledge graph"):
        graph_client.calculate_blast_radius("nonexistent-service")

    with pytest.raises(KeyError, match="not found in knowledge graph"):
        graph_client.calculate_coupling_metrics("nonexistent-service")

    # get_node returns None for missing node
    assert graph_client.get_node("nonexistent-service") is None


def test_graph_immutability_during_analysis(graph_client: MockGraphClient):
    """Test that analysis operations do not mutate the internal graph."""
    initial_nodes = graph_client._graph.number_of_nodes()
    initial_edges = graph_client._graph.number_of_edges()

    # Perform all analysis operations
    graph_client.get_schema()
    graph_client.calculate_blast_radius("legacy-auth-module")
    graph_client.detect_cycles()
    graph_client.calculate_coupling_metrics("legacy-auth-module")
    graph_client.calculate_coupling_metrics("order-service")

    assert graph_client._graph.number_of_nodes() == initial_nodes
    assert graph_client._graph.number_of_edges() == initial_edges

