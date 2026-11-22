"""
Phase 7.3: Comprehensive Secure Multi-User RBAC and Reviewer Access Test Suite

Validates:
1. Admin full permissions (user management, repo management, ingest, report deletion)
2. Reviewer read-only permissions on assigned repositories
3. Viewer read-only restrictions
4. Cross-repository access denial (403 Forbidden on unassigned repos)
5. Unauthorized repository creation denial (403 Forbidden for non-admins)
6. Unauthorized repository deletion denial (403 Forbidden for non-admins)
7. Unauthorized ingestion trigger denial (403 Forbidden for non-admins)
8. Unauthorized user management and role escalation denial
9. Admin user lifecycle (create, list, activate/deactivate, role update, password reset)
10. Repository membership management by admin (assign and revoke)
11. Report deletion permissions restricted to admin
12. Assistant thread cancellation ownership (owner or admin only)
13. Repository listing isolation (GET /api/v1/repos filters for non-admins)
14. Inactive user enforcement (login rejected, refresh rejected, active requests rejected)
15. Self-deactivation and self-demotion prevention for admin
"""
import uuid
import datetime
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.database import init_db, get_db_connection, hash_password
from backend.app.main import app
from backend.app.auth import create_access_token

client = TestClient(app)

TEST_REPO_A = "test_rbac_repo_a"
TEST_REPO_B = "test_rbac_repo_b"
TEST_COMMIT = "c0ffee1234567890abcdef1234567890abcdef12"

ADMIN_USER = "rbac_admin"
ADMIN_PASS = "admin_secure_123"

REVIEWER_USER = "rbac_reviewer"
REVIEWER_PASS = "reviewer_secure_123"

VIEWER_USER = "rbac_viewer"
VIEWER_PASS = "viewer_secure_123"

UNASSIGNED_USER = "rbac_unassigned"
UNASSIGNED_PASS = "unassigned_123"


@pytest.fixture(scope="module", autouse=True)
def setup_rbac_test_data():
    """Setup test repositories, users, and memberships."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create two isolated test repositories
        for repo_id, name in [(TEST_REPO_A, "RBAC Repo A"), (TEST_REPO_B, "RBAC Repo B")]:
            cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (repo_id,))
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO repositories (repo_id, name, git_url, default_branch, status)
                    VALUES (?, ?, ?, 'main', 'ACTIVE')
                    """,
                    (repo_id, name, f"https://github.com/example/{repo_id}.git"),
                )

        # Helper to create/reset user
        def ensure_user(username, password, role, is_active=1):
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                uid = row["user_id"]
                cursor.execute(
                    "UPDATE users SET password_hash = ?, role = ?, is_active = ? WHERE user_id = ?",
                    (hash_password(password), role, is_active, uid),
                )
            else:
                uid = f"usr_{uuid.uuid4().hex[:10]}"
                cursor.execute(
                    "INSERT INTO users (user_id, username, password_hash, role, is_active) VALUES (?, ?, ?, ?, ?)",
                    (uid, username, hash_password(password), role, is_active),
                )
            return uid

        admin_id = ensure_user(ADMIN_USER, ADMIN_PASS, "admin", 1)
        reviewer_id = ensure_user(REVIEWER_USER, REVIEWER_PASS, "reviewer", 1)
        viewer_id = ensure_user(VIEWER_USER, VIEWER_PASS, "viewer", 1)
        unassigned_id = ensure_user(UNASSIGNED_USER, UNASSIGNED_PASS, "viewer", 1)

        # Clear existing test memberships
        cursor.execute("DELETE FROM repo_memberships WHERE user_id IN (?, ?, ?, ?)",
                       (admin_id, reviewer_id, viewer_id, unassigned_id))

        # Grant Reviewer and Viewer access to REPO_A ONLY
        cursor.execute(
            "INSERT INTO repo_memberships (id, user_id, repo_id, role) VALUES (?, ?, ?, ?)",
            (f"mem_{uuid.uuid4().hex[:8]}", reviewer_id, TEST_REPO_A, "reviewer"),
        )
        cursor.execute(
            "INSERT INTO repo_memberships (id, user_id, repo_id, role) VALUES (?, ?, ?, ?)",
            (f"mem_{uuid.uuid4().hex[:8]}", viewer_id, TEST_REPO_A, "viewer"),
        )
        # UNASSIGNED_USER has NO repo memberships

        conn.commit()


