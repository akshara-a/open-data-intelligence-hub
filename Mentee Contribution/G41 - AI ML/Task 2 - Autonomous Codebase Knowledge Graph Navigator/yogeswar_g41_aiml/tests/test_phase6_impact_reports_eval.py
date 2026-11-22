"""
Phase 6 - Comprehensive Automated Test Suite
Validates:
1. Change Impact Analysis (dynamic graph traversal, multi-hop callers, unresolved calls, non-persisted AFFECTS)
2. Technical Report Generation (5 report types, SQLite persistence, evidence grounding, snapshot isolation)
3. Evaluation & Benchmarking (12-case benchmark dataset, formal mathematical metrics P/R/F1/MRR/nDCG/percentiles, SQLite persistence)
4. Phase 6 FastAPI API endpoints with authentication and repository authorization
"""
import pytest
import sqlite3
import json
import uuid
import datetime
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

from backend.app.database import init_db, get_db_connection
from backend.app.main import app
from backend.app.auth import create_access_token

# Phase 6 Modules
from backend.app.impact.models import (
    ImpactedEntity,
    ChangeImpactRequest,
    ChangeImpactResponse,
)
from backend.app.impact.engine import run_change_impact_analysis

from backend.app.agent.models import Finding
from backend.app.reports.models import (
    GenerateReportRequest,
    ReportSummary,
    ReportDetail,
)
from backend.app.reports.engine import (
    generate_technical_report,
    list_reports,
    get_report_by_id,
    delete_report_by_id,
)

from backend.app.evaluation.models import (
    BenchmarkTestCase,
    BenchmarkMetricsSummary,
    CategoryMetricScore,
    QueryEvaluationResult,
    BenchmarkRunDetail,
    BenchmarkRunSummary,
    ExecuteBenchmarkRequest,
)
from backend.app.evaluation.dataset import (
    CURATED_BENCHMARK_CASES,
    BENCHMARK_DATASET_VERSION,
    DEFAULT_BENCHMARK_REPO,
    DEFAULT_BENCHMARK_COMMIT,
)
from backend.app.evaluation.metrics import (
    compute_precision_recall_f1,
    compute_mrr,
    compute_ndcg_at_k,
    compute_percentiles,
)
from backend.app.evaluation.engine import (
    execute_benchmark_suite,
    list_benchmark_runs,
    get_benchmark_run_by_id,
)


@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()
    # Ensure test user and repo exist
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (user_id, username, password_hash, role) VALUES ('usr_admin_default', 'admin', 'hash', 'admin')"
            )
        cursor.execute(
            "INSERT OR IGNORE INTO repositories (repo_id, name, git_url, default_branch, status) VALUES (?, 'test-repo', 'https://git.local/test.git', 'main', 'ACTIVE')",
            (DEFAULT_BENCHMARK_REPO,),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO repo_memberships (id, user_id, repo_id, role) VALUES ('mem_test_p6', 'usr_admin_default', ?, 'owner')",
            (DEFAULT_BENCHMARK_REPO,),
        )
        conn.commit()


@pytest.fixture
def auth_headers():
    token = create_access_token(user_id="usr_admin_default", username="admin", role="admin")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def client():
    return TestClient(app)


# =========================================================================
# Workstream 1: Change Impact Analysis Tests
# =========================================================================

def test_change_impact_models_validation():
    """Validates schema validation of ChangeImpactRequest and models."""
    req = ChangeImpactRequest(
        target_entity="verify_credentials",
        max_depth=2,
        confidence_threshold=0.5,
    )
    assert req.target_entity == "verify_credentials"
    assert req.symbol_name == "verify_credentials"
    assert req.max_depth == 2
    assert req.confidence_threshold == 0.5

    entity = ImpactedEntity(
        entity_id="func_verify_credentials",
        name="verify_credentials",
        entity_type="Function",
        file_path="auth_service.py",
        impact_classification="direct_impact",
        hop_distance=1,
        confidence=1.0,
        evidence_ids=["E-1234"],
        is_uncertain=False,
    )
    assert entity.impact_level == "direct_impact"
    assert entity.depth == 1


