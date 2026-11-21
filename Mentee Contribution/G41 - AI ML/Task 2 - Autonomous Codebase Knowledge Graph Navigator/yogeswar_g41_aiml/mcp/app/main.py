import os
import datetime
import asyncio
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from .cgg_engine import (
    get_cgg_engine,
    cancel_query,
    ResultLimitExceededException,
    MemoryLimitExceededException,
    QueryCancelledException,
    InvalidQueryException,
)
from .auth import get_internal_service_claims, enforce_scope
from .git_reader import read_file_from_git
from .templates import get_template, QUERY_TEMPLATES
from .mcp_server import handle_json_rpc, list_tools, execute_tool

GIT_STORAGE_ROOT = os.getenv("GIT_STORAGE_ROOT", "/app/git_storage")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Idempotent schema initialization on startup
    try:
        engine = get_cgg_engine()
        engine.ensure_schema()
    except Exception as e:
        # Log warning if Neo4j is initializing or connecting in local dev mode
        print(f"[CGG/MCP] Schema initialization notice: {e}")
    yield
    engine = get_cgg_engine()
    engine.close()


app = FastAPI(
    title="Controlled Graph Gateway (CGG / MCP Server)",
    version="1.0.0",
    lifespan=lifespan,
)


# Exception Handlers
@app.exception_handler(ResultLimitExceededException)
async def result_limit_exceeded_handler(request: Request, exc: ResultLimitExceededException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "RESULT_LIMIT_EXCEEDED", "detail": str(exc)},
    )


@app.exception_handler(MemoryLimitExceededException)
async def memory_limit_exceeded_handler(request: Request, exc: MemoryLimitExceededException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "MEMORY_LIMIT_EXCEEDED", "detail": str(exc)},
    )


@app.exception_handler(QueryCancelledException)
async def query_cancelled_handler(request: Request, exc: QueryCancelledException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "QUERY_CANCELLED", "detail": str(exc)},
    )


@app.exception_handler(InvalidQueryException)
async def invalid_query_handler(request: Request, exc: InvalidQueryException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "INVALID_QUERY", "detail": str(exc)},
    )


# Health Check
class HealthResponse(BaseModel):
    status: str
    service: str
    neo4j_configured: bool
    neo4j_connected: Optional[bool] = None
    git_storage_mounted: bool
    timestamp: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    git_mounted = os.path.isdir(GIT_STORAGE_ROOT) or os.path.isdir("./git_storage")
    configured = True
    neo4j_ok = None
    try:
        engine = get_cgg_engine()
        with engine.get_driver().session(database="neo4j") as session:
            res = session.run("RETURN 1 AS alive;")
            neo4j_ok = res.single()["alive"] == 1
    except Exception:
        neo4j_ok = False

    return HealthResponse(
        status="healthy",
        service="mcp_cgg",
        neo4j_configured=configured,
        neo4j_connected=neo4j_ok,
        git_storage_mounted=git_mounted,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


# MCP Protocol Transport (HTTP + SSE) per Section 6.1
@app.get("/mcp/sse")
async def mcp_sse():
    """
    SSE stream endpoint conforming to MCP HTTP+SSE transport specification.
    """
    async def event_generator():
        yield "event: endpoint\ndata: /mcp/message\n\n"
        while True:
            await asyncio.sleep(15)
            yield ": ping\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/mcp/message")