def get_token(username: str, password: str) -> str:
    """Helper to log in and get access token."""
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, f"Login failed for {username}: {resp.text}"
    return resp.json()["access_token"]


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# 1. Repository Listing Isolation
# ============================================================================

def test_repository_listing_isolation():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)
    unassigned_token = get_token(UNASSIGNED_USER, UNASSIGNED_PASS)

    # Admin sees all repositories
    admin_resp = client.get("/api/v1/repos", headers=auth_header(admin_token))
    assert admin_resp.status_code == 200
    admin_repo_ids = [r["repo_id"] for r in admin_resp.json()]
    assert TEST_REPO_A in admin_repo_ids
    assert TEST_REPO_B in admin_repo_ids

    # Reviewer sees ONLY assigned repo (TEST_REPO_A)
    rev_resp = client.get("/api/v1/repos", headers=auth_header(rev_token))
    assert rev_resp.status_code == 200
    rev_repo_ids = [r["repo_id"] for r in rev_resp.json()]
    assert TEST_REPO_A in rev_repo_ids
    assert TEST_REPO_B not in rev_repo_ids

    # Unassigned user sees 0 repositories
    unassigned_resp = client.get("/api/v1/repos", headers=auth_header(unassigned_token))
    assert unassigned_resp.status_code == 200
    assert len(unassigned_resp.json()) == 0


# ============================================================================
# 2. Privileged Actions Restricted to Admin
# ============================================================================

def test_repository_creation_restricted_to_admin():
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # Reviewer attempted creation -> 403 Forbidden
    resp = client.post(
        "/api/v1/repos",
        headers=auth_header(rev_token),
        json={"name": "Illegal Repo", "git_url": "https://github.com/example/illegal.git"},
    )
    assert resp.status_code == 403
    assert "Administrative privileges required" in resp.json()["detail"]

    # Admin creation -> 201 Created
    unique_name = f"Admin Created {uuid.uuid4().hex[:6]}"
    admin_resp = client.post(
        "/api/v1/repos",
        headers=auth_header(admin_token),
        json={"name": unique_name, "git_url": "https://github.com/example/valid.git"},
    )
    assert admin_resp.status_code == 201
    created_id = admin_resp.json()["repo_id"]

    # Reviewer attempted deletion -> 403 Forbidden
    del_resp = client.delete(f"/api/v1/repos/{created_id}", headers=auth_header(rev_token))
    assert del_resp.status_code == 403

    # Admin deletion -> 200 OK
    admin_del = client.delete(f"/api/v1/repos/{created_id}", headers=auth_header(admin_token))
    assert admin_del.status_code == 200


def test_ingestion_restricted_to_admin():
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # Reviewer attempted ingest -> 403 Forbidden
    resp = client.post(
        f"/api/v1/repos/{TEST_REPO_A}/ingest",
        headers=auth_header(rev_token),
        json={"commit_sha": TEST_COMMIT},
    )
    assert resp.status_code == 403
    assert "Administrative privileges required" in resp.json()["detail"]

    # Admin ingest -> 200 OK
    admin_resp = client.post(
        f"/api/v1/repos/{TEST_REPO_A}/ingest",
        headers=auth_header(admin_token),
        json={"commit_sha": TEST_COMMIT},
    )
    assert admin_resp.status_code == 200
    assert admin_resp.json()["status"] == "PENDING"


# ============================================================================
# 3. Cross-Repository Access Denial
# ============================================================================

def test_cross_repository_access_denial():
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)

    # Reviewer accessing assigned TEST_REPO_A snapshots -> 200 OK
    resp_a = client.get(f"/api/v1/repos/{TEST_REPO_A}/snapshots", headers=auth_header(rev_token))
    assert resp_a.status_code == 200

    # Reviewer accessing unassigned TEST_REPO_B snapshots -> 403 Forbidden
    resp_b = client.get(f"/api/v1/repos/{TEST_REPO_B}/snapshots", headers=auth_header(rev_token))
    assert resp_b.status_code == 403
    assert "Access denied: user is not a member of this repository" in resp_b.json()["detail"]


