"""Unit tests for the NaturalLanguageQueryParser."""

import json
import pytest

from src.agent.query_parser import NaturalLanguageQueryParser, QueryIntent
from src.graph.mock_graph_client import MockGraphClient


@pytest.fixture
def parser() -> NaturalLanguageQueryParser:
    """Fixture providing a fresh NaturalLanguageQueryParser backed by MockGraphClient."""
    return NaturalLanguageQueryParser(graph_client=MockGraphClient())


def test_supported_natural_language_queries(parser: NaturalLanguageQueryParser):
    """Test all explicitly required example questions from the prompt."""
    test_cases = [
        ("Show graph schema", QueryIntent.GET_SCHEMA, None),
        ("Find services depending on auth-service", QueryIntent.GET_DEPENDENTS, "auth-service"),
        ("What depends on legacy-auth-module?", QueryIntent.GET_DEPENDENTS, "legacy-auth-module"),
        ("What is the blast radius of order-service?", QueryIntent.BLAST_RADIUS, "order-service"),
        ("Find circular dependencies", QueryIntent.DETECT_CYCLES, None),
        ("Analyze coupling of payment-service", QueryIntent.ANALYZE_COUPLING, "payment-service"),
        ("Search for database nodes", QueryIntent.SEARCH_NODES, None),
        ("Find nodes matching authentication", QueryIntent.SEARCH_NODES, None),
    ]

    for question, expected_intent, expected_node in test_cases:
        res = parser.parse(question)
        assert res.intent == expected_intent, f"Failed on '{question}': got {res.intent}"
        assert res.is_supported is True
        if expected_node:
            assert res.target_node_id == expected_node


def test_case_and_whitespace_normalization(parser: NaturalLanguageQueryParser):
    """Test that parser normalizes uppercase letters, irregular spacing, and leading/trailing tabs."""
    queries = [
        "   WHAT   IS   THE   BLAST   RADIUS   OF   ORDER-SERVICE?   ",
        "\twhat is the blast radius of order-service?\n",
        "What Is The Blast Radius Of Order-Service?",
    ]

    for q in queries:
        res = parser.parse(q)
        assert res.intent == QueryIntent.BLAST_RADIUS
        assert res.target_node_id == "order-service"
        assert res.normalized_query == "what is the blast radius of order-service?"


def test_synonym_recognition(parser: NaturalLanguageQueryParser):
    """Test recognition of architectural category and intent synonyms."""
    # 'db' -> Database
    res_db = parser.parse("search for db nodes")
    assert res_db.intent == QueryIntent.SEARCH_NODES
    assert res_db.target_category == "Database"

    # 'services' -> Microservice
    res_svc = parser.parse("find microservices")
    assert res_svc.intent == QueryIntent.SEARCH_NODES
    assert res_svc.target_category == "Microservice"

    # 'redis' / 'cache' -> Cache
    res_cache = parser.parse("list cache nodes")
    assert res_cache.intent == QueryIntent.SEARCH_NODES
    assert res_cache.target_category == "Cache"

    # 'loop' / 'circular' -> Cycle detection
    res_loop = parser.parse("detect dependency loops")
    assert res_loop.intent == QueryIntent.DETECT_CYCLES


def test_node_id_extraction_accuracy(parser: NaturalLanguageQueryParser):
    """Test exact extraction of valid graph node IDs without partial match collisions."""
    # Exact hyphenated ID
    res1 = parser.parse("What depends on legacy-auth-module?")
    assert res1.target_node_id == "legacy-auth-module"

    # Natural conversational phrasing mapped to valid node ID
    res2 = parser.parse("Analyze coupling for legacy auth module")
    assert res2.target_node_id == "legacy-auth-module"

    res3 = parser.parse("What is the blast radius of web portal?")
    assert res3.target_node_id == "web-portal"

    res4 = parser.parse("Show dependencies of edge api gateway")
    assert res4.target_node_id == "edge-api-gateway"


def test_unknown_node_and_ambiguous_handling(parser: NaturalLanguageQueryParser):
    """Test handling of unknown nodes and ambiguous questions."""
    # Unknown component ID
    res = parser.parse("What is the blast radius of nonexistent-phantom-service?")
    # Must NOT invent IDs; if ID is not in graph, should gracefully report unsupported/ambiguous
    assert res.target_node_id is None
    assert res.is_supported is False
    assert res.intent == QueryIntent.UNSUPPORTED

    # Ambiguous question without node ID
    res_ambiguous = parser.parse("What is the blast radius?")
    assert res_ambiguous.is_supported is False
    assert res_ambiguous.target_node_id is None


def test_unsupported_questions(parser: NaturalLanguageQueryParser):
    """Test handling of completely unsupported questions."""
    unsupported_queries = [
        "Write a poem about microservices",
        "What is the capital of France?",
        "Delete all tables in PostgreSQL",
        "",
        "   ",
    ]

    for q in unsupported_queries:
        res = parser.parse(q)
        assert res.is_supported is False
        assert res.intent == QueryIntent.UNSUPPORTED
        assert res.recommended_tool is None


def test_parsed_intent_json_serializability(parser: NaturalLanguageQueryParser):
    """Test that all fields in ParsedQueryIntent are 100% JSON-serializable."""
    res = parser.parse("What is the blast radius of legacy-auth-module?")
    dumped_dict = res.model_dump()
    serialized = json.dumps(dumped_dict)
    deserialized = json.loads(serialized)

    assert deserialized["intent"] == "blast_radius"
    assert deserialized["target_node_id"] == "legacy-auth-module"
    assert deserialized["is_supported"] is True
    assert deserialized["recommended_tool"] == "analyze_blast_radius"