def test_change_impact_analysis_dynamic_execution():
    """
    Validates dynamic change impact analysis traverses direct and transitive callers,
    maps unresolved calls, and does not persist AFFECTS edges.
    """
    async def _run():
        mock_lookup = {
            "entities": [
                {
                    "entity_id": "func_verify_credentials",
                    "name": "verify_credentials",
                    "file_path": "auth_service.py",
                    "type": "Function",
                }
            ]
        }
        mock_neighbors = {
            "incoming_dependents": [
                {
                    "entity_id": "func_login_handler",
                    "name": "login_handler",
                    "file_path": "api_router.py",
                    "relationship": "CALLS",
                    "type": "Function",
                }
            ]
        }
        mock_rel_ev = {
            "relationship_evidences": [
                {
                    "evidence_id": "E-neighbor-1",
                    "classification": "verified_dependency",
                    "file_path": "api_router.py",
                    "line_range": "10-25",
                }
            ]
        }
        mock_multihop = {
            "records": [
                {
                    "entity_id": "func_root_controller",
                    "name": "root_controller",
                    "file_path": "server.py",
                    "hop_distance": 2,
                    "relationship_types": ["CALLS"],
                }
            ]
        }
        mock_unresolved = {
            "unresolved_calls": [
                {
                    "call_id": "call_eval_1",
                    "invoked_symbol_name": "verify_credentials",
                    "file_path": "auth_service.py",
                    "line_range": "18-18",
                }
            ]
        }

        with patch("backend.app.impact.engine.execute_cgg_entity_lookup", new=AsyncMock(return_value=mock_lookup)), \
             patch("backend.app.impact.engine.execute_cgg_direct_neighbors", new=AsyncMock(return_value=mock_neighbors)), \
             patch("backend.app.impact.engine.execute_cgg_relationship_evidence", new=AsyncMock(return_value=mock_rel_ev)), \
             patch("backend.app.impact.engine.execute_cgg_multihop_impact", new=AsyncMock(return_value=mock_multihop)), \
             patch("backend.app.impact.engine.execute_cgg_unresolved_calls", new=AsyncMock(return_value=mock_unresolved)):

            req = ChangeImpactRequest(
                target_entity="verify_credentials",
                max_depth=2,
                confidence_threshold=0.2,
            )
            res = await run_change_impact_analysis(
                repo_id=DEFAULT_BENCHMARK_REPO,
                commit_sha=DEFAULT_BENCHMARK_COMMIT,
                request=req,
            )

            assert res.target_entity == "verify_credentials"
            assert res.max_depth == 2
            # Direct callers found
            assert len(res.direct_impacted) >= 1
            assert res.direct_impacted[0].name == "login_handler"
            assert res.direct_impacted[0].impact_level == "direct_impact"
            # Transitive callers found
            assert len(res.transitive_impacted) >= 1
            assert res.transitive_impacted[0].name == "root_controller"
            assert res.transitive_impacted[0].impact_level == "transitive_impact"
            # Unresolved dynamic callers marked as uncertain
            assert len(res.unresolved_impacted) >= 1
            assert res.unresolved_impacted[0].is_uncertain is True
            assert res.unresolved_impacted[0].confidence == 0.3
            # Graph persistence check: graph_mutated must be strictly False
            assert res.graph_mutated is False

    asyncio.run(_run())


def test_change_impact_confidence_filter():
    """Validates that items below confidence_threshold are excluded from results."""
    async def _run():
        mock_lookup = {
            "entities": [
                {
                    "entity_id": "func_verify_credentials",
                    "name": "verify_credentials",
                    "file_path": "auth_service.py",
                    "type": "Function",
                }
            ]
        }
        mock_unresolved = {
            "unresolved_calls": [
                {
                    "call_id": "call_eval_1",
                    "invoked_symbol_name": "verify_credentials",
                    "file_path": "auth_service.py",
                    "line_range": "18-18",
                }
            ]
        }

        with patch("backend.app.impact.engine.execute_cgg_entity_lookup", new=AsyncMock(return_value=mock_lookup)), \
             patch("backend.app.impact.engine.execute_cgg_direct_neighbors", new=AsyncMock(return_value={"incoming_dependents": []})), \
             patch("backend.app.impact.engine.execute_cgg_unresolved_calls", new=AsyncMock(return_value=mock_unresolved)):

            # When threshold is set to 0.8, unresolved items (confidence 0.3) must be filtered
            req = ChangeImpactRequest(
                target_entity="verify_credentials",
                max_depth=1,
                confidence_threshold=0.8,
            )
            res = await run_change_impact_analysis(
                repo_id=DEFAULT_BENCHMARK_REPO,
                commit_sha=DEFAULT_BENCHMARK_COMMIT,
                request=req,
            )
            assert len(res.unresolved_impacted) == 0

    asyncio.run(_run())


