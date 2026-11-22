"""FastAPI REST interface for the Autonomous Codebase Knowledge Graph Navigator."""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.agent.navigator import AutonomousCodebaseNavigator, NavigationResult
from src.config import get_settings
from src.graph.mock_graph_client import MockGraphClient
from src.mcp.tools import GraphToolRegistry

# Application initialization
settings = get_settings()
app = FastAPI(
    title="Autonomous Codebase Knowledge Graph Navigator API",
    description="REST API for exploring codebase microservice architectures, assessing blast radius, and synthesizing refactoring plans.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared instances
graph_client = MockGraphClient()
tool_registry = GraphToolRegistry(graph_client=graph_client)
navigator = AutonomousCodebaseNavigator(graph_client=graph_client, tool_registry=tool_registry)


class QueryRequest(BaseModel):
    """Natural language query request payload."""

    query: str = Field(..., description="Developer question regarding system architecture or blast radius")


class BlastRadiusRequest(BaseModel):
    """Component blast radius request payload."""

    node_id: str = Field(..., description="Target component ID (e.g. 'legacy-auth-module')")


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Check service health and report knowledge graph status."""
    schema = graph_client.get_schema()
    return {
        "status": "healthy",
        "engine": "mock-networkx",
        "graph_nodes": schema.get("total_nodes", 0),
        "graph_edges": schema.get("total_edges", 0),
        "dataset_source": "data/mock_graph_seed.json",
    }


@app.get("/schema", tags=["Graph Exploration"])
def get_schema() -> Dict[str, Any]:
    """Retrieve graph structural schema including node types, relationship types, and counts."""
    return graph_client.get_schema()


@app.get("/nodes", tags=["Graph Exploration"])
def list_nodes(category: Optional[str] = Query(None, description="Optional node category filter")) -> List[Dict[str, Any]]:
    """List all components in the knowledge graph, optionally filtered by category."""
    return graph_client.get_nodes(category=category)


@app.get("/nodes/{node_id}", tags=["Graph Exploration"])
def get_node_details(node_id: str) -> Dict[str, Any]:
    """Retrieve metadata, direct dependencies, and callers for a specific component."""
    node = graph_client.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Component '{node_id}' not found in knowledge graph.")
    
    deps = graph_client.get_direct_dependencies(node_id)
    callers = graph_client.get_direct_dependents(node_id)
    return {
        **node,
        "direct_dependencies": deps,
        "direct_dependents": callers,
    }


@app.get("/cycles", tags=["Architectural Debt"])
def get_cycles() -> Dict[str, Any]:
    """Detect circular dependency loops in the codebase architecture."""
    cycles = graph_client.detect_cycles()
    return {
        "total_cycles": len(cycles),
        "cycles": cycles,
        "has_architectural_debt": len(cycles) > 0,
    }


@app.post("/blast-radius", tags=["Impact Analysis"])
def analyze_blast_radius(req: BlastRadiusRequest) -> Dict[str, Any]:
    """Calculate blast radius and downstream dependents for a specific component."""
    node = graph_client.get_node(req.node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Component '{req.node_id}' not found in knowledge graph.")
    
    return graph_client.calculate_blast_radius(req.node_id)


@app.post("/navigate", response_model=NavigationResult, tags=["Autonomous Navigation"])
def navigate_architecture(req: QueryRequest) -> NavigationResult:
    """Execute end-to-end autonomous navigation: parse query, generate Cypher, evaluate reasoning, and synthesize report."""
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    
    return navigator.navigate(req.query)
