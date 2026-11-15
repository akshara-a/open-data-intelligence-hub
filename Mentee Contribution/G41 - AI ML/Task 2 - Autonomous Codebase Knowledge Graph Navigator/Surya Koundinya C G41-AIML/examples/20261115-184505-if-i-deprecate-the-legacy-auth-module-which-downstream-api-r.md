> **Query:** If I deprecate the legacy-auth-module, which downstream API routes and frontend components will break?
> **Generated:** 2026-11-15 13:15 UTC · **Models:** `gemini-3.5-flash-lite` (investigate) / `gemini-3.5-flash-lite` (report) · **Grounding check:** PASSED

# Impact Analysis Report: Deprecating legacy-auth-module

## 1. Executive summary

This report assesses the architectural and runtime impact of deprecating the `legacy-auth-module` code module.

- **Risk Level:** High (proposed engineering assessment based on graph evidence)
- **Justification:** The `legacy-auth-module` sits at the foundation of authentication flows, directly or transitively affecting `9` `APIRoute` nodes, `8` `Module` nodes, and `4` `FrontendComponent` nodes across `7` downstream microservices. Furthermore, deprecation touches components involved in service-level and module-level strongly connected components (SCCs) and introduces risks related to shared database access (`auth-sessions-db`).
- **Affected Downstream Services:** `api-gateway`, `auth-service-v2`, `inventory-service`, `notification-service`, `order-service`, `payment-service`, and `user-service`.
- **Blast Radius Assumption:** The computed blast radius is an upper bound based on the hard-dependency assumption (assuming each dependency is a hard runtime dependency with no fallbacks or circuit breakers).
- **Runtime Failure Note:** Graph reachability and structural dependency do not guarantee runtime failure without operational context, but they dictate required migration boundaries.

---

## 2. Scope & target resolution

- **Developer Question:** If I deprecate the `legacy-auth-module`, which downstream API routes and frontend components will break?
- **Target Node:** `legacy-auth-module` (Label: `Module`)
- **Owner Information:** Owned by `legacy-auth-service` (Label: `Service`)
- **Impact-Analysis Assumptions:** Upper-bound analysis assuming hard runtime dependencies. Max depth evaluated: `8`.
- **Missing Information:** An established replacement microservice or replacement module for `legacy-auth-module` is not determinable from the graph. Individual cycle enumeration within SCCs was not provided by the analysis.

---

## 3. Affected downstream components

### 3.1 Microservices

| Service | Impact Classification | Why Affected | Service-level Distance |
| :--- | :--- | :--- | :--- |
| `api-gateway` | Affected (Direct) | Depends on `legacy-auth-service` and calls routes dependent on the target | 1 |
| `auth-service-v2` | Affected (Direct) | Depends on `legacy-auth-service` | 1 |
| `order-service` | Affected (Direct) | Depends on `legacy-auth-service` | 1 |
| `payment-service` | Affected (Direct) | Depends on `legacy-auth-service` | 1 |
| `user-service` | Affected (Direct) | Depends on `legacy-auth-service` | 1 |
| `notification-service` | Affected (Transitive) | Transitive dependency via `order-service` | 2 |
| `inventory-service` | Affected (Transitive) | Transitive dependency via `order-service` and `notification-service` | 3 |

### 3.2 API routes

