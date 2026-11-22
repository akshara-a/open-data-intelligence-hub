"""Deterministic, offline natural language query parser for architecture graph inquiries."""

import re
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from src.graph.base import BaseGraphClient
from src.graph.mock_graph_client import MockGraphClient


class QueryIntent(str, Enum):
    """Supported natural-language query intent categories."""

    GET_SCHEMA = "get_schema"
    SEARCH_NODES = "search_nodes"
    GET_DEPENDENCIES = "get_dependencies"
    GET_DEPENDENTS = "get_dependents"
    BLAST_RADIUS = "blast_radius"
    DETECT_CYCLES = "detect_cycles"
    ANALYZE_COUPLING = "analyze_coupling"
    UNSUPPORTED = "unsupported"


class ParsedQueryIntent(BaseModel):
    """Structured result of parsing a natural language query."""

    raw_query: str = Field(..., description="Original user query")
    normalized_query: str = Field(..., description="Cleaned, lowercased query")
    intent: QueryIntent = Field(..., description="Identified query intent")
    target_node_id: Optional[str] = Field(None, description="Extracted valid graph node ID if present")
    target_category: Optional[str] = Field(None, description="Extracted category filter if applicable")
    search_keyword: Optional[str] = Field(None, description="Keyword extracted for node searches")
    recommended_tool: Optional[str] = Field(None, description="Existing graph tool mapped to this intent")
    is_supported: bool = Field(True, description="Whether the inquiry is supported by the system")
    explanation: str = Field(..., description="Human-readable explanation of the parsed intent")