# ============================================================================
# 4. User Management Endpoints (Admin Only)
# ============================================================================

def test_user_management_restricted_to_admin():
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)

    # Reviewer cannot list users
    assert client.get("/api/v1/users", headers=auth_header(rev_token)).status_code == 403

    # Reviewer cannot create users
    assert client.post(
        "/api/v1/users",
        headers=auth_header(rev_token),
        json={"username": "hacker", "password": "password123", "role": "admin"},
    ).status_code == 403

    # Reviewer cannot update status or roles
    assert client.put(
        "/api/v1/users/some_id/status",
        headers=auth_header(rev_token),
        json={"is_active": False},
    ).status_code == 403

    assert client.put(
        "/api/v1/users/some_id/role",
        headers=auth_header(rev_token),
        json={"role": "admin"},
    ).status_code == 403


def test_admin_user_lifecycle():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    new_username = f"user_{uuid.uuid4().hex[:8]}"
    new_password = "TemporaryPassword123!"

    # 1. Admin creates new reviewer user
    create_resp = client.post(
        "/api/v1/users",
        headers=auth_header(admin_token),
        json={"username": new_username, "password": new_password, "role": "reviewer"},
    )
    assert create_resp.status_code == 201
    created_user = create_resp.json()
    assert created_user["username"] == new_username
    assert created_user["role"] == "reviewer"
    assert created_user["is_active"] is True
    target_uid = created_user["user_id"]

    # 2. Created user can log in
    user_token = get_token(new_username, new_password)
    assert user_token is not None

    # 3. Admin lists users and sees new user (without password hash)
    list_resp = client.get("/api/v1/users", headers=auth_header(admin_token))
    assert list_resp.status_code == 200
    user_names = [u["username"] for u in list_resp.json()]
    assert new_username in user_names
    # Verify password hash is never exposed
    for u in list_resp.json():
        assert "password" not in u
        assert "password_hash" not in u

    # 4. Admin updates role to viewer
    role_resp = client.put(
        f"/api/v1/users/{target_uid}/role",
        headers=auth_header(admin_token),
        json={"role": "viewer"},
    )
    assert role_resp.status_code == 200

    # 5. Admin resets password
    new_secret_pass = "BrandNewSecretPassword99!"
    pwd_resp = client.post(
        f"/api/v1/users/{target_uid}/password",
        headers=auth_header(admin_token),
        json={"new_password": new_secret_pass},
    )
    assert pwd_resp.status_code == 200

    # Old password fails, new password succeeds
    fail_login = client.post("/api/v1/auth/login", json={"username": new_username, "password": new_password})
    assert fail_login.status_code == 401
    succ_login = client.post("/api/v1/auth/login", json={"username": new_username, "password": new_secret_pass})
    assert succ_login.status_code == 200

    # 6. Admin deactivates user
    deact_resp = client.put(
        f"/api/v1/users/{target_uid}/status",
        headers=auth_header(admin_token),
        json={"is_active": False},
    )
    assert deact_resp.status_code == 200

    # Deactivated user cannot log in
    deact_login = client.post("/api/v1/auth/login", json={"username": new_username, "password": new_secret_pass})
    assert deact_login.status_code == 403
    assert "Account is deactivated" in deact_login.json()["detail"]

    # 7. Admin reactivates user
    react_resp = client.put(
        f"/api/v1/users/{target_uid}/status",
        headers=auth_header(admin_token),
        json={"is_active": True},
    )
    assert react_resp.status_code == 200
    react_login = client.post("/api/v1/auth/login", json={"username": new_username, "password": new_secret_pass})
    assert react_login.status_code == 200


def test_invalid_role_assignment_rejected():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # Attempt to create user with invalid role
    resp = client.post(
        "/api/v1/users",
        headers=auth_header(admin_token),
        json={"username": f"bad_role_{uuid.uuid4().hex[:6]}", "password": "password123", "role": "superadmin"},
    )
    assert resp.status_code == 400
    assert "Invalid role" in resp.json()["detail"]