| Route | Owner Service | Route-level Distance | Dependency Chain |
| :--- | :--- | :--- | :--- |
| `POST /auth/login` | `legacy-auth-service` | 1 | `POST /auth/login` -> `legacy-auth-module` |
| `GET /auth/validate` | `legacy-auth-service` | 2 | `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `POST /v2/auth/token` | `auth-service-v2` | 3 | `POST /v2/auth/token` -> `session-manager` -> `legacy-token-validator` -> `legacy-auth-module` |
| `GET /orders/{id}` | `order-service` | 4 | `GET /orders/{id}` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `GET /users/{id}` | `user-service` | 4 | `GET /users/{id}` -> `user-profile-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `POST /orders` | `order-service` | 4 | `POST /orders` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `POST /payments/charge` | `payment-service` | 4 | `POST /payments/charge` -> `payment-processor` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `POST /notifications/send` | `notification-service` | 6 | `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `POST /inventory/reserve` | `inventory-service` | 8 | `POST /inventory/reserve` -> `stock-manager` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |

### 3.3 Frontend components

| Component | Component-level Distance | Dependency Chain | Owner Service If Known |
| :--- | :--- | :--- | :--- |
| `web-login-page` | 2 | `web-login-page` -> `POST /auth/login` -> `legacy-auth-module` | not established |
| `web-checkout-page` | 3 | `web-checkout-page` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` | not established |
| `mobile-app-auth` | 4 | `mobile-app-auth` -> `POST /v2/auth/token` -> `session-manager` -> `legacy-token-validator` -> `legacy-auth-module` | not established |
| `customer-portal` | 5 | `customer-portal` -> `GET /users/{id}` -> `user-profile-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` | not established |

### 3.4 Modules and data stores

#### Affected Modules

