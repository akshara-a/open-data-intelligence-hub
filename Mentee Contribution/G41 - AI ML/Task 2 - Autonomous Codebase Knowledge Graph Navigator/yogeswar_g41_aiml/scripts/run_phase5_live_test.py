#!/usr/bin/env python3
"""
Phase 5 Live Docker Integration Test
Proves end-to-end functionality of the Agentic AI Assistant running in Docker Compose:
1. Verifies assistant service health via HTTPS.
2. Authenticates through Nginx reverse proxy using secure credentials.
3. Retrieves or uses an ingested repository snapshot.
4. Executes real assistant chat endpoint (/api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/chat).
5. Verifies 7-stage workflow completion, verified vs uncertain findings, tool trace, and citations.
6. Verifies conversation thread persistence and continuation (/assistant/threads).
7. Validates security controls: snapshot context isolation, unauthorized repo rejection.
"""
import sys
import os
import json
import httpx
from pathlib import Path

BASE_URL = os.getenv("API_BASE_URL", "https://localhost")
VERIFY_SSL = False  # Self-signed certificate in local docker environment

def get_admin_password() -> str:
    candidates = [
        Path("./secrets/admin.password"),
        Path("../secrets/admin.password"),
        Path(__file__).resolve().parent.parent / "secrets" / "admin.password",
    ]
    for p in candidates:
        if p.is_file():
            val = p.read_text(encoding="utf-8").strip()
            if val:
                return val
    raise RuntimeError("Admin password secret file not found in secrets/admin.password")