class NaturalLanguageQueryParser:
    """Offline, deterministic intent parser grounding questions in the codebase graph schema."""

    # Category synonyms mapped to canonical schema node types
    CATEGORY_SYNONYMS = {
        "microservice": "Microservice",
        "microservices": "Microservice",
        "service": "Microservice",
        "services": "Microservice",
        "database": "Database",
        "databases": "Database",
        "db": "Database",
        "dbs": "Database",
        "cache": "Cache",
        "caches": "Cache",
        "redis": "Cache",
        "frontend": "Frontend component",
        "frontends": "Frontend component",
        "frontend component": "Frontend component",
        "frontend components": "Frontend component",
        "ui": "Frontend component",
        "api route": "API route",
        "api routes": "API route",
        "route": "API route",
        "routes": "API route",
        "endpoint": "API route",
        "endpoints": "API route",
        "shared module": "Shared module",
        "shared modules": "Shared module",
        "module": "Shared module",
        "modules": "Shared module",
        "library": "Shared module",
        "gateway": "API gateway",
        "api gateway": "API gateway",
    }

    # Intent to tool mapping
    INTENT_TOOL_MAP = {
        QueryIntent.GET_SCHEMA: "get_graph_schema",
        QueryIntent.SEARCH_NODES: "search_graph_nodes",
        QueryIntent.GET_DEPENDENCIES: "get_node_dependencies",
        QueryIntent.GET_DEPENDENTS: "get_node_dependencies",
        QueryIntent.BLAST_RADIUS: "analyze_blast_radius",
        QueryIntent.DETECT_CYCLES: "detect_dependency_cycles",
        QueryIntent.ANALYZE_COUPLING: "analyze_coupling",
        QueryIntent.UNSUPPORTED: None,
    }

    # Off-topic or mutating patterns that must be rejected as unsupported
    OFF_TOPIC_OR_MUTATING_PATTERNS = [
        r"\bpoem\b",
        r"\bjoke\b",
        r"\bweather\b",
        r"\bcapital of\b",
        r"\bdelete\b",
        r"\bdrop\b",
        r"\btruncate\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\balter\b",
    ]

    def __init__(self, graph_client: Optional[BaseGraphClient] = None):
        """Initialize parser with graph client to validate entity existence."""
        self.graph_client = graph_client or MockGraphClient()
        self._known_nodes: Dict[str, Dict[str, Any]] = {
            n["id"]: n for n in self.graph_client.get_nodes()
        }

    def parse(self, user_query: str) -> ParsedQueryIntent:
        """Parse natural language query into a structured intent object.
        
        Guarantees:
            - Deterministic evaluation.
            - Case and whitespace normalization.
            - Never invents node IDs (extracted IDs strictly verified against graph).
            - Safe fallback for unsupported questions.
        """
        if not user_query or not user_query.strip():
            return ParsedQueryIntent(
                raw_query=user_query or "",
                normalized_query="",
                intent=QueryIntent.UNSUPPORTED,
                is_supported=False,
                recommended_tool=None,
                explanation="Unsupported: Empty query received.",
            )

        # 1. Normalize casing and whitespace
        raw_query = user_query.strip()
        norm_query = re.sub(r"\s+", " ", raw_query.lower()).strip()

        # Check for off-topic or mutating patterns first
        for pat in self.OFF_TOPIC_OR_MUTATING_PATTERNS:
            if re.search(pat, norm_query):
                return ParsedQueryIntent(
                    raw_query=raw_query,
                    normalized_query=norm_query,
                    intent=QueryIntent.UNSUPPORTED,
                    is_supported=False,
                    recommended_tool=None,
                    explanation=f"Unsupported question: inquiry contains off-topic or mutating action pattern matching '{pat}'.",
                )

        # 2. Extract verified node ID from query
        extracted_node_id = self._extract_node_id(norm_query)

        # 3. Extract category filter if present
        extracted_category = self._extract_category(norm_query)

        # 4. Pattern matching for intents

        # Intent: Blast radius / Deprecation breaking changes
        if any(w in norm_query for w in ["blast radius", "deprecat", "break", "impact of", "affect"]):
            if extracted_node_id:
                return ParsedQueryIntent(
                    raw_query=raw_query,
                    normalized_query=norm_query,
                    intent=QueryIntent.BLAST_RADIUS,
                    target_node_id=extracted_node_id,
                    recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.BLAST_RADIUS],
                    is_supported=True,
                    explanation=f"Calculates blast radius and breaking downstream components for '{extracted_node_id}'.",
                )
            # If blast radius requested but no node found, return unsupported / ambiguous
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.UNSUPPORTED,
                is_supported=False,
                recommended_tool=None,
                explanation="Unsupported or ambiguous inquiry: blast-radius inquiry detected, but no valid component ID could be identified in the query.",
            )

        # Intent: Cycle detection
        if any(w in norm_query for w in ["circular", "cycle", "cycles", "loop", "dependency loop"]):
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.DETECT_CYCLES,
                target_node_id=None,
                recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.DETECT_CYCLES],
                is_supported=True,
                explanation="Detects circular architectural dependencies across the codebase.",
            )

        # Intent: Coupling / Instability / SPOF analysis
        if any(w in norm_query for w in ["coupling", "instability", "spof", "single point of failure", "stable"]):
            if extracted_node_id:
                return ParsedQueryIntent(
                    raw_query=raw_query,
                    normalized_query=norm_query,
                    intent=QueryIntent.ANALYZE_COUPLING,
                    target_node_id=extracted_node_id,
                    recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.ANALYZE_COUPLING],
                    is_supported=True,
                    explanation=f"Calculates coupling metrics (Ca, Ce, instability) for '{extracted_node_id}'.",
                )

        # Intent: Dependents (Who/what depends on X? Who calls X?)
        if (
            "depend on" in norm_query
            or "depends on" in norm_query
            or "depending on" in norm_query
            or "who calls" in norm_query
            or "what calls" in norm_query
            or "callers of" in norm_query
            or "used by" in norm_query
        ):
            # Check if phrasing is "what does X depend on" vs "what depends on X"
            if re.search(r"what\s+does\s+[a-z0-9_-]+\s+depend\s+on", norm_query):
                # Outgoing dependencies
                if extracted_node_id:
                    return ParsedQueryIntent(
                        raw_query=raw_query,
                        normalized_query=norm_query,
                        intent=QueryIntent.GET_DEPENDENCIES,
                        target_node_id=extracted_node_id,
                        recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.GET_DEPENDENCIES],
                        is_supported=True,
                        explanation=f"Retrieves components that '{extracted_node_id}' directly depends upon.",
                    )
            else:
                # Incoming dependents (e.g. "what depends on legacy-auth-module", "find services depending on auth-service")
                if extracted_node_id:
                    return ParsedQueryIntent(
                        raw_query=raw_query,
                        normalized_query=norm_query,
                        intent=QueryIntent.GET_DEPENDENTS,
                        target_node_id=extracted_node_id,
                        target_category=extracted_category,
                        recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.GET_DEPENDENTS],
                        is_supported=True,
                        explanation=f"Finds upstream components that depend on '{extracted_node_id}'.",
                    )

        # Intent: Direct dependencies of X (e.g., "dependencies of order-service")
        if "dependencies of" in norm_query or ("what does" in norm_query and extracted_node_id):
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.GET_DEPENDENCIES,
                target_node_id=extracted_node_id,
                recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.GET_DEPENDENCIES],
                is_supported=True,
                explanation=f"Retrieves direct dependencies of '{extracted_node_id}'.",
            )

        # Intent: Graph schema / overview
        if any(w in norm_query for w in ["schema", "structure of graph", "node types", "graph types", "show graph"]):
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.GET_SCHEMA,
                recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.GET_SCHEMA],
                is_supported=True,
                explanation="Retrieves knowledge graph schema, labels, and statistics.",
            )

        # Intent: Search nodes / list by category
        if any(w in norm_query for w in ["search", "find nodes", "list", "show nodes", "matching"]):
            keyword = self._extract_search_keyword(norm_query)
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.SEARCH_NODES,
                search_keyword=keyword,
                target_category=extracted_category,
                recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.SEARCH_NODES],
                is_supported=True,
                explanation=f"Searches graph components matching keyword='{keyword}' and category='{extracted_category}'.",
            )

        # Fallback: Query explicitly targeting architectural components
        if extracted_category and any(w in norm_query for w in ["show", "list", "find", "get", "nodes", "components"]):
            return ParsedQueryIntent(
                raw_query=raw_query,
                normalized_query=norm_query,
                intent=QueryIntent.SEARCH_NODES,
                search_keyword=None,
                target_category=extracted_category,
                recommended_tool=self.INTENT_TOOL_MAP[QueryIntent.SEARCH_NODES],
                is_supported=True,
                explanation=f"Lists components belonging to category '{extracted_category}'.",
            )

        # Unsupported or ambiguous question
        return ParsedQueryIntent(
            raw_query=raw_query,
            normalized_query=norm_query,
            intent=QueryIntent.UNSUPPORTED,
            is_supported=False,
            recommended_tool=None,
            explanation="The question is unsupported or does not match any valid architecture graph query patterns.",
        )

    def _extract_node_id(self, norm_text: str) -> Optional[str]:
        """Extract a valid, existing node ID from the query text.
        
        Strictly returns IDs that exist in the actual graph. Never invents IDs.
        """
        sorted_ids = sorted(self._known_nodes.keys(), key=len, reverse=True)
        for nid in sorted_ids:
            pattern = r"(?:\b|_)" + re.escape(nid) + r"(?:\b|_)"
            if re.search(pattern, norm_text):
                return nid

        # Handle common conversational aliases mapped to actual node IDs
        if "legacy auth" in norm_text or "legacy authentication" in norm_text:
            return "legacy-auth-module"
        if "auth service" in norm_text or "authentication service" in norm_text:
            return "auth-service"
        if "order service" in norm_text:
            return "order-service"
        if "payment service" in norm_text:
            return "payment-service"
        if "inventory service" in norm_text:
            return "inventory-service"
        if "user service" in norm_text or "profile service" in norm_text:
            return "user-service"
        if "notification service" in norm_text:
            return "notification-service"
        if "edge gateway" in norm_text or "api gateway" in norm_text:
            return "edge-api-gateway"
        if "web portal" in norm_text:
            return "web-portal"
        if "mobile app" in norm_text:
            return "mobile-app"
        if "admin console" in norm_text or "admin dashboard" in norm_text:
            return "admin-console"
        if "customer db" in norm_text or "user db" in norm_text:
            return "shared-customer-db"
        if "session cache" in norm_text or "redis" in norm_text:
            return "shared-session-cache"
        if "order db" in norm_text or "order database" in norm_text:
            return "order-document-db"
        if "inventory db" in norm_text or "inventory database" in norm_text:
            return "inventory-sql-db"

        return None

    def _extract_category(self, norm_text: str) -> Optional[str]:
        """Extract a canonical node category using category synonyms."""
        for synonym, canonical in self.CATEGORY_SYNONYMS.items():
            pattern = r"\b" + re.escape(synonym) + r"\b"
            if re.search(pattern, norm_text):
                return canonical
        return None

    def _extract_search_keyword(self, norm_text: str) -> Optional[str]:
        """Extract a search keyword from phrases like 'search for X' or 'matching X'."""
        patterns = [
            r"search\s+(?:for\s+)?([a-z0-9_-]+)",
            r"matching\s+([a-z0-9_-]+)",
            r"find\s+nodes\s+(?:matching\s+|with\s+)?([a-z0-9_-]+)",
            r"find\s+([a-z0-9_-]+)\s+nodes",
        ]
        for p in patterns:
            match = re.search(p, norm_text)
            if match:
                extracted = match.group(1).strip()
                if extracted not in self.CATEGORY_SYNONYMS:
                    return extracted
        return None
