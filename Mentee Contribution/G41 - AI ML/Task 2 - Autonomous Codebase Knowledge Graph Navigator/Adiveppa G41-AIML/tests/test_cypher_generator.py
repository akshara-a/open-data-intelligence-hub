"""Unit tests for the SafeCypherGenerator."""

import json
import pytest

from src.agent.cypher_generator import GeneratedCypherResult, SafeCypherGenerator
from src.agent.query_parser import NaturalLanguageQueryParser
from src.graph.mock_graph_client import MockGraphClient


@pytest.fixture
def cypher_generator() -> SafeCypherGenerator:
    """Fixture providing a fresh SafeCypherGenerator instance."""
    client = MockGraphClient()
    parser = NaturalLanguageQueryParser(graph_client=client)
    return SafeCypherGenerator(graph_client=client, parser=parser)


def test_schema_cypher_generation(cypher_generator: SafeCypherGenerator):
    """Test Cypher generation for graph schema inspection."""
    res = cypher_generator.generate("Show graph schema")
    assert res.is_valid is True
    assert res.is_safe is True
    assert res.intent == "get_schema"
    assert res.query_type == "schema_inspection"
    assert "MATCH (n)" in res.cypher_query
    assert "labels(n)" in res.cypher_query
    assert res.parameters == {}


def test_search_cypher_parameterization(cypher_generator: SafeCypherGenerator):
    """Test that search queries use Cypher parameters and never raw string interpolation."""
    res = cypher_generator.generate("Search for database nodes matching user")
    assert res.is_valid is True
    assert res.intent == "search_nodes"

    # Must contain parameter placeholders $category and $search_term
    assert "$category" in res.cypher_query
    assert "$search_term" in res.cypher_query

    # Parameters dictionary must contain the actual extracted values
    assert res.parameters.get("category") == "Database"
    assert res.parameters.get("search_term") == "user"

    # Cypher body must NOT contain literal raw strings
    assert "n.type = 'Database'" not in res.cypher_query


def test_dependencies_and_dependents_parameterization(cypher_generator: SafeCypherGenerator):
    """Test parameterized Cypher generation for direct dependencies and callers."""
    # Outgoing dependencies
    res_out = cypher_generator.generate("What does order-service depend on?")
    assert res_out.is_valid is True
    assert res_out.intent == "get_dependencies"
    assert "$node_id" in res_out.cypher_query
    assert res_out.parameters == {"node_id": "order-service"}

    # Incoming callers/dependents
    res_in = cypher_generator.generate("What depends on legacy-auth-module?")
    assert res_in.is_valid is True
    assert res_in.intent == "get_dependents"
    assert "$node_id" in res_in.cypher_query
    assert res_in.parameters["node_id"] == "legacy-auth-module"


def test_blast_radius_cypher_and_source_exclusion(cypher_generator: SafeCypherGenerator):
    """Test blast-radius Cypher query structure, parameterization, and source node exclusion."""
    res = cypher_generator.generate("What is the blast radius of legacy-auth-module?")
    assert res.is_valid is True
    assert res.intent == "blast_radius"
    assert res.query_type == "blast_radius_traversal"

    # Parameterized with target node ID
    assert "$node_id" in res.cypher_query
    assert res.parameters == {"node_id": "legacy-auth-module"}

    # Must traverse incoming relationships up to 5 hops
    assert "*1..5" in res.cypher_query
    assert "[:CALLS|DEPENDS_ON|USES|AUTHENTICATES_WITH|CONNECTS_TO*1..5]" in res.cypher_query

    # Must explicitly exclude starting node from affected dependents in WHERE clause
    assert "WHERE dependent.id <> $node_id" in res.cypher_query


def test_cycle_detection_cypher(cypher_generator: SafeCypherGenerator):
    """Test Cypher generation for cycle detection."""
    res = cypher_generator.generate("Find circular dependencies")
    assert res.is_valid is True
    assert res.intent == "detect_cycles"
    assert res.query_type == "cycle_detection"
    assert "MATCH path = (a:Microservice)-[:DEPENDS_ON|CALLS*2..5]->(a)" in res.cypher_query


def test_coupling_analysis_cypher(cypher_generator: SafeCypherGenerator):
    """Test Cypher generation for coupling metrics calculation."""
    res = cypher_generator.generate("Analyze coupling of payment-service")
    assert res.is_valid is True
    assert res.intent == "analyze_coupling"
    assert res.query_type == "coupling_analysis"
    assert "$node_id" in res.cypher_query
    assert res.parameters == {"node_id": "payment-service"}
    assert "count(DISTINCT caller) AS afferent_coupling_Ca" in res.cypher_query
    assert "count(DISTINCT dependency) AS efferent_coupling_Ce" in res.cypher_query


def test_no_write_or_mutation_queries(cypher_generator: SafeCypherGenerator):
    """Test that all generated Cypher queries are strictly read-only and mutations are rejected."""
    prohibited = ["CREATE", "DELETE", "SET", "MERGE", "DROP", "REMOVE", "DETACH"]

    test_queries = [
        "Show graph schema",
        "What depends on legacy-auth-module?",
        "What is the blast radius of order-service?",
        "Find circular dependencies",
        "Analyze coupling of payment-service",
    ]

    for q in test_queries:
        res = cypher_generator.generate(q)
        for keyword in prohibited:
            assert f" {keyword} " not in f" {res.cypher_query} "
        assert res.is_safe is True
        assert res.validation_status == "VALID"


def test_unsupported_query_handling(cypher_generator: SafeCypherGenerator):
    """Test that unsupported questions produce safe, non-executable rejection envelopes."""
    res = cypher_generator.generate("How do I make chocolate cake?")
    assert res.is_valid is False
    assert res.cypher_query == ""
    assert res.validation_status == "REJECTED_UNSUPPORTED"
    assert "cannot be mapped" in res.explanatory_message.lower() or "unsupported" in res.explanatory_message.lower()


def test_execution_note_clarification(cypher_generator: SafeCypherGenerator):
    """Test that execution note explicitly states Cypher is generated for future Neo4j integration."""
    res = cypher_generator.generate("Show graph schema")
    assert "not executed against Neo4j in this step" in res.execution_note
    assert "future Neo4j integration" in res.execution_note


def test_cypher_result_json_serializability(cypher_generator: SafeCypherGenerator):
    """Test that GeneratedCypherResult is 100% JSON serializable."""
    res = cypher_generator.generate("What is the blast radius of legacy-auth-module?")
    dumped = res.model_dump()
    serialized = json.dumps(dumped)
    deserialized = json.loads(serialized)

    assert deserialized["intent"] == "blast_radius"
    assert deserialized["is_safe"] is True
    assert deserialized["parameters"]["node_id"] == "legacy-auth-module"

