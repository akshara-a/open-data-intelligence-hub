from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CodeChunk(BaseModel):
    chunk_id: str
    repo_id: str
    commit_sha: str
    file_path: str
    line_start: int
    line_end: int
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None
    content: str
    content_hash: str
    indexed_text: str


class IndexRequest(BaseModel):
    repo_id: str = Field(..., description="Target repository ID")
    commit_sha: str = Field(..., description="Target commit SHA")
    force_reindex: bool = Field(default=False, description="Whether to recompute all embeddings ignoring cache")


class IndexResponse(BaseModel):
    repo_id: str
    commit_sha: str
    total_files: int
    total_chunks: int
    cached_chunks_reused: int
    new_chunks_embedded: int
    status: str


class RetrievalRequest(BaseModel):
    repo_id: str = Field(..., description="Target repository ID")
    commit_sha: str = Field(..., description="Target commit SHA")
    query: str = Field(..., min_length=1, max_length=2000, description="Natural language search query")
    top_k: int = Field(default=10, ge=1, le=50, description="Maximum number of retrieved results")
    include_graph: bool = Field(default=True, description="Whether to perform hybrid graph expansion via CGG")
    max_graph_hops: int = Field(default=2, ge=1, le=3, description="Maximum graph traversal depth")


class RankingExplanation(BaseModel):
    semantic_score: float
    graph_score: float
    combined_score: float
    hop_distance: Optional[int] = None
    relationship_type: Optional[str] = None
    relationship_classification: str = Field(
        default="none",
        description="'verified_static', 'potential_uncertain', or 'none'"
    )
    explanation: str


class RetrievalResultItem(BaseModel):
    chunk_id: str
    repo_id: str
    commit_sha: str
    file_path: str
    line_start: int
    line_end: int
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None
    content: str
    semantic_similarity: float
    graph_relevance: float
    combined_score: float
    evidence_ids: List[str] = Field(default_factory=list)
    relationship_path: List[str] = Field(default_factory=list)
    relationship_classification: str = "none"
    ranking_explanation: RankingExplanation
    provenance_status: str = Field(
        default="evidence_grounded",
        description="'evidence_grounded' or 'unsupported'"
    )


class HybridRetrievalResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    repo_id: str
    commit_sha: str
    query: str
    total_candidates_scanned: int
    results_returned: int
    model_version: str
    model_status: str
    backend: str = "sentence_transformers"
    fallback_mode: bool = False
    results: List[RetrievalResultItem]
