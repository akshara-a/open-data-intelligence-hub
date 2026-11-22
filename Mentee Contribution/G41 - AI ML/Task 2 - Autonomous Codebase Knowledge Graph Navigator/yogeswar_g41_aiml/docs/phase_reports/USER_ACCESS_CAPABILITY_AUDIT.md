# USER ACCESS & CAPABILITY AUDIT REPORT
**Autonomous Codebase Knowledge Graph Navigator**

**Audit Date:** November 15, 2026
**Audit Scope:** Authentication, Authorization, Role-Based Access Control (RBAC), Multi-User Support, Repository Isolation, and User Lifecycle Management
**Audit Mode:** READ-ONLY Architectural & Codebase Inspection

---

## Executive Summary

A comprehensive architectural and source code inspection of the authentication and authorization subsystems in the Autonomous Codebase Knowledge Graph Navigator was conducted.

The current implementation features a robust cryptographic authentication foundation (RS256 JWT access tokens, HttpOnly refresh cookie rotation with reuse detection, and tenant-level repository membership checks). However, **administrative user lifecycle management, granular role-based permissions (RBAC), and user-facing administration interfaces are currently incomplete or missing**.

### Summary of Key Findings

| Question | Status | Core Finding |
| :--- | :---: | :--- |
| **1. Can administrator create additional users?** | **NO** | No API endpoints, CLI tools, or UI forms exist to create or invite users. New accounts can only be provisioned via direct SQL operations on SQLite. |
| **2. Does backend support multiple users?** | **PARTIAL** | Database schema (`users`, `refresh_tokens`, `repo_memberships`, `assistant_threads`) and JWT token verification natively support multiple concurrent users, but lifecycle management is absent. |
| **3. Which roles currently exist?** | **ADMIN ONLY** | Functionally, only `"admin"` is recognized in code logic (universal bypass). Default schema strings like `"user"` and `"owner"` exist in the database, but `"reviewer"` does not exist anywhere. |
| **4. Can repository access be restricted?** | **PARTIAL** | Graph, snapshot, file, assistant, and report APIs enforce repository membership via `repo_memberships` (returning 403 Forbidden). However, `GET /api/v1/repos` returns all repos, and `POST /ingest` and `DELETE /repos` lack membership checks. |
| **5. Can a read-only reviewer access core tools?** | **YES** | If granted repository membership, a user can access Knowledge Graph, Repo Explorer, Assistant, Impact Analysis, and Reports. |
| **6. Can a reviewer be prevented from privileged actions?** | **NO** | `POST /api/v1/repos`, `DELETE /api/v1/repos/{id}`, and `POST /api/v1/repos/{id}/ingest` have no role checks. Any authenticated user can create repos, trigger ingestion, or delete repos. |
| **7. Are user-management API endpoints implemented?** | **NO** | No CRUD endpoints for users (`/api/v1/users`) or repo memberships (`/api/v1/repos/{id}/members`) exist. |
| **8. Is public self-registration enabled or disabled?** | **DISABLED** | No registration endpoint or registration UI exists. Self-registration is completely blocked. |

---

## Detailed Audit Findings

### 1. User Creation Capabilities
**Question:** Can the administrator create additional user accounts?
**Finding:** **NO (Missing Feature)**

- **Inspection of API Layer (`backend/app/main.py`):**
  - There are no endpoints for user creation (e.g., `POST /api/v1/users`, `POST /api/v1/admin/users`, or `POST /api/v1/invites`).
  - The authentication router only exposes `/api/v1/auth/login`, `/api/v1/auth/refresh`, and `/api/v1/auth/logout`.
- **Inspection of CLI Tools & Scripts (`scripts/`, `backend/scripts/`):**
  - No administrative user provisioning or user management scripts exist.
- **Inspection of Frontend UI (`frontend/src/`):**
  - `SettingsPage.tsx` displays active repository identity and token lifetime parameters; it contains no user administration panel or creation forms.
- **Current Workaround:** Additional users can only be created by manually running SQL `INSERT INTO users ...` statements directly on the SQLite database container/volume.

---

### 2. Multi-User Backend Support
**Question:** Does the backend support multiple users?
**Finding:** **PARTIALLY IMPLEMENTED (Data & Token Architecture Present; Lifecycle Management Missing)**

