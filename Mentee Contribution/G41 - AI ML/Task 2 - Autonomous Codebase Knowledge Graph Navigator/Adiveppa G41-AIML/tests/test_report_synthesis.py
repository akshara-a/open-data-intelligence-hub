"""Unit and integration tests for ReportSynthesizer and AutonomousCodebaseNavigator."""

import json
import re
import pytest

from src.agent.architecture_reasoner import ArchitectureReasoner
from src.agent.navigator import AutonomousCodebaseNavigator, NavigationResult
from src.agent.report_synthesizer import ReportSynthesizer
from src.graph.mock_graph_client import MockGraphClient


@pytest.fixture
def mock_client() -> MockGraphClient:
    """Fixture providing a fresh MockGraphClient."""
    return MockGraphClient()


@pytest.fixture
def reasoner(mock_client: MockGraphClient) -> ArchitectureReasoner:
    """Fixture providing an ArchitectureReasoner."""
    return ArchitectureReasoner(graph_client=mock_client)


@pytest.fixture
def synthesizer(reasoner: ArchitectureReasoner) -> ReportSynthesizer:
    """Fixture providing a ReportSynthesizer."""
    return ReportSynthesizer(reasoner=reasoner)


@pytest.fixture
def navigator(mock_client: MockGraphClient) -> AutonomousCodebaseNavigator:
    """Fixture providing an AutonomousCodebaseNavigator."""
    return AutonomousCodebaseNavigator(graph_client=mock_client)


def test_report_synthesis_required_sections(
    reasoner: ArchitectureReasoner,
    synthesizer: ReportSynthesizer,
):
    """Test that the synthesized Markdown report contains all required sections from task-info.md."""
    analysis_data = reasoner.analyze_component("legacy-auth-module")
    report = synthesizer.synthesize(
        analysis_data,
        user_query="If I deprecate legacy-auth-module, what downstream services and routes break?",
    )

    # Required Section 1: Executive Summary & Blast-Radius Header
    assert "# Architectural Impact & Blast-Radius Assessment Report" in report
    assert "## Executive Summary" in report
    assert "Total Downstream Affected Components" in report

    # Required Section 2: Exact List of Affected Microservices & API Routes
    assert "## 1. Downstream Blast-Radius Breakdown" in report
    assert "### 1.1 Affected Microservices" in report
    assert "### 1.2 Affected Downstream API Routes" in report
    assert "### 1.3 Affected Frontend Applications" in report
    assert "`auth-service`" in report
    assert "`order-service`" in report
    assert "`payment-service`" in report
    assert "`route-auth-login`" in report
    assert "`route-auth-verify`" in report

    # Required Section 3: Assessment of Architectural Debt Involved
    assert "## 2. Assessment of Architectural Debt Involved" in report
    assert "Afferent Coupling ($C_a$)" in report
    assert "Instability Index ($I$)" in report
    assert "Single Point of Failure" in report or "Inbound Coupling" in report

    # Required Section 4: Step-by-Step Refactoring Strategy
    assert "## 3. Step-by-Step Refactoring Strategy" in report
    assert "Phase 1:" in report
    assert "Anti-Corruption Layer" in report or "Phase" in report
    assert "Implementation Actions:" in report

    # Required Section 5: Mermaid Subgraph Diagram
    assert "## 4. Architectural Impact Subgraph (Mermaid Visualization)" in report
    assert "```mermaid" in report
    assert "flowchart TD" in report

    # Required Section 6: Grounding Guarantee & Source Disclosures
    assert "## 5. Grounding Guarantee & Analytical Limitations" in report
    assert "Strict Contextual Grounding" in report
    assert "mock_graph_seed.json" in report