def test_admin_cannot_deactivate_or_demote_self():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # Retrieve admin's own user_id
    users_resp = client.get("/api/v1/users", headers=auth_header(admin_token))
    admin_entry = next(u for u in users_resp.json() if u["username"] == ADMIN_USER)
    admin_uid = admin_entry["user_id"]

    # Deactivating self -> 400 Bad Request
    deact_resp = client.put(
        f"/api/v1/users/{admin_uid}/status",
        headers=auth_header(admin_token),
        json={"is_active": False},
    )
    assert deact_resp.status_code == 400
    assert "Cannot deactivate your own administrative account" in deact_resp.json()["detail"]

    # Demoting self -> 400 Bad Request
    demote_resp = client.put(
        f"/api/v1/users/{admin_uid}/role",
        headers=auth_header(admin_token),
        json={"role": "viewer"},
    )
    assert demote_resp.status_code == 400
    assert "Cannot demote your own administrative account" in demote_resp.json()["detail"]


# ============================================================================
# 5. Repository Membership Management Endpoints (Admin Only)
# ============================================================================

def test_repo_membership_management():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)

    # Non-admin cannot manage memberships
    assert client.get(f"/api/v1/repos/{TEST_REPO_A}/members", headers=auth_header(rev_token)).status_code == 403
    assert client.post(
        f"/api/v1/repos/{TEST_REPO_A}/members",
        headers=auth_header(rev_token),
        json={"user_id": "usr_test", "role": "reviewer"},
    ).status_code == 403

    # Admin lists memberships for TEST_REPO_A
    list_mem = client.get(f"/api/v1/repos/{TEST_REPO_A}/members", headers=auth_header(admin_token))
    assert list_mem.status_code == 200
    member_usernames = [m["username"] for m in list_mem.json()]
    assert REVIEWER_USER in member_usernames
    assert VIEWER_USER in member_usernames

    # Admin grants UNASSIGNED_USER reviewer membership to TEST_REPO_B
    users_resp = client.get("/api/v1/users", headers=auth_header(admin_token))
    unassigned_uid = next(u["user_id"] for u in users_resp.json() if u["username"] == UNASSIGNED_USER)

    grant_resp = client.post(
        f"/api/v1/repos/{TEST_REPO_B}/members",
        headers=auth_header(admin_token),
        json={"user_id": unassigned_uid, "role": "reviewer"},
    )
    assert grant_resp.status_code == 200

    # UNASSIGNED_USER now has access to TEST_REPO_B
    unassigned_token = get_token(UNASSIGNED_USER, UNASSIGNED_PASS)
    snap_resp = client.get(f"/api/v1/repos/{TEST_REPO_B}/snapshots", headers=auth_header(unassigned_token))
    assert snap_resp.status_code == 200

    # Admin revokes membership from TEST_REPO_B
    revoke_resp = client.delete(
        f"/api/v1/repos/{TEST_REPO_B}/members/{unassigned_uid}",
        headers=auth_header(admin_token),
    )
    assert revoke_resp.status_code == 200

    # Access is now denied (403 Forbidden)
    snap_denied = client.get(f"/api/v1/repos/{TEST_REPO_B}/snapshots", headers=auth_header(unassigned_token))
    assert snap_denied.status_code == 403


# ============================================================================
# 6. Report Deletion & Thread Cancellation Permissions
# ============================================================================

