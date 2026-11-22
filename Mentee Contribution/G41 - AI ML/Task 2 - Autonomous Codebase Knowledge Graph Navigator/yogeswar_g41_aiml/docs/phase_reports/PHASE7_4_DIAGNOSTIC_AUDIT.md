# PHASE 7.4 DIAGNOSTIC AUDIT: VIEWER EXPERIENCE, REAL GRAPH DATA & DASHBOARD NAVIGATION

**Project**: Autonomous Codebase Knowledge Graph Navigator
**Audit Phase**: Phase 7.4 (Read-Only Diagnostic Audit)
**Date**: November 15, 2026
**Status**: COMPLETED — READ-ONLY INVESTIGATION

---

## 1. Executive Summary

This diagnostic audit investigates three distinct operational issues identified in the Autonomous Codebase Knowledge Graph Navigator:
1. **Issue 1**: Reviewer or Viewer role cannot access or interact with the AI Assistant.
2. **Issue 2**: The Knowledge Graph visualization displays synthetic/artificial data rather than real repository AST data.
3. **Issue 3**: Dashboard quick-action navigation cards (*Change Impact Analysis*, *Technical Report Viewer*, and *Evaluation & Benchmarks*) fail to open destination pages or redirect back to the dashboard.

All three issues have been traced to their exact root causes across frontend routing, navigation gating, backend authorization dependencies, and repository dataset states without modifying any production code, database records, Docker volumes, or credentials.

---

## 2. Issue 1 Diagnosis: Reviewer or Viewer Cannot Access AI Assistant

### 2.1 Observed Behavior
When signed in under a `viewer` role account (e.g., `restricted_viewer` or `repo_member`), the user has no visible navigation entry for **4. AI Assistant** in the main navigation header. When accessing the URL directly, the backend permits read-only chat requests only if repository membership exists.

### 2.2 Root Cause Analysis
1. **Frontend Navigation Exclusion (`frontend/src/App.tsx` lines 64–67)**:
   ```typescript
   if (role === 'admin' || role === 'reviewer') {
     navLinks.push({ name: '4. AI Assistant', path: `/assistant/${activeRepoId}/snapshot/${activeCommitSha}` });
     navLinks.push({ name: '5. Impact Analysis', path: `/impact/${activeRepoId}/snapshot/${activeCommitSha}` });
   }
   ```
   The top navigation bar explicitly excluded `4. AI Assistant` for `role === 'viewer'`.
2. **Route Authorization (`frontend/src/App.tsx` lines 306–312)**:
   ```typescript
   <Route
     path="/assistant/:repoId/snapshot/:commitSha"
     element={
       <ProtectedRoute>
         <AssistantPage />
       </ProtectedRoute>
     }
   />
   ```
   The route itself has no `allowedRoles` restriction (any authenticated session can access it), but users could not navigate to it via the UI.
3. **Backend Authorization (`backend/app/main.py` lines 868–884)**:
   `POST /api/v1/repos/{repo_id}/snapshots/{commit_sha}/assistant/chat` calls `verify_repo_access(user, repo_id, write=False)`.
   Non-admin users (both reviewers and viewers) are authorized if and only if they possess an active record in `repo_memberships` for that `repo_id`.
   When a viewer user has no assigned repository memberships (e.g., `restricted_viewer`), all assistant requests correctly return HTTP 403 Forbidden.
4. **Thread Ownership & Tenant Isolation (`backend/app/agent/checkpoint_store.py`)**:
   `get_thread_history()` and `get_or_create_thread()` enforce strict user isolation:
   `if row["user_id"] != user_id: raise PermissionError(...)`.
   Cancelling threads via `cancel_thread_endpoint` is restricted to thread owners or admins.

### 2.3 Proposed Remediations
1. Update `frontend/src/App.tsx`:
   Include `4. AI Assistant` in `navLinks` for `admin`, `reviewer`, and `viewer` roles, allowing all authorized users to query their repositories.
2. Ensure viewer test users have active repository memberships in SQLite `repo_memberships` for their assigned demo/monitored repositories.

---

## 3. Issue 2 Diagnosis: Knowledge Graph Appears Artificial

### 3.1 Observed Behavior
In the viewer account, the Knowledge Graph displays 4 static nodes (`verify_credentials()`, `DatabasePool`, `DatabasePool.query()`, `dispatch_dynamic_route()`) and 2 edges, regardless of graph complexity.

