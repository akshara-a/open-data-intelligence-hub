"""Unit tests for ArchitectureReasoner, evidence-based risk evaluation, and refactoring guidance."""

import json
import pytest

from src.agent.architecture_reasoner import (
    ArchitectureAnalysisResult,
    ArchitectureReasoner,
)
from src.graph.mock_graph_client import MockGraphClient


@pytest.fixture
def reasoner() -> ArchitectureReasoner:
    """Fixture providing an ArchitectureReasoner backed by MockGraphClient."""
    return ArchitectureReasoner(graph_client=MockGraphClient())


def test_blast_radius_analysis_and_source_node_exclusion(reasoner: ArchitectureReasoner):
    """Test blast-radius calculation for legacy-auth-module and verify source exclusion."""
    res = reasoner.analyze_component("legacy-auth-module")
    assert res.is_valid is True
    assert res.target_node_id == "legacy-auth-module"

    affected = res.affected_nodes
    # Total affected count must be 15
    assert affected["total_affected_count"] == 15
    assert affected["starting_node_included"] is False

    # The starting node must NOT be in any affected lists
    assert "legacy-auth-module" not in affected["direct_dependents"]
    assert "legacy-auth-module" not in affected["indirect_dependents"]
    assert "legacy-auth-module" not in affected["affected_microservices"]
    assert "legacy-auth-module" not in affected["affected_api_routes"]
    assert "legacy-auth-module" not in affected["affected_frontend_components"]

    # Verify breakdown
    assert len(affected["affected_microservices"]) == 5
    assert len(affected["affected_api_routes"]) == 6
    assert len(affected["affected_frontend_components"]) == 3
    assert len(affected["direct_dependents"]) == 5
    assert len(affected["indirect_dependents"]) == 10


def test_dependency_paths_in_analysis(reasoner: ArchitectureReasoner):
    """Test that observed shortest paths from callers to target are included and valid."""
    res = reasoner.analyze_component("legacy-auth-module")
    paths = res.dependency_paths
    assert len(paths) == 15

    for p in paths:
        # Every path must lead to legacy-auth-module
        assert p[-1] == "legacy-auth-module"
        # The first element must be an affected downstream dependent
        assert p[0] != "legacy-auth-module"
        assert len(p) >= 2


def test_cycle_detection_and_explanations(reasoner: ArchitectureReasoner):
    """Test cycle detection, actual node IDs, and architectural explanations."""
    res = reasoner.analyze_component("order-service")
    assert len(res.cycles) >= 1

    # Verify order-service <-> inventory-service cycle is present
    found_cycle = False
    for cycle_info in res.cycles:
        nodes = cycle_info["cycle_nodes"]
        assert "explanation" in cycle_info
        assert len(cycle_info["explanation"]) > 20
        if "order-service" in nodes and "inventory-service" in nodes:
            found_cycle = True
            assert cycle_info["involves_target"] is True
    assert found_cycle, "Expected order-service <-> inventory-service cycle to be detected."


def test_coupling_analysis(reasoner: ArchitectureReasoner):
    """Test coupling metrics in component analysis."""
    # legacy-auth-module: high incoming coupling (Ca=5, Ce=0)
    res_auth = reasoner.analyze_component("legacy-auth-module")
    cm_auth = res_auth.coupling_metrics
    assert cm_auth is not None
    assert cm_auth["afferent_coupling"] == 5
    assert cm_auth["efferent_coupling"] == 0
    assert cm_auth["instability"] == 0.0

    # order-service: high outgoing coupling (Ca=2, Ce=8)
    res_order = reasoner.analyze_component("order-service")
    cm_order = res_order.coupling_metrics
    assert cm_order is not None
    assert cm_order["afferent_coupling"] == 2
    assert cm_order["efferent_coupling"] == 8
    assert cm_order["instability"] == 0.8


def test_shared_dependency_identification(reasoner: ArchitectureReasoner):
    """Test identification of shared datastores and modules used by multiple services."""
    res = reasoner.analyze_component("auth-service")
    shared = res.shared_dependencies

    # In our sample graph, shared-customer-db is accessed by auth-service and user-service
    shared_db_ids = {s["component_id"] for s in shared}
    assert "shared-customer-db" in shared_db_ids or "shared-session-cache" in shared_db_ids

    for item in shared:
        assert item["access_count"] >= 2
        assert len(item["accessing_components"]) >= 2


def test_evidence_backed_risk_generation(reasoner: ArchitectureReasoner):
    """Test that architectural risks are generated with concrete graph evidence and calibrated severity."""
    res = reasoner.analyze_component("legacy-auth-module")
    risks = res.risks
    assert len(risks) >= 1

    # Find the high inbound coupling risk
    high_coupling_risk = next((r for r in risks if "High Inbound Coupling" in r.risk_title), None)
    assert high_coupling_risk is not None
    assert high_coupling_risk.severity == "HIGH"
    assert high_coupling_risk.evidence["afferent_coupling_Ca"] == 5
    assert high_coupling_risk.evidence["total_affected_downstream_components"] == 15
    assert high_coupling_risk.assessment_basis == "observed_graph_structure"
    assert "confidence_level" in high_coupling_risk.model_dump()


def test_refactoring_recommendation_grounding(reasoner: ArchitectureReasoner):
    """Test that refactoring recommendations reference real graph entities and intended benefits."""
    res = reasoner.analyze_component("order-service")
    recs = res.recommendations
    assert len(recs) >= 1

    for rec in recs:
        assert rec.title
        assert len(rec.target_components) > 0
        assert rec.supporting_graph_evidence
        assert rec.intended_architectural_benefit
        assert len(rec.action_steps) >= 2

        # Verify target components are real graph node IDs
        all_nodes = {n["id"] for n in reasoner.graph_client.get_nodes()}
        for target in rec.target_components:
            assert target in all_nodes, f"Target '{target}' is not in the knowledge graph!"


def test_unknown_node_handling_graceful(reasoner: ArchitectureReasoner):
    """Test that analyzing an unknown node ID returns a safe error result without raising unhandled exceptions."""
    res = reasoner.analyze_component("nonexistent-ghost-service")
    assert res.is_valid is False
    assert res.error_message is not None
    assert "not found" in res.error_message
    assert res.target_node_id == "nonexistent-ghost-service"
    assert res.risks == []
    assert res.recommendations == []


def test_mock_graph_source_disclosure(reasoner: ArchitectureReasoner):
    """Test that the sample/mock graph source is explicitly disclosed in the result."""
    res = reasoner.analyze_component("legacy-auth-module")
    assert "sample/mock architecture graph" in res.graph_source
    assert "mock_graph_seed.json" in res.graph_source
    assert len(res.limitations) >= 3
    assert any("fictional sample architecture graph" in lim for lim in res.limitations)


def test_json_serialization(reasoner: ArchitectureReasoner):
    """Test that ArchitectureAnalysisResult is 100% JSON-serializable."""
    res = reasoner.analyze_component("legacy-auth-module")
    dumped = res.model_dump()
    serialized = json.dumps(dumped)
    deserialized = json.loads(serialized)

    assert deserialized["target_node_id"] == "legacy-auth-module"
    assert deserialized["is_valid"] is True
    assert deserialized["affected_nodes"]["total_affected_count"] == 15


def test_deterministic_output(reasoner: ArchitectureReasoner):
    """Test that multiple runs produce strictly identical output for the same input."""
    res1 = reasoner.analyze_component("legacy-auth-module")
    res2 = reasoner.analyze_component("legacy-auth-module")

    assert res1.model_dump() == res2.model_dump()

