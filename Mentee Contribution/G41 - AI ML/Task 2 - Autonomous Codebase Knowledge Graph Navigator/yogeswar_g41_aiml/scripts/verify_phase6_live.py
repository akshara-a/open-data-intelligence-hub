"""
Phase 6 Live Docker End-to-End Verification Script
Tests real HTTP endpoints against the live Docker stack:
1. Health and Authentication
2. Change Impact Analysis (dynamic graph traversal, no Neo4j mutation)
3. Technical Report Generation and Retrieval (SQLite persistence, evidence citations)
4. Evaluation and Benchmarking Suite (formal metrics, SQLite persistence)
5. Snapshot isolation enforcement
"""
import sys
import json
import httpx
from pathlib import Path

# Add backend to path for admin pwd resolution
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from backend.app.database import get_admin_password

REPO_ID = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
COMMIT_SHA = "d730e05672cb7673365022a44d3814bdc66ec033"
BASE_URL = "https://localhost"


def run_live_verification():
    print("=" * 70)
    print("PHASE 6 LIVE DOCKER END-TO-END VERIFICATION")
    print("=" * 70)

    client = httpx.Client(verify=False, timeout=30.0)

    # 1. Health Check
    print("\n[Step 1] Checking Live Backend Health...")
    r = client.get(f"{BASE_URL}/api/v1/health")
    assert r.status_code == 200, f"Health check failed: {r.status_code} {r.text}"
    health = r.json()
    print(f"  Health status: {health.get('status')} | Database: {health.get('database')}")

    # 2. Authentication
    print("\n[Step 2] Authenticating as Admin User...")
    admin_pwd = get_admin_password()
    login_resp = client.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": "admin", "password": admin_pwd},
    )
    assert login_resp.status_code == 200, f"Login failed: {login_resp.status_code} {login_resp.text}"
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print(f"  Authenticated successfully. RS256 token acquired.")

    # 3. Change Impact Analysis
    print("\n[Step 3] Executing Live Change Impact Analysis...")
    impact_resp = client.post(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/impact/analyze",
        headers=headers,
        json={
            "target_entity": "verify_credentials",
            "max_depth": 2,
            "confidence_threshold": 0.2,
        },
    )
    assert impact_resp.status_code == 200, f"Impact analysis failed: {impact_resp.status_code} {impact_resp.text}"
    impact_data = impact_resp.json()
    print(f"  Target Entity: {impact_data.get('target_entity')}")
    print(f"  Summary: {impact_data.get('summary')}")
    print(f"  Target Found: {impact_data.get('target_found')}")
    print(f"  Direct Impacted: {len(impact_data.get('direct_impacted', []))}")
    print(f"  Transitive Impacted: {len(impact_data.get('transitive_impacted', []))}")
    print(f"  Unresolved Impacted: {len(impact_data.get('unresolved_impacted', []))}")
    print(f"  Graph Mutated (Must be False): {impact_data.get('graph_mutated')}")
    assert impact_data.get("graph_mutated") is False, "AFFECTS edges must not be persisted to Neo4j!"

    # 4. Technical Report Generation
    print("\n[Step 4] Generating Architecture Technical Report...")
    rep_resp = client.post(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/reports",
        headers=headers,
        json={
            "report_type": "architecture",
            "title": "Live E2E Architecture Assessment",
            "target_symbols": ["verify_credentials", "DatabasePool"],
        },
    )
    assert rep_resp.status_code == 201, f"Report generation failed: {rep_resp.status_code} {rep_resp.text}"
    report_data = rep_resp.json()
    report_id = report_data["report_id"]
    print(f"  Generated Report ID: {report_id}")
    print(f"  Report Title: {report_data['title']}")
    print(f"  Executive Summary: {report_data['executive_summary'][:90]}...")
    print(f"  Verified Findings Count: {len(report_data.get('verified_findings', []))}")
    print(f"  Uncertain Findings Count: {len(report_data.get('uncertain_findings', []))}")
    print(f"  Evidence Citations Count: {len(report_data.get('evidence', []))}")

    # 5. List and Get Report by ID
    print("\n[Step 5] Listing Reports and Validating Snapshot Isolation...")
    list_resp = client.get(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/reports",
        headers=headers,
    )
    assert list_resp.status_code == 200, f"List reports failed: {list_resp.status_code} {list_resp.text}"
    reports_list = list_resp.json()
    assert any(r["report_id"] == report_id for r in reports_list), "Created report must appear in snapshot reports list"
    print(f"  Snapshot Reports Count: {len(reports_list)} (Found newly generated report)")

    get_resp = client.get(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/reports/{report_id}",
        headers=headers,
    )
    assert get_resp.status_code == 200, f"Get report by ID failed: {get_resp.status_code}"
    print(f"  Retrieved Report Detail successfully.")

    # Isolation check: fetching with invalid commit should fail
    iso_resp = client.get(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/0000000000000000000000000000000000000000/reports/{report_id}",
        headers=headers,
    )
    assert iso_resp.status_code == 404, f"Snapshot isolation violation: expected 404, got {iso_resp.status_code}"
    print(f"  Snapshot isolation verified: foreign commit SHA returned 404 Not Found.")

    # 6. Evaluation Benchmark Suite Execution
    print("\n[Step 6] Triggering Curated Benchmark Evaluation Suite (Selected 3-case subset)...")
    eval_resp = client.post(
        f"{BASE_URL}/api/v1/evaluation/run",
        headers=headers,
        json={
            "repo_id": REPO_ID,
            "commit_sha": COMMIT_SHA,
            "selected_query_ids": ["TC-01-ENT-ID", "TC-03-DIR-DEP", "TC-09-UNANSWERABLE"],
        },
    )
    assert eval_resp.status_code == 201, f"Benchmark execution failed: {eval_resp.status_code} {eval_resp.text}"
    eval_data = eval_resp.json()
    run_id = eval_data["run_id"]
    metrics = eval_data["metrics"]
    print(f"  Benchmark Run ID: {run_id}")
    print(f"  Sample Count: {eval_data['sample_count']}")
    print(f"  Entity Extraction F1: {metrics.get('entity_f1')}")
    print(f"  Grounding Coverage: {metrics.get('evidence_coverage')}")
    print(f"  Unsupported Claim Rate: {metrics.get('unsupported_claim_rate')}")
    print(f"  p50 Latency: {metrics.get('p50_latency_ms')} ms")
    print(f"  Provider: {metrics.get('provider_name')} | Mode: {metrics.get('mode')}")

    # 7. List Historical Benchmark Runs
    print("\n[Step 7] Listing Historical Benchmark Runs...")
    runs_resp = client.get(f"{BASE_URL}/api/v1/evaluation/runs", headers=headers)
    assert runs_resp.status_code == 200, f"List runs failed: {runs_resp.status_code}"
    runs_list = runs_resp.json()
    assert any(r["run_id"] == run_id for r in runs_list), "Executed benchmark run must be in history list"
    print(f"  Total Historical Runs: {len(runs_list)} (Found newly executed run {run_id})")

    # 8. Clean up test report
    print("\n[Step 8] Deleting Test Report...")
    del_resp = client.delete(
        f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/reports/{report_id}",
        headers=headers,
    )
    assert del_resp.status_code == 200, f"Delete report failed: {del_resp.status_code}"
    print(f"  Report deleted cleanly.")

    print("\n" + "=" * 70)
    print("ALL LIVE DOCKER PHASE 6 E2E VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_live_verification()
