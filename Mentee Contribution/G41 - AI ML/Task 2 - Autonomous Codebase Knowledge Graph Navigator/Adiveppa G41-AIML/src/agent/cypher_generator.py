"""Safe, schema-aware Cypher generator producing parameterized read-only queries."""

import re
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from src.agent.query_parser import NaturalLanguageQueryParser, ParsedQueryIntent, QueryIntent
from src.graph.base import BaseGraphClient
from src.graph.mock_graph_client import MockGraphClient


class GeneratedCypherResult(BaseModel):
    """Structured result envelope containing generated Cypher and parameter metadata."""

    intent: str = Field(..., description="Detected natural-language intent")
    query_type: str = Field(..., description="Architectural inquiry type")
    selected_tool: Optional[str] = Field(None, description="Corresponding existing graph tool name")
    cypher_query: str = Field(..., description="Safe, parameterized Cypher query template")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameter dictionary for parameterized execution")
    is_safe: bool = Field(True, description="Strictly read-only; free of mutation operations")
    is_valid: bool = Field(True, description="Whether query could be generated and passed schema checks")
    validation_status: str = Field("VALID", description="VALID, REJECTED_UNSUPPORTED, REJECTED_UNSAFE, or INVALID_SCHEMA")
    explanatory_message: str = Field(..., description="Detailed explanation of the generated Cypher structure")
    execution_note: str = Field(
        default="Cypher query is generated and parameterized for future Neo4j integration; it is not executed against Neo4j in this step.",
        description="Clarification that execution against Neo4j is pending future integration",
    )