def test_contextual_grounding_no_hallucinations(
    reasoner: ArchitectureReasoner,
    synthesizer: ReportSynthesizer,
    mock_client: MockGraphClient,
):
    """Verify that every component referenced in the report exists in the graph (zero hallucinations)."""
    analysis_data = reasoner.analyze_component("legacy-auth-module")
    report = synthesizer.synthesize(analysis_data)

    known_nodes = {n["id"] for n in mock_client.get_nodes()}

    # Extract all backticked identifiers in the report that look like node IDs
    backticked = re.findall(r"`([a-zA-Z0-9_-]+)`", report)

    # Filter out metrics or generic markdown keywords
    non_entity_words = {
        "legacy-auth-module", "Ca", "Ce", "I", "True", "False", "None", "Component",
        "Microservice", "Database", "Cache", "High", "Medium", "Low", "CRITICAL",
        "Architecture", "Query",
    }
    candidate_entities = [w for w in backticked if "-" in w and w not in non_entity_words]

    for entity in candidate_entities:
        assert entity in known_nodes, f"Hallucinated entity detected in report: '{entity}'"


def test_end_to_end_navigator_core_problem_statement(navigator: AutonomousCodebaseNavigator):
    """Test full multi-step navigation for the central assignment scenario."""
    query = "If I deprecate the legacy authentication module, which downstream API routes and frontend components will break?"
    result: NavigationResult = navigator.navigate(query)

    assert result.user_query == query
    assert result.parsed_intent.intent == "blast_radius"
    assert result.parsed_intent.target_node_id == "legacy-auth-module"

    # Cypher generation
    assert result.cypher_result.is_valid is True
    assert result.cypher_result.is_safe is True
    assert "$node_id" in result.cypher_result.cypher_query
    assert result.cypher_result.parameters["node_id"] == "legacy-auth-module"

    # Tool output & Reasoning
    assert result.tool_executed == "analyze_blast_radius"
    assert result.reasoning_result is not None
    assert result.reasoning_result.is_valid is True

    # Report verification
    report = result.report_markdown
    assert "legacy-auth-module" in report
    assert "`route-auth-login`" in report
    assert "`route-auth-verify`" in report
    assert "`web-portal`" in report
    assert "`mobile-app`" in report
    assert "```mermaid" in report


def test_end_to_end_navigator_cycle_query(navigator: AutonomousCodebaseNavigator):
    """Test full navigation for circular dependency detection inquiry."""
    result = navigator.navigate("Find circular dependencies")
    assert result.parsed_intent.intent == "detect_cycles"
    assert result.cypher_result.is_valid is True
    assert result.tool_executed == "detect_dependency_cycles"
    assert result.reasoning_result is not None
    assert len(result.reasoning_result.cycles) >= 1
    assert "Circular Dependencies Detected" in result.report_markdown


def test_end_to_end_navigator_coupling_query(navigator: AutonomousCodebaseNavigator):
    """Test full navigation for coupling analysis inquiry."""
    result = navigator.navigate("Analyze coupling of payment-service")
    assert result.parsed_intent.intent == "analyze_coupling"
    assert result.cypher_result.is_valid is True
    assert result.cypher_result.parameters["node_id"] == "payment-service"
    assert "Afferent Coupling" in result.report_markdown


def test_end_to_end_navigator_unsupported_query(navigator: AutonomousCodebaseNavigator):
    """Test full navigation on an unsupported question."""
    result = navigator.navigate("What is the recipe for chocolate cake?")
    assert result.parsed_intent.is_supported is False
    assert result.cypher_result.is_valid is False
    assert result.reasoning_result is None
    assert "Unsupported" in result.report_markdown


def test_navigation_result_json_serialization(navigator: AutonomousCodebaseNavigator):
    """Test that NavigationResult is 100% JSON-serializable."""
    result = navigator.navigate("What is the blast radius of legacy-auth-module?")
    dumped = result.model_dump()
    serialized = json.dumps(dumped)
    deserialized = json.loads(serialized)

    assert deserialized["user_query"] == "What is the blast radius of legacy-auth-module?"
    assert deserialized["parsed_intent"]["intent"] == "blast_radius"
    assert deserialized["cypher_result"]["is_safe"] is True
    assert "Architectural Impact" in deserialized["report_markdown"]

