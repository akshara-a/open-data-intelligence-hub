"""Local tool-server adapter and transport-independent dispatcher for codebase graph tools.

Note on MCP Integration:
The official Model Context Protocol (`mcp`) Python SDK is not currently installed
in the environment. This module provides a clean, transport-independent local tool
dispatcher that follows standard MCP tool-calling schemas. It is designed so that
the official FastMCP or stdio/SSE MCP server transport can be hooked in cleanly
once the official `mcp` package is installed, without rewriting tool definitions.
"""

import json
from typing import Any, Dict, Optional

from src.graph.base import BaseGraphClient
from src.mcp.tools import GraphToolRegistry

# Detect if the official 'mcp' Python SDK is available
try:
    import mcp  # type: ignore # noqa: F401
    HAS_OFFICIAL_MCP = True
except ImportError:
    HAS_OFFICIAL_MCP = False


class LocalToolServerAdapter:
    """Local transport-independent tool server adapter for graph analysis operations.
    
    Acts as an intermediary dispatcher bridging local agent workflows with
    MCP-compatible tool definitions.
    """

    PROTOCOL_SPEC = "Model Context Protocol (Tool-Calling Schema)"
    ADAPTER_VERSION = "0.1.0"

    def __init__(self, graph_client: Optional[BaseGraphClient] = None):
        """Initialize adapter with tool registry."""
        self.registry = GraphToolRegistry(graph_client=graph_client)

    def get_server_status(self) -> Dict[str, Any]:
        """Inspect and report the runtime capabilities and MCP integration status."""
        return {
            "official_mcp_sdk_installed": HAS_OFFICIAL_MCP,
            "transport_mode": "official-mcp" if HAS_OFFICIAL_MCP else "local-adapter-only",
            "protocol_spec": self.PROTOCOL_SPEC,
            "adapter_version": self.ADAPTER_VERSION,
            "registered_tools_count": len(self.registry.list_tools()),
            "available_tools": [t["name"] for t in self.registry.list_tools()],
            "documentation": (
                "Official MCP Python SDK is currently pending installation. "
                "The local tool registry provides transport-independent execution "
                "matching MCP tool-calling schemas for offline and in-process execution."
            ),
        }

    def list_tools(self) -> Dict[str, Any]:
        """List all available read-only graph tools."""
        return {
            "tools": self.registry.list_tools(),
            "count": len(self.registry.list_tools()),
        }

    def execute_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dispatch a tool execution request through the tool registry."""
        return self.registry.call_tool(name=tool_name, arguments=arguments)

    def dispatch_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a structured JSON-RPC 2.0 style tool request."""
        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "official_mcp_sdk_available": HAS_OFFICIAL_MCP,
                    "serverInfo": {
                        "name": "codebase-graph-tool-adapter",
                        "version": self.ADAPTER_VERSION,
                    },
                    "capabilities": {
                        "tools": {"listChanged": False},
                    },
                },
            }

        elif method in ("tools/list", "list_tools"):
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": self.list_tools(),
            }

        elif method in ("tools/call", "call_tool"):
            name = params.get("name", "")
            arguments = params.get("arguments", {})
            call_result = self.execute_tool(name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": call_result,
            }

        elif method == "ping":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"status": "ok"},
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not recognized by tool adapter.",
                },
            }


def create_tool_server_adapter(graph_client: Optional[BaseGraphClient] = None) -> LocalToolServerAdapter:
    """Factory function to instantiate the local graph tool server adapter."""
    return LocalToolServerAdapter(graph_client=graph_client)