- **Implemented Multi-User Architectural Features:**
  - **Relational Schema (`backend/app/database.py`):**
    - `users` table: Has `user_id` PRIMARY KEY, unique `username`, `password_hash`, and `role`.
    - `refresh_tokens` table: Foreign key constraint `FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE`.
    - `repo_memberships` table: Unique `(user_id, repo_id)` pairing with cascading foreign keys.
    - `assistant_threads` table: Scoped by `user_id` and `(repo_id, commit_sha)`.
  - **Cryptographic Token Issuance (`backend/app/auth.py`):**
    - `create_access_token`: Encodes `sub: user_id`, `username`, and `role` into RS256 JWT claims.
    - `mint_refresh_token` & `rotate_refresh_token`: Cryptographically tracks token families and revocation per `user_id`.
  - **Live Verification:**
    - Live database inspection confirms multiple distinct users currently reside in the SQLite database:
      - `admin` (`usr_admin_default`, role: `admin`)
      - `restricted_viewer` (`e7a1fa6f-...`, role: `viewer`)
      - `repo_member` (`c5f2a918-...`, role: `viewer`)
      - `auth_test_user` (`usr_67b093bb`, role: `admin`)
- **Missing Features:**
  - No user provisioning, profile editing, password reset, or account deactivation flows.

---

### 3. Existing & Defined Roles
**Question:** Which roles currently exist (admin, reviewer, viewer, etc.)?
**Finding:** **ONLY "admin" HAS FUNCTIONAL LOGIC; "reviewer" DOES NOT EXIST**

- **Code Logic Role Checks (`backend/app/main.py:419`):**
  ```python
  def verify_repo_access(user: dict, repo_id: str):
      ...
      if user.get("role") == "admin":
          return  # Admin bypasses repository membership checks
      user_id = user.get("sub") or user.get("user_id")
      cursor.execute(
          "SELECT role FROM repo_memberships WHERE user_id = ? AND repo_id = ?",
          (user_id, repo_id),
      )
      if not cursor.fetchone():
          raise HTTPException(status_code=403, detail="Access denied: user is not a member of this repository")
  ```
  - **`admin`**: The only system role that alters backend authorization behavior. An `admin` user is exempt from repository membership checks and can access any repository's data.
  - **`user`**: The default fallback in the `users` schema (`role TEXT NOT NULL DEFAULT 'user'`). It has no specific elevated or restricted privileges; it is simply treated as a non-admin.
  - **`owner`**: Inserted into `repo_memberships` when a user creates a repository (`main.py:309`). However, **no backend endpoint ever evaluates whether `repo_memberships.role == 'owner'`**.
  - **`viewer`**: Appears in unit tests (`test_phase6_4_remediation.py`) and as a fallback in `AuthContext.tsx`. It has no distinct permission handling in the backend.
  - **`reviewer`**: **DOES NOT EXIST**. There is no reference to a `reviewer` role in any backend schema, database migration, API handler, or frontend component.

---

### 4. Repository Access Restriction to Selected Users
**Question:** Can repository access be restricted to selected users?
**Finding:** **PARTIALLY IMPLEMENTED (Granular at Snapshot/Graph Layer; Leaked at Repo Meta Layer)**

- **Enforced Restrictions (Access Blocked for Non-Members):**
  - If a user has `role: "viewer"` (or any non-admin role) and has **no entry** in `repo_memberships` for `repo_id`, `verify_repo_access()` blocks the following endpoints with **HTTP 403 Forbidden**:
    - `GET /api/v1/repos/{repo_id}/snapshots`
    - `POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/query`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{id}`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/entities/{id}/neighbors`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/graph/evidence/{id}`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/file`
    - `POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/chat`
    - `POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/impact/analyze`
    - `POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports`
    - `GET /api/v1/repos/{repo_id}/snapshots/{commit_sha}/reports`
- **Security Deficiencies / Missing Restrictions:**
  1. **Repository Listing Leak (`GET /api/v1/repos`):**
     - Queries `SELECT * FROM repositories` without checking `repo_memberships`.
     - Non-member users can see repository IDs, Git URLs, names, and creation timestamps for repositories they do not belong to.
  2. **Ingestion Trigger (`POST /api/v1/repos/{repo_id}/ingest`):**
     - Does **not** invoke `verify_repo_access(user, repo_id)`. Any authenticated user can trigger snapshot ingestion jobs on any repository.
  3. **Repository Deletion (`DELETE /api/v1/repos/{repo_id}`):**
     - Does **not** invoke `verify_repo_access(user, repo_id)` or check for `role == 'admin'`. Any authenticated user can mark any repository as `DELETING`.
  4. **Membership Administration:**
     - There is no API to assign or unassign users to repositories.

---

### 5. Reviewer / Read-Only Feature Access
**Question:** Can a read-only reviewer access Knowledge Graph, Repository Explorer, GraphRAG Assistant, Impact Analysis, and Technical Reports?
**Finding:** **YES, CONDITIONAL ON REPOSITORY MEMBERSHIP (No Distinct Reviewer Role)**

