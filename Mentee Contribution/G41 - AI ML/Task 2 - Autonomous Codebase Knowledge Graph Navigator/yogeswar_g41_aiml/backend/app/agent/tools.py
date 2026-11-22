"""
Phase 5 - Approved, Read-Only Tools for Agentic Codebase Navigation
All tools execute against existing GraphRAG and MCP/CGG services.
Strictly read-only: no arbitrary Cypher, no direct Neo4j access, no file modification.
Every call is scoped to (repo_id, commit_sha).
"""
import os
import logging
from typing import Dict, Any, List, Optional
import httpx
from pydantic import BaseModel, Field

from ..auth import create_internal_service_token

logger = logging.getLogger("agent.tools")

MCP_SERVICE_URL = os.getenv("MCP_SERVICE_URL", "http://mcp:8000")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag:8000")

DEFAULT_TOOL_TIMEOUT = 10.0
MAX_TOOL_CALLS_PER_REQUEST = 15


class ToolExecutionError(Exception):
    """Raised when an approved tool fails execution."""
    pass


# ============================================================================
# Tool Implementations
# ============================================================================

async def execute_graph_rag_retrieve(
    repo_id: str,
    commit_sha: str,
    query: str,
    top_k: int = 5,
    include_graph: bool = True,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """
    Executes hybrid GraphRAG retrieval (semantic embeddings + structural graph signals).
    Preserves uncertainty classifications and evidence citations.
    """
    url = f"{RAG_SERVICE_URL}/api/v1/rag/retrieve"
    payload = {
        "repo_id": repo_id,
        "commit_sha": commit_sha,
        "query": query,
        "top_k": min(top_k, 10),
        "include_graph": include_graph,
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"RAG retrieve HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("GraphRAG retrieval failed: %s", str(e))
        return {"results": [], "error": str(e)}


async def execute_cgg_entity_lookup(
    repo_id: str,
    commit_sha: str,
    name: Optional[str] = None,
    entity_type: Optional[str] = None,
    file_path: Optional[str] = None,
    entity_id: Optional[str] = None,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Look up entities in the active snapshot via CGG."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    payload = {
        "name": name,
        "entity_type": entity_type,
        "file_path": file_path,
        "entity_id": entity_id,
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/cgg/entity_lookup"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG entity_lookup HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG entity_lookup failed: %s", str(e))
        return {"entities": [], "error": str(e)}


async def execute_cgg_entity_details(
    repo_id: str,
    commit_sha: str,
    entity_id: str,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Get full properties, declaration provenance, and signatures for an entity."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    payload = {
        "entity_id": entity_id,
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/cgg/entity_details"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG entity_details HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG entity_details failed: %s", str(e))
        return {"entity": None, "error": str(e)}


async def execute_cgg_direct_neighbors(
    repo_id: str,
    commit_sha: str,
    entity_id: str,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Retrieve verified incoming dependents and outgoing dependencies for an entity."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    payload = {
        "entity_id": entity_id,
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/cgg/direct_neighbors"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG direct_neighbors HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG direct_neighbors failed: %s", str(e))
        return {"outgoing_dependencies": [], "incoming_dependents": [], "error": str(e)}


async def execute_cgg_multihop_impact(
    repo_id: str,
    commit_sha: str,
    start_entity_id: str,
    max_hops: int = 2,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """
    Execute approved bounded multi-hop traversal template (impact_downstream_1hop/2hop/3hop).
    Raw Cypher is strictly disallowed.
    """
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    op_name = f"impact_downstream_{min(max(max_hops, 1), 3)}hop"
    payload = {
        "operation": op_name,
        "parameters": {
            "start_entity_id": start_entity_id,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        },
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/tools/run_query"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG multihop impact HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG multihop impact failed: %s", str(e))
        return {"records": [], "error": str(e)}


async def execute_cgg_relationship_evidence(
    repo_id: str,
    commit_sha: str,
    source_entity_id: str,
    target_entity_id: str,
    evidence_id: Optional[str] = None,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Retrieve verified relationship evidence between two entities."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    payload = {
        "source_entity_id": source_entity_id,
        "target_entity_id": target_entity_id,
        "evidence_id": evidence_id,
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/cgg/relationship_evidence"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG relationship_evidence HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG relationship_evidence failed: %s", str(e))
        return {"relationship_evidences": [], "error": str(e)}


async def execute_cgg_unresolved_calls(
    repo_id: str,
    commit_sha: str,
    source_entity_id: Optional[str] = None,
    file_path: Optional[str] = None,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Retrieve unresolvable dynamic invocation records for entity or file."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Service-Auth": token,
    }
    payload = {
        "source_entity_id": source_entity_id,
        "file_path": file_path,
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/cgg/unresolved_calls"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG unresolved_calls HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG unresolved_calls failed: %s", str(e))
        return {"unresolved_calls": [], "error": str(e)}


async def execute_cgg_evidence_lookup(
    repo_id: str,
    commit_sha: str,
    evidence_id: str,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Look up immutable provenance evidence record by ID."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "X-Internal-Service-Auth": token,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/tools/evidence/{evidence_id}"
    params = {
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"CGG evidence lookup HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("CGG evidence lookup failed: %s", str(e))
        return {"evidence": None, "error": str(e)}


async def execute_repo_read_file(
    repo_id: str,
    commit_sha: str,
    file_path: str,
    start_line: int = 1,
    end_line: int = 100,
    timeout: float = DEFAULT_TOOL_TIMEOUT,
) -> Dict[str, Any]:
    """Retrieve source code lines pinned to exact commit SHA from bare Git mirror."""
    token = create_internal_service_token(repo_id, commit_sha, sub="agent_supervisor")
    headers = {
        "X-Internal-Service-Auth": token,
    }
    url = f"{MCP_SERVICE_URL}/api/v1/tools/file"
    params = {
        "file_path": file_path,
        "start_line": max(1, start_line),
        "end_line": min(start_line + 200, end_line),
        "repo_id": repo_id,
        "commit_sha": commit_sha,
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code >= 400:
                raise ToolExecutionError(f"Repo read_file HTTP {resp.status_code}: {resp.text}")
            return resp.json()
    except Exception as e:
        logger.warning("Repo read_file failed: %s", str(e))
        return {"content": "", "lines": [], "error": str(e)}
