import os
import datetime
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel, Field

from .models import (
    IndexRequest,
    IndexResponse,
    RetrievalRequest,
    HybridRetrievalResponse,
)
from .embedding_engine import get_embedding_engine
from .indexer import SnapshotIndexer
from .retriever import GraphRAGRetriever
from .sqlite_storage import SQLiteChunkStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("graph_rag_service")

SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/app_state.db")

app = FastAPI(
    title="GraphRAG Semantic & Structural Retrieval Engine",
    version="1.0.0",
)


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str
    service: str
    database_path: str
    model_version: str
    model_status: str
    backend: str
    fallback_mode: bool
    timestamp: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    engine = get_embedding_engine()
    status_str = "healthy" if engine.status in ("active_transformer", "fallback_deterministic_projection") else "degraded"
    return HealthResponse(
        status=status_str,
        service="graph_rag",
        database_path=SQLITE_DB_PATH,
        model_version=engine.model_version,
        model_status=engine.status,
        backend=engine.backend,
        fallback_mode=engine.fallback_mode,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )


@app.post("/api/v1/rag/index", response_model=IndexResponse)
def index_snapshot_endpoint(req: IndexRequest):
    """
    Indexes source code chunks and embeds semantic representations for a snapshot.
    Reuses existing embeddings across commits based on content hash.
    """
    if not req.repo_id or not req.commit_sha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="repo_id and commit_sha are mandatory for snapshot indexing",
        )
    logger.info("Indexing snapshot for repo=%s commit=%s (force=%s)", req.repo_id, req.commit_sha, req.force_reindex)
    try:
        indexer = SnapshotIndexer(SQLITE_DB_PATH)
        resp = indexer.index_snapshot(
            repo_id=req.repo_id,
            commit_sha=req.commit_sha,
            force_reindex=req.force_reindex,
        )
        return resp
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Failed to index snapshot: %s", str(e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Indexing failed: {str(e)}")


@app.post("/api/v1/rag/retrieve", response_model=HybridRetrievalResponse)
def hybrid_retrieval_endpoint(req: RetrievalRequest):
    """
    Executes Hybrid GraphRAG retrieval:
    1. Semantic retrieval from SQLite chunk embeddings
    2. Structural graph traversal via Controlled Graph Gateway (CGG)
    3. Deterministic hybrid ranking and evidence provenance grounding
    """
    if not req.repo_id or not req.commit_sha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="repo_id and commit_sha are mandatory for snapshot retrieval",
        )
    if not req.query or not req.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="query text must not be empty",
        )

    logger.info("Retrieving for repo=%s commit=%s top_k=%d query='%s'", req.repo_id, req.commit_sha, req.top_k, req.query[:50])
    try:
        retriever = GraphRAGRetriever(SQLITE_DB_PATH)
        response = retriever.retrieve(req)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Retrieval failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Retrieval failed: {str(e)}")


class VectorSearchRequest(BaseModel):
    repo_id: str
    commit_sha: str
    query: str
    top_k: int = 10


@app.post("/api/v1/search/vectors")
def search_vectors_endpoint(req: VectorSearchRequest):
    """
    Backward-compatibility vector search endpoint per Section 9.
    """
    retriever = GraphRAGRetriever(SQLITE_DB_PATH)
    res = retriever.retrieve(
        RetrievalRequest(
            repo_id=req.repo_id,
            commit_sha=req.commit_sha,
            query=req.query,
            top_k=req.top_k,
            include_graph=False,
        )
    )
    return {"matches": res.results}