def test_report_deletion_restricted_to_admin():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)

    # Seed a test report in SQLite
    report_id = f"rpt_test_{uuid.uuid4().hex[:8]}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reports (report_id, query_id, repo_id, commit_sha, title, query_text, markdown_body)
            VALUES (?, 'qry_test', ?, ?, 'Test Architecture Report', 'Overview', '# Architecture Overview')
            """,
            (report_id, TEST_REPO_A, TEST_COMMIT),
        )
        conn.commit()

    # Reviewer can view report
    view_resp = client.get(
        f"/api/v1/repos/{TEST_REPO_A}/snapshots/{TEST_COMMIT}/reports/{report_id}",
        headers=auth_header(rev_token),
    )
    assert view_resp.status_code == 200

    # Reviewer attempted deletion -> 403 Forbidden
    del_rev = client.delete(
        f"/api/v1/repos/{TEST_REPO_A}/snapshots/{TEST_COMMIT}/reports/{report_id}",
        headers=auth_header(rev_token),
    )
    assert del_rev.status_code == 403
    assert "Administrative privileges required" in del_rev.json()["detail"]

    # Admin deletion -> 200 OK
    del_admin = client.delete(
        f"/api/v1/repos/{TEST_REPO_A}/snapshots/{TEST_COMMIT}/reports/{report_id}",
        headers=auth_header(admin_token),
    )
    assert del_admin.status_code == 200


def test_assistant_thread_cancellation_ownership():
    rev_token = get_token(REVIEWER_USER, REVIEWER_PASS)
    viewer_token = get_token(VIEWER_USER, VIEWER_PASS)
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # Find reviewer user_id
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (REVIEWER_USER,))
        rev_uid = cursor.fetchone()["user_id"]

        thread_id = f"th_{uuid.uuid4().hex[:8]}"
        cursor.execute(
            """
            INSERT INTO assistant_threads (thread_id, user_id, repo_id, commit_sha, title, status)
            VALUES (?, ?, ?, ?, 'Reviewer Architecture Thread', 'ACTIVE')
            """,
            (thread_id, rev_uid, TEST_REPO_A, TEST_COMMIT),
        )
        conn.commit()

    # Another user (Viewer) tries to cancel Reviewer's thread -> 403 Forbidden
    cancel_by_viewer = client.post(
        f"/api/v1/repos/{TEST_REPO_A}/snapshots/{TEST_COMMIT}/assistant/threads/{thread_id}/cancel",
        headers=auth_header(viewer_token),
    )
    assert cancel_by_viewer.status_code == 403
    assert "Cannot cancel another user's assistant thread" in cancel_by_viewer.json()["detail"]

    # Thread owner (Reviewer) can cancel own thread -> 200 OK
    cancel_by_owner = client.post(
        f"/api/v1/repos/{TEST_REPO_A}/snapshots/{TEST_COMMIT}/assistant/threads/{thread_id}/cancel",
        headers=auth_header(rev_token),
    )
    assert cancel_by_owner.status_code == 200
    assert cancel_by_owner.json()["status"] == "CANCELLED"


# ============================================================================
# 7. Inactive User Immediate Invalidation & Token Rejection
# ============================================================================

def test_deactivated_user_immediate_token_rejection():
    admin_token = get_token(ADMIN_USER, ADMIN_PASS)

    # 1. Create a temporary user
    temp_user = f"temp_deact_{uuid.uuid4().hex[:6]}"
    temp_pass = "TempPass123!"
    create_resp = client.post(
        "/api/v1/users",
        headers=auth_header(admin_token),
        json={"username": temp_user, "password": temp_pass, "role": "reviewer"},
    )
    assert create_resp.status_code == 201
    temp_uid = create_resp.json()["user_id"]

    # 2. User logs in and gets an access token
    login_resp = client.post("/api/v1/auth/login", json={"username": temp_user, "password": temp_pass})
    assert login_resp.status_code == 200
    valid_access_token = login_resp.json()["access_token"]
    refresh_cookie = login_resp.cookies.get("refresh_token")

    # Access is working with this token
    assert client.get("/api/v1/repos", headers=auth_header(valid_access_token)).status_code == 200

    # 3. Admin deactivates user
    deact_resp = client.put(
        f"/api/v1/users/{temp_uid}/status",
        headers=auth_header(admin_token),
        json={"is_active": False},
    )
    assert deact_resp.status_code == 200

    # 4. Immediate rejection: Even with unexpired access token, DB check rejects with 403 Forbidden
    imm_resp = client.get("/api/v1/repos", headers=auth_header(valid_access_token))
    assert imm_resp.status_code == 403
    assert "Account is deactivated" in imm_resp.json()["detail"]

    # 5. Token refresh is also rejected with 403 Forbidden
    client.cookies.set("refresh_token", refresh_cookie)
    ref_resp = client.post("/api/v1/auth/refresh")
    assert ref_resp.status_code == 403
    assert "Account is deactivated" in ref_resp.json()["detail"]
