"""
Phase 6.4 - Comprehensive Production Authentication & Public Exposure Remediation Test Suite
Validates:
1. Finding M-1 Resolution: Authorization on GET /api/v1/repos/{repo_id}/snapshots
   - Rejects unauthenticated requests (HTTP 401)
   - Allows authenticated authorized members (HTTP 200)
   - Enforces multi-tenant isolation (HTTP 403 for unauthorized users)
   - Returns HTTP 404 for nonexistent repos
2. Finding L-1 Resolution: Public Health Endpoint Sanitization
   - GET /api/v1/rag/health no longer exposes internal SQLite filesystem paths (/app/data/app_state.db)
   - GET /api/v1/assistant/health returns minimal operational status
3. Full Authentication Lifecycle
   - Login sets HttpOnly refresh cookie & mints short-lived access token
   - Token refresh rotates refresh token securely
   - Revoked / reused refresh tokens are rejected
   - Logout clears cookie and invalidates token family
   - Expired access tokens are rejected
4. Frontend Artifacts & Finding L-2 Resolution
   - ProtectedRoute and LoginPage in App.tsx
   - AuthContext session restoration and storage handling
   - Demo Benchmark Dataset banners in RepoExplorerPage and KnowledgeGraphPage
"""
import os
import json
import uuid
import time
import datetime
import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.database import init_db, get_db_connection, hash_password
from backend.app.main import app
from backend.app.auth import (
    create_access_token,
    load_private_key,
    verify_access_token,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_REPO_ID = "repo_demo_sample"
TEST_COMMIT_SHA = "c0ffee1234567890abcdef1234567890abcdef12"
TEST_AUTH_USER = "auth_test_user"
TEST_AUTH_PASS = "test_pass_123"


@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    """Ensure database and test repository/users exist."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Ensure test repository exists
        cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (TEST_REPO_ID,))
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO repositories (repo_id, name, git_url, default_branch, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    TEST_REPO_ID,
                    "Demo Sample Repository",
                    "https://github.com/example/demo.git",
                    "main",
                    "ACTIVE",
                    datetime.datetime.now(datetime.timezone.utc).isoformat(),
                ),
            )

        # Create isolated auth test user for login/refresh tests
        cursor.execute("DELETE FROM users WHERE username = ?", (TEST_AUTH_USER,))
        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash, role) VALUES (?, ?, ?, ?)",
            (f"usr_{uuid.uuid4().hex[:8]}", TEST_AUTH_USER, hash_password(TEST_AUTH_PASS), "admin"),
        )

        # Create viewer user who is NOT a member of TEST_REPO_ID
        cursor.execute("SELECT user_id FROM users WHERE username = 'restricted_viewer'")
        restricted = cursor.fetchone()
        if not restricted:
            restricted_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO users (user_id, username, password_hash, role) VALUES (?, ?, ?, ?)",
                (restricted_id, "restricted_viewer", hash_password("viewer123"), "viewer"),
            )

        # Create member user who IS a member of TEST_REPO_ID
        cursor.execute("SELECT user_id FROM users WHERE username = 'repo_member'")
        member = cursor.fetchone()
        if not member:
            member_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO users (user_id, username, password_hash, role) VALUES (?, ?, ?, ?)",
                (member_id, "repo_member", hash_password("member123"), "viewer"),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO repo_memberships (id, user_id, repo_id, role) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), member_id, TEST_REPO_ID, "viewer"),
            )
        conn.commit()


@pytest.fixture
def client():
    return TestClient(app)


# ============================================================================
# 1. Finding M-1 Resolution: Secure Snapshot Endpoint
# ============================================================================

def test_snapshots_unauthenticated_rejection(client):
    """AC-M1.1: GET /api/v1/repos/{repo_id}/snapshots MUST reject requests without credentials with HTTP 401."""
    resp = client.get(f"/api/v1/repos/{TEST_REPO_ID}/snapshots")
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
    assert "Missing or invalid Authorization header" in resp.json().get("detail", "")


def test_snapshots_authenticated_admin_success(client):
    """AC-M1.2: Authenticated administrator can list repository snapshots."""
    token = create_access_token(user_id="admin-id", role="admin", username="admin")
    resp = client.get(
        f"/api/v1/repos/{TEST_REPO_ID}/snapshots",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["repo_id"] == TEST_REPO_ID
    assert "commit_sha" in data[0]


def test_snapshots_authenticated_member_success(client):
    """AC-M1.3: Authenticated repo member can access snapshots."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = 'repo_member'")
        user_id = cursor.fetchone()["user_id"]

    token = create_access_token(user_id=user_id, role="viewer", username="repo_member")
    resp = client.get(
        f"/api/v1/repos/{TEST_REPO_ID}/snapshots",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_snapshots_unauthorized_cross_tenant_rejection(client):
    """AC-M1.4: Cross-tenant isolation - user with no repo membership receives HTTP 403."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = 'restricted_viewer'")
        user_id = cursor.fetchone()["user_id"]

    token = create_access_token(user_id=user_id, role="viewer", username="restricted_viewer")
    resp = client.get(
        f"/api/v1/repos/{TEST_REPO_ID}/snapshots",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403, f"Expected 403 Forbidden, got {resp.status_code}"
    assert "not a member of this repository" in resp.json().get("detail", "")


def test_snapshots_nonexistent_repo_404(client):
    """AC-M1.5: Nonexistent repo returns HTTP 404."""
    token = create_access_token(user_id="admin-id", role="admin", username="admin")
    resp = client.get(
        "/api/v1/repos/nonexistent_repo_id_9999/snapshots",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


# ============================================================================
# 2. Finding L-1 Resolution: Sanitized Health Endpoints
# ============================================================================

def test_sanitized_rag_health(client):
    """AC-L1.1: GET /api/v1/rag/health MUST NOT leak internal filesystem paths or database files."""
    mock_rag_response = {
        "status": "healthy",
        "service": "graph_rag",
        "database_path": "/app/data/app_state.db",
        "internal_host": "rag:8000",
        "model_status": "active_transformer",
        "timestamp": "2026-11-14T17:00:00Z",
    }
    with patch("backend.app.main.forward_to_rag", new_callable=AsyncMock) as mock_forward:
        mock_forward.return_value = mock_rag_response
        resp = client.get("/api/v1/rag/health")
        assert resp.status_code == 200
        data = resp.json()
        # Verify internal paths are sanitized
        assert "database_path" not in data, "database_path MUST NOT be present in sanitized health"
        assert "internal_host" not in data, "internal_host MUST NOT be present"
        assert "/app/data" not in json.dumps(data), "Internal filesystem path MUST NOT be disclosed"
        # Verify essential operational fields are preserved
        assert data.get("status") == "healthy"
        assert data.get("service") == "graph_rag"
        assert data.get("model_status") == "active_transformer"


def test_sanitized_assistant_health(client):
    """AC-L1.2: GET /api/v1/assistant/health returns minimal operational status without leaks."""
    resp = client.get("/api/v1/assistant/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data.get("service") == "assistant"
    assert "database_path" not in data
    assert "/app/data" not in json.dumps(data)


# ============================================================================
# 3. Complete Authentication Lifecycle & Security
# ============================================================================

def test_auth_login_sets_refresh_cookie_and_returns_access_token(client):
    """AC-AUTH.1: Successful login sets HttpOnly cookie and provides access token."""
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": TEST_AUTH_USER, "password": TEST_AUTH_PASS},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"
    assert data["expires_in"] == 900

    # Verify refresh token cookie
    cookies = resp.cookies
    assert "refresh_token" in cookies
    # Inspect Set-Cookie header for security attributes
    set_cookie = resp.headers.get("set-cookie", "")
    assert "HttpOnly" in set_cookie or "httponly" in set_cookie.lower()
    assert "Path=/api/v1/auth" in set_cookie or "path=/api/v1/auth" in set_cookie.lower()


def test_auth_refresh_rotation_and_token_minting(client):
    """AC-AUTH.2: Token refresh rotates the refresh token and mints fresh access token."""
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": TEST_AUTH_USER, "password": TEST_AUTH_PASS},
    )
    assert login_resp.status_code == 200
    initial_refresh_cookie = login_resp.cookies.get("refresh_token")
    assert initial_refresh_cookie is not None

    # Call refresh endpoint with cookie
    client.cookies.set("refresh_token", initial_refresh_cookie)
    refresh_resp = client.post("/api/v1/auth/refresh")
    assert refresh_resp.status_code == 200
    new_data = refresh_resp.json()
    assert "access_token" in new_data
    rotated_refresh_cookie = refresh_resp.cookies.get("refresh_token")
    assert rotated_refresh_cookie is not None
    assert rotated_refresh_cookie != initial_refresh_cookie, "Refresh token MUST be rotated"


def test_auth_refresh_reuse_detection(client):
    """AC-AUTH.3: Replaying a superseded refresh token revokes token family and fails with 401."""
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": TEST_AUTH_USER, "password": TEST_AUTH_PASS},
    )
    stale_token = login_resp.cookies.get("refresh_token")

    # Rotate once
    client.cookies.set("refresh_token", stale_token)
    refresh_resp1 = client.post("/api/v1/auth/refresh")
    assert refresh_resp1.status_code == 200

    # Replay stale token -> reuse detection
    client.cookies.set("refresh_token", stale_token)
    refresh_resp2 = client.post("/api/v1/auth/refresh")
    assert refresh_resp2.status_code == 401


def test_auth_logout_clears_cookie_and_revokes(client):
    """AC-AUTH.4: Logout revokes refresh token and clears cookie."""
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": TEST_AUTH_USER, "password": TEST_AUTH_PASS},
    )
    refresh_cookie = login_resp.cookies.get("refresh_token")

    client.cookies.set("refresh_token", refresh_cookie)
    logout_resp = client.post("/api/v1/auth/logout")
    assert logout_resp.status_code == 200
    assert "logged out" in logout_resp.json().get("message", "").lower()

    # Further refresh with that cookie must fail
    client.cookies.set("refresh_token", refresh_cookie)
    follow_up_refresh = client.post("/api/v1/auth/refresh")
    assert follow_up_refresh.status_code == 401


def test_expired_access_token_rejected(client):
    """AC-AUTH.5: Expired access token is rejected with HTTP 401."""
    import jwt
    private_key_pem = load_private_key()
    now = int(time.time())
    payload = {
        "sub": "user-expired",
        "user_id": "user-expired",
        "role": "admin",
        "iat": now - 3600,
        "exp": now - 1800,
        "iss": "autonomous_kg_navigator",
        "aud": "kg_navigator_clients",
    }
    expired_token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers={"kid": "cgg-nav-key-1"})

    resp = client.get(
        f"/api/v1/repos/{TEST_REPO_ID}/snapshots",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert resp.status_code == 401
    assert "expired" in resp.json().get("detail", "").lower()


# ============================================================================
# 4. Frontend Security & Finding L-2 Resolution
# ============================================================================

def test_frontend_protected_routes_specification():
    """AC-FE.1: App.tsx wraps all dashboard routes with ProtectedRoute and mounts LoginPage."""
    app_file = ROOT_DIR / "frontend" / "src" / "App.tsx"
    assert app_file.is_file()
    content = app_file.read_text(encoding="utf-8")

    assert "ProtectedRoute" in content
    assert "LoginPage" in content
    assert 'path="/login"' in content
    assert "useAuth" in content
    assert "logout" in content
    assert "Active Snapshot:" in content


def test_frontend_auth_context_specification():
    """AC-FE.2: AuthContext manages access tokens in memory and storage with auto-refresh."""
    auth_ctx = ROOT_DIR / "frontend" / "src" / "context" / "AuthContext.tsx"
    assert auth_ctx.is_file()
    content = auth_ctx.read_text(encoding="utf-8")

    assert "AuthProvider" in content
    assert "useAuth" in content
    assert "refreshToken" in content
    assert "credentials: 'include'" in content
    assert "sessionStorage" in content
    assert "localStorage" in content
    assert "parseJwt" in content


def test_frontend_demo_dataset_banners_specification():
    """AC-L2.1: Finding L-2 - RepoExplorerPage & KnowledgeGraphPage display DEMO BENCHMARK DATASET banners."""
    repo_page = ROOT_DIR / "frontend" / "src" / "pages" / "RepoExplorerPage.tsx"
    assert repo_page.is_file()
    repo_content = repo_page.read_text(encoding="utf-8")
    assert "Demo Benchmark Dataset" in repo_content or "DEMO BENCHMARK DATASET" in repo_content

    graph_page = ROOT_DIR / "frontend" / "src" / "pages" / "KnowledgeGraphPage.tsx"
    assert graph_page.is_file()
    graph_content = graph_page.read_text(encoding="utf-8")
    assert "Demo Benchmark Dataset" in graph_content or "DEMO BENCHMARK DATASET" in graph_content
