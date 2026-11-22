"""Unit tests for safe, read-only graph tools and MCP local server adapter."""

import json
import pytest

from src.graph.mock_graph_client import MockGraphClient
from src.mcp.server import (
    HAS_OFFICIAL_MCP,
    LocalToolServerAdapter,
    create_tool_server_adapter,
)
from src.mcp.tools import GraphToolRegistry


@pytest.fixture
def tool_registry() -> GraphToolRegistry:
    """Fixture providing a fresh GraphToolRegistry backed by MockGraphClient."""
    return GraphToolRegistry(graph_client=MockGraphClient())


@pytest.fixture
def tool_adapter() -> LocalToolServerAdapter:
    """Fixture providing a LocalToolServerAdapter instance."""
    return create_tool_server_adapter(graph_client=MockGraphClient())


def test_all_six_tools_registered(tool_registry: GraphToolRegistry):
    """Test that exactly the six specified read-only tools are registered with schemas."""
    tools = tool_registry.list_tools()
    assert len(tools) == 6

    registered_names = {t["name"] for t in tools}
    expected_names = {
        "get_graph_schema",
        "search_graph_nodes",
        "get_node_dependencies",
        "analyze_blast_radius",
        "detect_dependency_cycles",
        "analyze_coupling",
    }
    assert registered_names == expected_names

    for tool in tools:
        assert "description" in tool and len(tool["description"]) > 10
        assert "input_schema" in tool
        assert tool["input_schema"]["type"] == "object"


def test_schema_tool_returns_graph_metadata(tool_registry: GraphToolRegistry):
    """Test get_graph_schema tool execution and returned metadata."""
    res = tool_registry.call_tool("get_graph_schema")
    assert res["success"] is True
    assert res["error"] is None

    data = res["data"]
    assert data["total_nodes"] == 22
    assert data["total_edges"] == 35
    assert "node_types" in data
    assert "relationship_types" in data
    assert "Microservice" in data["node_types"]
    assert "DEPENDS_ON" in data["relationship_types"]


def test_node_search_returns_only_existing_graph_nodes(tool_registry: GraphToolRegistry):
    """Test search_graph_nodes returns existing nodes and handles case-insensitivity."""
    # Search for 'auth'
    res = tool_registry.call_tool("search_graph_nodes", {"query": "auth"})
    assert res["success"] is True
    matches = res["data"]
    assert len(matches) > 0

    all_graph_node_ids = {n["id"] for n in tool_registry.graph_client.get_nodes()}
    for match in matches:
        # Guarantee no fabricated nodes
        assert match["id"] in all_graph_node_ids
        # Match text must contain query term in id, name, type, or description
        text_corpus = f"{match['id']} {match['name']} {match['type']} {match['description']}".lower()
        assert "auth" in text_corpus

    # Search with category filter
    res_filtered = tool_registry.call_tool(
        "search_graph_nodes", {"query": "service", "category": "Microservice"}
    )
    assert res_filtered["success"] is True
    for match in res_filtered["data"]:
        assert match["type"] == "Microservice"

    # Search with non-matching query returns empty list, not error
    res_empty = tool_registry.call_tool("search_graph_nodes", {"query": "nonexistent_term_xyz"})
    assert res_empty["success"] is True
    assert res_empty["data"] == []


def test_direct_dependency_tool(tool_registry: GraphToolRegistry):
    """Test get_node_dependencies returns direct dependencies and dependents."""
    res = tool_registry.call_tool("get_node_dependencies", {"node_id": "order-service"})
    assert res["success"] is True
    data = res["data"]

    assert data["node_id"] == "order-service"
    assert "direct_dependencies" in data
    assert "direct_dependents" in data

    # order-service is called by route-orders-checkout and inventory-service
    assert "inventory-service" in data["direct_dependents"]
    assert "route-orders-checkout" in data["direct_dependents"]

    # order-service calls inventory-service, payment-service, legacy-auth-module, etc.
    assert "legacy-auth-module" in data["direct_dependencies"]
    assert "inventory-service" in data["direct_dependencies"]


def test_blast_radius_tool_and_source_node_exclusion(tool_registry: GraphToolRegistry):
    """Test analyze_blast_radius evaluates downstream impact and strictly excludes the target node."""
    res = tool_registry.call_tool("analyze_blast_radius", {"node_id": "legacy-auth-module"})
    assert res["success"] is True
    data = res["data"]

    assert data["target_id"] == "legacy-auth-module"
    assert data["starting_node_included"] is False
    assert data["total_affected_count"] == 15

    # Target node must NOT appear in any affected lists
    assert "legacy-auth-module" not in data["direct_dependents"]
    assert "legacy-auth-module" not in data["indirect_dependents"]
    assert "legacy-auth-module" not in data["affected_services"]

    # Direct dependents: 5 components
    assert len(data["direct_dependents"]) == 5
    assert set(data["direct_dependents"]) == {
        "auth-service",
        "edge-api-gateway",
        "order-service",
        "payment-service",
        "user-service",
    }

    # Breakdown by category
    assert len(data["affected_services"]) == 5
    assert len(data["affected_api_routes"]) == 6
    assert len(data["affected_frontend_components"]) == 3

    # Traversal paths verification
    assert len(data["traversal_paths"]) == 15
    for path in data["traversal_paths"]:
        assert path[-1] == "legacy-auth-module"
        assert path[0] != "legacy-auth-module"


