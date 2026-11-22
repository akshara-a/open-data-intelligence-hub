"""
Phase 7.1 - Frontend Integration & Live Repository-Aware Graph Test Suite
Validates:
1. Dynamic repository and snapshot selection architecture
2. Live Knowledge Graph API integration and snapshot-scoping
3. Switching between Repository A and Repository B replaces all graph data
4. Zero cross-repository entity and relationship leakage
5. Repository Explorer live file and code endpoint integration
6. Empty and unauthenticated error states
"""
import os
import json
import uuid
import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database import init_db, get_db_connection
from backend.app.auth import create_access_token

ROOT_DIR = Path(__file__).resolve().parent.parent

REPO_A_ID = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
COMMIT_A = "d730e05672cb7673365022a44d3814bdc66ec033"

REPO_B_ID = "07fbd7dc-1fcc-4b1f-8030-7e87b3ddd4ea"
COMMIT_B = "178ff98b0eb43540bc7986acc66b33af7bd4929c"

MOCK_ENTITIES_A = {
    "entities": [
        {
            "entity_id": f"{REPO_A_ID}::{COMMIT_A}::Function::verify_credentials",
            "name": "verify_credentials",
            "file_path": "auth_service.py",
            "entity_types": ["Function"],
        },
        {
            "entity_id": f"{REPO_A_ID}::{COMMIT_A}::Class::DatabasePool",
            "name": "DatabasePool",
            "file_path": "db_pool.py",
            "entity_types": ["Class"],
        },
    ]
}

MOCK_ENTITIES_B = {
    "entities": [
        {
            "entity_id": f"{REPO_B_ID}::{COMMIT_B}::Function::add",
            "name": "add",
            "file_path": "calculator.py",
            "entity_types": ["Function"],
        },
        {
            "entity_id": f"{REPO_B_ID}::{COMMIT_B}::Class::AppService",
            "name": "AppService",
            "file_path": "app.py",
            "entity_types": ["Class"],
        },
    ]
}


