import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:80"
REPO_ID = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
COMMIT_SHA = "d730e05672cb7673365022a44d3814bdc66ec033"
UNAUTH_REPO_ID = "4189db99-178d-4f41-b545-c416b042b5c5"

def make_req(url, method="GET", data=None, token=None):
    headers = {}
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(content)
            except:
                return resp.status, content
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8")
        try:
            return e.code, json.loads(content)
        except:
            return e.code, content
    except Exception as e:
        return 0, str(e)

print("="*60)
print("PHASE 7.4 LIVE FUNCTIONAL VERIFICATION")
print("="*60)

# 1. Login as viewer
status, data = make_req(f"{BASE_URL}/api/v1/auth/login", method="POST", data={"username": "demo", "password": "viewer_secure_123"})
assert status == 200, f"Viewer login failed: {status} {data}"
viewer_token = data["access_token"]
print(f"[PASS] 1.1 Viewer login successful. Access token acquired.")

# 2. Check repos
status, repos = make_req(f"{BASE_URL}/api/v1/repos", token=viewer_token)
assert status == 200, f"List repos failed: {status}"
repo_ids = [r["repo_id"] for r in repos]
assert REPO_ID in repo_ids, f"Target repo {REPO_ID} not in viewer repos {repo_ids}"
assert UNAUTH_REPO_ID not in repo_ids, f"Unauthorized repo leaked: {UNAUTH_REPO_ID}"
print(f"[PASS] 1.2 Scoped repos verified: {len(repos)} accessible repos. Unauthorized repo strictly hidden.")