def test_cycle_detection_tool(tool_registry: GraphToolRegistry):
    """Test detect_dependency_cycles finds cycles in the architecture graph."""
    res = tool_registry.call_tool("detect_dependency_cycles")
    assert res["success"] is True
    data = res["data"]

    assert data["has_architectural_debt"] is True
    assert data["total_cycles_detected"] >= 1

    # Verify cycle between order-service and inventory-service exists
    cycles = data["cycles"]
    found_order_inventory = any(
        "order-service" in cycle and "inventory-service" in cycle for cycle in cycles
    )
    assert found_order_inventory


def test_coupling_tool(tool_registry: GraphToolRegistry):
    """Test analyze_coupling returns afferent, efferent, and instability metrics."""
    res = tool_registry.call_tool("analyze_coupling", {"node_id": "legacy-auth-module"})
    assert res["success"] is True
    data = res["data"]

    assert data["node_id"] == "legacy-auth-module"
    assert data["afferent_coupling"] == 5
    assert data["efferent_coupling"] == 0
    assert data["instability"] == 0.0
    assert data["is_single_point_of_failure"] is True


def test_invalid_node_ids_handled_safely(tool_registry: GraphToolRegistry):
    """Test that querying nonexistent node IDs returns safe error envelopes without crashing."""
    # get_node_dependencies with invalid ID
    res1 = tool_registry.call_tool("get_node_dependencies", {"node_id": "nonexistent_svc"})
    assert res1["success"] is False
    assert "not found" in res1["error"].lower()

    # analyze_blast_radius with invalid ID
    res2 = tool_registry.call_tool("analyze_blast_radius", {"node_id": "nonexistent_svc"})
    assert res2["success"] is False
    assert "not found" in res2["error"].lower()

    # analyze_coupling with invalid ID
    res3 = tool_registry.call_tool("analyze_coupling", {"node_id": "nonexistent_svc"})
    assert res3["success"] is False
    assert "not found" in res3["error"].lower()

    # Missing required parameter
    res4 = tool_registry.call_tool("analyze_coupling", {})
    assert res4["success"] is False
    assert "missing required parameter" in res4["error"].lower()


def test_no_write_or_mutation_tools_exposed(tool_registry: GraphToolRegistry):
    """Test that all registered tools are strictly read-only and mutations are rejected."""
    prohibited_words = {"create", "delete", "update", "set", "remove", "drop", "merge", "write"}

    for tool in tool_registry.list_tools():
        name = tool["name"].lower()
        for word in prohibited_words:
            assert word not in name, f"Prohibited mutation keyword '{word}' found in tool '{tool['name']}'"

    # Attempting to register a mutating tool must raise PermissionError
    with pytest.raises(PermissionError, match="Mutating tool"):
        tool_registry._register_tool(
            name="delete_service_node",
            description="Prohibited write tool",
            input_schema={"type": "object"},
            handler=lambda args: None,
        )


def test_tool_results_are_json_serializable(tool_registry: GraphToolRegistry):
    """Test that every registered tool produces 100% JSON-serializable output."""
    test_cases = [
        ("get_graph_schema", {}),
        ("search_graph_nodes", {"query": "auth"}),
        ("get_node_dependencies", {"node_id": "order-service"}),
        ("analyze_blast_radius", {"node_id": "legacy-auth-module"}),
        ("detect_dependency_cycles", {}),
        ("analyze_coupling", {"node_id": "legacy-auth-module"}),
    ]

    for tool_name, args in test_cases:
        res = tool_registry.call_tool(tool_name, args)
        assert res["success"] is True
        # Verify serialization and round-trip parsing
        serialized = json.dumps(res)
        deserialized = json.loads(serialized)
        assert deserialized["tool"] == tool_name
        assert deserialized["success"] is True


def test_local_tool_server_adapter_status_and_jsonrpc(tool_adapter: LocalToolServerAdapter):
    """Test adapter status reporting and JSON-RPC dispatching."""
    status = tool_adapter.get_server_status()
    assert status["registered_tools_count"] == 6
    assert status["official_mcp_sdk_installed"] == HAS_OFFICIAL_MCP
    assert "pending installation" in status["documentation"]

    # Test JSON-RPC initialize
    init_res = tool_adapter.dispatch_jsonrpc({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert init_res["result"]["serverInfo"]["name"] == "codebase-graph-tool-adapter"

    # Test JSON-RPC tools/call
    call_res = tool_adapter.dispatch_jsonrpc({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_graph_schema", "arguments": {}},
    })
    assert call_res["result"]["success"] is True
    assert call_res["result"]["data"]["total_nodes"] == 22
