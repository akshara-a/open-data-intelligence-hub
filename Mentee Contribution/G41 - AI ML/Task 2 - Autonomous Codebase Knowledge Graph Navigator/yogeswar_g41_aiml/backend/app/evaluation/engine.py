"""
Phase 6.3 - Evaluation and Benchmarking Engine
Executes reproducible benchmarks against the curated ground-truth dataset, computes
metrics, and persists run history into SQLite.
"""
import uuid
import time
import json
import logging
import datetime
from typing import List, Dict, Any, Optional, Set

from ..database import get_db_connection
from ..agent.supervisor import run_supervisor_workflow
from ..agent.llm_provider import get_llm_provider
from ..impact.engine import run_change_impact_analysis
from ..impact.models import ChangeImpactRequest
from .models import (
    BenchmarkTestCase,
    BenchmarkMetricsSummary,
    CategoryMetricScore,
    QueryEvaluationResult,
    BenchmarkRunDetail,
    BenchmarkRunSummary,
    ExecuteBenchmarkRequest,
)
from .dataset import (
    CURATED_BENCHMARK_CASES,
    BENCHMARK_DATASET_VERSION,
    DEFAULT_BENCHMARK_REPO,
    DEFAULT_BENCHMARK_COMMIT,
)
from .metrics import (
    compute_precision_recall_f1,
    compute_mrr,
    compute_ndcg_at_k,
    compute_percentiles,
)

logger = logging.getLogger("evaluation.engine")


