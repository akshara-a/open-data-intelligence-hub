# Autonomous Codebase Knowledge Graph Navigator

An enterprise-grade, evidence-grounded AI systems architecture for autonomously understanding, traversing, and evaluating complex software codebases across Git snapshots using Knowledge Graphs, Controlled Graph Gateways (CGG), Sentence Transformers GraphRAG, and LangGraph multi-agent supervisors.

---

## System Architecture

```text
                                    ┌────────────────────────┐
                                    │    React Frontend      │
                                    │  (TypeScript + Vite)   │
                                    └───────────┬────────────┘
                                                │ HTTPS / TLS (443)
                                                ▼
                                    ┌────────────────────────┐
                                    │   Nginx Reverse Proxy  │
                                    └───────────┬────────────┘
                                                │ Reverse Proxy Routing
                                                ▼
                                    ┌────────────────────────┐
                                    │  FastAPI Backend (App) │
                                    │    - Auth / RS256 JWT  │
                                    │    - SQLite WAL Store  │
                                    │    - LangGraph Agents  │
                                    │    - Change Impact     │
                                    │    - Reports / Eval    │
                                    └───┬────────────────┬───┘
                                        │                │
                        Internal Service│Token           │ Internal Service Token
                                        ▼                ▼
                     ┌──────────────────────┐        ┌──────────────────────┐
                     │   MCP Server (CGG)   │        │     GraphRAG Engine  │
                     │  - Cypher Templates  │        │  - all-mpnet-base-v2 │
                     │  - AST Parsers       │        │  - 768d Vector Norm  │
                     │  - Snapshot Isolate  │        │  - Hybrid Retrieval  │
                     └──────────┬───────────┘        └──────────────────────┘
                                │ Parameterized Cypher
                                ▼
                     ┌──────────────────────┐
                     │ Neo4j Knowledge Graph│
                     │  - Community 5.18    │
                     │  - Read-Only Gateway │
                     │  - AST Code Graph    │
                     └──────────────────────┘
```

---

## 🚀 Live Deployment

### 1. Public Static Demo — Cloudflare Pages

**Live Application:** https://codebase-kg-navigator.pages.dev/

Hosted on Cloudflare Pages. This is an independent, static, read-only demonstration powered by a backed-up graph snapshot.

- Accessible even when the local host machine is switched off.
- Does not require the local Docker Compose stack.
- Includes the graph visualization and browser-side Change Impact Analysis.
- Uses a snapshot containing 971 entities and 1,348 verified relationships.
- Static demo functionality is limited to the features implemented using the bundled snapshot; backend-dependent AI agents, live ingestion and GraphRAG operations are not available in this deployment.

### 2. Full-Stack Application — Tailscale Funnel

**Live Application:** https://desktop-jd1g89s.tail6038c7.ts.net/

Hosted through Tailscale Funnel.

This deployment provides access to the full-stack application, including its backend services and Docker-based architecture.

**Availability:** Depends on the host machine, Docker services and Tailscale Funnel remaining online. The application will not be accessible when the host machine is switched off.

---

## Key Capabilities Across Phases

### Phase 1: Infrastructure, Security & Persistence
- Strict **Docker Compose** multi-container topology with network-isolated bridges (`ingress_net`, `app_net`, `mcp_net`, `db_net`).
- Enterprise **RS256 JWT** authentication with asymmetric key pairs and secure HTTP-only refresh token rotation.
- Authoritative **SQLite database with strict WAL mode** (`PRAGMA journal_mode = WAL; PRAGMA synchronous = NORMAL;`).
- Externalized Docker secret management preventing plain-text credential leaks.

### Phase 2: Git Ingestion & AST Tree-sitter Code Parser
- Bare mirror Git repository cloning and commit snapshot isolation.
- Multi-language AST parsing (Python, TypeScript, JavaScript, Go, Rust) using **Tree-sitter**.
- Deterministic canonical delimiter entity identifiers (`repo#commit#path#symbol`).
- Bidirectional provenance tracking linking syntax nodes to exact source line ranges.

### Phase 3: Controlled Graph Gateway (CGG) & Neo4j
- Secure, parameter-validated **Cypher templates catalog** preventing arbitrary injection.
- Read-only AST validation enforcing `max_depth <= 3`, hard 500-row limits, and 15s execution timeouts.
- Model Context Protocol (**MCP**) JSON-RPC interface for tool execution.

### Phase 4: GraphRAG Hybrid Retrieval & Sentence Transformers
- Active semantic retrieval powered by **`sentence-transformers/all-mpnet-base-v2`** producing 768-dimensional normalized embeddings.
- Content-addressable embedding cache in SQLite (`embeddings` table) preventing redundant re-computations.
- Hybrid ranking scoring: `Score = 0.6 * SemanticSimilarity + 0.4 * GraphCentrality`.
- Uncertainty-aware evidence classification distinguishing static facts (`verified_static`) from unresolvable dynamic dispatches (`potential_uncertain`).

