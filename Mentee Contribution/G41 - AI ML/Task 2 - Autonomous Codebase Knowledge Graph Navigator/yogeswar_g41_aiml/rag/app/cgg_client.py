import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
import jwt

KEY_SEARCH_PATHS = [
    Path("/run/secrets"),
    Path("./secrets"),
    Path("../secrets"),
    Path(__file__).resolve().parent.parent.parent / "secrets",
]

MCP_SERVICE_URL = os.getenv("MCP_SERVICE_URL", "http://mcp:8000")


def find_secret_file(filename: str) -> Optional[Path]:
    for base in KEY_SEARCH_PATHS:
        p1 = base / filename
        if p1.is_file():
            return p1
        p2 = base / f"{filename}.pem"
        if p2.is_file():
            return p2
    return None


def load_internal_service_private_key() -> str:
    path = find_secret_file("internal_service_key")
    if not path:
        raise RuntimeError("Internal service private key file not found in secrets directory")
    return path.read_text(encoding="utf-8")


def create_internal_service_token(repo_id: str, commit_sha: str, sub: str = "rag_service") -> str:
    priv_key_pem = load_internal_service_private_key()
    now = int(time.time())
    payload = {
        "sub": sub,
        "authorized_repo_id": repo_id,
        "authorized_commit_sha": commit_sha,
        "aud": "cgg_mcp_service",
        "iss": "autonomous_kg_navigator",
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(payload, priv_key_pem, algorithm="RS256")


class CGGClient:
    """
    Client interface for querying the Controlled Graph Gateway (CGG) per Section 6 & 10.
    Direct database connection to Neo4j is strictly disallowed.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or MCP_SERVICE_URL).rstrip("/")

    def _post(self, path: str, repo_id: str, commit_sha: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        token = create_internal_service_token(repo_id, commit_sha)
        headers = {
            "Content-Type": "application/json",
            "X-Internal-Service-Auth": token,
        }
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=json_data, headers=headers)
            if resp.status_code >= 400:
                raise RuntimeError(f"CGG RPC {path} returned HTTP {resp.status_code}: {resp.text}")
            return resp.json()

    def _get(self, path: str, repo_id: str, commit_sha: str, params: Dict[str, Any]) -> Dict[str, Any]:
        token = create_internal_service_token(repo_id, commit_sha)
        headers = {
            "X-Internal-Service-Auth": token,
        }
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, params=params, headers=headers)
            if resp.status_code >= 400:
                raise RuntimeError(f"CGG RPC {path} returned HTTP {resp.status_code}: {resp.text}")
            return resp.json()

    def lookup_entities(self, repo_id: str, commit_sha: str, name: Optional[str] = None, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        res = self._post("/api/v1/cgg/entity_lookup", repo_id, commit_sha, {
            "name": name,
            "file_path": file_path,
            "repo_id": repo_id,
            "commit_sha": commit_sha,
        })
        return res.get("entities", [])

    def get_entity_details(self, repo_id: str, commit_sha: str, entity_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = self._post("/api/v1/cgg/entity_details", repo_id, commit_sha, {
                "entity_id": entity_id,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            })
            return res.get("entity")
        except Exception:
            return None

    def get_direct_neighbors(self, repo_id: str, commit_sha: str, entity_id: str) -> Dict[str, Any]:
        try:
            res = self._post("/api/v1/cgg/direct_neighbors", repo_id, commit_sha, {
                "entity_id": entity_id,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            })
            return res
        except Exception:
            return {"outgoing_dependencies": [], "incoming_dependents": []}

    def multi_hop_traversal(self, repo_id: str, commit_sha: str, start_entity_id: str, max_depth: int = 2, direction: str = "downstream") -> List[Dict[str, Any]]:
        try:
            res = self._post("/api/v1/cgg/multi_hop_dependencies", repo_id, commit_sha, {
                "start_entity_id": start_entity_id,
                "max_depth": max_depth,
                "direction": direction,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            })
            return res.get("traversal_results", [])
        except Exception:
            return []

    def get_unresolved_calls(
        self,
        repo_id: str,
        commit_sha: str,
        source_entity_id: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        try:
            payload: Dict[str, Any] = {
                "source_entity_id": source_entity_id,
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            }
            if file_path:
                payload["file_path"] = file_path
            res = self._post("/api/v1/cgg/unresolved_calls", repo_id, commit_sha, payload)
            return res.get("unresolved_calls", [])
        except Exception:
            return []

    def get_evidence(self, repo_id: str, commit_sha: str, evidence_id: str) -> Optional[Dict[str, Any]]:
        try:
            res = self._get(f"/api/v1/tools/evidence/{evidence_id}", repo_id, commit_sha, {
                "repo_id": repo_id,
                "commit_sha": commit_sha,
            })
            return res.get("evidence")
        except Exception:
            return None


# Global singleton
_cgg_client: Optional[CGGClient] = None


def get_cgg_client() -> CGGClient:
    global _cgg_client
    if _cgg_client is None:
        _cgg_client = CGGClient()
    return _cgg_client