If a non-admin user is granted a record in `repo_memberships` for a given `repo_id`:
- **Knowledge Graph:** **YES** (`/graph/entities`, `/graph/query`, `/graph/neighbors`).
- **Repository Explorer:** **YES** (`/graph/entities`, `/file` viewer).
- **GraphRAG Assistant:** **YES** (`/assistant/chat`, `/assistant/threads`, `/assistant/threads/{id}`).
- **Impact Analysis:** **YES** (`/impact/analyze`).
- **Technical Reports:** **YES** (`GET /reports`, `GET /reports/{id}`).

*Note:* Because `verify_repo_access` treats any row in `repo_memberships` as full repository authorization, a "viewer" or "reviewer" can also execute state-mutating actions on that repository, such as generating reports, deleting reports, and initiating RAG reindexing.

---

### 6. Prevention of Privileged / Administrative Actions
**Question:** Can a reviewer be prevented from creating/deleting repos, starting ingestion, modifying configurations, and managing users?
**Finding:** **NO FOR REPO/JOB MUTATIONS; N/A FOR CONFIG & USERS**

| Action | Can Reviewer / Non-Admin Be Prevented? | Vulnerability / Implementation Detail |
| :--- | :---: | :--- |
| **Creating Repositories** | **NO (Cannot be prevented)** | `POST /api/v1/repos` only checks `get_authenticated_user()`. Any authenticated user can register new repositories. |
| **Deleting Repositories** | **NO (Cannot be prevented)** | `DELETE /api/v1/repos/{repo_id}` does not verify repository membership or admin role. Any authenticated user can initiate repository deletion. |
| **Starting Ingestion Jobs** | **NO (Cannot be prevented)** | `POST /api/v1/repos/{repo_id}/ingest` does not check membership or admin role. Any authenticated user can enqueue an ingestion job on any repository. |
| **Deleting Reports** | **NO (Cannot be prevented)** | `DELETE /api/v1/repos/{id}/snapshots/{sha}/reports/{id}` calls `verify_repo_access()`. Any user with membership can delete reports. |
| **Triggering RAG Indexing** | **NO (Cannot be prevented)** | `POST /api/v1/repos/{id}/snapshots/{sha}/rag/index` calls `verify_repo_access()`. Any user with membership can trigger reindexing. |
| **Modifying Configurations** | **YES (Protected by omission)** | No backend API exists to modify environment configuration or system settings at runtime. |
| **Managing Users** | **YES (Protected by omission)** | No user management API exists; non-admins cannot manage users because nobody can manage users via API. |

---

### 7. User-Management API Endpoints Inventory
**Question:** Are user-management API endpoints already implemented?
**Finding:** **NO (Completely Missing)**

The following standard user-management endpoints are **not implemented**:
- `GET /api/v1/users` (List users)
- `POST /api/v1/users` (Create user)
- `GET /api/v1/users/{id}` (Get user profile)
- `PUT /api/v1/users/{id}` (Update user profile/role)
- `DELETE /api/v1/users/{id}` (Deactivate/delete user)
- `POST /api/v1/users/{id}/password` (Admin reset password)
- `POST /api/v1/repos/{repo_id}/members` (Add user to repository)
- `GET /api/v1/repos/{repo_id}/members` (List repository members)
- `DELETE /api/v1/repos/{repo_id}/members/{user_id}` (Remove user from repository)
- `PUT /api/v1/repos/{repo_id}/members/{user_id}` (Update repository role)

Only session lifecycle endpoints are implemented (`/login`, `/refresh`, `/logout`, `/.well-known/jwks.json`).

---

### 8. Public Self-Registration Status
**Question:** Is public self-registration enabled or disabled?
**Finding:** **DISABLED / NOT IMPLEMENTED (Secure by Default)**

- **Backend:** There is no registration route (e.g. `POST /api/v1/auth/register`). Anonymous visitors cannot register or mint tokens.
- **Frontend:** `LoginPage.tsx` renders exclusively username and password inputs with a direct "Sign In" button. There is no "Register", "Sign Up", or "Forgot Password" link.
- **Exposure Risk:** Zero public registration exposure. All accounts must be pre-provisioned in the database.

---

## Implemented vs. Missing Features Matrix