| Module | Owner Service | Module-level Distance | Dependency Chain |
| :--- | :--- | :--- | :--- |
| `legacy-token-validator` | `legacy-auth-service` | 1 | `legacy-token-validator` -> `legacy-auth-module` |
| `gateway-router` | `api-gateway` | 2 | `gateway-router` -> `POST /auth/login` -> `legacy-auth-module` |
| `session-manager` | `auth-service-v2` | 2 | `session-manager` -> `legacy-token-validator` -> `legacy-auth-module` |
| `order-processing-module` | `order-service` | 3 | `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `payment-processor` | `payment-service` | 3 | `payment-processor` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `user-profile-module` | `user-service` | 3 | `user-profile-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `email-dispatcher` | `notification-service` | 5 | `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |
| `stock-manager` | `inventory-service` | 7 | `stock-manager` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `GET /auth/validate` -> `legacy-token-validator` -> `legacy-auth-module` |

#### Data Stores & Shared Access

| Database | Accessor Module | Access Type |
| :--- | :--- | :--- |
| `auth-sessions-db` | `legacy-auth-module` | `WRITES_TO` |
| `auth-sessions-db` | `session-manager` | `READS_FROM` |

*Note: No blast-radius distance is assigned to `auth-sessions-db` because the evidence does not provide one. The shared database is not established as a replacement or migration destination.*

### 3.5 Not affected / exclusions

The available evidence does not establish a reliable list of unaffected entities.

---

## 4. Architectural debt assessment

### Circular dependencies
- **Service-Level Strongly Connected Component:** Size `4`. Members: `inventory-service`, `notification-service`, `order-service`, `payment-service`.
  - *Internal directed edges:* `inventory-service -> notification-service`, `notification-service -> order-service`, `order-service -> inventory-service`, `order-service -> payment-service`, `payment-service -> notification-service`.
- **Module-Level Strongly Connected Component:** Size `4`. Members: `email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`.
  - *Internal directed edges:* `email-dispatcher -> order-processing-module`, `order-processing-module -> payment-processor`, `order-processing-module -> stock-manager`, `payment-processor -> email-dispatcher`, `stock-manager -> email-dispatcher`.
- *Architectural Interpretation:* Members within an SCC are reachable from each other through directed paths, but this does not imply direct bidirectional edges between every pair of members. Individual cycle enumeration was not provided by the analysis. These SCCs indicate that deprecating or modifying authentication components tied into these execution paths will require coordinated changes across these tightly bound modules and services.

### Single points of failure
- **In-Radius Single Points of Failure:**
  - `legacy-auth-service`: `fan_in = 5`, reasons: `high fan-in (5 dependents)`. Dependents: `api-gateway`, `auth-service-v2`, `order-service`, `payment-service`, `user-service`. `graph_components_if_removed` is reported as an empty/null schema field value.
  - `api-gateway`: `fan_in = 0`, reasons: `articulation point (removal splits the service graph)`. Dependents: `[]`. `graph_components_if_removed` is `[7]`.
- *Global SPOF Query Note:* When queried with `min_fan_in = 3`, the exact same two nodes (`legacy-auth-service` and `api-gateway`) are returned. `legacy-auth-service` represents a high-fan-in concentration risk due to serving 5 dependent services.

### Shared-database / hidden coupling
- `auth-sessions-db` is written to by `legacy-auth-module` and read from by `session-manager`, creating hidden cross-module data coupling that bypasses service boundaries.

### Deprecated nodes still referenced
- `legacy-auth-module` (Module, explicitly marked with deprecated property) is still actively depended upon by `legacy-token-validator` and `POST /auth/login`.
- `legacy-token-validator` (Module, explicitly marked with deprecated property) is still referenced by `session-manager`, `gateway-router`, `order-processing-module`, `payment-processor`, and `user-profile-module`.
- `legacy-auth-service` (Service, explicitly marked with deprecated property) is depended on by 5 services.

### Coupling metrics
- **Service-Level Coupling Highlights:**
  - `legacy-auth-service`: `afferent_ca = 5`, `efferent_ce = 0`, `instability = 0.0`.
  - `api-gateway`: `afferent_ca = 0`, `efferent_ce = 5`, `instability = 1.0`.
  - `order-service`: `afferent_ca = 2`, `efferent_ce = 3`, `instability = 0.6`.
- **Module-Level Coupling Highlights:**
  - `legacy-auth-module`: `afferent_ca = 2`, `efferent_ce = 0`, `instability = 0.0`.
  - `legacy-token-validator`: `afferent_ca = 5`, `efferent_ce = 1`, `instability = 0.17`.
  - `gateway-router`: `afferent_ca = 0`, `efferent_ce = 6`, `instability = 1.0`.
- *Interpretation:* Low instability (0.0) for `legacy-auth-module` reflects high dependency concentration (afferent coupling with zero outgoing dependencies), confirming that removing it breaks incoming consumers. Coupling metrics describe structural dependency concentrations, not direct proof of runtime failure.

### Debt rating and prioritised findings
- **Debt Rating:** High (engineering assessment). Driven by high afferent coupling on deprecated authentication modules, shared database access (`auth-sessions-db`), and participation in service- and module-level SCCs.
- **Prioritised Findings:**
  1. High fan-in on `legacy-auth-service` and `legacy-auth-module`.
  2. Active references to deprecated `legacy-token-validator` and `legacy-auth-module`.
  3. Shared database access on `auth-sessions-db`.
  4. Circular dependencies across service and module tiers.

---

## 5. Refactoring strategy (step-by-step)

Because no replacement module or service is established in the graph, remediation must follow a rigorous, phased approach.

### Step 1: Characterise existing behaviour and introduce contract tests
- **Goal:** Establish baseline verification for all authentication flows (`POST /auth/login` and `GET /auth/validate`) before altering dependencies.
- **Concrete existing nodes involved:** `legacy-auth-module`, `legacy-token-validator`, `POST /auth/login`, `GET /auth/validate`, `web-login-page`, `web-checkout-page`.
- **Proposed new artefacts:** *AuthContractTests* (new).
- **Verification:** Execute contract tests against existing routes to verify input/output payloads.
- **Rollback:** N/A (non-destructive additive testing).

### Step 2: Identify and validate an approved replacement
- **Goal:** Formally define and validate a replacement target (e.g., verifying `auth-service-v2` capabilities), as no replacement is currently established by the graph.
- **Concrete existing nodes involved:** `auth-service-v2`, `legacy-auth-service`.
- **Proposed new artefacts:** *AuthReplacementSpec* (new).
- **Verification:** Ensure the replacement candidate can service token creation and validation without depending on `legacy-auth-module`.
- **Rollback:** Halt migration if replacement capabilities are deficient.

### Step 3: Introduce an abstraction or facade
- **Goal:** Decouple direct consumers from legacy modules using a single abstraction layer to ease migration.
- **Concrete existing nodes involved:** `gateway-router`, `legacy-auth-module`, `legacy-token-validator`.
- **Proposed new artefacts:** *AuthFacade* (new).
- **Verification:** Route test traffic through *AuthFacade* (new) to ensure parity with legacy outputs.
- **Rollback:** Revert routing rules back to `legacy-auth-module`.

### Step 4: Migrate direct consumers and shared storage access
- **Goal:** Migrate modules with distance 1 and address shared database coupling on `auth-sessions-db`.
- **Concrete existing nodes involved:** `legacy-token-validator`, `session-manager`, `auth-sessions-db`, `POST /auth/login`.
- **Proposed new artefacts:** *AuthStorageAdapter* (new).
- **Verification:** Verify that `session-manager` reads from the new storage mechanism rather than directly contending with `legacy-auth-module` on `auth-sessions-db`.
- **Rollback:** Restore direct database access pointers to `auth-sessions-db`.

### Step 5: Migrate transitive consumers according to verified dependency chains
- **Goal:** Systematically update transitive consumers across the service graph (distances 2 through 8), accounting for the module SCC (`email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`) and service SCC (`inventory-service`, `notification-service`, `order-service`, `payment-service`).
- **Concrete existing nodes involved:** `order-processing-module`, `user-profile-module`, `payment-processor`, `email-dispatcher`, `stock-manager`.
- **Proposed new artefacts:** None.
- **Verification:** Run integration suites across `order-service`, `user-service`, `payment-service`, `notification-service`, and `inventory-service`.
- **Rollback:** Re-enable legacy token validation fallbacks if downstream communication fails.

### Step 6: Validate replacement behaviour and cut over
- **Goal:** Switch primary traffic entirely to the new auth infrastructure and verify end-to-end frontend component flows (`web-login-page`, `web-checkout-page`, `mobile-app-auth`, `customer-portal`).
- **Concrete existing nodes involved:** All affected `FrontendComponent` and `APIRoute` nodes.
- **Proposed new artefacts:** None.
- **Verification:** End-to-end synthetic user transactions across all 4 frontend components.
- **Rollback:** Revert DNS/gateway routing to legacy endpoints.

### Step 7: Remove deprecated nodes
- **Goal:** Safely excise deprecated artefacts from the codebase and graph.
- **Concrete existing nodes involved:** `legacy-auth-module`, `legacy-token-validator`.
- **Proposed new artefacts:** None.
- **Verification:** Build verification ensuring zero compiler or runtime references remain to `legacy-auth-module` or `legacy-token-validator`.
- **Rollback:** Restore from version control tag if compilation fails.

---

## 6. Risks, assumptions & unknowns

| Type | Description |
| :--- | :--- |
| **Assumption** | Upper bound blast radius assumes hard runtime dependencies with no circuit breakers or fallbacks. |
| **Fact** | `legacy-auth-module`, `legacy-token-validator`, and `legacy-auth-service` are explicitly marked as deprecated in their node properties. |
| **Fact** | `legacy-auth-service` has an afferent coupling ($\text{Ca}$) of 5 and 0 efferent coupling ($\text{Ce}$). |
| **Risk** | Shared database coupling on `auth-sessions-db` between `legacy-auth-module` and `session-manager` creates hidden data dependencies. |
| **Risk** | Service-level and module-level SCCs require highly coordinated migration steps to prevent circular deadlocks or partial integration failures. |
| **Unknown** | Individual cycles within the reported service and module strongly connected components were not enumerated by the graph analysis. |
| **Unknown** | An established replacement service or module for `legacy-auth-module` is not determinable from the graph. |
| **Unknown** | Owner services for frontend components (`web-login-page`, `web-checkout-page`, `mobile-app-auth`, `customer-portal`) are not established. |

---
## Appendix A — Evidence trail (tool calls executed)

**1. `get_schema`** — ok
**2. `find_nodes`** — ok
```json
{"text": "If I deprecate the legacy-auth-module, which downstream API routes and frontend components will break?"}
```
**3. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-auth-module'})-[:CALLS_ROUTE]->(r:APIRoute) OPTIONAL MATCH (r)<-[:CONSUMES]-(f:FrontendComponent) RETURN m, r, f
```
**4. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-auth-module'})<-[:IMPLEMENTED_BY]-(r:APIRoute) OPTIONAL MATCH (r)<-[:CONSUMES]-(f:FrontendComponent) RETURN m, r, f
```
**5. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-auth-module'})-[r]-(n) RETURN type(r) AS relType, labels(n) AS nodeLabel, n.name AS nodeName
```
**6. `run_cypher`** — ok
```cypher
MATCH path = (m:Module {name: 'legacy-auth-module'})-[:CALLS_ROUTE*1..3]->(r:APIRoute) RETURN path
```
**7. `run_cypher`** — ok
```cypher
MATCH path = (m:Module {name: 'legacy-auth-module'})-[:CALLS*1..3]->(other:Module)-[:CALLS_ROUTE]->(r:APIRoute) OPTIONAL MATCH (r)<-[:CONSUMES]-(f:FrontendComponent) RETURN m, other, r, f
```
**8. `run_cypher`** — ok
```cypher
MATCH path = (other:Module)-[:CALLS_ROUTE]->(r:APIRoute) OPTIONAL MATCH (r)<-[:CONSUMES]-(f:FrontendComponent) RETURN other.name, r.name, f.name
```
**9. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-token-validator'})<-[:IMPLEMENTED_BY]-(r:APIRoute) OPTIONAL MATCH (r)<-[:CONSUMES]-(f:FrontendComponent) RETURN m, r, f
```
**10. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-token-validator'})-[r]-(n) RETURN type(r) AS relType, labels(n) AS nodeLabel, n.name AS nodeName
```
**11. `run_cypher`** — ok
```cypher
MATCH (f:FrontendComponent)-[:CONSUMES]->(r:APIRoute)<-[:IMPLEMENTED_BY]-(m:Module) WHERE m.name IN ['legacy-auth-module', 'legacy-token-validator'] RETURN f.name AS frontendComponent, r.name AS apiRoute, m.name AS moduleName
```
**12. `run_cypher`** — ok
```cypher
MATCH (f:FrontendComponent)-[:CONSUMES]->(r:APIRoute) OPTIONAL MATCH (r)-[:IMPLEMENTED_BY]->(m:Module) RETURN f.name AS frontendComponent, r.name AS apiRoute, m.name AS moduleName
```
**13. `run_cypher`** — ok
```cypher
MATCH (m:Module {name: 'legacy-auth-module'})<-[:IMPLEMENTED_BY]-(r:APIRoute) OPTIONAL MATCH (f:FrontendComponent)-[:CONSUMES]->(r) RETURN r.name AS apiRoute, f.name AS frontendComponent
```
**14. `impact_analysis`** — ok
```json
{"target": "legacy-auth-module", "max_depth": 8}
```
**15. `detect_circular_dependencies`** — ok
```json
{"level": "service"}
```
**16. `detect_circular_dependencies`** — ok
```json
{"level": "module"}
```
**17. `find_single_points_of_failure`** — ok
```json
{"min_fan_in": 3}
```
**18. `coupling_metrics`** — ok
```json
{"level": "service", "top": 15}
```
**19. `coupling_metrics`** — ok
```json
{"level": "module", "top": 15}
```