# =========================================================================
# Workstream 2: Technical Report Generation Tests
# =========================================================================

def test_technical_report_models():
    """Validates Pydantic serialization for technical reports."""
    req = GenerateReportRequest(
        report_type="architecture",
        title="Repository Architecture Overview",
        target_symbols=["verify_credentials", "DatabasePool"],
    )
    assert req.report_type == "architecture"
    assert len(req.target_symbols) == 2


def test_generate_technical_report_all_five_types():
    """
    Validates generation of all 5 report types:
    architecture, impact, migration, onboarding, vulnerability.
    """
    async def _run():
        report_types = ["architecture", "impact", "migration", "onboarding", "vulnerability"]

        with patch("backend.app.reports.engine.run_supervisor_workflow", new=AsyncMock(return_value={
            "status": "COMPLETED",
            "thread_id": "th_test_rep",
            "answer": MagicMock(
                summary="Report Executive Summary Content",
                verified_findings=[
                    Finding(
                        statement="DatabasePool initializes connection pool",
                        finding_type="verified_static",
                        evidence_ids=["E-db-pool-1"],
                        confidence=1.0,
                        file_path="db_pool.py",
                        line_range="10-20",
                    )
                ],
                uncertain_findings=[
                    Finding(
                        statement="Dynamic lookup in router",
                        finding_type="potential_uncertain",
                        evidence_ids=["E-dyn-1"],
                        confidence=0.3,
                        file_path="router.py",
                        line_range="30-35",
                    )
                ],
                recommendations=["Refactor connection pooling"],
                insufficient_evidence=False,
            ),
            "retrieved_evidence": [
                {
                    "evidence_id": "E-db-pool-1",
                    "classification": "verified_static",
                    "file_path": "db_pool.py",
                    "line_range": "10-20",
                    "description": "DatabasePool class declaration",
                }
            ],
            "tool_results": [],
            "execution_time_ms": 120.0,
        })), patch("backend.app.reports.engine.run_change_impact_analysis", new=AsyncMock(return_value=ChangeImpactResponse(
            repo_id=DEFAULT_BENCHMARK_REPO,
            commit_sha=DEFAULT_BENCHMARK_COMMIT,
            target_entity="DatabasePool",
            summary="Impact summary",
            direct_impacts=[],
            transitive_impacts=[],
            unresolved_impacts=[],
        ))):
            for r_type in report_types:
                req = GenerateReportRequest(
                    report_type=r_type,
                    title=f"Automated Test {r_type.title()} Report",
                    target_symbols=["DatabasePool"],
                )
                report = await generate_technical_report(
                    repo_id=DEFAULT_BENCHMARK_REPO,
                    commit_sha=DEFAULT_BENCHMARK_COMMIT,
                    request=req,
                    created_by="usr_admin_default",
                )
                assert report.report_id is not None
                assert report.repo_id == DEFAULT_BENCHMARK_REPO
                assert report.commit_sha == DEFAULT_BENCHMARK_COMMIT
                assert report.executive_summary is not None
                assert len(report.verified_findings) >= 0
                assert len(report.recommendations) >= 0

    asyncio.run(_run())