```
+-------------------------------------------------------------------------------+
|                        AUTHENTICATION & ACCESS MATRIX                         |
+------------------------------------------------------+------------+-----------+
| Feature Capability                                   | Status     | Type      |
+------------------------------------------------------+------------+-----------+
| RS256 JWT Access Token Verification                  | Implemented| Auth Core |
| HttpOnly Cookie Rotation with Family Reuse Detection | Implemented| Auth Core |
| Password Hashing (SHA-256 with Salt)                 | Implemented| Auth Core |
| Pre-seeded Administrator Bootstrap                   | Implemented| Auth Core |
| Multi-tenant Repository Isolation on Graph / Data    | Implemented| AuthZ     |
| User-scoped Assistant Conversation Threads           | Implemented| AuthZ     |
| Public Registration Disabled                         | Implemented| Security  |
+------------------------------------------------------+------------+-----------+
| Admin User Creation API / Interface                  | Missing    | User Mgmt |
| User Profile & Password Change API                   | Missing    | User Mgmt |
| Repository Membership Management API (Add/Remove)    | Missing    | User Mgmt |
| Granular Role Definitions (Admin vs Reviewer vs User)| Missing    | RBAC      |
| Role-based Access in repo_memberships (Owner vs Read)| Missing    | RBAC      |
| Admin-only Restriction on POST /api/v1/repos         | Missing    | RBAC      |
| Admin/Owner-only Restriction on DELETE /repos/{id}   | Missing    | RBAC      |
| Member-only Restriction on POST /repos/{id}/ingest   | Missing    | RBAC      |
| User-filtered Repository Listing (GET /repos)        | Missing    | AuthZ     |
+------------------------------------------------------+------------+-----------+
```

---

## Detailed Endpoint Authorization Audit Table

| HTTP Method & Endpoint | Auth Required? | Membership Check (`verify_repo_access`) | Role Check Enforced | Security / Authorization Assessment |
| :--- | :---: | :---: | :---: | :--- |
| `GET /api/v1/health` | No | No | None | Public health check. |
| `GET /.well-known/jwks.json` | No | No | None | Public RSA public key for token verification. |
| `POST /api/v1/auth/login` | No | No | None | Public authentication entry point. |
| `POST /api/v1/auth/refresh` | Cookie | No | None | Rotates refresh token; checks revocation. |
| `POST /api/v1/auth/logout` | Cookie | No | None | Revokes refresh token family. |
| `GET /api/v1/repos` | Yes | **No** | None | **Deficiency:** Returns all repos; does not filter by membership. |
| `POST /api/v1/repos` | Yes | N/A | **None** | **Deficiency:** Any authenticated user can create repos. |
| `DELETE /api/v1/repos/{repo_id}` | Yes | **No** | **None** | **Deficiency:** Any authenticated user can delete any repo. |
| `POST /api/v1/repos/{repo_id}/ingest` | Yes | **No** | **None** | **Deficiency:** Any authenticated user can trigger ingest on any repo. |
| `GET /api/v1/jobs/{job_id}` | Yes | No | None | Returns job status for any authenticated user. |
| `GET /api/v1/repos/{id}/snapshots` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `POST /api/v1/repos/{id}/snapshots/{sha}/graph/query` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `GET /api/v1/repos/{id}/snapshots/{sha}/graph/*` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `GET /api/v1/repos/{id}/snapshots/{sha}/file` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `POST /api/v1/repos/{id}/snapshots/{sha}/rag/*` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `POST /api/v1/repos/{id}/snapshots/{sha}/assistant/*` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `POST /api/v1/repos/{id}/snapshots/{sha}/impact/*` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `POST /api/v1/repos/{id}/snapshots/{sha}/reports` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `GET /api/v1/repos/{id}/snapshots/{sha}/reports` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `DELETE /api/v1/repos/{id}/snapshots/{sha}/reports/{id}`| Yes | **Yes** | Admin bypass | **Note:** Any member can delete reports. |
| `POST /api/v1/evaluation/run` | Yes | **Yes** | Admin bypass | Properly restricted to members or admin. |
| `GET /api/v1/evaluation/runs` | Yes | Conditional | None | If `repo_id` omitted, returns all runs. |

---

## Architectural Recommendations for Future Implementation (No Changes Applied)

1. **Implement Formal RBAC Model:**
   - Define an explicit enum for system roles: `SystemRole = ("admin", "user")`.
   - Define an explicit enum for repository membership roles: `RepoRole = ("owner", "maintainer", "reviewer", "viewer")`.
2. **Close Endpoint Privilege Gaps:**
   - Restrict `POST /api/v1/repos` and `DELETE /api/v1/repos/{repo_id}` to users with `role == 'admin'` or `repo_memberships.role == 'owner'`.
   - Add `verify_repo_access(user, repo_id)` to `POST /api/v1/repos/{repo_id}/ingest` and require at least `maintainer` role.
   - Filter `GET /api/v1/repos` so non-admin users only see repositories where a record exists in `repo_memberships`.
3. **Implement Administrative User Management APIs:**
   - Provide an admin-only router (`/api/v1/admin/users`) for user provisioning, deactivation, and role changes.
   - Provide repository membership management APIs (`POST /api/v1/repos/{repo_id}/members`) allowing repository owners to invite read-only reviewers.