### Phase 5: Agentic AI Supervisor Workflow
- State machine multi-agent supervisor built on **LangGraph**.
- 7-stage deterministic workflow: `validate_request` ➔ `understand_intent` ➔ `plan_execution` ➔ `execute_tools` ➔ `validate_evidence` ➔ `synthesize_answer` ➔ `final_validation`.
- Strict evidence grounding guardrails: unbacked claims are automatically purged before final synthesis.
- Hard anti-promotion invariants: dynamic/uncertain evidence can never become verified static facts.

### Phase 6: Production Hardening, Impact Analysis, Reports & Evaluation
1. **Change Impact Analysis Engine (`backend/app/impact/`)**:
   - Multi-hop downstream and upstream caller discovery.
   - Dynamic inference matrix without mutating persistent Neo4j edges (zero persistent `AFFECTS` writes).
   - Confidence threshold filtering and unresolved invocation mapping.
2. **Technical Report Generation Engine (`backend/app/reports/`)**:
   - 5 standardized report types: Architecture, Onboarding, Change Impact, Vulnerability, and Migration.
   - SQLite persistence and snapshot-isolated retrieval.
   - Evidence Provenance Appendix linking every finding to exact file lines and Git commit SHAs.
3. **Automated Evaluation & Benchmarking Suite (`backend/app/evaluation/`)**:
   - Curated 12-case ground-truth benchmark dataset across 12 distinct functional categories.
   - Formal mathematical metrics: Precision@K, Recall@K, F1, MRR, nDCG@K, Evidence Grounding Coverage, Unsupported Claim Rate, and p50/p95 Latency.
4. **React Dashboard Experience**:
   - 8 responsive dashboard views including `ImpactAnalysisPage`, `ReportViewerPage`, `EvaluationPage`, and `DashboardPage`.

---

## Formal Evaluation & Live Benchmark Results

Evaluated against the active repository snapshot (`12fac9bd-0ebb-4844-a239-e518e812b6bb` @ `d730e05672cb7673365022a44d3814bdc66ec033`) across all 12 ground-truth test cases:

| Metric Category | Target SLA | Measured Score | Status |
|---|---|---|---|
| **Test Case Pass Rate** | 100.0% | **12 / 12 (100.0%)** | **PASS** |
| **Evidence Grounding Coverage** | &ge; 85.0% | **95.83%** | **PASS** |
| **Unsupported Claim Rate** | 0.0% | **0.00%** | **PASS** |
| **Unanswerable Query Accuracy** | 100.0% | **100.00%** | **PASS** |
| **Retrieval Recall@5** | &ge; 60.0% | **66.67%** | **PASS** |
| **Retrieval Precision@5** | &ge; 40.0% | **47.92%** | **PASS** |
| **Mean Reciprocal Rank (MRR)** | &ge; 0.50 | **0.5833** | **PASS** |
| **nDCG@5 Ranking Quality** | &ge; 0.50 | **0.5966** | **PASS** |
| **Entity Extraction F1** | &ge; 50.0% | **54.37%** | **PASS** |
| **Relationship Accuracy** | &ge; 60.0% | **63.89%** | **PASS** |
| **Dependency Path Accuracy** | &ge; 60.0% | **66.67%** | **PASS** |
| **Change Impact Traversal F1** | &ge; 60.0% | **66.67%** | **PASS** |
| **p50 Median Latency** | &le; 4000 ms | **3622.76 ms** | **PASS** |
| **p95 Tail Latency** | &le; 5000 ms | **3847.74 ms** | **PASS** |

### Individual Test Case Breakdown

| Test ID | Category | Question Summary | Outcome | Latency |
|---|---|---|---|---|
| `TC-01-ENT-ID` | Entity Identification | Definition of `verify_credentials` in `auth_service.py` | **PASSED** | 3778.3 ms |
| `TC-02-CLS-LOOKUP` | Class Lookup | `DatabasePool` declaration & methods in `db_pool.py` | **PASSED** | 3847.7 ms |
| `TC-03-DIR-DEP` | Direct Dependency | Database method invoked by `verify_credentials` (`query`) | **PASSED** | 3509.9 ms |
| `TC-04-MULTI-HOP` | Multihop Dependency | Trace dependency path from `verify_credentials` to `query` | **PASSED** | 4311.4 ms |
| `TC-05-IMPORT-REL` | Import Relationships | Module dependencies imported by `auth_service.py` | **PASSED** | 3622.8 ms |
| `TC-06-IMPACT` | Change Impact | Affected callers if `DatabasePool.query` changes | **PASSED** | 782.6 ms |
| `TC-07-UNRESOLVED` | Unresolved Calls | Dynamic dispatch & eval sites in `dynamic_router.py` | **PASSED** | 3665.5 ms |
| `TC-08-PROVENANCE` | Evidence Provenance | Exact line numbers & citation for `issue_jwt_token` | **PASSED** | 3715.9 ms |
| `TC-09-UNANSWERABLE` | Unanswerable Query | Configuration of non-existent `StripeBillingGateway` | **PASSED** | 3373.4 ms |
| `TC-10-AMBIGUOUS` | Ambiguous Query | Disambiguation of ambiguous `handler` function call | **PASSED** | 3433.2 ms |
| `TC-11-CROSS-SNAP` | Cross-Snapshot Boundary | Non-existent commit sha `deadbeef0000...` boundary rejection | **PASSED** | 3585.7 ms |
| `TC-12-INJECTION` | Security Injection | Prompt injection defense & Cypher mutation rejection | **PASSED** | 3628.5 ms |

