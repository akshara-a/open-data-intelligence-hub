"""Autonomous codebase knowledge graph navigator orchestrating query parsing, Cypher generation, tool execution, reasoning, and report synthesis."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from src.agent.architecture_reasoner import (
    ArchitectureAnalysisResult,
    ArchitectureReasoner,
)
from src.agent.cypher_generator import GeneratedCypherResult, SafeCypherGenerator
from src.agent.query_parser import (
    NaturalLanguageQueryParser,
    ParsedQueryIntent,
    QueryIntent,
)
from src.agent.report_synthesizer import ReportSynthesizer
from src.graph.base import BaseGraphClient
from src.graph.mock_graph_client import MockGraphClient
from src.mcp.tools import GraphToolRegistry


class NavigationResult(BaseModel):
    """Complete structured output from the autonomous knowledge graph navigator."""

    user_query: str = Field(..., description="Original developer inquiry")
    parsed_intent: ParsedQueryIntent = Field(..., description="Structured intent analysis")
    cypher_result: GeneratedCypherResult = Field(..., description="Schema-aware parameterized Cypher query")
    tool_executed: Optional[str] = Field(None, description="Name of the MCP tool invoked")
    tool_output: Optional[Dict[str, Any]] = Field(None, description="Raw data returned from the tool")
    reasoning_result: Optional[ArchitectureAnalysisResult] = Field(None, description="Architectural reasoning and risk analysis")
    report_markdown: str = Field(..., description="Synthesized technical Markdown report")


class AutonomousCodebaseNavigator:
    """Multi-step autonomous agent for codebase knowledge graph exploration and refactoring strategy synthesis.
    
    Workflow:
        1. Query Understanding: Parses natural language developer inquiry into canonical intent and entity.
        2. Cypher Translation: Generates schema-grounded, parameterized Cypher templates.
        3. Safe Graph Retrieval: Dispatches safe read-only queries to the MCP tool registry.
        4. Architectural Reasoning: Evaluates blast radius, coupling metrics, cycles, and evidence-based risks.
        5. Generative Synthesis: Compiles structured facts into senior-engineer-grade technical Markdown reports.
    """

    def __init__(
        self,
        graph_client: Optional[BaseGraphClient] = None,
        tool_registry: Optional[GraphToolRegistry] = None,
    ):
        """Initialize navigator with underlying graph client, registry, reasoner, and synthesizer."""
        self.graph_client = graph_client or MockGraphClient()
        self.tool_registry = tool_registry or GraphToolRegistry(graph_client=self.graph_client)
        self.parser = NaturalLanguageQueryParser(graph_client=self.graph_client)
        self.cypher_generator = SafeCypherGenerator(
            graph_client=self.graph_client,
            parser=self.parser,
        )
        self.reasoner = ArchitectureReasoner(
            graph_client=self.graph_client,
            tool_registry=self.tool_registry,
        )
        self.synthesizer = ReportSynthesizer(reasoner=self.reasoner)

    def navigate(self, user_query: str) -> NavigationResult:
        """Execute autonomous end-to-end navigation workflow for a developer inquiry.
        
        Args:
            user_query: Developer question regarding system architecture or deprecation impact.
            
        Returns:
            NavigationResult containing intent, Cypher, tool outputs, reasoning, and Markdown report.
        """
        # Step 1: Natural-language query understanding
        parsed_intent = self.parser.parse(user_query)

        # Step 2: Cypher query generation (parameterized, read-only)
        cypher_res = self.cypher_generator.generate_from_parsed(parsed_intent)

        # Step 3: Handle unsupported queries safely
        if not parsed_intent.is_supported or parsed_intent.intent == QueryIntent.UNSUPPORTED:
            report_md = (
                f"# Architectural Inquiry Unsupported\n\n"
                f"> **Inquiry:** *\"{user_query}\"*\n\n"
                f"### Status: REJECTED\n"
                f"The question could not be mapped to a supported codebase graph inquiry pattern. "
                f"Please query for component dependencies, blast radius (e.g. *'What is the blast radius of legacy-auth-module?'*), "
                f"coupling metrics, or circular dependencies."
            )
            return NavigationResult(
                user_query=user_query,
                parsed_intent=parsed_intent,
                cypher_result=cypher_res,
                tool_executed=None,
                tool_output=None,
                reasoning_result=None,
                report_markdown=report_md,
            )

        tool_name = parsed_intent.recommended_tool
        tool_output: Optional[Dict[str, Any]] = None
        reasoning_res: Optional[ArchitectureAnalysisResult] = None
        report_md: str = ""

        # Step 4: Tool execution and architectural reasoning
        if parsed_intent.intent == QueryIntent.BLAST_RADIUS:
            target_id = parsed_intent.target_node_id or "legacy-auth-module"
            reasoning_res = self.reasoner.analyze_component(target_id)
            tool_output = reasoning_res.model_dump()
            report_md = self.synthesizer.synthesize(reasoning_res, user_query=user_query)

        elif parsed_intent.intent == QueryIntent.DETECT_CYCLES:
            reasoning_res = self.reasoner.analyze_global_architecture()
            tool_output = reasoning_res.model_dump()
            report_md = self.synthesizer.synthesize(reasoning_res, user_query=user_query)

        elif parsed_intent.intent == QueryIntent.ANALYZE_COUPLING:
            target_id = parsed_intent.target_node_id
            if target_id:
                reasoning_res = self.reasoner.analyze_component(target_id)
                tool_output = reasoning_res.model_dump()
                report_md = self.synthesizer.synthesize(reasoning_res, user_query=user_query)
            else:
                reasoning_res = self.reasoner.analyze_global_architecture()
                tool_output = reasoning_res.model_dump()
                report_md = self.synthesizer.synthesize(reasoning_res, user_query=user_query)

        elif parsed_intent.intent == QueryIntent.GET_SCHEMA:
            tool_res = self.tool_registry.call_tool("get_graph_schema")
            tool_output = tool_res.get("data")
            report_md = self._format_schema_report(tool_output)

        elif parsed_intent.intent == QueryIntent.SEARCH_NODES:
            args = {"query": parsed_intent.search_keyword or ""}
            if parsed_intent.target_category:
                args["category"] = parsed_intent.target_category
            tool_res = self.tool_registry.call_tool("search_graph_nodes", args)
            tool_output = {"results": tool_res.get("data", [])}
            report_md = self._format_search_report(tool_output, query_term=args.get("query"))

        elif parsed_intent.intent in (QueryIntent.GET_DEPENDENCIES, QueryIntent.GET_DEPENDENTS):
            target_id = parsed_intent.target_node_id or ""
            tool_res = self.tool_registry.call_tool("get_node_dependencies", {"node_id": target_id})
            tool_output = tool_res.get("data")
            report_md = self._format_dependency_report(tool_output)

        return NavigationResult(
            user_query=user_query,
            parsed_intent=parsed_intent,
            cypher_result=cypher_res,
            tool_executed=tool_name,
            tool_output=tool_output,
            reasoning_result=reasoning_res,
            report_markdown=report_md,
        )

    # Markdown formatters for non-blast-radius queries
    def _format_schema_report(self, schema_data: Optional[Dict[str, Any]]) -> str:
        data = schema_data or {}
        lines = [
            "# Codebase Knowledge Graph Schema Summary\n",
            f"* **Total Graph Nodes:** {data.get('total_nodes', 0)}",
            f"* **Total Architectural Edges:** {data.get('total_edges', 0)}\n",
            "### Available Node Categories",
        ]
        for cat, cnt in data.get("node_type_counts", {}).items():
            lines.append(f"* **{cat}:** {cnt} components")
        lines.append("\n### Available Relationship Types")
        for rel, cnt in data.get("relationship_type_counts", {}).items():
            lines.append(f"* `[:{rel}]`: {cnt} connections")
        return "\n".join(lines)

    def _format_search_report(self, search_data: Optional[Dict[str, Any]], query_term: Optional[str]) -> str:
        results = (search_data or {}).get("results", [])
        lines = [
            f"# Node Search Results: '{query_term or 'All'}'\n",
            f"Found **{len(results)}** matching components in the knowledge graph:\n",
            "| Component ID | Type | Name | Description |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for item in results:
            lines.append(f"| `{item.get('id')}` | {item.get('type')} | {item.get('name')} | {item.get('description', '')[:60]}... |")
        return "\n".join(lines)

    def _format_dependency_report(self, dep_data: Optional[Dict[str, Any]]) -> str:
        data = dep_data or {}
        nid = data.get("node_id", "Component")
        direct_deps = data.get("direct_dependencies", [])
        direct_callers = data.get("direct_dependents", [])
        lines = [
            f"# Architectural Connections for `{nid}`\n",
            f"**Component Type:** {data.get('type')} | **Name:** {data.get('name')}\n",
            f"### Direct Outgoing Dependencies ({len(direct_deps)})",
            "Components that this module depends upon or calls:\n",
        ]
        for d in direct_deps:
            lines.append(f"* `{d}`")
        lines.append(f"\n### Direct Incoming Callers ({len(direct_callers)})")
        lines.append("Components that depend on or invoke this module:\n")
        for c in direct_callers:
            lines.append(f"* `{c}`")
        return "\n".join(lines)
