import os
import sys
import time
import json
import ssl
import shutil
import tempfile
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Disable SSL verification for self-signed development certs
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://localhost"


def api_request(method: str, path: str, token: str = None, body: dict = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ssl_ctx) as resp:
            resp_body = resp.read().decode("utf-8")
            return json.loads(resp_body) if resp_body else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"API {method} {path} returned HTTP {e.code}: {err_msg}")


def main():
    print("=" * 70)
    print("PHASE 3: LIVE DOCKER INTEGRATION TEST")
    print("Controlled Graph Gateway (CGG) & MCP Integration")
    print("=" * 70)

    # 1. Authenticate with backend over HTTPS
    print("\n[1/10] Authenticating as administrator via Nginx HTTPS...")
    admin_pwd_file = Path("secrets/admin.password")
    if not admin_pwd_file.exists():
        raise RuntimeError("secrets/admin.password not found")
    admin_pwd = admin_pwd_file.read_text(encoding="utf-8").strip()

    login_resp = api_request("POST", "/api/v1/auth/login", body={"username": "admin", "password": admin_pwd})
    token = login_resp.get("access_token")
    assert token, "Failed to retrieve access token"
    print(f"Authenticated successfully. Token type: {login_resp.get('token_type')}")

    # 2. Create temporary repository & commit
    temp_dir = Path(tempfile.mkdtemp(prefix="phase3_repo_"))
    print(f"\n[2/10] Initializing local Git test repository at {temp_dir}...")
    calc_py = temp_dir / "calculator.py"
    calc_py.write_text(
        """def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b
""",
        encoding="utf-8",
    )

    app_py = temp_dir / "app.py"
    app_py.write_text(
        """from calculator import add

class AppService:
    def execute(self, x: int, y: int) -> int:
        result = add(x, y)
        self.dynamic_dispatch(result)
        return result
""",
        encoding="utf-8",
    )

    subprocess.run(["git", "init", "-b", "main"], cwd=str(temp_dir), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Phase3Tester"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "config", "user.email", "phase3@example.com"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "add", "."], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "commit", "-m", "Phase 3 test commit"], cwd=str(temp_dir), check=True)

    commit_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(temp_dir), check=True, capture_output=True, text=True).stdout.strip()
    print(f"Created commit: {commit_sha}")

    # Copy to ingestion container
    container_repo_path = "/app/git_storage/phase3_repo"
    subprocess.run(["docker", "exec", "autonomous_codebase_knowledge_graph_navigator-ingestion-1", "rm", "-rf", container_repo_path], check=True)
    subprocess.run(["docker", "cp", str(temp_dir), f"autonomous_codebase_knowledge_graph_navigator-ingestion-1:{container_repo_path}"], check=True)

    # 3. Register repo and trigger ingestion
    print("\n[3/10] Submitting ingestion job via Backend API...")
    repo_resp = api_request("POST", "/api/v1/repos", token=token, body={
        "name": "Phase 3 CGG Test Repo",
        "git_url": container_repo_path,
        "default_branch": "main",
    })
    repo_id = repo_resp["repo_id"]
    print(f"Registered repo_id: {repo_id}")

    job_resp = api_request("POST", f"/api/v1/repos/{repo_id}/ingest", token=token, body={"commit_sha": commit_sha})
    job_id = job_resp["job_id"]
    print(f"Ingestion job enqueued: {job_id}")

    # Poll until completed
    for _ in range(30):
        time.sleep(1)
        st = api_request("GET", f"/api/v1/jobs/{job_id}", token=token)
        if st["status"] == "COMPLETED":
            print(f"Ingestion worker finished successfully: {st['status']}")
            break
        elif st["status"] == "FAILED":
            raise RuntimeError(f"Ingestion job failed: {st.get('log_output')}")
    else:
        raise TimeoutError("Ingestion job timed out")

    # 4. Test Operation 8 & 1: Graph Statistics & Snapshot Info
    print("\n[4/10] Testing Operation 8 & 1: Graph Statistics & Snapshot Metadata...")
    stats = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/statistics", token=token)
    print("Graph Statistics returned:", json.dumps(stats, indent=2))
    assert stats["total_entities"] > 0, "Expected entities to be recorded"
    assert stats["total_relationships"] > 0, "Expected relationships to be recorded"
    assert stats["total_evidence"] > 0, "Expected evidence to be recorded"

    # 5. Test Operation 2: Entity Lookup
    print("\n[5/10] Testing Operation 2: Entity Lookup by name...")
    entities_resp = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities?name=add", token=token)
    entities = entities_resp.get("entities", [])
    assert len(entities) >= 1, "Entity 'add' not found in lookup"
    add_fn = entities[0]
    add_entity_id = add_fn["entity_id"]
    print(f"Found entity 'add': {add_entity_id} ({add_fn['file_path']}:{add_fn['line_start']}-{add_fn['line_end']})")

    # 6. Test Operation 3: Entity Details & Source Provenance
    print("\n[6/10] Testing Operation 3: Entity Details & Declaration Provenance...")
    import urllib.parse
    encoded_id = urllib.parse.quote(add_entity_id, safe="")
    details_resp = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{encoded_id}", token=token)
    ent_details = details_resp["entity"]
    print("Entity Details:", json.dumps(ent_details, indent=2))
    assert ent_details["name"] == "add"
    assert ent_details.get("declaration_evidence_id"), "Missing declaration evidence ID"

    # 7. Test Operation 4: Direct Dependencies & Dependents
    print("\n[7/10] Testing Operation 4: Direct Dependencies and Dependents...")
    neighbors = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{encoded_id}/neighbors", token=token)
    print("Direct Neighbors:", json.dumps(neighbors, indent=2))
    assert len(neighbors.get("incoming_dependents", [])) >= 1, "Expected incoming caller dependency for 'add'"

    # 8. Test Operation 5: Bounded Multi-Hop Traversal
    print("\n[8/10] Testing Operation 5: Bounded Multi-Hop Traversal (impact_downstream_1hop)...")
    query_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/query",
        token=token,
        body={
            "operation": "impact_downstream_1hop",
            "parameters": {"start_entity_id": add_entity_id},
        },
    )
    print("Multi-Hop Query Result:", json.dumps(query_resp, indent=2))
    assert query_resp["record_count"] >= 1, "Expected downstream callers in 1-hop traversal"

    # 9. Test Operation 6 & 7: Evidence Retrieval & Unresolved Calls
    print("\n[9/10] Testing Operation 6 & 7: Evidence Retrieval and Unresolved Calls...")
    ev_id = ent_details["declaration_evidence_id"]
    ev_resp = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/evidence/{ev_id}", token=token)
    print(f"Evidence retrieved ({ev_id}):", json.dumps(ev_resp, indent=2))
    assert ev_resp["evidence"]["evidence_id"] == ev_id

    unresolved_resp = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/unresolved_calls", token=token)
    print("Unresolved Calls:", json.dumps(unresolved_resp, indent=2))
    assert unresolved_resp["count"] >= 1, "Expected unresolved dynamic call for dynamic_dispatch"
    assert unresolved_resp["unresolved_calls"][0]["invoked_symbol_name"] == "dynamic_dispatch"

    # 10. Test Commit-Pinned Source Code Extraction (repo.read_file) & Security Rejection
    print("\n[10/10] Testing repo.read_file and Security Guards...")
    file_resp = api_request("GET", f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/file?file_path=calculator.py&start_line=1&end_line=3", token=token)
    print("Git source extraction:", json.dumps(file_resp, indent=2))
    assert "def add" in file_resp["content"]
    assert file_resp["start_line"] == 1
    assert file_resp["end_line"] == 3

    # Security Test: Mutation Rejection
    print("Verifying mutation rejection on CGG...")
    try:
        api_request(
            "POST",
            f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/query",
            token=token,
            body={
                "operation": "invalid_mutation_op",
                "parameters": {},
            },
        )
        assert False, "Expected rejection of unapproved operation"
    except RuntimeError as e:
        print(f"Correctly rejected unapproved operation: {e}")

    print("\n" + "=" * 70)
    print("PHASE 3 LIVE DOCKER INTEGRATION TEST PASSED SUCCESSFULLY!")
    print("=" * 70)

    # Cleanup temp directory
    shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
