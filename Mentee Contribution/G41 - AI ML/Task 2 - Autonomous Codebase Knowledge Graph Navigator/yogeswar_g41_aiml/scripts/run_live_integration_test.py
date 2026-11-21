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

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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


def get_neo4j_password() -> str:
    path = Path("secrets/neo4j_admin.password")
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return os.getenv("NEO4J_PASSWORD", "")


def run_cypher(cypher_query: str) -> str:
    pwd = get_neo4j_password()
    cmd = [
        "docker", "exec", "autonomous_codebase_knowledge_graph_navigator-neo4j-1",
        "cypher-shell", "-u", "neo4j", "-p", pwd,
        "--format", "plain", cypher_query
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return res.stdout.strip()


def main():
    print("=" * 70)
    print("PHASE 2: LIVE DOCKER INTEGRATION TEST")
    print("=" * 70)

    # 1. Create temporary Git repository
    temp_dir = Path(tempfile.mkdtemp(prefix="live_test_repo_"))
    print(f"\n[1/7] Creating temporary local Git repository at {temp_dir}...")

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

    # Initialize Git
    subprocess.run(["git", "init", "-b", "main"], cwd=str(temp_dir), check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "LiveTester"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "config", "user.email", "livetest@example.com"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "add", "."], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "commit", "-m", "Initial test commit with resolved and unresolved calls"], cwd=str(temp_dir), check=True)

    commit_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(temp_dir), check=True, capture_output=True, text=True).stdout.strip()
    print(f"Created commit SHA: {commit_sha}")

    # Copy to Docker ingestion container git storage
    container_repo_path = "/app/git_storage/live_test_repo"
    print(f"Copying repository to container at {container_repo_path}...")
    subprocess.run(
        ["docker", "exec", "autonomous_codebase_knowledge_graph_navigator-ingestion-1", "rm", "-rf", container_repo_path],
        check=True
    )
    subprocess.run(
        ["docker", "cp", str(temp_dir), f"autonomous_codebase_knowledge_graph_navigator-ingestion-1:{container_repo_path}"],
        check=True
    )

    # 2. Authenticate via Nginx
    from backend.app.database import get_admin_password
    admin_password = get_admin_password()
    print("\n[2/7] Authenticating via HTTP API (POST /api/v1/auth/login)...")
    login_resp = api_request("POST", "/api/v1/auth/login", body={"username": "admin", "password": admin_password})
    access_token = login_resp["access_token"]
    print(f"Authenticated successfully! Token type: {login_resp['token_type']}, expires in: {login_resp['expires_in']}s")

    # 3. Create repository
    print("\n[3/7] Submitting repository via HTTP API (POST /api/v1/repos)...")
    repo_resp = api_request(
        "POST", "/api/v1/repos", token=access_token,
        body={"name": "Live Integration Test Repo", "git_url": container_repo_path, "default_branch": "main"}
    )
    repo_id = repo_resp["repo_id"]
    print(f"Repository created: repo_id = {repo_id}")

    # 4. Trigger Ingestion Job
    print(f"\n[4/7] Triggering ingestion job for commit {commit_sha} (POST /api/v1/repos/{repo_id}/ingest)...")
    ingest_resp = api_request(
        "POST", f"/api/v1/repos/{repo_id}/ingest", token=access_token,
        body={"commit_sha": commit_sha}
    )
    job_id = ingest_resp["job_id"]
    print(f"Ingestion job enqueued: job_id = {job_id}, status = {ingest_resp['status']}")

    # 5. Poll Job Status until terminal state
    print(f"Polling job status (GET /api/v1/jobs/{job_id})...")
    final_job = None
    for attempt in range(30):
        job_status = api_request("GET", f"/api/v1/jobs/{job_id}", token=access_token)
        status = job_status["status"]
        progress = job_status.get("progress", 0)
        log = job_status.get("log_output", "")
        print(f"  Attempt {attempt + 1}: status = {status}, progress = {progress}%")
        if status in ("COMPLETED", "FAILED"):
            final_job = job_status
            break
        time.sleep(2)

    if not final_job or final_job["status"] != "COMPLETED":
        print(f"FATAL: Ingestion job did not complete successfully. Status: {final_job}")
        sys.exit(1)

    print(f"Job completed successfully! Log: {final_job['log_output']}")

    # 6. Verify directly in Neo4j via Cypher-shell
    print("\n[5/7] Verifying graph data in Neo4j using cypher-shell...")

    # (a) Snapshot node
    snapshot_res = run_cypher(f"MATCH (s:Snapshot {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) RETURN s.snapshot_id AS snapshot_id;")
    print(f"Snapshot in Neo4j:\n{snapshot_res}")
    assert f"{repo_id}::{commit_sha}" in snapshot_res, "Snapshot node missing in Neo4j"

    # (b) Entities
    ent_res = run_cypher(
        f"MATCH (e:Entity {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) "
        f"RETURN labels(e) AS labels, e.name AS name, e.entity_type AS type, e.file_path AS file, e.line_start AS start, e.line_end AS end "
        f"ORDER BY e.file_path, e.line_start;"
    )
    print(f"Entities in Neo4j:\n{ent_res}")

    # (c) Verified Relationships
    rel_res = run_cypher(
        f"MATCH (s:Entity {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}})-[r]->(t:Entity {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) "
        f"RETURN s.name AS source, type(r) AS rel_type, t.name AS target;"
    )
    print(f"Relationships in Neo4j:\n{rel_res}")

    # (d) Unresolved Calls
    unres_res = run_cypher(
        f"MATCH (s:Entity {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}})-[:HAS_UNRESOLVED_CALL]->(uc:UnresolvedCall {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) "
        f"RETURN s.name AS caller, uc.invoked_symbol_name AS invoked_symbol, uc.line_range AS lines, uc.file_path AS file;"
    )
    print(f"Unresolved calls in Neo4j:\n{unres_res}")
    assert "dynamic_dispatch" in unres_res, "Unresolved call 'dynamic_dispatch' missing in Neo4j"

    # (e) Evidence nodes
    ev_res = run_cypher(
        f"MATCH (ev:Evidence {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) "
        f"RETURN ev.evidence_type AS ev_type, count(ev) AS count;"
    )
    print(f"Evidence counts in Neo4j:\n{ev_res}")

    # Count nodes and relationships before re-ingest
    count_before = run_cypher(
        f"MATCH (n {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) RETURN count(n) AS node_count;"
    )
    print(f"Node count before re-ingest: {count_before}")

    # 7. Test Idempotency: re-submit same commit
    print("\n[6/7] Testing Idempotency: re-submitting identical commit...")
    re_ingest_resp = api_request(
        "POST", f"/api/v1/repos/{repo_id}/ingest", token=access_token,
        body={"commit_sha": commit_sha}
    )
    job_id_2 = re_ingest_resp["job_id"]
    print(f"Second ingestion job enqueued: job_id = {job_id_2}")
    status_2 = None
    for attempt in range(30):
        status_2 = api_request("GET", f"/api/v1/jobs/{job_id_2}", token=access_token)
        print(f"  Attempt {attempt + 1}: status = {status_2['status']}, progress = {status_2.get('progress', 0)}%", flush=True)
        if status_2["status"] in ("COMPLETED", "FAILED"):
            break
        time.sleep(2)

    assert status_2["status"] == "COMPLETED", f"Re-ingestion failed: {status_2}"
    count_after = run_cypher(
        f"MATCH (n {{repo_id: '{repo_id}', commit_sha: '{commit_sha}'}}) RETURN count(n) AS node_count;"
    )
    print(f"Node count after re-ingest: {count_after}")
    assert count_before == count_after, f"Idempotency violation! Node count changed from {count_before} to {count_after}"
    print("Idempotency VERIFIED: node counts are identical, zero duplicates created!")

    # 8. Clean up test repository
    print(f"\n[7/7] Cleaning up test repository {repo_id} via DELETE /api/v1/repos/{repo_id}...")
    del_resp = api_request("DELETE", f"/api/v1/repos/{repo_id}", token=access_token)
    print(f"Delete response: {del_resp['message']}")

    # Wait for purge job to complete
    time.sleep(5)
    remaining_nodes = run_cypher(f"MATCH (n {{repo_id: '{repo_id}'}}) RETURN count(n) AS remaining;")
    print(f"Remaining nodes in Neo4j for {repo_id}:\n{remaining_nodes}")

    # Clean local temp
    shutil.rmtree(str(temp_dir), ignore_errors=True)
    subprocess.run(
        ["docker", "exec", "autonomous_codebase_knowledge_graph_navigator-ingestion-1", "rm", "-rf", container_repo_path],
        check=True
    )
    print("\nCleanup completed cleanly!")
    print("=" * 70)
    print("LIVE DOCKER INTEGRATION TEST: PASS")
    print("=" * 70)


if __name__ == "__main__":
    main()