@pytest.fixture(scope="module", autouse=True)
def ensure_test_repos():
    """Ensure REPO_A_ID and REPO_B_ID exist in the active test SQLite database."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for r_id in [REPO_A_ID, REPO_B_ID]:
            cursor.execute("SELECT repo_id FROM repositories WHERE repo_id = ?", (r_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO repositories (repo_id, name, git_url) VALUES (?, ?, ?)",
                    (r_id, f"Test Repo {r_id[:8]}", f"https://github.com/example/{r_id}.git")
                )
        conn.commit()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def admin_token():
    return create_access_token(user_id="usr_admin_default", role="admin", username="admin")


# ============================================================================
# 1. Frontend Source Code Specifications
# ============================================================================

def test_frontend_dynamic_repository_selector_specification():
    """Validates that App.tsx dynamically renders repositories from SnapshotContext without hardcoded lists."""
    app_file = ROOT_DIR / "frontend" / "src" / "App.tsx"
    assert app_file.is_file()
    content = app_file.read_text(encoding="utf-8")

    assert "repositories.map" in content, "App.tsx must dynamically map repositories"
    assert "snapshots.map" in content, "App.tsx must dynamically map snapshots"
    assert "handleRepoChange" in content
    assert "handleCommitChange" in content
    assert "repo_tier1_python" not in content, "Hardcoded repo_tier1_python must be removed"
    assert "repo_tier1_typescript" not in content, "Hardcoded repo_tier1_typescript must be removed"


def test_frontend_snapshot_context_specification():
    """Validates that SnapshotContext manages async repositories, snapshots, and race condition guards."""
    ctx_file = ROOT_DIR / "frontend" / "src" / "context" / "SnapshotContext.tsx"
    assert ctx_file.is_file()
    content = ctx_file.read_text(encoding="utf-8")

    assert "refreshRepositories" in content
    assert "selectRepo" in content
    assert "authFetch" in content
    assert "/api/v1/repos" in content
    assert "snapshotReqIdRef" in content, "Race-condition guard must be present"
    assert "sessionStorage" in content


def test_frontend_knowledge_graph_live_wiring_specification():
    """Validates KnowledgeGraphPage fetches real entities, neighbors, statistics, and handles empty state."""
    kg_file = ROOT_DIR / "frontend" / "src" / "pages" / "KnowledgeGraphPage.tsx"
    assert kg_file.is_file()
    content = kg_file.read_text(encoding="utf-8")

    assert "authFetch" in content
    assert "/graph/entities" in content
    assert "/graph/statistics" in content
    assert "/neighbors" in content
    assert "CytoscapeGraphCanvas" in content
    assert "GraphFilterToolbar" in content
    assert "EvidencePopover" in content
    assert "No AST Entities in Snapshot" in content


def test_frontend_repo_explorer_live_wiring_specification():
    """Validates RepoExplorerPage fetches real file entities and content via /file endpoint."""
    explorer_file = ROOT_DIR / "frontend" / "src" / "pages" / "RepoExplorerPage.tsx"
    assert explorer_file.is_file()
    content = explorer_file.read_text(encoding="utf-8")

    assert "authFetch" in content
    assert "/graph/entities" in content
    assert "/file?file_path=" in content
    assert "VirtualFileTree" in content
    assert "EntityDetailDrawer" in content
    assert "CodeViewerModal" in content


# ============================================================================
# 2. Live API Repository Isolation & Graph Data Differentiation
# ============================================================================

def test_api_repository_list_loading(client, admin_token):
    """GET /api/v1/repos returns real persistent repositories."""
    resp = client.get("/api/v1/repos", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    repos = resp.json()
    assert isinstance(repos, list)
    assert len(repos) >= 2


def test_api_snapshot_list_for_different_repos(client, admin_token):
    """Snapshots change dynamically based on the selected repository."""
    resp_a = client.get(f"/api/v1/repos/{REPO_A_ID}/snapshots", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp_a.status_code == 200
    snaps_a = resp_a.json()
    assert len(snaps_a) >= 1
    assert snaps_a[0]["repo_id"] == REPO_A_ID

    resp_b = client.get(f"/api/v1/repos/{REPO_B_ID}/snapshots", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp_b.status_code == 200
    snaps_b = resp_b.json()
    assert len(snaps_b) >= 1
    assert snaps_b[0]["repo_id"] == REPO_B_ID


def test_api_graph_entities_strict_isolation(client, admin_token):
    """Switching Repo A -> Repo B yields completely distinct AST entities with zero cross-contamination."""
    async def mock_forward(path, repo_id, commit_sha, method="POST", json_data=None, params=None):
        if repo_id == REPO_A_ID:
            return MOCK_ENTITIES_A
        elif repo_id == REPO_B_ID:
            return MOCK_ENTITIES_B
        return {"entities": []}

    with patch("backend.app.main.forward_to_cgg", side_effect=mock_forward):
        # 1. Fetch Repo A entities
        resp_a = client.get(
            f"/api/v1/repos/{REPO_A_ID}/snapshots/{COMMIT_A}/graph/entities",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_a.status_code == 200
        ents_a = resp_a.json().get("entities", [])
        assert len(ents_a) > 0
        names_a = {e["name"] for e in ents_a}

        # 2. Fetch Repo B entities
        resp_b = client.get(
            f"/api/v1/repos/{REPO_B_ID}/snapshots/{COMMIT_B}/graph/entities",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_b.status_code == 200
        ents_b = resp_b.json().get("entities", [])
        assert len(ents_b) > 0
        names_b = {e["name"] for e in ents_b}

        # 3. Isolation assertions
        overlap = names_a.intersection(names_b)
        assert len(overlap) == 0, f"Entity overlap detected between Repo A and Repo B: {overlap}"
        assert "verify_credentials" in names_a
        assert "verify_credentials" not in names_b
        assert "add" in names_b
        assert "add" not in names_a


def test_api_file_content_strict_isolation(client, admin_token):
    """Repo Explorer /file endpoint delivers isolated source code per repository."""
    async def mock_forward_file(path, repo_id, commit_sha, method="GET", json_data=None, params=None):
        if repo_id == REPO_A_ID:
            return {"content": "def verify_credentials(): pass", "lines": ["def verify_credentials(): pass"]}
        elif repo_id == REPO_B_ID:
            return {"content": "def add(a, b): return a + b", "lines": ["def add(a, b): return a + b"]}
        return {"content": "", "lines": []}

    with patch("backend.app.main.forward_to_cgg", side_effect=mock_forward_file):
        # Repo A auth_service.py
        resp_a = client.get(
            f"/api/v1/repos/{REPO_A_ID}/snapshots/{COMMIT_A}/file",
            params={"file_path": "auth_service.py", "start_line": 1, "end_line": 50},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_a.status_code == 200
        content_a = resp_a.json().get("content", "")
        assert "verify_credentials" in content_a

        # Repo B calculator.py
        resp_b = client.get(
            f"/api/v1/repos/{REPO_B_ID}/snapshots/{COMMIT_B}/file",
            params={"file_path": "calculator.py", "start_line": 1, "end_line": 50},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp_b.status_code == 200
        content_b = resp_b.json().get("content", "")
        assert "def add(a, b)" in content_b
        assert "verify_credentials" not in content_b


def test_unauthenticated_graph_entities_rejection(client):
    """Unauthenticated access to graph entities returns HTTP 401."""
    resp = client.get(f"/api/v1/repos/{REPO_A_ID}/snapshots/{COMMIT_A}/graph/entities")
    assert resp.status_code == 401


def test_unauthorized_tenant_graph_entities_rejection(client):
    """Cross-tenant access to graph entities by non-member returns HTTP 403."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = 'restricted_viewer'")
        user_row = cursor.fetchone()
        assert user_row is not None
        user_id = user_row["user_id"]

    viewer_token = create_access_token(user_id=user_id, role="viewer", username="restricted_viewer")
    resp = client.get(
        f"/api/v1/repos/{REPO_A_ID}/snapshots/{COMMIT_A}/graph/entities",
        headers={"Authorization": f"Bearer {viewer_token}"},
    )
    assert resp.status_code == 403