def run_test():
    print("=" * 80)
    print("Phase 5 Live Docker Integration Test: Autonomous Codebase Assistant")
    print("=" * 80)

    with httpx.Client(base_url=BASE_URL, verify=VERIFY_SSL, timeout=30.0) as client:
        # Step 1: Health Check
        print("\n[Step 1] Checking Assistant Health Endpoint...")
        health_resp = client.get("/api/v1/assistant/health")
        assert health_resp.status_code == 200, f"Assistant health check failed: {health_resp.status_code} {health_resp.text}"
        health_data = health_resp.json()
        print(f"  Status: {health_data.get('status')}")
        print(f"  Provider: {health_data.get('provider')}")
        print(f"  Mode: {health_data.get('mode')}")
        print("  -> Health Check PASSED")

        # Step 2: Authentication
        print("\n[Step 2] Authenticating as Administrator...")
        admin_pwd = get_admin_password()
        login_resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": admin_pwd})
        assert login_resp.status_code == 200, f"Admin login failed: {login_resp.status_code} {login_resp.text}"
        tokens = login_resp.json()
        access_token = tokens["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print("  -> Admin Login Successful. RS256 token acquired.")

        # Step 3: Discover Active Repositories and Snapshots
        print("\n[Step 3] Querying Repositories and Snapshots...")
        repos_resp = client.get("/api/v1/repos", headers=headers)
        assert repos_resp.status_code == 200, f"Failed to list repos: {repos_resp.status_code} {repos_resp.text}"
        repos_data = repos_resp.json()
        repos = repos_data if isinstance(repos_data, list) else repos_data.get("repositories", [])
        print(f"  Found {len(repos)} registered repository/repositories.")

        target_repo_id = None
        target_commit_sha = None

        for r in repos:
            rid = r.get("repo_id")
            if rid == "12fac9bd-0ebb-4844-a239-e518e812b6bb":
                snaps_resp = client.get(f"/api/v1/repos/{rid}/snapshots", headers=headers)
                if snaps_resp.status_code == 200:
                    snaps_json = snaps_resp.json()
                    snaps = snaps_json if isinstance(snaps_json, list) else snaps_json.get("snapshots", [])
                    if snaps:
                        target_repo_id = rid
                        target_commit_sha = snaps[0].get("commit_sha")
                        print(f"  Selected Ingested Snapshot: repo_id={target_repo_id}, commit_sha={target_commit_sha[:8]}")
                        break

        if not target_repo_id:
            for r in repos:
                rid = r.get("repo_id")
                if rid == "repo_demo_sample":
                    continue
                snaps_resp = client.get(f"/api/v1/repos/{rid}/snapshots", headers=headers)
                if snaps_resp.status_code == 200:
                    snaps_json = snaps_resp.json()
                    snaps = snaps_json if isinstance(snaps_json, list) else snaps_json.get("snapshots", [])
                    if snaps:
                        target_repo_id = rid
                        target_commit_sha = snaps[0].get("commit_sha")
                        print(f"  Selected Ingested Snapshot: repo_id={target_repo_id}, commit_sha={target_commit_sha[:8]}")
                        break

        if not target_repo_id or not target_commit_sha:
            # Fallback to demo sample repository if no ingested snapshots exist
            target_repo_id = "repo_demo_sample"
            target_commit_sha = "c0ffee12"
            print(f"  Using demo fallback: repo_id={target_repo_id}, commit_sha={target_commit_sha[:8]}")

        # Step 4: Execute Assistant Chat Query
        print("\n[Step 4] Submitting Multi-Tool Architectural Inquiry to LangGraph Assistant...")
        query_payload = {
            "question": "Explain the dependency chain between verify_credentials in auth_service.py and DatabasePool in db_pool.py, including any dynamic calls in dynamic_router.py.",
        }
        chat_url = f"/api/v1/repos/{target_repo_id}/snapshots/{target_commit_sha}/assistant/chat"
        chat_resp = client.post(chat_url, json=query_payload, headers=headers)
        assert chat_resp.status_code == 200, f"Assistant chat failed: {chat_resp.status_code} {chat_resp.text}"
        chat_data = chat_resp.json()

        print(f"  Status: {chat_data.get('status')}")
        thread_id = chat_data.get("thread_id")
        print(f"  Thread ID: {thread_id}")
        print(f"  Execution Time: {chat_data.get('execution_time_ms')} ms")
        answer = chat_data.get("answer", {})
        print(f"  Summary: {answer.get('summary', '')[:100]}...")
        verified_findings = answer.get("verified_findings", [])
        uncertain_findings = answer.get("uncertain_findings", [])
        tool_trace = chat_data.get("tool_trace", [])
        print(f"  Verified Findings: {len(verified_findings)}")
        print(f"  Uncertain Findings: {len(uncertain_findings)}")
        print(f"  Tool Trace Entries: {len(tool_trace)}")
        for i, t_entry in enumerate(tool_trace, 1):
            extra = f", count: {t_entry.get('count')}" if 'count' in t_entry else ""
            if 'source' in t_entry:
                extra += f", source: {t_entry.get('source')[:40]}..., target: {t_entry.get('target')[:40]}..."
            elif 'entity_id' in t_entry:
                extra += f", entity_id: {t_entry.get('entity_id')[:40]}..."
            print(f"    {i}. Tool: {t_entry.get('tool')}, Status: {t_entry.get('status')}{extra}")

        print("\n  [Verified Static Findings Detail]:")
        for i, vf in enumerate(verified_findings, 1):
            print(f"    {i}. {vf.get('statement')} (Evidence: {vf.get('evidence_ids')}, Type: {vf.get('finding_type')})")

        print("\n  [Potential / Uncertain Findings Detail]:")
        for i, uf in enumerate(uncertain_findings, 1):
            print(f"    {i}. {uf.get('statement')} (Evidence: {uf.get('evidence_ids')}, Conf: {uf.get('confidence')})")

        assert chat_data.get("status") in ("COMPLETED", "SUCCESS"), "Chat response status was not COMPLETED"
        assert thread_id is not None, "Thread ID was not generated"

        # Assert tool coverage
        tools_executed = {t.get("tool") for t in tool_trace}
        assert "graph_rag_retrieve" in tools_executed, "Expected graph_rag_retrieve in tool trace"
        assert "cgg_entity_lookup" in tools_executed, "Expected cgg_entity_lookup in tool trace"
        assert "cgg_direct_neighbors" in tools_executed, "Expected cgg_direct_neighbors in tool trace"
        assert "cgg_relationship_evidence" in tools_executed, "Expected cgg_relationship_evidence in tool trace"
        assert "cgg_unresolved_calls" in tools_executed, "Expected cgg_unresolved_calls in tool trace"

        # Assert Issue 1 invariant: E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5 is NOT in verified_findings
        verified_ev_ids = [ev for vf in verified_findings for ev in vf.get("evidence_ids", [])]
        uncertain_ev_ids = [ev for uf in uncertain_findings for ev in uf.get("evidence_ids", [])]

        assert not any("3ae13403" in ev for ev in verified_ev_ids), (
            "Invariant Violation: E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5 was present in verified_findings!"
        )
        assert any("3ae13403" in ev for ev in uncertain_ev_ids), (
            "Expected E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5 to be retained in uncertain_findings"
        )

        # Assert Issue 2 invariant: E-ba14eed9-79ff-51a9-b677-7d2711056d7a is in verified_findings
        assert any("ba14eed9" in ev for ev in verified_ev_ids), (
            "Expected verified CALLS relationship evidence E-ba14eed9-79ff-51a9-b677-7d2711056d7a in verified_findings"
        )

        # Verify findings citation validity
        for vf in verified_findings:
            assert vf.get("finding_type") == "verified_static"
            assert vf.get("confidence") == 1.0
            for ev in vf.get("evidence_ids", []):
                assert ev.startswith("E-") or "::" in ev, f"Invalid evidence ID format: {ev}"

        for uf in uncertain_findings:
            assert uf.get("finding_type") == "potential_uncertain"
            assert uf.get("confidence") == 0.3, f"Expected 0.3 confidence for uncertain finding, got {uf.get('confidence')}"

        print("  -> Multi-Tool Workflow and Grounding Validation PASSED")

        # Step 5: Verify Thread History Persistence
        print("\n[Step 5] Checking Persistent Thread History and Continuation...")
        thread_url = f"/api/v1/repos/{target_repo_id}/snapshots/{target_commit_sha}/assistant/threads/{thread_id}"
        hist_resp = client.get(thread_url, headers=headers)
        assert hist_resp.status_code == 200, f"Failed to get thread history: {hist_resp.status_code} {hist_resp.text}"
        messages = hist_resp.json().get("messages", [])
        print(f"  Total Messages in Thread: {len(messages)}")
        roles = [m.get("role") for m in messages]
        print(f"  Roles: {roles}")
        assert "user" in roles and "assistant" in roles, "Expected both user and assistant messages in thread history"
        print("  -> Thread History Persistence PASSED")

        # Step 6: Verify Thread Listing
        print("\n[Step 6] Listing Snapshot Assistant Threads...")
        threads_url = f"/api/v1/repos/{target_repo_id}/snapshots/{target_commit_sha}/assistant/threads"
        list_resp = client.get(threads_url, headers=headers)
        assert list_resp.status_code == 200, f"Failed to list threads: {list_resp.status_code} {list_resp.text}"
        threads_json = list_resp.json()
        threads_list = threads_json if isinstance(threads_json, list) else threads_json.get("threads", [])
        matching_threads = [t for t in threads_list if t.get("thread_id") == thread_id]
        assert len(matching_threads) > 0, "Current thread not found in snapshot thread listing"
        print(f"  Successfully listed {len(threads_list)} thread(s) for snapshot.")
        print("  -> Thread Listing PASSED")

        # Step 7: Security Boundary & Snapshot Isolation
        print("\n[Step 7] Testing Security Boundaries & Snapshot Isolation...")
        # A. Mismatched / Unknown Repo
        bad_url = f"/api/v1/repos/nonexistent_repo_id/snapshots/{target_commit_sha}/assistant/chat"
        bad_resp = client.post(bad_url, json=query_payload, headers=headers)
        print(f"  Non-existent repo response status: {bad_resp.status_code}")
        assert bad_resp.status_code in (403, 404), f"Expected 403/404 for nonexistent repo, got {bad_resp.status_code}"

        # B. Unauthenticated Access
        unauth_resp = client.post(chat_url, json=query_payload)
        print(f"  Unauthenticated request response status: {unauth_resp.status_code}")
        assert unauth_resp.status_code == 401, f"Expected 401 for unauthenticated request, got {unauth_resp.status_code}"
        print("  -> Security Boundaries PASSED")

    print("\n" + "=" * 80)
    print("ALL PHASE 5 LIVE DOCKER INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)
    return True

if __name__ == "__main__":
    try:
        success = run_test()
        sys.exit(0 if success else 1)
    except Exception as exc:
        print(f"\n[FAIL] Phase 5 Live Integration Test failed: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