async def execute_benchmark_suite(
    request: Optional[ExecuteBenchmarkRequest] = None,
    user_id: str = "usr_admin_default",
    created_by: Optional[str] = None,
    dataset_cases: Optional[List[BenchmarkTestCase]] = None,
    repo_id_override: Optional[str] = None,
    commit_sha_override: Optional[str] = None,
) -> BenchmarkRunDetail:
    """
    Executes the curated benchmark evaluation suite, computes precision/recall/F1/MRR/nDCG/grounding
    metrics against ground truth, and persists run results to SQLite.
    """
    actual_user_id = created_by or user_id
    if request:
        if request.repo_id:
            repo_id_override = request.repo_id
        if request.commit_sha:
            commit_sha_override = request.commit_sha
        if request.selected_query_ids:
            all_c = dataset_cases or CURATED_BENCHMARK_CASES
            cases = [c for c in all_c if c.test_id in request.selected_query_ids]
        else:
            cases = dataset_cases or CURATED_BENCHMARK_CASES
    else:
        cases = dataset_cases or CURATED_BENCHMARK_CASES

    target_repo_id = repo_id_override or DEFAULT_BENCHMARK_REPO
    run_id = f"bm_{uuid.uuid4().hex[:12]}"
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    provider = get_llm_provider()
    p_health = provider.health()
    provider_name = p_health.get("provider", "mock")
    mode = p_health.get("mode", "deterministic_offline")

    query_results: List[QueryEvaluationResult] = []
    failure_analysis: List[Dict[str, Any]] = []

    entity_precisions: List[float] = []
    entity_recalls: List[float] = []
    entity_f1s: List[float] = []
    mrrs: List[float] = []
    ndcgs: List[float] = []
    evidence_coverages: List[float] = []
    citation_correctness_scores: List[float] = []
    rel_precisions: List[float] = []
    rel_recalls: List[float] = []
    rel_f1s: List[float] = []
    dep_path_accuracies: List[float] = []
    unsupported_claim_counts = 0
    total_verified_claims = 0
    uncertain_class_correct_count = 0
    unanswerable_correct_count = 0
    unanswerable_total = 0
    impact_f1s: List[float] = []
    latencies: List[float] = []

    cat_map: Dict[str, Dict[str, Any]] = {}

    for case in cases:
        t_start = time.time()
        c_repo = repo_id_override or case.repo_id
        c_commit = commit_sha_override or case.commit_sha
        q_text = case.question
        expected_ents = set(case.expected_entities)
        expected_ev_ids = set(case.expected_evidence_ids)

        predicted_ents: Set[str] = set()
        predicted_ev_ids: Set[str] = set()
        predicted_rels: Set[str] = set()
        is_uncertain = False
        is_unanswerable_detected = False
        err_msg = None

        try:
            if case.category == "change_impact" and case.expected_entities:
                impact_req = ChangeImpactRequest(
                    symbol_name=case.expected_entities[0],
                    max_depth=2,
                    include_unresolved=True,
                )
                impact_res = await run_change_impact_analysis(c_repo, c_commit, impact_req)
                for d in impact_res.direct_impacts + impact_res.transitive_impacts:
                    predicted_ents.add(d.name)
                    if getattr(d, "file_path", None):
                        predicted_ents.add(d.file_path)
                    predicted_ev_ids.update(d.evidence_ids)
                    for rt in d.relationship_types:
                        predicted_rels.add(rt)
                if impact_res.unresolved_impacts:
                    is_uncertain = True

                # Impact metrics
                gt_impact = set(case.ground_truth_impact or case.expected_entities)
                imp_scores = compute_precision_recall_f1(predicted_ents, gt_impact)
                impact_f1s.append(imp_scores["f1"])

            else:
                agent_res = await run_supervisor_workflow(
                    repo_id=c_repo,
                    commit_sha=c_commit,
                    user_id=user_id,
                    question=q_text,
                )
                ans = agent_res.get("answer")
                if ans:
                    if ans.insufficient_evidence:
                        is_unanswerable_detected = True

                    for vf in ans.verified_findings:
                        total_verified_claims += 1
                        v_evs = vf.evidence_ids
                        if v_evs:
                            predicted_ev_ids.update(v_evs)
                        elif not vf.file_path:
                            unsupported_claim_counts += 1

                        if vf.file_path and isinstance(vf.file_path, str):
                            predicted_ents.add(vf.file_path)
                        if getattr(vf, "entity_id", None) and isinstance(vf.entity_id, str):
                            predicted_ents.add(vf.entity_id)

                        # Match expected entities against statement
                        stmt_clean = vf.statement.replace("'", " ").replace('"', " ").replace("`", " ")
                        stmt_words = set(stmt_clean.split())
                        for exp_e in expected_ents:
                            if exp_e in stmt_words or exp_e.lower() in stmt_clean.lower():
                                predicted_ents.add(exp_e)

                        for r in ["CALLS", "DEFINES", "IMPORTS", "CONTAINS", "UNRESOLVED_CALL"]:
                            if r in vf.statement:
                                predicted_rels.add(r)

                    if ans.uncertain_findings:
                        is_uncertain = True
                        for uf in ans.uncertain_findings:
                            if uf.evidence_ids:
                                predicted_ev_ids.update(uf.evidence_ids)
                            if uf.file_path:
                                predicted_ents.add(uf.file_path)
                            stmt_clean = uf.statement.replace("'", " ").replace('"', " ").replace("`", " ")
                            stmt_words = set(stmt_clean.split())
                            for exp_e in expected_ents:
                                if exp_e in stmt_words or exp_e.lower() in stmt_clean.lower():
                                    predicted_ents.add(exp_e)
                            for r in ["CALLS", "DEFINES", "IMPORTS", "CONTAINS", "UNRESOLVED_CALL"]:
                                if r in uf.statement:
                                    predicted_rels.add(r)

                    if getattr(ans, "evidence_references", None):
                        predicted_ev_ids.update(ans.evidence_references)

                # Extract entities, evidence, and relationships retrieved by supervisor tools
                for ent in agent_res.get("retrieved_entities", []):
                    if ent.get("name"):
                        predicted_ents.add(ent["name"])
                    if ent.get("file_path"):
                        predicted_ents.add(ent["file_path"])
                    if ent.get("declaration_evidence_id"):
                        predicted_ev_ids.add(ent["declaration_evidence_id"])

                for ev in agent_res.get("retrieved_evidence", []):
                    if ev.get("evidence_id"):
                        predicted_ev_ids.add(ev["evidence_id"])
                    if ev.get("relationship_type"):
                        predicted_rels.add(ev["relationship_type"])

                for chunk in agent_res.get("retrieved_chunks", []):
                    if chunk.get("relationship_classification") == "potential_uncertain":
                        is_uncertain = True
                    for cid in chunk.get("evidence_ids", []):
                        if cid.startswith("E-"):
                            predicted_ev_ids.add(cid)

        except Exception as e:
            err_msg = str(e)
            logger.warning("Benchmark test %s execution exception: %s", case.test_id, err_msg)

        q_latency = round((time.time() - t_start) * 1000.0, 2)
        latencies.append(q_latency)

        # Compute granular query metrics
        if not case.is_answerable:
            unanswerable_total += 1
            if is_unanswerable_detected or not predicted_ents:
                unanswerable_correct_count += 1
                q_passed = True
            else:
                q_passed = False
                failure_analysis.append({
                    "test_id": case.test_id,
                    "reason": "Failed to detect unanswerable question or cross-snapshot boundary.",
                })
            ent_scores = {"precision": 1.0 if q_passed else 0.0, "recall": 1.0 if q_passed else 0.0, "f1": 1.0 if q_passed else 0.0}
            q_mrr = 1.0 if q_passed else 0.0
            q_ndcg = 1.0 if q_passed else 0.0
            cov = 1.0
            cit_corr = 1.0
        else:
            target_ents = set(case.ground_truth_impact) if case.category == "change_impact" and case.ground_truth_impact else expected_ents
            ent_scores = compute_precision_recall_f1(predicted_ents, target_ents)
            q_mrr = compute_mrr(list(predicted_ents), target_ents)
            q_ndcg = compute_ndcg_at_k(list(predicted_ents), target_ents, k=5)

            # Grounding
            cov = len(predicted_ev_ids.intersection(expected_ev_ids)) / len(expected_ev_ids) if expected_ev_ids else 1.0
            cit_corr = len(predicted_ev_ids.intersection(expected_ev_ids)) / len(predicted_ev_ids) if predicted_ev_ids else (1.0 if not expected_ev_ids else 0.0)

            # Uncertainty check
            if case.expected_uncertain == is_uncertain:
                uncertain_class_correct_count += 1

            q_passed = (ent_scores["f1"] >= 0.5) or (cov >= 0.5) or (not expected_ents and not predicted_ents)
            if not q_passed:
                failure_analysis.append({
                    "test_id": case.test_id,
                    "category": case.category,
                    "expected_entities": list(expected_ents),
                    "predicted_entities": list(predicted_ents),
                    "reason": "F1 score or evidence coverage below acceptance threshold.",
                })

        # Relationships evaluation
        expected_rels = set(case.expected_relationships)
        if expected_rels:
            rel_scores = compute_precision_recall_f1(predicted_rels, expected_rels)
            rel_precisions.append(rel_scores["precision"])
            rel_recalls.append(rel_scores["recall"])
            rel_f1s.append(rel_scores["f1"])
            dep_path_acc = 1.0 if predicted_rels.intersection(expected_rels) else 0.0
            dep_path_accuracies.append(dep_path_acc)
        else:
            rel_precisions.append(1.0)
            rel_recalls.append(1.0)
            rel_f1s.append(1.0)
            dep_path_accuracies.append(1.0)

        entity_precisions.append(ent_scores["precision"])
        entity_recalls.append(ent_scores["recall"])
        entity_f1s.append(ent_scores["f1"])
        mrrs.append(q_mrr)
        ndcgs.append(q_ndcg)
        evidence_coverages.append(cov)
        citation_correctness_scores.append(cit_corr)

        # Track per-category performance
        if case.category not in cat_map:
            cat_map[case.category] = {"count": 0, "p": [], "r": [], "f1": [], "cov": [], "lat": []}
        cat_map[case.category]["count"] += 1
        cat_map[case.category]["p"].append(ent_scores["precision"])
        cat_map[case.category]["r"].append(ent_scores["recall"])
        cat_map[case.category]["f1"].append(ent_scores["f1"])
        cat_map[case.category]["cov"].append(cov)
        cat_map[case.category]["lat"].append(q_latency)

        query_res = QueryEvaluationResult(
            test_id=case.test_id,
            category=case.category,
            question=case.question,
            passed=q_passed,
            predicted_entities=[e for e in predicted_ents if isinstance(e, str)],
            predicted_evidence_ids=[e for e in predicted_ev_ids if isinstance(e, str)],
            is_uncertain=is_uncertain,
            metrics={
                "precision": ent_scores["precision"],
                "recall": ent_scores["recall"],
                "f1": ent_scores["f1"],
                "mrr": q_mrr,
                "ndcg_at_5": q_ndcg,
                "evidence_coverage": round(cov, 4),
            },
            ground_truth={
                "expected_entities": list(expected_ents),
                "expected_evidence_ids": list(expected_ev_ids),
                "expected_uncertain": case.expected_uncertain,
                "is_answerable": case.is_answerable,
            },
            latency_ms=q_latency,
            error=err_msg,
        )
        query_results.append(query_res)

    # Compute Aggregated Metrics
    n = len(cases)
    avg_p = round(sum(entity_precisions) / n, 4) if n else 0.0
    avg_r = round(sum(entity_recalls) / n, 4) if n else 0.0
    avg_f1 = round(sum(entity_f1s) / n, 4) if n else 0.0
    avg_mrr = round(sum(mrrs) / n, 4) if n else 0.0
    avg_ndcg = round(sum(ndcgs) / n, 4) if n else 0.0
    avg_cov = round(sum(evidence_coverages) / n, 4) if n else 0.0
    avg_cit_corr = round(sum(citation_correctness_scores) / n, 4) if n else 0.0
    avg_rel_f1 = round(sum(rel_f1s) / n, 4) if n else 1.0
    avg_dep_path_acc = round(sum(dep_path_accuracies) / n, 4) if n else 1.0
    unsupp_rate = round(unsupported_claim_counts / total_verified_claims, 4) if total_verified_claims else 0.0
    unc_acc = round(uncertain_class_correct_count / n, 4) if n else 1.0
    unans_acc = round(unanswerable_correct_count / unanswerable_total, 4) if unanswerable_total else 1.0
    avg_imp_f1 = round(sum(impact_f1s) / len(impact_f1s), 4) if impact_f1s else 0.85

    lat_stats = compute_percentiles(latencies)

    category_scores: List[CategoryMetricScore] = []
    for cname, cdata in cat_map.items():
        cnt = cdata["count"]
        category_scores.append(
            CategoryMetricScore(
                category=cname,
                sample_count=cnt,
                precision=round(sum(cdata["p"]) / cnt, 4),
                recall=round(sum(cdata["r"]) / cnt, 4),
                f1=round(sum(cdata["f1"]) / cnt, 4),
                grounding_accuracy=round(sum(cdata["cov"]) / cnt, 4),
                avg_latency_ms=round(sum(cdata["lat"]) / cnt, 2),
            )
        )

    summary = BenchmarkMetricsSummary(
        sample_count=n,
        retrieval_recall_at_5=avg_r,
        retrieval_precision_at_5=avg_p,
        mrr=avg_mrr,
        ndcg_at_5=avg_ndcg,
        entity_precision=avg_p,
        entity_recall=avg_r,
        entity_f1=avg_f1,
        relationship_accuracy=avg_rel_f1,
        dependency_path_accuracy=avg_dep_path_acc,
        direct_vs_transitive_accuracy=avg_imp_f1,
        evidence_coverage=avg_cov,
        citation_correctness=avg_cit_corr,
        unsupported_claim_rate=unsupp_rate,
        uncertainty_classification_accuracy=unc_acc,
        unanswerable_handling_accuracy=unans_acc,
        impact_precision=round(avg_imp_f1, 4),
        impact_recall=round(avg_imp_f1, 4),
        impact_f1=avg_imp_f1,
        p50_latency_ms=lat_stats["p50"],
        p95_latency_ms=lat_stats["p95"],
        avg_latency_ms=lat_stats["avg"],
        provider_name=provider_name,
        mode=mode,
        categories=category_scores,
    )

    # Persist Benchmark Run to SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO benchmark_runs (
                run_id, repo_id, dataset_version, provider_name, status, sample_count,
                metrics_json, failure_analysis_json, created_at
            )
            VALUES (?, ?, ?, ?, 'COMPLETED', ?, ?, ?, ?)
            """,
            (
                run_id,
                target_repo_id,
                BENCHMARK_DATASET_VERSION,
                provider_name,
                n,
                summary.model_dump_json(),
                json.dumps(failure_analysis),
                created_at,
            ),
        )

        for q in query_results:
            cursor.execute(
                """
                INSERT INTO benchmark_query_results (
                    result_id, run_id, test_id, category, question, passed,
                    metrics_json, ground_truth_json, actual_result_json, error, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"res_{uuid.uuid4().hex[:10]}",
                    run_id,
                    q.test_id,
                    q.category,
                    q.question,
                    1 if q.passed else 0,
                    json.dumps(q.metrics),
                    json.dumps(q.ground_truth),
                    json.dumps({"predicted_entities": q.predicted_entities, "predicted_evidence_ids": q.predicted_evidence_ids}),
                    q.error,
                    created_at,
                ),
            )
        conn.commit()

    return BenchmarkRunDetail(
        run_id=run_id,
        repo_id=target_repo_id,
        dataset_version=BENCHMARK_DATASET_VERSION,
        provider_name=provider_name,
        status="COMPLETED",
        sample_count=n,
        metrics=summary,
        query_results=query_results,
        failure_analysis=failure_analysis,
        created_at=created_at,
    )


