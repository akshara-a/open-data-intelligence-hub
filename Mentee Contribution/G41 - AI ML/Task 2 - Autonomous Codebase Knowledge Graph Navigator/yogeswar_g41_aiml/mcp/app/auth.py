import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
import jwt
from fastapi import Header, HTTPException, status

KEY_SEARCH_PATHS = [
    Path("/run/secrets"),
    Path("./secrets"),
    Path("../secrets"),
    Path(__file__).resolve().parent.parent.parent / "secrets",
]


def find_secret_file(filename: str) -> Optional[Path]:
    for base in KEY_SEARCH_PATHS:
        p1 = base / filename
        if p1.is_file():
            return p1
        p2 = base / f"{filename}.pem"
        if p2.is_file():
            return p2
    return None


def load_internal_service_public_key() -> str:
    path = find_secret_file("internal_service_pubkey")
    if not path:
        raise RuntimeError("Internal service public key file not found in secrets directory")
    return path.read_text(encoding="utf-8")


def verify_internal_service_token(token: str) -> Dict[str, Any]:
    """
    Verifies the RS256 internal service token from X-Internal-Service-Auth header.
    Validates signature, audience ('cgg_mcp_service'), and expiration.
    """
    pub_key_pem = load_internal_service_public_key()
    try:
        payload = jwt.decode(
            token,
            pub_key_pem,
            algorithms=["RS256"],
            audience="cgg_mcp_service",
            issuer="autonomous_kg_navigator",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Internal service token has expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid internal service token: {str(e)}",
        )


def get_internal_service_claims(
    x_internal_service_auth: Optional[str] = Header(None, alias="X-Internal-Service-Auth"),
) -> Dict[str, Any]:
    if not x_internal_service_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Internal-Service-Auth header",
        )
    token = x_internal_service_auth.strip()
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    return verify_internal_service_token(token)


def enforce_scope(claims: Dict[str, Any], repo_id: Optional[str] = None, commit_sha: Optional[str] = None):
    """
    Scope Enforcement per Section 6.2 / AC-3.4:
    Derives authorized repo_id and commit_sha exclusively from verified token claims.
    If requested repo_id or commit_sha does not match, rejects with HTTP 403 SCOPE_MISMATCH.
    """
    auth_repo = claims.get("authorized_repo_id")
    auth_commit = claims.get("authorized_commit_sha")

    if repo_id and repo_id != auth_repo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"SCOPE_MISMATCH: Requested repo_id '{repo_id}' does not match token scope '{auth_repo}'",
        )

    if commit_sha and commit_sha != auth_commit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"SCOPE_MISMATCH: Requested commit_sha '{commit_sha}' does not match token scope '{auth_commit}'",
        )