### 3.2 Root Cause Analysis
1. **Demo Fixture Bypass (`frontend/src/pages/KnowledgeGraphPage.tsx` lines 118–137)**:
   ```typescript
   const isDemoRepo = repoId === 'repo_demo_sample';
   if (isDemoRepo) {
     setEntities(DEMO_BENCHMARK_ENTITIES);
     setEdges(DEMO_BENCHMARK_EDGES);
     ...
     return;
   }
   ```
   When `repoId === 'repo_demo_sample'`, the component completely skips backend API calls and loads the frontend constant `DEMO_BENCHMARK_ENTITIES`.
2. **Repository Assignment State**:
   In `data/app_state.db`, the viewer account `repo_member` is only assigned to `repo_demo_sample`.
   `repo_demo_sample` is a bootstrap DB fixture with **0 ingested snapshots and 0 Neo4j nodes**.
3. **Real Ingested Graph State in Neo4j**:
   The Neo4j database actually contains **464 live nodes and 470+ relationships** across 13 ingested snapshot commits (e.g., repository `12fac9bd-0ebb-4844-a239-e518e812b6bb` commit `d730e05672cb7673365022a44d3814bdc66ec033` with 40 nodes).
   These nodes are genuine AST extractions containing exact file paths (`auth_service.py`, `db_pool.py`), exact AST line numbers (e.g., `verify_credentials` at line 4, `DatabasePool` at line 3), exact symbols, and verified evidence references (`RelationshipEvidence`, `EntityEvidence`).
4. **Distinction & Transparency**:
   `KnowledgeGraphPage.tsx` displays a `DEMO BENCHMARK DATASET` banner for `repo_demo_sample` and a `LIVE REPOSITORY GRAPH` banner for real repositories.
   Because the viewer was default-assigned to `repo_demo_sample`, the viewer only saw the demo benchmark dataset.

### 3.3 Proposed Remediations
1. Maintain strict distinction between demo benchmark fixtures and live Neo4j extractions. Never inject synthetic nodes into live repository graphs.
2. Assign viewer membership to a real ingested repository (such as `12fac9bd-0ebb-4844-a239-e518e812b6bb`) in `repo_memberships` so viewers can inspect genuine AST entities, dynamic call classifications, and evidence links in Neo4j.

---

## 4. Issue 3 Diagnosis: Dashboard Navigation Cards Do Not Work

### 4.1 Observed Behavior
Clicking **Change Impact Analysis** or **Technical Report Viewer** on the Dashboard causes the browser to reload the Dashboard instead of opening the target feature. Clicking **Evaluation & Benchmarks** results in an Access Denied view for non-admin users.

### 4.2 Root Cause Analysis
1. **URL Route Mismatch in `frontend/src/pages/DashboardPage.tsx` (lines 124–150)**:
   - **Card 1 (Change Impact Analysis)**:
     ```typescript
     <Link to={`/repo/${activeRepoId}/snapshot/${activeCommitSha}/impact`}>
     ```
     Registered route in `frontend/src/App.tsx`:
     ```typescript
     <Route path="/impact/:repoId/snapshot/:commitSha" element={<ImpactAnalysisPage />} />
     ```
     Path mismatch: `/repo/:repoId/snapshot/:commitSha/impact` vs `/impact/:repoId/snapshot/:commitSha`.
   - **Card 2 (Technical Report Viewer)**:
     ```typescript
     <Link to={`/repo/${activeRepoId}/snapshot/${activeCommitSha}/reports`}>
     ```
     Registered route in `frontend/src/App.tsx`:
     ```typescript
     <Route path="/report/:repoId/:queryId" element={<ReportViewerPage />} />
     ```
     Path mismatch: `/repo/:repoId/snapshot/:commitSha/reports` vs `/report/:repoId/:queryId`.
   - **Fallback Wildcard Redirect**:
     In `frontend/src/App.tsx`, unmatched paths fall through to `<Route path="*" element={<DashboardPage />} />`. Consequently, clicking either card navigated to an unregistered path and immediately bounced back to the Dashboard.
2. **Card 3 (Evaluation & Benchmarks)**:
     ```typescript
     <Link to="/evaluation">
     ```
     In `App.tsx`:
     ```typescript
     <Route path="/evaluation" element={<ProtectedRoute allowedRoles={['admin']}><EvaluationPage /></ProtectedRoute>} />
     ```
     The card was displayed unconditionally to all users without any role indicator. Non-admin users who click it are blocked with a 403 Forbidden screen.