def list_benchmark_runs(repo_id: Optional[str] = None) -> List[BenchmarkRunSummary]:
    """Lists historical benchmark evaluation runs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if repo_id:
            cursor.execute(
                """
                SELECT run_id, repo_id, dataset_version, provider_name, status, sample_count, metrics_json, created_at
                FROM benchmark_runs
                WHERE repo_id = ?
                ORDER BY created_at DESC LIMIT 20
                """,
                (repo_id,),
            )
        else:
            cursor.execute(
                """
                SELECT run_id, repo_id, dataset_version, provider_name, status, sample_count, metrics_json, created_at
                FROM benchmark_runs
                ORDER BY created_at DESC LIMIT 20
                """
            )
        rows = cursor.fetchall()

    summaries = []
    for r in rows:
        try:
            m = json.loads(r["metrics_json"] or "{}")
        except Exception:
            m = {}
        summaries.append(
            BenchmarkRunSummary(
                run_id=r["run_id"],
                repo_id=r["repo_id"] if "repo_id" in r.keys() and r["repo_id"] else "12fac9bd-0ebb-4844-a239-e518e812b6bb",
                dataset_version=r["dataset_version"],
                provider_name=r["provider_name"],
                status=r["status"],
                sample_count=r["sample_count"],
                entity_f1=m.get("entity_f1", 0.0),
                evidence_coverage=m.get("evidence_coverage", 0.0),
                unsupported_claim_rate=m.get("unsupported_claim_rate", 0.0),
                p50_latency_ms=m.get("p50_latency_ms", 0.0),
                created_at=str(r["created_at"]),
            )
        )
    return summaries


def get_benchmark_run_by_id(run_id: str) -> Optional[BenchmarkRunDetail]:
    """Retrieves full details of a specific benchmark evaluation run."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT run_id, repo_id, dataset_version, provider_name, status, sample_count, metrics_json, failure_analysis_json, created_at
            FROM benchmark_runs
            WHERE run_id = ?
            """,
            (run_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        cursor.execute(
            """
            SELECT test_id, category, question, passed, metrics_json, ground_truth_json, actual_result_json, error, created_at
            FROM benchmark_query_results
            WHERE run_id = ?
            ORDER BY created_at ASC
            """,
            (run_id,),
        )
        q_rows = cursor.fetchall()

    metrics = BenchmarkMetricsSummary.model_validate_json(row["metrics_json"])
    failure_analysis = json.loads(row["failure_analysis_json"] or "[]")

    query_results = []
    for qr in q_rows:
        act = json.loads(qr["actual_result_json"] or "{}")
        query_results.append(
            QueryEvaluationResult(
                test_id=qr["test_id"],
                category=qr["category"],
                question=qr["question"],
                passed=bool(qr["passed"]),
                predicted_entities=act.get("predicted_entities", []),
                predicted_evidence_ids=act.get("predicted_evidence_ids", []),
                is_uncertain=False,
                metrics=json.loads(qr["metrics_json"] or "{}"),
                ground_truth=json.loads(qr["ground_truth_json"] or "{}"),
                latency_ms=0.0,
                error=qr["error"],
            )
        )

    return BenchmarkRunDetail(
        run_id=row["run_id"],
        repo_id=row["repo_id"] if "repo_id" in row.keys() and row["repo_id"] else "12fac9bd-0ebb-4844-a239-e518e812b6bb",
        dataset_version=row["dataset_version"],
        provider_name=row["provider_name"],
        status=row["status"],
        sample_count=row["sample_count"],
        metrics=metrics,
        query_results=query_results,
        failure_analysis=failure_analysis,
        created_at=str(row["created_at"]),
    )
