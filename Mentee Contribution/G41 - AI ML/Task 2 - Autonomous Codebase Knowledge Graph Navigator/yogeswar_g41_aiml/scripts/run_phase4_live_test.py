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
    print("PHASE 4: LIVE DOCKER INTEGRATION TEST")
    print("GraphRAG Semantic & Structural Retrieval Engine")
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

    # 2. Check Service Health
    print("\n[2/10] Verifying service health across all backend dependencies...")
    health_resp = api_request("GET", "/api/v1/health", token=token)
    print(f"Backend Health Status: {health_resp.get('status')} ({health_resp.get('database')})")
    assert health_resp.get("status") == "healthy"

    rag_health = api_request("GET", "/api/v1/rag/health", token=token)
    print(f"RAG Service Health: {rag_health.get('status')} ({rag_health.get('service')}, backend: {rag_health.get('backend')}, model: {rag_health.get('model_version')}, status: {rag_health.get('model_status')})")
    assert rag_health.get("status") == "healthy", f"RAG service not healthy: {rag_health}"
    assert rag_health.get("backend") == "sentence_transformers", f"Expected sentence_transformers backend, got {rag_health.get('backend')}"
    assert rag_health.get("model_status") == "active_transformer", f"Expected active_transformer, got {rag_health.get('model_status')}"
    assert rag_health.get("model_version") == "sentence-transformers/all-mpnet-base-v2@9a32259"
    assert rag_health.get("fallback_mode") is False

    # 3. Create temporary repository & commit
    temp_dir = Path(tempfile.mkdtemp(prefix="phase4_repo_"))
    print(f"\n[3/10] Initializing local Git test repository at {temp_dir}...")

    auth_py = temp_dir / "auth_service.py"
    auth_py.write_text(
        '"""Authentication and Token Verification Service"""\n'
        'from db_pool import DatabasePool\n\n'
        'def verify_credentials(username: str, token_hash: str) -> bool:\n'
        '    """Verifies user login credentials and queries the database pool."""\n'
        '    pool = DatabasePool("sqlite:///app.db")\n'
        '    result = pool.query(f"SELECT id FROM users WHERE user={username}")\n'
        '    return bool(result)\n\n'
        'def issue_jwt_token(username: str) -> str:\n'
        '    """Issues RS256 token."""\n'
        '    return f"token_{username}_secure"\n',
        encoding="utf-8",
    )

    db_py = temp_dir / "db_pool.py"
    db_py.write_text(
        '"""Database Connection Pool and Query Execution"""\n\n'
        'class DatabasePool:\n'
        '    def __init__(self, connection_uri: str):\n'
        '        self.uri = connection_uri\n\n'
        '    def query(self, sql_query: str):\n'
        '        """Executes a SQL query against the connection pool."""\n'
        '        return [{"id": 1, "status": "active"}]\n',
        encoding="utf-8",
    )

    dyn_py = temp_dir / "dynamic_router.py"
    dyn_py.write_text(
        '"""Dynamic Request Router"""\n\n'
        'def dispatch_dynamic_route(route_name: str):\n'
        '    """Deliberate unresolvable dynamic invocation site."""\n'
        '    handler = eval(f"route_{route_name}")\n'
        '    return handler()\n',
        encoding="utf-8",
    )

    subprocess.run(["git", "init", "-b", "main"], cwd=str(temp_dir), check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Phase4 Tester"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "config", "user.email", "phase4@antigravity.test"], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "add", "."], cwd=str(temp_dir), check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit for Phase 4 GraphRAG test"], cwd=str(temp_dir), check=True)

    commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(temp_dir)).decode().strip()
    print(f"Created commit {commit_sha[:8]} with auth_service.py, db_pool.py, dynamic_router.py")

    # Copy to ingestion container
    container_repo_path = "/app/git_storage/phase4_repo"
    subprocess.run(["docker", "exec", "autonomous_codebase_knowledge_graph_navigator-ingestion-1", "rm", "-rf", container_repo_path], check=True)
    subprocess.run(["docker", "cp", str(temp_dir), f"autonomous_codebase_knowledge_graph_navigator-ingestion-1:{container_repo_path}"], check=True)

    # 4. Ingest repository into Phase 2 pipeline
    print("\n[4/10] Ingesting repository into persistent Git storage and Phase 2 graph...")
    repo_payload = {
        "name": f"phase4-test-{int(time.time())}",
        "git_url": container_repo_path,
        "default_branch": "main",
    }
    repo_resp = api_request("POST", "/api/v1/repos", token=token, body=repo_payload)
    repo_id = repo_resp.get("repo_id")
    print(f"Repository registered: repo_id={repo_id}")

    job_resp = api_request("POST", f"/api/v1/repos/{repo_id}/ingest", token=token, body={"commit_sha": commit_sha})
    job_id = job_resp.get("job_id")
    print(f"Ingestion job enqueued: job_id={job_id}")

    # Wait for Phase 2 ingestion job to complete
    print("Waiting for ingestion worker to process snapshot...")
    for _ in range(30):
        time.sleep(1)
        status_resp = api_request("GET", f"/api/v1/jobs/{job_id}", token=token)
        job_status = status_resp.get("status")
        if job_status in ("COMPLETED", "FAILED"):
            break

    print(f"Ingestion job completed with status: {job_status}")
    assert job_status == "COMPLETED", f"Ingestion failed: {status_resp}"

    # 5. Index Snapshot into GraphRAG
    print("\n[5/10] Indexing snapshot into GraphRAG engine...")
    index_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/index",
        token=token,
        body={"force_reindex": True},
    )
    print(f"Indexing completed: {index_resp}")
    assert index_resp.get("status") in ("completed", "indexed")
    assert index_resp.get("total_files") >= 3
    assert index_resp.get("total_chunks") >= 3
    assert index_resp.get("new_chunks_embedded") >= 3

    # 6. Test Cache Reuse across re-indexing
    print("\n[6/10] Testing persistent chunk embedding cache reuse...")
    reindex_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/index",
        token=token,
        body={"force_reindex": False},
    )
    print(f"Re-indexing result: {reindex_resp}")
    assert reindex_resp.get("cached_chunks_reused") == index_resp.get("total_chunks"), (
        f"Expected all chunks reused, got {reindex_resp.get('cached_chunks_reused')} / {index_resp.get('total_chunks')}"
    )
    assert reindex_resp.get("new_chunks_embedded") == 0, (
        f"Expected 0 newly embedded chunks, got {reindex_resp.get('new_chunks_embedded')}"
    )
    print("Cache reuse verified: 100% cache hit rate achieved!")

    # 7. Semantic & Hybrid Retrieval Test
    print("\n[7/10] Executing Hybrid GraphRAG Retrieval query...")
    query_req = {
        "query": "verify user credentials and access token with database pool",
        "top_k": 5,
        "include_graph": True,
        "max_graph_hops": 2,
    }
    retrieval_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/retrieve",
        token=token,
        body=query_req,
    )
    results = retrieval_resp.get("results", [])
    print(f"Retrieved {len(results)} items (model: {retrieval_resp.get('model_version')} [{retrieval_resp.get('model_status')}])")
    assert len(results) > 0, "No retrieval results returned"

    top_result = results[0]
    print(f"Top result: {top_result.get('file_path')}:{top_result.get('line_start')}-{top_result.get('line_end')}")
    print(f" - Semantic score: {top_result.get('semantic_similarity'):.4f}")
    print(f" - Graph score:    {top_result.get('graph_relevance'):.4f}")
    print(f" - Combined score: {top_result.get('combined_score'):.4f}")
    print(f" - Relationship:   {top_result.get('relationship_classification')}")
    print(f" - Explanation:    {top_result.get('ranking_explanation', {}).get('explanation')}")

    assert "auth_service.py" in top_result.get("file_path")
    assert top_result.get("line_start") >= 1
    assert top_result.get("line_end") >= top_result.get("line_start")
    assert top_result.get("provenance_status") == "evidence_grounded"

    # 8. Unresolved Call Classification Test
    print("\n[8/10] Verifying dynamic unresolved call retrieval & classification...")
    dyn_req = {
        "query": "dispatch dynamic route handler eval",
        "top_k": 5,
        "include_graph": True,
    }
    dyn_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/retrieve",
        token=token,
        body=dyn_req,
    )
    dyn_results = dyn_resp.get("results", [])
    assert len(dyn_results) > 0, "Expected dynamic route results"
    dyn_top = next((r for r in dyn_results if "dynamic_router.py" in r.get("file_path")), dyn_results[0])
    print(f"Dynamic query top result: {dyn_top.get('file_path')}:{dyn_top.get('line_start')}-{dyn_top.get('line_end')}")
    print(f" - Relationship classification: {dyn_top.get('relationship_classification')}")
    print(f" - Explanation: {dyn_top.get('ranking_explanation', {}).get('explanation')}")
    assert "dynamic_router.py" in dyn_top.get("file_path")
    assert dyn_top.get("relationship_classification") == "potential_uncertain", (
        f"Expected 'potential_uncertain', got '{dyn_top.get('relationship_classification')}'"
    )
    assert dyn_top.get("relationship_classification") != "verified_static", (
        "Regression detected: dynamic unresolved call cannot be returned as verified_static!"
    )
    assert dyn_top.get("ranking_explanation", {}).get("relationship_classification") == "potential_uncertain"
    assert dyn_top.get("ranking_explanation", {}).get("relationship_type") == "UNRESOLVED_CALL"

    # 9. Strict Snapshot Isolation Test
    print("\n[9/10] Testing strict repository and snapshot isolation...")
    fake_sha = "0123456789abcdef0123456789abcdef01234567"
    isolated_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{fake_sha}/rag/retrieve",
        token=token,
        body={"query": "verify credentials", "top_k": 5},
    )
    print(f"Isolated query for non-existent commit returned {len(isolated_resp.get('results', []))} results")
    assert len(isolated_resp.get("results", [])) == 0, "Isolation breach: results returned for non-existent commit"

    # 10. Container Restart Persistence Verification
    print("\n[10/10] Verifying persistence across RAG container restart...")
    print("Restarting 'rag' Docker container...")
    subprocess.run(["docker-compose", "restart", "rag"], check=True, stdout=subprocess.DEVNULL)

    # Wait for RAG service to come back up
    print("Waiting for RAG container to regain healthy state...")
    time.sleep(3)
    for _ in range(15):
        try:
            h = api_request("GET", "/api/v1/rag/health", token=token)
            if h.get("status") == "healthy":
                print("RAG container restarted and confirmed healthy.")
                break
        except Exception:
            pass
        time.sleep(1)

    # Query again without indexing
    post_restart_resp = api_request(
        "POST",
        f"/api/v1/repos/{repo_id}/snapshots/{commit_sha}/rag/retrieve",
        token=token,
        body=query_req,
    )
    post_results = post_restart_resp.get("results", [])
    print(f"Post-restart retrieval returned {len(post_results)} items")
    assert len(post_results) == len(results), f"Expected {len(results)} items, got {len(post_results)}"
    assert post_results[0].get("chunk_id") == top_result.get("chunk_id"), "Top retrieved chunk changed after restart"
    print("Persistence verified: Identical retrieval results preserved across container restart!")

    # Cleanup temp dir
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n" + "=" * 70)
    print("SUCCESS: Phase 4 GraphRAG Live Docker Integration Test PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
