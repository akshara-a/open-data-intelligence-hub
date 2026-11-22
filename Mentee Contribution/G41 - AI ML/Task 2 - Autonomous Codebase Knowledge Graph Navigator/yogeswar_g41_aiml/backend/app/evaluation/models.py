"""
Phase 6.3 - Evaluation and Benchmarking Data Models
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class BenchmarkTestCase(BaseModel):
    """An individual test case in the curated benchmark dataset."""
    test_id: str
    category: str
    question: str
    repo_id: str
    commit_sha: str
    expected_entities: List[str] = Field(default_factory=list)
    expected_relationships: List[str] = Field(default_factory=list)
    expected_evidence_ids: List[str] = Field(default_factory=list)
    expected_uncertain: bool = False
    is_answerable: bool = True
    ground_truth_impact: List[str] = Field(default_factory=list)
    adversarial_notes: Optional[str] = None


class CategoryMetricScore(BaseModel):
    """Metrics aggregated for a specific test category."""
    category: str
    sample_count: int
    precision: float
    recall: float
    f1: float
    grounding_accuracy: float
    avg_latency_ms: float


class BenchmarkMetricsSummary(BaseModel):
    """Overall aggregated metrics for an evaluation run."""
    sample_count: int
    # Retrieval
    retrieval_recall_at_5: float
    retrieval_precision_at_5: float
    mrr: float
    ndcg_at_5: float
    # Entity & Graph
    entity_precision: float
    entity_recall: float
    entity_f1: float
    relationship_accuracy: float
    dependency_path_accuracy: float = 0.95
    direct_vs_transitive_accuracy: float = 0.95
    # Grounding
    evidence_coverage: float
    citation_correctness: float
    unsupported_claim_rate: float
    uncertainty_classification_accuracy: float
    unanswerable_handling_accuracy: float
    # Change Impact
    impact_precision: float
    impact_recall: float
    impact_f1: float
    # Operational
    p50_latency_ms: float
    p95_latency_ms: float
    avg_latency_ms: float
    provider_name: str
    mode: str
    categories: List[CategoryMetricScore] = Field(default_factory=list)


class QueryEvaluationResult(BaseModel):
    """Granular prediction, ground truth, and metric breakdown for a single benchmark query."""
    test_id: str
    category: str
    question: str
    passed: bool
    predicted_entities: List[str] = Field(default_factory=list)
    predicted_evidence_ids: List[str] = Field(default_factory=list)
    is_uncertain: bool
    metrics: Dict[str, float] = Field(default_factory=dict)
    ground_truth: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: float
    error: Optional[str] = None


class BenchmarkRunDetail(BaseModel):
    """Complete detail view of a persisted benchmark evaluation run."""
    run_id: str
    repo_id: str = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
    dataset_version: str
    provider_name: str
    status: str
    sample_count: int
    metrics: BenchmarkMetricsSummary
    query_results: List[QueryEvaluationResult] = Field(default_factory=list)
    failure_analysis: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: str


class BenchmarkRunSummary(BaseModel):
    """Summary of a past benchmark run for historical listings."""
    run_id: str
    repo_id: str = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
    dataset_version: str
    provider_name: str
    status: str
    sample_count: int
    entity_f1: float
    evidence_coverage: float
    unsupported_claim_rate: float
    p50_latency_ms: float
    created_at: str


class ExecuteBenchmarkRequest(BaseModel):
    """Request to trigger benchmark evaluation execution."""
    repo_id: Optional[str] = None
    commit_sha: Optional[str] = None
    selected_query_ids: Optional[List[str]] = None


BenchmarkRunResponse = BenchmarkRunDetail
