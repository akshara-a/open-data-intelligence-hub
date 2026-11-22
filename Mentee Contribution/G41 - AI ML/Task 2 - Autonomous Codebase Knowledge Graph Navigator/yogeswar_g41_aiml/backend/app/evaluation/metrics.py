"""
Phase 6.3 - Evaluation Metrics Computation
Pure mathematical and statistical implementations of retrieval, grounding, entity,
impact, and operational benchmark metrics.
"""
import math
from typing import List, Set, Dict, Any, Optional, Union, Iterable


class PrecisionRecallF1Result(dict):
    """Dictionary supporting both dict key access and tuple unpacking (precision, recall, f1)."""
    @property
    def precision(self) -> float:
        return self["precision"]

    @property
    def recall(self) -> float:
        return self["recall"]

    @property
    def f1(self) -> float:
        return self["f1"]

    def __iter__(self):
        return iter((self["precision"], self["recall"], self["f1"]))


class PercentileResult(dict):
    """Dictionary supporting both dict key access and tuple unpacking (p50, p95)."""
    @property
    def p50(self) -> float:
        return self["p50"]

    @property
    def p95(self) -> float:
        return self["p95"]

    @property
    def avg(self) -> float:
        return self["avg"]

    def __iter__(self):
        return iter((self["p50"], self["p95"]))


def compute_precision_recall_f1(
    predicted: Union[Set[str], Iterable[str]],
    expected: Union[Set[str], Iterable[str]],
) -> PrecisionRecallF1Result:
    """Computes exact precision, recall, and harmonic F1 score."""
    p_set = set(predicted) if not isinstance(predicted, set) else predicted
    e_set = set(expected) if not isinstance(expected, set) else expected

    if not e_set and not p_set:
        return PrecisionRecallF1Result({"precision": 1.0, "recall": 1.0, "f1": 1.0})
    if not p_set or not e_set:
        return PrecisionRecallF1Result({"precision": 0.0, "recall": 0.0, "f1": 0.0})

    tp = len(p_set.intersection(e_set))
    fp = len(p_set - e_set)
    fn = len(e_set - p_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return PrecisionRecallF1Result({
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    })


def compute_mrr(ranked_items: List[str], expected: Union[Set[str], Iterable[str]]) -> float:
    """Computes Mean Reciprocal Rank (MRR) for the first relevant retrieved entity."""
    e_set = set(expected) if not isinstance(expected, set) else expected
    if not e_set:
        return 1.0 if not ranked_items else 0.0
    for idx, item in enumerate(ranked_items, 1):
        if item in e_set:
            return round(1.0 / idx, 4)
    return 0.0


def compute_ndcg_at_k(
    ranked_items: List[str],
    expected: Union[Set[str], Iterable[str]],
    k: int = 5,
) -> float:
    """Computes Normalized Discounted Cumulative Gain at rank K."""
    e_set = set(expected) if not isinstance(expected, set) else expected
    if not e_set:
        return 1.0 if not ranked_items else 0.0

    cutoff = ranked_items[:k]
    dcg = 0.0
    for i, item in enumerate(cutoff, 1):
        rel = 1.0 if item in e_set else 0.0
        dcg += (2**rel - 1) / math.log2(i + 1)

    # Ideal DCG
    ideal_count = min(len(e_set), k)
    idcg = sum((2**1.0 - 1) / math.log2(i + 1) for i in range(1, ideal_count + 1))

    if idcg == 0.0:
        return 0.0
    return round(dcg / idcg, 4)


def compute_percentiles(values: List[float]) -> PercentileResult:
    """Computes p50 (median), p95, and average latency."""
    if not values:
        return PercentileResult({"p50": 0.0, "p95": 0.0, "avg": 0.0})

    sorted_vals = sorted(values)
    n = len(sorted_vals)
    p50_idx = int(0.50 * (n - 1))
    p95_idx = int(0.95 * (n - 1))

    return PercentileResult({
        "p50": round(sorted_vals[p50_idx], 2),
        "p95": round(sorted_vals[p95_idx], 2),
        "avg": round(sum(sorted_vals) / n, 2),
    })