### 4.3 Proposed Remediations
1. In `frontend/src/pages/DashboardPage.tsx`:
   - Update Card 1 to link to `/impact/${activeRepoId}/snapshot/${activeCommitSha}`.
   - Update Card 2 to link to `/repo/${activeRepoId}/snapshot/${activeCommitSha}/reports`.
   - Add visual role badge for Card 3 (`Admin Only` badge when non-admin).
2. In `frontend/src/App.tsx`:
   - Add alias routes for `/repo/:repoId/snapshot/:commitSha/impact` -> `<ImpactAnalysisPage />`.
   - Add alias routes for `/repo/:repoId/snapshot/:commitSha/reports` -> `<ReportViewerPage />`.
   - This guarantees that navigation succeeds regardless of whether the user clicks a card, uses top navigation, or pastes the URL directly.

---

## 5. Affected Files & Proposed Changes

| Component | File Path | Proposed Change |
| :--- | :--- | :--- |
| Frontend Routing | `frontend/src/App.tsx` | Include AI Assistant in navigation for viewer role; add alias routes for impact analysis and report viewer. |
| Dashboard UI | `frontend/src/pages/DashboardPage.tsx` | Correct target paths for Impact Analysis and Reports cards; add role badge for Evaluation card. |
| Knowledge Graph UI | `frontend/src/pages/KnowledgeGraphPage.tsx` | Ensure clear visual labeling, entity details, and evidence popovers are rendered seamlessly for both live and demo modes. |
| Report Viewer UI | `frontend/src/pages/ReportViewerPage.tsx` | Support direct snapshot routing `/repo/:repoId/snapshot/:commitSha/reports`. |
| Database Seed / State | SQLite `data/app_state.db` | Grant viewer membership to ingested repository `12fac9bd-0ebb-4844-a239-e518e812b6bb` so viewers can explore live Neo4j graph data. |

---

## 6. Security & RBAC Implications

1. **Authentication & RBAC Preservation**:
   - Zero modifications to password hashing (`hash_password`), JWT verification (`verify_token`), or token expiration.
   - Reviewer and viewer roles remain strictly forbidden from triggering ingestion, creating repositories, deleting repositories, modifying configurations, managing users, or executing benchmarks.
2. **Tenant & Repository Isolation**:
   - All assistant and graph queries continue to enforce `verify_repo_access(user, repo_id)` on the backend.
   - Assistant threads remain strictly isolated by `user_id` in `assistant_threads`.
3. **Read-Only Viewer Guarantee**:
   - Viewers can only view and query repositories to which they are explicitly assigned in `repo_memberships`.

---

## 7. Verification & Acceptance Test Plan

1. **Unit & Integration Regression Suite**:
   - Run Phase 6.4 Authentication tests (`tests/test_auth.py`).
   - Run Phase 7.3 Multi-user RBAC tests (`tests/test_rbac.py`).
   - Run Assistant & GraphRAG tests (`tests/test_agent.py` / `tests/test_cgg.py`).
2. **Frontend Production Build**:
   - Execute `npm run build` in `frontend/` to ensure zero TypeScript or bundling errors.
3. **Live Nginx & Service Validation**:
   - Verify all 7 Docker containers are running and healthy.
   - Probe live endpoints via Nginx (`http://127.0.0.1:80`):
     - Viewer login and session token acquisition.
     - Viewer querying AI Assistant for authorized repository.
     - Viewer blocked from unauthorized repository.
     - Viewer blocked from mutating operations (POST `/api/v1/repos`, DELETE `/api/v1/repos/{id}`, POST `/ingest`).
4. **Browser & Dashboard Navigation Verification**:
   - Test Card 1: Change Impact Analysis navigates to `/impact/:repoId/snapshot/:commitSha` and renders direct/transitive callers.
   - Test Card 2: Technical Report Viewer navigates to `/repo/:repoId/snapshot/:commitSha/reports` and renders report content.
   - Test Card 3: Evaluation & Benchmarks opens for admin and displays 403 / role badge for viewer.
   - Test Knowledge Graph: Verify viewer viewing real repository `12fac9bd...` renders actual AST entities (`verify_credentials`, `DatabasePool`, `query`), line numbers, and Neo4j evidence.
