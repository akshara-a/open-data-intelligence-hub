import os
import time
import uuid
import hashlib
import datetime
from pathlib import Path
from typing import Optional, Tuple
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException, status
from .database import get_db_connection

ACCESS_TOKEN_LIFETIME_SECONDS = 15 * 60  # 15 minutes per Section 14.1
REFRESH_TOKEN_LIFETIME_SECONDS = 7 * 24 * 60 * 60  # 7 days per Section 14.1

KEY_SEARCH_PATHS = [
    Path("/run/secrets"),
    Path("./secrets"),
    Path("../secrets"),
    Path(__file__).parent.parent.parent / "secrets",
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


def load_private_key() -> str:
    path = find_secret_file("jwt_private_key")
    if not path:
        raise RuntimeError("JWT private key file not found in secrets directory")
    return path.read_text(encoding="utf-8")


def load_public_key() -> str:
    path = find_secret_file("jwt_public_key")
    if not path:
        raise RuntimeError("JWT public key file not found in secrets directory")
    return path.read_text(encoding="utf-8")


def get_jwks() -> dict:
    pub_key_pem = load_public_key()
    pub_key = serialization.load_pem_public_key(pub_key_pem.encode("utf-8"))
    if not isinstance(pub_key, rsa.RSAPublicKey):
        raise ValueError("Invalid RSA public key")

    public_numbers = pub_key.public_numbers()
    def int_to_base64url(val: int) -> str:
        b = val.to_bytes((val.bit_length() + 7) // 8, byteorder="big")
        import base64
        return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")

    return {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "alg": "RS256",
                "kid": "cgg-nav-key-1",
                "n": int_to_base64url(public_numbers.n),
                "e": int_to_base64url(public_numbers.e),
            }
        ]
    }


VALID_ROLES = {"admin", "reviewer", "viewer"}


def create_access_token(user_id: str, username: str, role: str) -> str:
    if role not in VALID_ROLES:
        role = "viewer"  # Default-deny / safe fallback
    private_key_pem = load_private_key()
    now = int(time.time())
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "iss": "autonomous_kg_navigator",
        "aud": "kg_navigator_clients",
        "iat": now,
        "exp": now + ACCESS_TOKEN_LIFETIME_SECONDS,
    }
    return jwt.encode(payload, private_key_pem, algorithm="RS256", headers={"kid": "cgg-nav-key-1"})


def verify_access_token(token: str) -> dict:
    public_key_pem = load_public_key()
    try:
        payload = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            audience="kg_navigator_clients",
            issuer="autonomous_kg_navigator",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def mint_refresh_token(user_id: str, family_id: Optional[str] = None) -> Tuple[str, str]:
    raw_token = str(uuid.uuid4())
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    token_id = f"rtk_{uuid.uuid4().hex[:16]}"
    fam_id = family_id or f"fam_{uuid.uuid4().hex[:16]}"
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=REFRESH_TOKEN_LIFETIME_SECONDS)

    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO refresh_tokens (token_id, family_id, user_id, token_hash, is_revoked, expires_at)
            VALUES (?, ?, ?, ?, 0, ?)
            """,
            (token_id, fam_id, user_id, token_hash, expires_at.isoformat())
        )
        conn.commit()

    return raw_token, fam_id


def rotate_refresh_token(raw_refresh_token: str) -> Tuple[str, str, str]:
    """
    Implements Refresh Token Rotation & Reuse Invalidation (AC-1.3).
    Returns (new_access_token, new_raw_refresh_token, user_id).
    """
    token_hash = hashlib.sha256(raw_refresh_token.encode("utf-8")).hexdigest()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT rt.token_id, rt.family_id, rt.user_id, rt.is_revoked, rt.expires_at, u.username, u.role, u.is_active
            FROM refresh_tokens rt
            JOIN users u ON rt.user_id = u.user_id
            WHERE rt.token_hash = ?
            """,
            (token_hash,)
        )
        record = cursor.fetchone()

        if not record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        token_id = record["token_id"]
        family_id = record["family_id"]
        user_id = record["user_id"]
        is_revoked = record["is_revoked"]
        expires_at_str = record["expires_at"]
        username = record["username"]
        role = record["role"]
        is_active = record["is_active"] if "is_active" in record.keys() else 1

        # Check account activation status
        if is_active != 1:
            conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE family_id = ?", (family_id,))
            conn.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        # AC-1.3: Token reuse detection!
        if is_revoked == 1:
            # Immediate invalidation of the ENTIRE token family
            conn.execute(
                "UPDATE refresh_tokens SET is_revoked = 1 WHERE family_id = ?",
                (family_id,)
            )
            conn.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Security violation: Re-used refresh token detected. Entire token family has been invalidated.",
            )

        # Check expiration
        expires_at = datetime.datetime.fromisoformat(expires_at_str)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=datetime.timezone.utc)
        if datetime.datetime.now(datetime.timezone.utc) > expires_at:
            conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE token_id = ?", (token_id,))
            conn.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )

        # Normal rotation: Revoke current token and issue replacement within same family
        conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE token_id = ?", (token_id,))
        conn.commit()

        new_raw_refresh, _ = mint_refresh_token(user_id=user_id, family_id=family_id)
        new_access_token = create_access_token(user_id=user_id, username=username, role=role)

        return new_access_token, new_raw_refresh, user_id


def revoke_token_family(raw_refresh_token: str):
    token_hash = hashlib.sha256(raw_refresh_token.encode("utf-8")).hexdigest()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT family_id FROM refresh_tokens WHERE token_hash = ?", (token_hash,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE family_id = ?", (row["family_id"],))
            conn.commit()


def revoke_user_tokens(user_id: str):
    with get_db_connection() as conn:
        conn.execute("UPDATE refresh_tokens SET is_revoked = 1 WHERE user_id = ?", (user_id,))
        conn.commit()


def load_internal_service_private_key() -> str:
    path = find_secret_file("internal_service_key")
    if not path:
        raise RuntimeError("Internal service private key file not found in secrets directory")
    return path.read_text(encoding="utf-8")


def create_internal_service_token(
    repo_id: str,
    commit_sha: str,
    sub: str = "backend_service",
    expires_in: int = 3600,
) -> str:
    """
    Mints an RS256-signed internal service token per Section 6.2 for CGG/MCP communication.
    Bound to authorized_repo_id and authorized_commit_sha.
    """
    private_key_pem = load_internal_service_private_key()
    now = int(time.time())
    payload = {
        "sub": sub,
        "authorized_repo_id": repo_id,
        "authorized_commit_sha": commit_sha,
        "aud": "cgg_mcp_service",
        "iss": "autonomous_kg_navigator",
        "iat": now,
        "exp": now + expires_in,
    }
    return jwt.encode(payload, private_key_pem, algorithm="RS256")
