"""Evaluation and benchmarking module for Autonomous Codebase Knowledge Graph Navigator."""

from .dataset import (
    CURATED_BENCHMARK_CASES,
    BENCHMARK_DATASET_VERSION,
    DEFAULT_BENCHMARK_REPO,
    DEFAULT_BENCHMARK_COMMIT,
)
from .engine import (
    execute_benchmark_suite,
    get_benchmark_run_by_id,
    list_benchmark_runs,
)
from .metrics import (
    compute_mrr,
    compute_ndcg_at_k,
    compute_percentiles,
    compute_precision_recall_f1,
)
from .models import (
    BenchmarkMetricsSummary,
    BenchmarkRunDetail,
    BenchmarkRunResponse,
    BenchmarkRunSummary,
    BenchmarkTestCase,
    CategoryMetricScore,
    ExecuteBenchmarkRequest,
    QueryEvaluationResult,
)

BENCHMARK_DATASET = CURATED_BENCHMARK_CASES

__all__ = [
    "BENCHMARK_DATASET",
    "CURATED_BENCHMARK_CASES",
    "BENCHMARK_DATASET_VERSION",
    "DEFAULT_BENCHMARK_REPO",
    "DEFAULT_BENCHMARK_COMMIT",
    "BenchmarkTestCase",
    "execute_benchmark_suite",
    "get_benchmark_run_by_id",
    "list_benchmark_runs",
    "compute_precision_recall_f1",
    "compute_mrr",
    "compute_ndcg_at_k",
    "compute_percentiles",
    "BenchmarkMetricsSummary",
    "BenchmarkRunDetail",
    "BenchmarkRunResponse",
    "BenchmarkRunSummary",
    "CategoryMetricScore",
    "ExecuteBenchmarkRequest",
    "QueryEvaluationResult",
]
