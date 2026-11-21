import httpx
from app.auth import create_internal_service_token

repo_id = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
commit_sha = "d730e05672cb7673365022a44d3814bdc66ec033"
token = create_internal_service_token(repo_id, commit_sha)
headers = {"X-Internal-Service-Auth": token, "Content-Type": "application/json"}

resp = httpx.post("http://mcp:8000/api/v1/cgg/entity_lookup", json={
    "repo_id": repo_id, "commit_sha": commit_sha, "symbol_name": ""
}, headers=headers)

for e in resp.json().get("entities", []):
    eid = e["entity_id"]
    det = httpx.post("http://mcp:8000/api/v1/cgg/entity_details", json={
        "repo_id": repo_id, "commit_sha": commit_sha, "entity_id": eid
    }, headers=headers).json().get("entity", {})
    print(f"{det.get('name')} ({det.get('entity_types')}) in {det.get('file_path')}:{det.get('line_start')}-{det.get('line_end')} -> decl_ev: {det.get('declaration_evidence_id')}")