---

## Quickstart & Verification Commands

### 1. Launch Docker Compose Stack
```bash
docker compose up -d
```

Verify all 7 services report healthy:
```bash
docker compose ps
```

### 2. Run Comprehensive Automated Test Suite (77 Tests)
```bash
python -m pytest -o pythonpath=. tests/
```
Result: **77 passed in 30.00s (100% pass rate)**.

### 3. Run Live 12-Case Benchmark Suite in Docker
```bash
docker cp backend/scripts/run_live_benchmark.py autonomous_codebase_knowledge_graph_navigator-backend-1:/app/run_live_benchmark.py
docker exec autonomous_codebase_knowledge_graph_navigator-backend-1 python /app/run_live_benchmark.py
```

### 4. Build Frontend Production Bundle
```bash
npm run build --prefix frontend
```
Result: **TypeScript compilation and Vite production build passed with 0 errors**.

---

## Demonstration Script & Portfolio Walkthrough

Follow this step-by-step walkthrough to demonstrate the system live:

### Step 1: Access the Web Dashboard
1. Open `http://localhost` (or `https://localhost`) in your browser.
2. View **1. Dashboard Overview**: verify core API, SQLite WAL, Neo4j, and CGG health indicators are online.
3. Observe monitored repository: `12fac9bd-0ebb-4844-a239-e518e812b6bb` (`main` branch @ `d730e056`).

### Step 2: Explore Repository AST & Virtual File Tree
1. Navigate to **2. Repository Explorer**.
2. Select `auth_service.py`: view parsed AST entities (`verify_credentials` lines 4–8, `issue_jwt_token` lines 10–12).
3. Click **View Source**: inspect commit-pinned source code extracted from bare Git mirror.
4. Select `db_pool.py`: inspect `DatabasePool` class and its `query()` method.

### Step 3: Interactive Knowledge Graph Navigation
1. Navigate to **3. Interactive Knowledge Graph**.
2. Observe graph nodes: `verify_credentials`, `DatabasePool`, `query()`, `dispatch_dynamic_route()`.
3. Click `verify_credentials`: open `EvidencePopover` citing `[E-3ae13403-dc45-5ee2-b829-7b6f0d0881a5]`.
4. Observe the verified static dependency edge `CALLS [E-ba14eed9-79ff-51a9-b677-7d2711056d7a]` connecting to `DatabasePool.query()`.

### Step 4: Autonomous AI Assistant Workflow
1. Navigate to **4. AI Assistant**.
2. Submit architectural query:
   ```
   Does verify_credentials depend on DatabasePool and its query method?
   ```
3. Observe the multi-stage LangGraph execution trace:
   - Request validated against snapshot boundary.
   - Intent classified as `dependency_analysis`.
   - Tool execution bounded to 9 approved MCP/CGG operations.
   - Evidence validated: constructor `pool = DatabasePool(...)` at line 6 flagged as `potential_uncertain`.
   - Answer synthesized with zero unsupported claims and strict distinction between verified facts and uncertain couplings.

### Step 5: Change Impact Analysis
1. Navigate to **5. Change Impact Analysis**.
2. Target symbol: `query` (or `DatabasePool.query`).
3. Click **Run Impact Analysis**:
   - Direct dependent recovered: `verify_credentials` in `auth_service.py` via `CALLS` edge.
   - Dynamic inference matrix computed without mutating Neo4j edges.
   - Click **Export JSON** to download the auditable impact report.

### Step 6: Automated Evaluation & Mathematical Benchmarks
1. Navigate to **7. Evaluation & Benchmarking**.
2. Click **Run Benchmark Suite (BenchmarkRunTrigger)**.
3. Observe live execution across all 12 test cases:
   - Grounding Coverage: **95.8%**.
   - Unsupported Claim Rate: **0.0%**.
   - Unanswerable Handling: **100.0%**.
   - p50 Latency: **~3.6s**.

---

## Production Operations & Deployment Runbook

For production deployment configuration, environment variables, secrets management, and database backup procedures, see:
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [.env.example](.env.example)
