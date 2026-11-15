
import json

import kgnav.mcp_server as server

from kgnav.mcp_server import (
    downstream_services,
    downstream_service_distances,
)


# ---------------------------------------------------------------------------
# Downstream service propagation tests


def test_downstream_services_direct():
    pairs = [
        ("api-gateway", "auth-service"),
        ("payment-service", "auth-service"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service"},
    )

    assert result == {
        "api-gateway",
        "payment-service",
    }


def test_downstream_services_transitive():
    pairs = [
        ("api-gateway", "auth-service"),
        ("frontend-service", "api-gateway"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service"},
    )

    assert result == {
        "api-gateway",
        "frontend-service",
    }


def test_downstream_services_no_duplicates():
    pairs = [
        ("api-gateway", "auth-service"),
        ("api-gateway", "auth-service"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service"},
    )

    assert result == {"api-gateway"}


def test_downstream_services_multiple_targets():
    pairs = [
        ("api-gateway", "auth-service"),
        ("payment-service", "database-service"),
        ("order-service", "payment-service"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service", "database-service"},
    )

    assert result == {
        "api-gateway",
        "payment-service",
        "order-service",
    }


def test_downstream_services_handles_cycles():
    pairs = [
        ("api-gateway", "auth-service"),
        ("auth-service", "api-gateway"),
        ("frontend-service", "api-gateway"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service"},
    )

    assert result == {
        "api-gateway",
        "frontend-service",
    }

    assert "auth-service" not in result


def test_downstream_services_no_dependencies():
    result = downstream_services(
        [],
        {"auth-service"},
    )

    assert result == set()


def test_downstream_services_does_not_include_target():
    pairs = [
        ("api-gateway", "auth-service"),
    ]

    result = downstream_services(
        pairs,
        {"auth-service", "api-gateway"},
    )

    assert result == set()


# ---------------------------------------------------------------------------
# Service-level shortest-distance tests


def test_downstream_service_distances_direct_and_transitive():
    pairs = [
        ("api-gateway", "legacy-auth-service"),
        ("auth-service-v2", "legacy-auth-service"),
        ("order-service", "legacy-auth-service"),
        ("payment-service", "legacy-auth-service"),
        ("user-service", "legacy-auth-service"),
        ("notification-service", "api-gateway"),
        ("inventory-service", "notification-service"),
    ]

    result = downstream_service_distances(
        pairs,
        {"legacy-auth-service"},
    )

    assert result == {
        "api-gateway": 1,
        "auth-service-v2": 1,
        "order-service": 1,
        "payment-service": 1,
        "user-service": 1,
        "notification-service": 2,
        "inventory-service": 3,
    }


def test_downstream_service_distances_uses_shortest_path():
    pairs = [
        ("api-gateway", "auth-service"),
        ("payment-service", "api-gateway"),
        ("payment-service", "auth-service"),
    ]

    result = downstream_service_distances(
        pairs,
        {"auth-service"},
    )

    assert result == {
        "api-gateway": 1,
        "payment-service": 1,
    }


def test_downstream_service_distances_handles_cycles():
    pairs = [
        ("api-gateway", "auth-service"),
        ("auth-service", "api-gateway"),
        ("frontend-service", "api-gateway"),
    ]

    result = downstream_service_distances(
        pairs,
        {"auth-service"},
    )

    assert result == {
        "api-gateway": 1,
        "frontend-service": 2,
    }


def test_downstream_service_distances_multiple_targets():
    pairs = [
        ("api-gateway", "auth-service"),
        ("payment-service", "database-service"),
        ("order-service", "payment-service"),
    ]

    result = downstream_service_distances(
        pairs,
        {"auth-service", "database-service"},
    )

    assert result == {
        "api-gateway": 1,
        "payment-service": 1,
        "order-service": 2,
    }


def test_downstream_service_distances_no_dependencies():
    result = downstream_service_distances(
        [],
        {"auth-service"},
    )

    assert result == {}


# ---------------------------------------------------------------------------
# Circular dependency MCP response tests


def test_detect_circular_dependencies_service_level(monkeypatch):
    pairs = [
        ("api-gateway", "auth-service"),
        ("auth-service", "api-gateway"),
        ("payment-service", "database-service"),
        ("database-service", "payment-service"),
        ("frontend-service", "api-gateway"),
    ]

    monkeypatch.setattr(
        server,
        "graph",
        lambda: object(),
    )

    monkeypatch.setattr(
        server,
        "fetch_service_pairs",
        lambda g: pairs,
    )

    result = json.loads(
        server.detect_circular_dependencies(level="service")
    )

    assert result["level"] == "service"
    assert result["scc_count"] == 2
    assert result["individual_cycles_enumerated"] is False

    components = result["strongly_connected_components"]

    members = {
        frozenset(component["members"])
        for component in components
    }

    assert members == {
        frozenset({"api-gateway", "auth-service"}),
        frozenset({"payment-service", "database-service"}),
    }


def test_detect_circular_dependencies_module_level(monkeypatch):
    pairs = [
        ("module-a", "module-b"),
        ("module-b", "module-a"),
        ("module-b", "module-c"),
        ("module-c", "module-b"),
    ]

    monkeypatch.setattr(
        server,
        "graph",
        lambda: object(),
    )

    monkeypatch.setattr(
        server,
        "fetch_module_pairs",
        lambda g: pairs,
    )

    result = json.loads(
        server.detect_circular_dependencies(level="module")
    )

    assert result["level"] == "module"
    assert result["scc_count"] == 1
    assert result["individual_cycles_enumerated"] is False

    component = result["strongly_connected_components"][0]

    assert set(component["members"]) == {
        "module-a",
        "module-b",
        "module-c",
    }

    assert component["size"] == 3


def test_detect_circular_dependencies_invalid_level_returns_error():
    result = json.loads(
        server.detect_circular_dependencies(level="invalid")
    )

    assert result["error"] == "ValueError"
    assert "Invalid level" in result["message"]


def test_detect_circular_dependencies_empty_graph(monkeypatch):
    monkeypatch.setattr(
        server,
        "graph",
        lambda: object(),
    )

    monkeypatch.setattr(
        server,
        "fetch_service_pairs",
        lambda g: [],
    )

    result = json.loads(
        server.detect_circular_dependencies(level="service")
    )

    assert result == {
        "level": "service",
        "scc_count": 0,
        "strongly_connected_components": [],
        "individual_cycles_enumerated": False,
    }