async def mcp_message(
    request: Request,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    """
    JSON-RPC 2.0 endpoint for MCP protocol messages.
    """
    body = await request.json()
    response = handle_json_rpc(body, claims)
    return response


# Internal REST RPC Transport per Section 6.1
class RunQueryRequest(BaseModel):
    operation: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/tools/run_query")
def rest_run_query(
    req: RunQueryRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    result = execute_tool(
        "graph.run_query",
        {"operation": req.operation, "parameters": req.parameters},
        claims,
    )
    return result


@app.get("/api/v1/tools/evidence/{evidence_id}")
def rest_get_evidence(
    evidence_id: str,
    repo_id: Optional[str] = None,
    commit_sha: Optional[str] = None,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, repo_id, commit_sha)
    result = execute_tool(
        "graph.get_evidence",
        {"evidence_id": evidence_id},
        claims,
    )
    if not result.get("evidence"):
        raise HTTPException(status_code=404, detail=f"Evidence '{evidence_id}' not found in active snapshot")
    return result


class BatchEvidenceRequest(BaseModel):
    entity_ids: List[str]
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/tools/evidence/batch")
def rest_get_evidence_batch(
    req: BatchEvidenceRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    result = execute_tool(
        "graph.get_evidence_for_entities",
        {"entity_ids": req.entity_ids},
        claims,
    )
    return result


@app.get("/api/v1/tools/file")
def rest_read_file(
    file_path: str,
    start_line: int = 1,
    end_line: int = 100,
    repo_id: Optional[str] = None,
    commit_sha: Optional[str] = None,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, repo_id, commit_sha)
    result = execute_tool(
        "repo.read_file",
        {"file_path": file_path, "start_line": start_line, "end_line": end_line},
        claims,
    )
    return result


@app.post("/api/v1/tools/cancel/{query_id}")
def rest_cancel_query(
    query_id: str,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    """
    Cooperative query cancellation endpoint per Section 6.3 / AC-3.5.
    Sets cancellation flag for owning thread to safely abort.
    """
    success = cancel_query(query_id)
    return {"query_id": query_id, "cancelled": success}


# Named CGG Operations Endpoints
class SnapshotInfoRequest(BaseModel):
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/snapshot_info")
def cgg_snapshot_info(
    req: SnapshotInfoRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool("cgg.snapshot_info", {}, claims)


class EntityLookupRequest(BaseModel):
    name: Optional[str] = None
    entity_type: Optional[str] = None
    file_path: Optional[str] = None
    entity_id: Optional[str] = None
    limit: Optional[int] = 500
    skip: Optional[int] = 0
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/entity_lookup")
def cgg_entity_lookup(
    req: EntityLookupRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool(
        "cgg.entity_lookup",
        {
            "name": req.name,
            "entity_type": req.entity_type,
            "file_path": req.file_path,
            "entity_id": req.entity_id,
            "limit": req.limit,
            "skip": req.skip,
        },
        claims,
    )


class EntityDetailsRequest(BaseModel):
    entity_id: str
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/entity_details")
def cgg_entity_details(
    req: EntityDetailsRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    result = execute_tool("cgg.entity_details", {"entity_id": req.entity_id}, claims)
    if not result.get("entity"):
        raise HTTPException(status_code=404, detail=f"Entity '{req.entity_id}' not found in active snapshot")
    return result


class DirectNeighborsRequest(BaseModel):
    entity_id: str
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/direct_neighbors")
def cgg_direct_neighbors(
    req: DirectNeighborsRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool("cgg.direct_neighbors", {"entity_id": req.entity_id}, claims)


class MultiHopRequest(BaseModel):
    start_entity_id: str
    max_depth: int = Field(default=2, ge=1, le=3)
    direction: str = Field(default="downstream")
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/multi_hop_dependencies")
def cgg_multi_hop_dependencies(
    req: MultiHopRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool(
        "cgg.multi_hop_dependencies",
        {
            "start_entity_id": req.start_entity_id,
            "max_depth": req.max_depth,
            "direction": req.direction,
        },
        claims,
    )


class RelationshipEvidenceRequest(BaseModel):
    evidence_id: Optional[str] = None
    source_entity_id: Optional[str] = None
    target_entity_id: Optional[str] = None
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/relationship_evidence")
def cgg_relationship_evidence(
    req: RelationshipEvidenceRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool(
        "cgg.relationship_evidence",
        {
            "evidence_id": req.evidence_id,
            "source_entity_id": req.source_entity_id,
            "target_entity_id": req.target_entity_id,
        },
        claims,
    )


class UnresolvedCallsRequest(BaseModel):
    source_entity_id: Optional[str] = None
    file_path: Optional[str] = None
    limit: Optional[int] = 500
    skip: Optional[int] = 0
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/unresolved_calls")
def cgg_unresolved_calls(
    req: UnresolvedCallsRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool(
        "cgg.unresolved_calls",
        {
            "source_entity_id": req.source_entity_id,
            "file_path": req.file_path,
            "limit": req.limit,
            "skip": req.skip,
        },
        claims,
    )


class StatisticsRequest(BaseModel):
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/statistics")
def cgg_statistics(
    req: StatisticsRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool("cgg.graph_statistics", {}, claims)


class SnapshotRelationshipsRequest(BaseModel):
    relationship_type: Optional[str] = None
    limit: Optional[int] = 500
    skip: Optional[int] = 0
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None


@app.post("/api/v1/cgg/relationships")
def cgg_snapshot_relationships(
    req: SnapshotRelationshipsRequest,
    claims: Dict[str, Any] = Depends(get_internal_service_claims),
):
    enforce_scope(claims, req.repo_id, req.commit_sha)
    return execute_tool(
        "cgg.snapshot_relationships",
        {
            "relationship_type": req.relationship_type,
            "limit": req.limit,
            "skip": req.skip,
        },
        claims,
    )
