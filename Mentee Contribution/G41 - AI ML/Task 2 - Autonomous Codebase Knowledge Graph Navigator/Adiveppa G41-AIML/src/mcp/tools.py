"""Safe, read-only graph tool definitions and registry for codebase knowledge navigation."""

import json
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from src.graph.base import BaseGraphClient
from src.graph.mock_graph_client import MockGraphClient


class ToolDefinition(BaseModel):
    """Specification of a read-only graph analysis tool."""

    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Clear explanation of the tool's purpose and usage")
    input_schema: Dict[str, Any] = Field(..., description="JSON Schema for input parameter validation")


class GraphToolRegistry:
    """Safe, read-only tool registry and execution dispatcher for codebase knowledge graphs.
    
    Guarantees:
        - 100% read-only operations (no write, update, create, or delete tools).
        - Comprehensive argument validation.
        - Structured, JSON-serializable output envelopes.
        - Reuse of verified graph algorithms without duplication.
    """

    # Prohibited mutating operation keywords to prevent write-tool exposure
    PROHIBITED_MUTATION_KEYWORDS = {"create", "delete", "update", "set", "remove", "drop", "merge", "write"}

    def __init__(self, graph_client: Optional[BaseGraphClient] = None):
        """Initialize registry with a backing graph client."""
        self.graph_client = graph_client or MockGraphClient()
        self._tools: Dict[str, ToolDefinition] = {}
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register the 6 mandatory read-only graph analysis tools."""
        # 1. get_graph_schema
        self._register_tool(
            name="get_graph_schema",
            description="Inspect and return the knowledge graph structural schema, including node types, relationship types, total counts, and available node IDs.",
            input_schema={
                "type": "object",
                "properties": {},
                "required": [],
            },
            handler=self._handle_get_graph_schema,
        )

        # 2. search_graph_nodes
        self._register_tool(
            name="search_graph_nodes",
            description="Search for existing components in the knowledge graph by keyword across node IDs, names, types, and descriptions. Case-insensitive and strictly returns existing nodes only.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword or phrase (e.g., 'auth', 'order', 'database')",
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional category filter (e.g., 'Microservice', 'Database', 'API route')",
                    },
                },
                "required": ["query"],
            },
            handler=self._handle_search_graph_nodes,
        )

        # 3. get_node_dependencies
        self._register_tool(
            name="get_node_dependencies",
            description="Retrieve immediate architectural connections for a component: direct dependencies (outgoing) and direct dependents (incoming).",
            input_schema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Unique component ID (e.g., 'legacy-auth-module', 'order-service')",
                    }
                },
                "required": ["node_id"],
            },
            handler=self._handle_get_node_dependencies,
        )

        # 4. analyze_blast_radius
        self._register_tool(
            name="analyze_blast_radius",
            description="Evaluate the blast radius of modifying or deprecating a component. Returns downstream affected components, traversal paths, and counts grouped by type. The target node itself is strictly excluded from affected counts.",
            input_schema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "ID of the component to analyze for deprecation impact",
                    }
                },
                "required": ["node_id"],
            },
            handler=self._handle_analyze_blast_radius,
        )

        # 5. detect_dependency_cycles
        self._register_tool(
            name="detect_dependency_cycles",
            description="Detect circular architectural dependency loops across services and modules in the codebase knowledge graph.",
            input_schema={
                "type": "object",
                "properties": {},
                "required": [],
            },
            handler=self._handle_detect_dependency_cycles,
        )

        # 6. analyze_coupling
        self._register_tool(
            name="analyze_coupling",
            description="Calculate architectural coupling metrics for a component: afferent coupling (Ca), efferent coupling (Ce), instability index (I), and potential failure concentration risk assessment based on structural coupling.",
            input_schema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Target component ID",
                    }
                },
                "required": ["node_id"],
            },
            handler=self._handle_analyze_coupling,
        )

    def _register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """Register a tool, strictly enforcing read-only safety checks."""
        # Safety enforcement: reject any tool whose name contains mutation keywords
        for keyword in self.PROHIBITED_MUTATION_KEYWORDS:
            if keyword in name.lower():
                raise PermissionError(f"Security violation: Mutating tool '{name}' cannot be registered.")

        tool_def = ToolDefinition(name=name, description=description, input_schema=input_schema)
        self._tools[name] = tool_def
        self._handlers[name] = handler

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return specifications for all registered read-only tools."""
        return [tool.model_dump() for tool in self._tools.values()]

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dispatch and execute a tool by name with arguments.
        
        Returns:
            JSON-serializable result envelope:
            {"success": bool, "tool": str, "data": Any, "error": Optional[str]}
        """
        args = arguments or {}

        if name not in self._tools:
            return {
                "success": False,
                "tool": name,
                "data": None,
                "error": f"Tool '{name}' is not registered. Available tools: {sorted(list(self._tools.keys()))}",
            }

        tool_def = self._tools[name]
        handler = self._handlers[name]

        # Parameter validation
        required_params = tool_def.input_schema.get("required", [])
        for req in required_params:
            if req not in args or args[req] is None or str(args[req]).strip() == "":
                return {
                    "success": False,
                    "tool": name,
                    "data": None,
                    "error": f"Missing required parameter '{req}' for tool '{name}'.",
                }

        try:
            result_data = handler(args)
            # Verify JSON serializability before returning
            json.dumps(result_data)
            return {
                "success": True,
                "tool": name,
                "data": result_data,
                "error": None,
            }
        except KeyError as err:
            return {
                "success": False,
                "tool": name,
                "data": None,
                "error": str(err).strip("'\""),
            }
        except Exception as err:
            return {
                "success": False,
                "tool": name,
                "data": None,
                "error": f"Execution error in '{name}': {str(err)}",
            }

    # Tool Handlers
    def _handle_get_graph_schema(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_graph_schema."""
        return self.graph_client.get_schema()

    def _handle_search_graph_nodes(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handler for search_graph_nodes."""
        query = str(args["query"]).strip().lower()
        category = args.get("category")
        if category:
            category = str(category).strip().lower()

        all_nodes = self.graph_client.get_nodes()
        matches: List[Dict[str, Any]] = []

        for node in all_nodes:
            if category and node.get("type", "").lower() != category:
                continue

            node_id = str(node.get("id", "")).lower()
            name = str(node.get("name", "")).lower()
            ntype = str(node.get("type", "")).lower()
            desc = str(node.get("description", "")).lower()

            if query in node_id or query in name or query in ntype or query in desc:
                matches.append(node)

        return matches

    def _handle_get_node_dependencies(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_node_dependencies."""
        node_id = str(args["node_id"]).strip()
        node = self.graph_client.get_node(node_id)
        if not node:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")

        direct_deps = self.graph_client.get_direct_dependencies(node_id)
        direct_callers = self.graph_client.get_direct_dependents(node_id)

        return {
            "node_id": node_id,
            "name": node.get("name", node_id),
            "type": node.get("type", "Generic"),
            "description": node.get("description", ""),
            "direct_dependencies": direct_deps,
            "direct_dependents": direct_callers,
            "dependency_count": len(direct_deps),
            "dependent_count": len(direct_callers),
        }

    def _handle_analyze_blast_radius(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for analyze_blast_radius."""
        node_id = str(args["node_id"]).strip()
        # calculate_blast_radius raises KeyError if node does not exist
        return self.graph_client.calculate_blast_radius(node_id)

    def _handle_detect_dependency_cycles(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for detect_dependency_cycles."""
        cycles = self.graph_client.detect_cycles()
        return {
            "total_cycles_detected": len(cycles),
            "cycles": cycles,
            "has_architectural_debt": len(cycles) > 0,
        }

    def _handle_analyze_coupling(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for analyze_coupling."""
        node_id = str(args["node_id"]).strip()
        # calculate_coupling_metrics raises KeyError if node does not exist
        return self.graph_client.calculate_coupling_metrics(node_id)