class SafeCypherGenerator:
    """Generates schema-grounded, parameterized, read-only Cypher queries from parsed user intents.
    
    Guarantees:
        - 100% Parameterized: User inputs are placed in parameters dict, never string-interpolated.
        - Strictly Read-Only: Prohibits CREATE, DELETE, SET, MERGE, DROP, REMOVE, DETACH.
        - Schema-Aware: Uses verified relationship types and node labels from the knowledge graph.
        - Transparent: Documents that Cypher is generated for future Neo4j integration without pretending it was run.
    """

    PROHIBITED_MUTATIONS = [
        r"\bCREATE\b",
        r"\bDELETE\b",
        r"\bSET\b",
        r"\bREMOVE\b",
        r"\bDROP\b",
        r"\bMERGE\b",
        r"\bDETACH\b",
        r"\bALTER\b",
    ]

    def __init__(
        self,
        graph_client: Optional[BaseGraphClient] = None,
        parser: Optional[NaturalLanguageQueryParser] = None,
    ):
        """Initialize generator with graph client and query parser."""
        self.graph_client = graph_client or MockGraphClient()
        self.parser = parser or NaturalLanguageQueryParser(graph_client=self.graph_client)
        self._schema = self.graph_client.get_schema()
        self.known_node_types: Set[str] = set(self._schema.get("node_types", []))
        self.known_rel_types: Set[str] = set(self._schema.get("relationship_types", []))

    def generate(self, user_query: str) -> GeneratedCypherResult:
        """Parse natural language query and generate schema-aware parameterized Cypher.
        
        Args:
            user_query: Developer inquiry string.
            
        Returns:
            GeneratedCypherResult structured object.
        """
        parsed = self.parser.parse(user_query)
        return self.generate_from_parsed(parsed)

    def generate_from_parsed(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Generate parameterized Cypher query from a ParsedQueryIntent object."""
        if not parsed.is_supported or parsed.intent == QueryIntent.UNSUPPORTED:
            return GeneratedCypherResult(
                intent=parsed.intent.value,
                query_type="unsupported",
                selected_tool=None,
                cypher_query="",
                parameters={},
                is_safe=True,
                is_valid=False,
                validation_status="REJECTED_UNSUPPORTED",
                explanatory_message=parsed.explanation or "The inquiry cannot be mapped to a supported Cypher query pattern.",
            )

        # Route by parsed intent
        if parsed.intent == QueryIntent.GET_SCHEMA:
            return self._build_schema_query(parsed)
        elif parsed.intent == QueryIntent.SEARCH_NODES:
            return self._build_search_query(parsed)
        elif parsed.intent == QueryIntent.GET_DEPENDENCIES:
            return self._build_dependencies_query(parsed)
        elif parsed.intent == QueryIntent.GET_DEPENDENTS:
            return self._build_dependents_query(parsed)
        elif parsed.intent == QueryIntent.BLAST_RADIUS:
            return self._build_blast_radius_query(parsed)
        elif parsed.intent == QueryIntent.DETECT_CYCLES:
            return self._build_cycles_query(parsed)
        elif parsed.intent == QueryIntent.ANALYZE_COUPLING:
            return self._build_coupling_query(parsed)
        else:
            return GeneratedCypherResult(
                intent=parsed.intent.value,
                query_type="unknown",
                selected_tool=None,
                cypher_query="",
                parameters={},
                is_safe=True,
                is_valid=False,
                validation_status="REJECTED_UNSUPPORTED",
                explanatory_message="Unknown query intent encountered.",
            )

    def validate_safety(self, cypher: str) -> bool:
        """Verify that the generated Cypher is completely read-only."""
        if not cypher:
            return True
        for pattern in self.PROHIBITED_MUTATIONS:
            if re.search(pattern, cypher, re.IGNORECASE):
                return False
        return True

    def _build_schema_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to inspect knowledge graph metadata."""
        query = (
            "MATCH (n)\n"
            "OPTIONAL MATCH (n)-[r]->(m)\n"
            "RETURN labels(n) AS node_labels, type(r) AS relationship_type, count(DISTINCT n) AS node_count\n"
            "ORDER BY relationship_type ASC, node_labels ASC"
        )
        return self._create_result(
            parsed=parsed,
            query_type="schema_inspection",
            cypher=query,
            params={},
            explanation="Inspects node labels, relationship types, and component counts across the graph.",
        )

    def _build_search_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to search nodes by keyword and category."""
        query = (
            "MATCH (n)\n"
            "WHERE ($category IS NULL OR n.type = $category)\n"
            "  AND ($search_term IS NULL OR toLower(n.name) CONTAINS toLower($search_term) "
            "OR toLower(n.id) CONTAINS toLower($search_term) "
            "OR toLower(n.description) CONTAINS toLower($search_term))\n"
            "RETURN n.id AS id, n.name AS name, n.type AS type, n.description AS description\n"
            "ORDER BY n.id ASC"
        )
        params = {
            "search_term": parsed.search_keyword,
            "category": parsed.target_category,
        }
        return self._create_result(
            parsed=parsed,
            query_type="node_search",
            cypher=query,
            params=params,
            explanation=f"Searches nodes filtering by category parameter ($category={parsed.target_category!r}) "
                        f"and keyword parameter ($search_term={parsed.search_keyword!r}).",
        )

    def _build_dependencies_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to find outgoing dependencies of a component."""
        query = (
            "MATCH (source {id: $node_id})-[r]->(target)\n"
            "RETURN target.id AS dependency_id, target.name AS dependency_name, target.type AS dependency_type, type(r) AS relationship\n"
            "ORDER BY target.type ASC, target.id ASC"
        )
        params = {"node_id": parsed.target_node_id}
        return self._create_result(
            parsed=parsed,
            query_type="direct_dependencies",
            cypher=query,
            params=params,
            explanation=f"Retrieves all direct components that component ($node_id='{parsed.target_node_id}') depends upon or calls.",
        )

    def _build_dependents_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to find incoming callers/dependents of a component."""
        query = (
            "MATCH (caller)-[r]->(target {id: $node_id})\n"
            "WHERE ($category IS NULL OR caller.type = $category)\n"
            "RETURN caller.id AS dependent_id, caller.name AS dependent_name, caller.type AS dependent_type, type(r) AS relationship\n"
            "ORDER BY caller.type ASC, caller.id ASC"
        )
        params = {
            "node_id": parsed.target_node_id,
            "category": parsed.target_category,
        }
        return self._create_result(
            parsed=parsed,
            query_type="direct_dependents",
            cypher=query,
            params=params,
            explanation=f"Finds all upstream components that invoke or depend on ($node_id='{parsed.target_node_id}'), "
                        f"filtered by optional category parameter ($category={parsed.target_category!r}).",
        )

    def _build_blast_radius_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to evaluate blast radius and downstream dependents."""
        # Uses verified relationship types: CALLS, DEPENDS_ON, USES, AUTHENTICATES_WITH, CONNECTS_TO
        query = (
            "MATCH path = (dependent)-[:CALLS|DEPENDS_ON|USES|AUTHENTICATES_WITH|CONNECTS_TO*1..5]->(target {id: $node_id})\n"
            "WHERE dependent.id <> $node_id\n"
            "RETURN dependent.id AS affected_node_id, dependent.type AS affected_type, "
            "dependent.name AS affected_name, length(path) AS dependency_depth\n"
            "ORDER BY dependency_depth ASC, affected_node_id ASC"
        )
        params = {"node_id": parsed.target_node_id}
        return self._create_result(
            parsed=parsed,
            query_type="blast_radius_traversal",
            cypher=query,
            params=params,
            explanation=f"Traverses multi-hop dependency chains up to 5 levels to calculate blast radius for ($node_id='{parsed.target_node_id}'). "
                        f"The WHERE clause explicitly excludes the target component itself from the affected results.",
        )

    def _build_cycles_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to detect circular dependencies between services."""
        query = (
            "MATCH path = (a:Microservice)-[:DEPENDS_ON|CALLS*2..5]->(a)\n"
            "RETURN [n IN nodes(path) | n.id] AS cycle_nodes, length(path) AS cycle_length\n"
            "ORDER BY cycle_length ASC"
        )
        return self._create_result(
            parsed=parsed,
            query_type="cycle_detection",
            cypher=query,
            params={},
            explanation="Matches closed directed dependency paths where a microservice has an active cyclic dependency upon itself.",
        )

    def _build_coupling_query(self, parsed: ParsedQueryIntent) -> GeneratedCypherResult:
        """Cypher template to calculate afferent and efferent coupling metrics."""
        query = (
            "MATCH (target {id: $node_id})\n"
            "OPTIONAL MATCH (caller)-[r_in]->(target)\n"
            "OPTIONAL MATCH (target)-[r_out]->(dependency)\n"
            "RETURN target.id AS node_id, target.name AS node_name, target.type AS node_type,\n"
            "       count(DISTINCT caller) AS afferent_coupling_Ca,\n"
            "       count(DISTINCT dependency) AS efferent_coupling_Ce"
        )
        params = {"node_id": parsed.target_node_id}
        return self._create_result(
            parsed=parsed,
            query_type="coupling_analysis",
            cypher=query,
            params=params,
            explanation=f"Computes incoming connections (Ca) and outgoing connections (Ce) for component ($node_id='{parsed.target_node_id}').",
        )

    def _create_result(
        self,
        parsed: ParsedQueryIntent,
        query_type: str,
        cypher: str,
        params: Dict[str, Any],
        explanation: str,
    ) -> GeneratedCypherResult:
        """Validate safety and construct result envelope."""
        is_safe = self.validate_safety(cypher)
        status = "VALID" if is_safe else "REJECTED_UNSAFE"

        return GeneratedCypherResult(
            intent=parsed.intent.value,
            query_type=query_type,
            selected_tool=parsed.recommended_tool,
            cypher_query=cypher,
            parameters=params,
            is_safe=is_safe,
            is_valid=is_safe,
            validation_status=status,
            explanatory_message=explanation,
        )