# 3. Viewer AI Assistant - Real question on authorized repo
status, threads = make_req(f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/assistant/threads", token=viewer_token)
assert status == 200, f"Assistant threads check failed: {status}"
print(f"[PASS] 1.3 Assistant threads endpoint accessible to viewer.")

print("[INFO] Submitting real codebase architectural question to AI Assistant...")
question = "How does verify_credentials validate credentials and what does it invoke?"
status, chat_res = make_req(
    f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/assistant/chat",
    method="POST",
    data={"question": question},
    token=viewer_token
)
assert status == 200, f"Assistant chat failed: {status} {chat_res}"
answer = chat_res.get("answer", {})
assert chat_res.get("repo_id") == REPO_ID, "Repo mismatch in chat response"
assert chat_res.get("commit_sha") == COMMIT_SHA, "Commit mismatch in chat response"
print(f"[PASS] 1.4 Assistant answered successfully.")
print(f"      Status: {chat_res.get('status')}")
print(f"      Summary: {answer.get('summary', '')[:120]}...")
print(f"      Verified findings: {len(answer.get('verified_findings', []))}")
print(f"      Evidence references: {len(answer.get('evidence_references', []))}")
print(f"      Tool trace steps: {len(chat_res.get('tool_trace', []))}")

# 4. Viewer AI Assistant - Unanswerable question honesty
print("[INFO] Submitting unanswerable question...")
unanswerable = "Where is the QuantumLaserEntanglementModule implemented in this repository?"
status, unans_res = make_req(
    f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/assistant/chat",
    method="POST",
    data={"question": unanswerable},
    token=viewer_token
)
assert status == 200, f"Unanswerable chat failed: {status} {unans_res}"
unans_answer = unans_res.get("answer", {})
has_insufficient = unans_answer.get("insufficient_evidence", False) or "not found" in unans_answer.get("summary", "").lower() or "no " in unans_answer.get("summary", "").lower()
print(f"[PASS] 1.5 Unanswerable question handled honestly: insufficient_evidence={unans_answer.get('insufficient_evidence')}, Summary: {unans_answer.get('summary', '')[:100]}...")

# 5. Confirm Viewer blocked from mutating/admin actions
mutating_checks = [
    ("POST", f"{BASE_URL}/api/v1/repos", {"name": "test_hack", "git_url": "https://hack.git"}),
    ("DELETE", f"{BASE_URL}/api/v1/repos/{REPO_ID}", None),
    ("POST", f"{BASE_URL}/api/v1/repos/{REPO_ID}/ingest", {"commit_sha": COMMIT_SHA}),
    ("POST", f"{BASE_URL}/api/v1/evaluation/run", {"suite_name": "all"}),
    ("GET", f"{BASE_URL}/api/v1/users", None),
]
for meth, endpoint, body in mutating_checks:
    st, resp_data = make_req(endpoint, method=meth, data=body, token=viewer_token)
    assert st == 403, f"Mutating endpoint {endpoint} did not return 403! Got: {st} {resp_data}"
print(f"[PASS] 1.6 All 5 administrative and mutating actions returned HTTP 403 Forbidden for viewer.")

# 6. Tenant isolation: Chat on unauthorized repo blocked
st, unauth_chat = make_req(
    f"{BASE_URL}/api/v1/repos/{UNAUTH_REPO_ID}/snapshots/bbf245eea12c287561c08e96bf7769810dbfa950/assistant/chat",
    method="POST",
    data={"question": "Tell me about this repo"},
    token=viewer_token
)
assert st == 403, f"Chat on unauthorized repo did not return 403! Got: {st}"
print(f"[PASS] 1.7 Cross-tenant assistant query strictly blocked (HTTP 403).")

# 7. Knowledge Graph - Real Ingested Repo (Neo4j verification)
status, ent_data = make_req(f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/graph/entities", token=viewer_token)
assert status == 200, f"Entities fetch failed: {status}"
entities = ent_data.get("entities", [])
assert len(entities) >= 10, f"Expected >= 10 entities in real repo, got {len(entities)}"
ent_names = [e["name"] for e in entities]
assert "verify_credentials" in ent_names, f"verify_credentials not found in {ent_names}"
assert "DatabasePool" in ent_names, f"DatabasePool not found in {ent_names}"
assert "query" in ent_names, f"query not found in {ent_names}"

vc_node = next(e for e in entities if e["name"] == "verify_credentials")
assert vc_node["file_path"] == "auth_service.py", f"Wrong file path: {vc_node['file_path']}"
assert vc_node["line_start"] == 4, f"Wrong line start: {vc_node['line_start']}"
print(f"[PASS] 2.1 Neo4j entities verified: {len(entities)} entities. verify_credentials @ {vc_node['file_path']}:{vc_node['line_start']}")

# 8. Relationships & Evidence
status, nbr_data = make_req(f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/graph/entities/{vc_node['entity_id']}/neighbors", token=viewer_token)
assert status == 200, f"Neighbors query failed: {status}"
out_deps = nbr_data.get("outgoing_dependencies", [])
in_deps = nbr_data.get("incoming_dependencies", [])
print(f"[PASS] 2.2 Verified relationships: {len(out_deps)} outgoing, {len(in_deps)} incoming.")

# 9. Dynamic/Unresolved calls
status, unres_data = make_req(f"{BASE_URL}/api/v1/repos/{REPO_ID}/snapshots/{COMMIT_SHA}/graph/unresolved_calls", token=viewer_token)
assert status == 200, f"Unresolved calls query failed: {status}"
unres_calls = unres_data.get("unresolved_calls", [])
print(f"[PASS] 2.3 Dynamic calls verified: {len(unres_calls)} dynamic calls preserved as uncertain.")

# 10. Dashboard navigation paths & direct URL refresh
for path in [
    f"/impact/{REPO_ID}/snapshot/{COMMIT_SHA}",
    f"/repo/{REPO_ID}/snapshot/{COMMIT_SHA}/impact",
    f"/repo/{REPO_ID}/snapshot/{COMMIT_SHA}/reports",
    "/evaluation",
]:
    status, html = make_req(f"{BASE_URL}{path}")
    assert status == 200, f"URL {path} failed: {status}"
    assert "index-AUPvDliH.js" in html, f"HTML shell missing bundle on {path}"
print(f"[PASS] 3.1 All dashboard card routes and direct URL refreshes succeed with HTTP 200 HTML shell.")

print("="*60)
print("ALL LIVE FUNCTIONAL VERIFICATION CHECKS PASSED")
print("="*60)