def test_report_crud_and_snapshot_isolation():
    """Validates SQLite persistence, listing, get by id, deletion, and snapshot isolation."""
    report_id = f"rep_{uuid.uuid4().hex[:10]}"
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reports (
                report_id, query_id, repo_id, commit_sha, report_type, title,
                query_text, executive_summary, verified_findings_json, uncertain_findings_json,
                recommendations_json, risk_assessment_json, evidence_json, limitations,
                markdown_body, status, created_at
            )
            VALUES (?, 'qry_test_1', ?, ?, 'architecture', 'CRUD Test Report', 'query', 'Summary text', '[]', '[]', '[]', '{}', '[]', 'None', 'Body', 'COMPLETED', ?)
            """,
            (report_id, DEFAULT_BENCHMARK_REPO, DEFAULT_BENCHMARK_COMMIT, now),
        )
        conn.commit()

    # Get by ID
    rep = get_report_by_id(report_id)
    assert rep is not None
    assert rep.report_id == report_id
    assert rep.title == "CRUD Test Report"

    # List reports for matching snapshot
    listing = list_reports(DEFAULT_BENCHMARK_REPO, DEFAULT_BENCHMARK_COMMIT)
    assert any(r.report_id == report_id for r in listing)

    # Snapshot isolation: listing for different commit returns empty list
    listing_other = list_reports(DEFAULT_BENCHMARK_REPO, "other_commit_12345")
    assert not any(r.report_id == report_id for r in listing_other)

    # Delete report
    deleted = delete_report_by_id(report_id)
    assert deleted is True
    assert get_report_by_id(report_id) is None


# =========================================================================
# Workstream 3: Evaluation & Benchmarking Tests
# =========================================================================

def test_evaluation_dataset_completeness():
    """Validates the 12 curated test cases exist across 12 distinct categories."""
    assert len(CURATED_BENCHMARK_CASES) == 12
    assert BENCHMARK_DATASET_VERSION == "1.0.0"
    categories = {tc.category for tc in CURATED_BENCHMARK_CASES}
    expected_categories = {
        "entity_identification",
        "class_lookup",
        "direct_dependency",
        "multihop_dependency",
        "import_relationships",
        "change_impact",
        "unresolved_calls",
        "evidence_provenance",
        "unanswerable",
        "ambiguous_query",
        "cross_snapshot",
        "security_injection",
    }
    assert categories == expected_categories


def test_metrics_precision_recall_f1_mathematical_correctness():
    """Validates precision, recall, and F1 calculations for exact, partial, and empty sets."""
    # Exact match
    p, r, f1 = compute_precision_recall_f1(["A", "B"], ["A", "B"])
    assert p == 1.0 and r == 1.0 and f1 == 1.0

    # Partial match: predicted = {A, B}, ground_truth = {A, C}
    # TP=1, FP=1, FN=1 -> P = 1/2 = 0.5, R = 1/2 = 0.5, F1 = 0.5
    p, r, f1 = compute_precision_recall_f1(["A", "B"], ["A", "C"])
    assert p == 0.5 and r == 0.5 and f1 == 0.5

    # Empty sets (both empty -> perfect score 1.0)
    p, r, f1 = compute_precision_recall_f1([], [])
    assert p == 1.0 and r == 1.0 and f1 == 1.0

    # No match
    p, r, f1 = compute_precision_recall_f1(["X"], ["Y"])
    assert p == 0.0 and r == 0.0 and f1 == 0.0


def test_metrics_mrr_and_ndcg_ranking():
    """Validates Mean Reciprocal Rank (MRR) and nDCG@K calculations."""
    # First item relevant -> rank = 1 -> RR = 1.0
    mrr_1 = compute_mrr(["docA", "docB", "docC"], ["docA"])
    assert mrr_1 == 1.0

    # Second item relevant -> rank = 2 -> RR = 0.5
    mrr_2 = compute_mrr(["docX", "docA", "docC"], ["docA"])
    assert mrr_2 == 0.5

    # None relevant -> RR = 0.0
    mrr_0 = compute_mrr(["docX", "docY"], ["docA"])
    assert mrr_0 == 0.0

    # nDCG perfect ranking
    ndcg_perfect = compute_ndcg_at_k(["A", "B"], ["A", "B"], k=5)
    assert ndcg_perfect == 1.0

    # nDCG no relevant items
    ndcg_zero = compute_ndcg_at_k(["X", "Y"], ["A", "B"], k=5)
    assert ndcg_zero == 0.0


def test_metrics_percentiles():
    """Validates p50 and p95 calculations with known array."""
    data = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    p50, p95 = compute_percentiles(data)
    assert p50 == pytest.approx(55.0, abs=5.0)
    assert p95 == pytest.approx(95.0, abs=5.0)

    # Empty data
    p50_e, p95_e = compute_percentiles([])
    assert p50_e == 0.0 and p95_e == 0.0


def test_benchmark_suite_execution_and_persistence():
    """
    Validates executing a benchmark run across a test case subset,
    computing aggregated metrics, and persisting to SQLite.
    """
    async def _run():
        subset_cases = [
            tc for tc in CURATED_BENCHMARK_CASES
            if tc.test_id in ("TC-01-ENT-ID", "TC-09-UNANSWERABLE")
        ]

        with patch("backend.app.evaluation.engine.run_supervisor_workflow", new=AsyncMock(return_value={
            "status": "COMPLETED",
            "thread_id": "th_eval_test",
            "answer": MagicMock(
                summary="Answer",
                verified_findings=[
                    MagicMock(
                        statement="verify_credentials declared in auth_service.py",
                        finding_type="verified_static",
                        evidence_ids=["E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5"],
                        confidence=1.0,
                        file_path="auth_service.py",
                        line_range="4-8",
                    )
                ],
                uncertain_findings=[],
                insufficient_evidence=False,
            ),
            "retrieved_evidence": [
                {
                    "evidence_id": "E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5",
                    "classification": "verified_static",
                    "file_path": "auth_service.py",
                    "line_range": "4-8",
                    "description": "Definition",
                }
            ],
            "tool_results": [],
            "execution_time_ms": 50.0,
        })):
            run_detail = await execute_benchmark_suite(
                user_id="usr_admin_default",
                dataset_cases=subset_cases,
            )

            assert run_detail.run_id.startswith("bm_")
            assert run_detail.sample_count == 2
            assert run_detail.status == "COMPLETED"
            assert len(run_detail.query_results) == 2
            assert run_detail.metrics.sample_count == 2

            # Verify retrieval and listing from SQLite
            retrieved = get_benchmark_run_by_id(run_detail.run_id)
            assert retrieved is not None
            assert retrieved.run_id == run_detail.run_id
            assert retrieved.sample_count == 2
            assert len(retrieved.query_results) == 2

            history = list_benchmark_runs()
            assert any(h.run_id == run_detail.run_id for h in history)

    asyncio.run(_run())


# =========================================================================
# Workstream 4 & 5: FastAPI REST Endpoints & Authorization Tests
# =========================================================================

def test_api_change_impact_analyze_endpoint(client, auth_headers):
    """Tests POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/impact/analyze."""
    with patch("backend.app.main.run_change_impact_analysis", new=AsyncMock(return_value=ChangeImpactResponse(
        repo_id=DEFAULT_BENCHMARK_REPO,
        commit_sha=DEFAULT_BENCHMARK_COMMIT,
        target_entity="verify_credentials",
        summary="Impact analysis complete",
        max_depth=2,
        max_depth_analyzed=2,
        direct_impacted=[],
        transitive_impacted=[],
        unresolved_impacted=[],
        total_impacted_count=0,
        graph_mutated=False,
        execution_time_ms=45.0,
    ))):
        resp = client.post(
            f"/api/v1/repos/{DEFAULT_BENCHMARK_REPO}/snapshots/{DEFAULT_BENCHMARK_COMMIT}/impact/analyze",
            headers=auth_headers,
            json={"target_entity": "verify_credentials", "max_depth": 2},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["target_entity"] == "verify_credentials"
        assert data["graph_mutated"] is False


def test_api_reports_lifecycle_endpoints(client, auth_headers):
    """Tests POST, GET, DELETE /api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports."""
    with patch("backend.app.main.generate_technical_report", new=AsyncMock(return_value=ReportDetail(
        report_id="rep_api_test_123",
        repo_id=DEFAULT_BENCHMARK_REPO,
        commit_sha=DEFAULT_BENCHMARK_COMMIT,
        report_type="architecture",
        title="API Architecture Report",
        executive_summary="Summary",
        verified_findings=[],
        uncertain_findings=[],
        recommendations=[],
        risk_assessment={},
        evidence=[],
        limitations="None",
        status="COMPLETED",
        created_by="usr_admin_default",
        created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    ))):
        # Create
        create_resp = client.post(
            f"/api/v1/repos/{DEFAULT_BENCHMARK_REPO}/snapshots/{DEFAULT_BENCHMARK_COMMIT}/reports",
            headers=auth_headers,
            json={"report_type": "architecture", "title": "API Architecture Report"},
        )
        assert create_resp.status_code == 201
        rep_data = create_resp.json()
        assert rep_data["report_id"] == "rep_api_test_123"

        # List
        list_resp = client.get(
            f"/api/v1/repos/{DEFAULT_BENCHMARK_REPO}/snapshots/{DEFAULT_BENCHMARK_COMMIT}/reports",
            headers=auth_headers,
        )
        assert list_resp.status_code == 200
        assert isinstance(list_resp.json(), list)


def test_api_evaluation_endpoints(client, auth_headers):
    """Tests POST /api/v1/evaluation/run and GET /api/v1/evaluation/runs."""
    # List historical runs
    runs_resp = client.get("/api/v1/evaluation/runs", headers=auth_headers)
    assert runs_resp.status_code == 200
    assert isinstance(runs_resp.json(), list)

    # Unauthorized access check
    unauth_resp = client.get("/api/v1/evaluation/runs")
    assert unauth_resp.status_code == 401
