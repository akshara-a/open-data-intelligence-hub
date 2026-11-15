> **Query:** What is impacted if we change the schema of orders-db?
> **Generated:** 2026-11-15 13:17 UTC · **Models:** `gemini-3.5-flash-lite` (investigate) / `gemini-3.5-flash-lite` (report) · **Grounding check:** PASSED

# Impact Analysis Report: Schema Change for `orders-db`

## 1. Executive summary

This technical report assesses the downstream architectural impact of modifying the schema of `orders-db`.

- **Risk Level:** **HIGH**
- **Evidence-Based Justification:** The change affects 6 microservices (`api-gateway`, `inventory-service`, `notification-service`, `order-service`, `payment-service`, and `reporting-service`), 6 code modules, 6 API routes, and 3 frontend components. Furthermore, the impact radius intersects with a strongly connected service component (SCC) comprising `inventory-service`, `notification-service`, `order-service`, and `payment-service`, creating significant coordination requirements for any schema migration.
- **Affected Downstream Services:** 6 services are explicitly identified in the impact analysis.
- **Blast Radius Assumption:** The blast radius represents an upper bound based on the hard-dependency assumption (assuming each dependency is a hard runtime dependency with no fallback or circuit breaker).
- **Runtime Failure Notice:** This analysis establishes graph reachability and structural dependency, not guaranteed runtime failure.

---

## 2. Scope & target resolution

- **Developer Question:** What is impacted if we change the schema of `orders-db`?
- **Graph Node Mapping:** Maps to the `Database` node `orders-db`.
- **Target's Graph Label:** `Database`
- **Owner Information:** Owner services list is empty.
- **Impact Analysis Assumptions:** Upper bound assuming each dependency is a hard runtime dependency.
- **Missing Information:** Individual cycles within the strongly connected components were not enumerated by the analysis.

---

## 3. Affected downstream components

### 3.1 Microservices

| Service | Impact Classification | Why Affected | Service-level distance |
| :--- | :--- | :--- | :--- |
| `order-service` | Affected (Direct) | Owns module directly accessing `orders-db` | not determinable from the graph |
| `reporting-service` | Affected (Direct) | Owns module directly accessing `orders-db` | not determinable from the graph |
| `api-gateway` | Affected (Transitive) | Depends via API route / module chain | not determinable from the graph |
| `notification-service` | Affected (Transitive) | Depends via API route / module chain | not determinable from the graph |
| `inventory-service` | Affected (Transitive) | Depends via API route / module chain | not determinable from the graph |
| `payment-service` | Affected (Transitive) | Depends via API route / module chain | not determinable from the graph |

*Note on Service Distances:* Downstream service distances and propagated service distances returned empty in the impact analysis tool output.

### 3.2 API routes

| Route | Owner Service | Route-level distance | Dependency Chain |
| :--- | :--- | :--- | :--- |
| `GET /orders/{id}` | `order-service` | 2 | `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |
| `GET /reports/sales` | `reporting-service` | 2 | `GET /reports/sales` -> `report-builder` -> `orders-db` |
| `POST /orders` | `order-service` | 2 | `POST /orders` -> `order-processing-module` -> `orders-db` |
| `POST /notifications/send` | `notification-service` | 4 | `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |
| `POST /inventory/reserve` | `inventory-service` | 6 | `POST /inventory/reserve` -> `stock-manager` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |
| `POST /payments/charge` | `payment-service` | 6 | `POST /payments/charge` -> `payment-processor` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |

### 3.3 Frontend components

| Component | Component-level distance | Dependency Chain | Owner service if known |
| :--- | :--- | :--- | :--- |
| `admin-dashboard` | 3 | `admin-dashboard` -> `GET /reports/sales` -> `report-builder` -> `orders-db` | not established |
| `customer-portal` | 3 | `customer-portal` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` | not established |
| `web-checkout-page` | 3 | `web-checkout-page` -> `POST /orders` -> `order-processing-module` -> `orders-db` | not established |

### 3.4 Modules and data stores

#### Affected Modules

| Module | Owner Service | Module-level distance | Dependency Chain |
| :--- | :--- | :--- | :--- |
| `order-processing-module` | `order-service` | 1 | `order-processing-module` -> `orders-db` |
| `report-builder` | `reporting-service` | 1 | `report-builder` -> `orders-db` |
| `email-dispatcher` | `notification-service` | 3 | `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |
| `gateway-router` | `api-gateway` | 3 | `gateway-router` -> `POST /orders` -> `order-processing-module` -> `orders-db` |
| `payment-processor` | `payment-service` | 5 | `payment-processor` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |
| `stock-manager` | `inventory-service` | 5 | `stock-manager` -> `POST /notifications/send` -> `email-dispatcher` -> `GET /orders/{id}` -> `order-processing-module` -> `orders-db` |

#### Data Stores & Shared Access

| Database | Accessor Module | Access type |
| :--- | :--- | :--- |
| `orders-db` | `report-builder` | `READS_FROM` |
| `orders-db` | `order-processing-module` | `WRITES_TO` |

*(No distance value is assigned to `orders-db` as database nodes do not carry blast-radius distance metrics in the evidence).*

### 3.5 Not affected / exclusions

The available evidence does not establish a reliable list of unaffected entities. Entities not listed in the impact results cannot be confirmed as unaffected based solely on their absence.

---

## 4. Architectural debt assessment

### Circular dependencies
- **Service-Level SCC:** The impact analysis and service-level circular dependency detection reveal 1 strongly connected component (size 4) containing:
  - Members: `inventory-service`, `notification-service`, `order-service`, `payment-service`.
  - Internal directed edges:
    - `inventory-service -> notification-service`
    - `notification-service -> order-service`
    - `order-service -> inventory-service`
    - `order-service -> payment-service`
    - `payment-service -> notification-service`
  - *Architectural Interpretation:* Every member is reachable from every other member through directed paths. This tight coupling means schema changes impacting `order-service` can propagate across the entire SCC group, requiring coordinated changes or dependency-breaking steps.
  - *Note:* Individual cycle enumeration was not provided by the analysis.
- **Module-Level SCC:** Module-level circular dependency detection reveals 1 strongly connected component (size 4) containing:
  - Members: `email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`.
  - Internal directed edges:
    - `email-dispatcher -> order-processing-module`
    - `order-processing-module -> payment-processor`
    - `order-processing-module -> stock-manager`
    - `payment-processor -> email-dispatcher`
    - `stock-manager -> email-dispatcher`
  - *Note:* Individual cycle enumeration was not provided.

### Single points of failure
- **In-Radius SPOF:** `api-gateway` is identified in the impact radius with the reason articulation point (removal splits the service graph).
- **Global SPOF (Query Threshold `min_fan_in=1`):** A global query returned multiple nodes with high fan-in, including `legacy-auth-service`, `order-service`, `notification-service`, `payment-service`, `auth-service-v2`, `inventory-service`, `user-service`, `reporting-service`, and `api-gateway`.
  - *Context Note:* These global findings operate outside the strict impact radius except where overlapping with affected nodes (such as `order-service`, `notification-service`, `payment-service`, `inventory-service`, and `reporting-service`).

### Shared-database / hidden coupling
- `orders-db` is accessed by `report-builder` (`READS_FROM`) and `order-processing-module` (`WRITES_TO`). No other hidden shared-database coupling entries were returned in `debt_signals`.

### Deprecated nodes still referenced
- No deprecated nodes were reported in scope.

### Coupling metrics
- **Service Level:**
  - `legacy-auth-service`: $Ca = 5, Ce = 0, Instability = 0.0$
  - `order-service`: $Ca = 2, Ce = 3, Instability = 0.6$
  - `notification-service`: $Ca = 2, Ce = 1, Instability = 0.33$
  - `payment-service`: $Ca = 1, Ce = 2, Instability = 0.67$
  - `api-gateway`: $Ca = 0, Ce = 5, Instability = 1.0$
- **Module Level:**
  - `legacy-token-validator`: $Ca = 5, Ce = 1, Instability = 0.17$
  - `order-processing-module`: $Ca = 2, Ce = 3, Instability = 0.6$
- *Interpretation:* High efferent coupling ($Ce$) and instability in `order-service` and `order-processing-module` indicate high susceptibility to upstream/downstream changes, though metrics do not prove runtime failure.

### Debt Rating & Priorised Findings
- **Architectural Debt Rating:** HIGH (driven by service-level and module-level SCCs coupled with broad fan-out to 6 microservices).
- **Prioritised Findings:**
  1. Direct database writes by `order-processing-module` (`order-service`) and reads by `report-builder` (`reporting-service`).
  2. Four-service service-level SCC (`inventory-service`, `notification-service`, `order-service`, `payment-service`).
  3. Four-module module-level SCC (`email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`).

---

## 5. Refactoring strategy (step-by-step)

*Note: The following steps are proposed engineering recommendations to safely manage the schema migration given the complex dependency chains and SCC memberships.*

### Step 1: Characterise existing behaviour and introduce contract tests
- **Goal:** Establish baseline behavior for data reads and writes against `orders-db`.
- **Concrete existing graph nodes involved:** `orders-db`, `order-processing-module`, `report-builder`, `GET /orders/{id}`, `POST /orders`, `GET /reports/sales`.
- **Proposed new artefacts:** *DataContractTestSuite* (new).
- **Verification:** Execute contract tests against current database schema to verify input/output payloads.
- **Rollback:** Revert test suite additions if test harness fails.

### Step 2: Introduce a data access abstraction / database facade
- **Goal:** Decouple direct module SQL/ORM dependencies from the underlying table structure.
- **Concrete existing graph nodes involved:** `order-processing-module`, `report-builder`, `orders-db`.
- **Proposed new artefacts:** *OrdersDataFacade* (new).
- **Verification:** Verify that modules route persistence and query calls through *OrdersDataFacade* (new) without altering direct database connectivity prior to migration.
- **Rollback:** Remove *OrdersDataFacade* (new) and restore direct queries.

### Step 3: Migrate direct consumers (`order-service` and `reporting-service`)
- **Goal:** Update direct database accessors to handle the new schema version via backward-compatible views or dual-writing strategies.
- **Concrete existing graph nodes involved:** `order-service`, `reporting-service`, `order-processing-module`, `report-builder`, `orders-db`.
- **Proposed new artefacts:** *SchemaAdapter* (new).
- **Verification:** Run integration tests on `order-processing-module` and `report-builder` against a staging instance of `orders-db`.
- **Rollback:** Roll back module deployments and revert *SchemaAdapter* (new) mappings.

### Step 4: Coordinate changes across the strongly connected components (SCCs)
- **Goal:** Safely manage schema-dependent propagation across the service-level SCC (`inventory-service`, `notification-service`, `order-service`, `payment-service`) and module-level SCC (`email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`).
- **Concrete existing graph nodes involved:** `inventory-service`, `notification-service`, `order-service`, `payment-service`, `email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`.
- **Proposed new artefacts:** None.
- **Verification:** Perform end-to-end integration tests tracing flows from `api-gateway` through `order-service` down to `payment-service` and `inventory-service`.
- **Rollback:** Halt downstream service deployments and failover to previous transaction boundaries.

### Step 5: Migrate transitive consumers and validate cutover
- **Goal:** Ensure all transitive API routes (`GET /orders/{id}`, `POST /orders`, `GET /reports/sales`, `POST /notifications/send`, `POST /inventory/reserve`, `POST /payments/charge`) and frontend components (`admin-dashboard`, `customer-portal`, `web-checkout-page`) function correctly under the new schema.
- **Concrete existing graph nodes involved:** All 6 affected microservices, their corresponding APIRoutes, and FrontendComponents (`admin-dashboard`, `customer-portal`, `web-checkout-page`).
- **Proposed new artefacts:** None.
- **Verification:** Comprehensive end-to-end UI and API regression testing.
- **Rollback:** Switch database read/write pointers back to legacy schema snapshot and roll back client services.

---

## 6. Risks, assumptions & unknowns

| Type | Description |
| :--- | :--- |
| **Evidence-backed fact** | 6 microservices, 6 modules, 6 API routes, and 3 frontend components are in the impact radius of `orders-db`. |
| **Evidence-backed fact** | Service-level SCC exists containing `inventory-service`, `notification-service`, `order-service`, and `payment-service`. |
| **Evidence-backed fact** | Module-level SCC exists containing `email-dispatcher`, `order-processing-module`, `payment-processor`, and `stock-manager`. |
| **Assumption** | Upper bound assumption: each dependency is a hard runtime dependency with no fallback or circuit breaker. |
| **Risk** | High coupling and circular dependencies across services and modules amplify the risk of cascading failures during schema modification. |
| **Unknown** | Individual cycles within the strongly connected components were not enumerated by the analysis. |
| **Unknown** | Service-level distances and owner service information for frontend components (`admin-dashboard`, `customer-portal`, `web-checkout-page`) are not determinable from the graph. |

---
## Appendix A — Evidence trail (tool calls executed)

**1. `get_schema`** — ok
**2. `find_nodes`** — ok
```json
{"text": "What is impacted if we change the schema of orders-db?"}
```
**3. `impact_analysis`** — ok
```json
{"target": "orders-db"}
```
**4. `run_cypher`** — ok
```cypher
MATCH (m:Module)-[r:READS_FROM|WRITES_TO]->(db:Database {name: 'orders-db'}) RETURN m.name, type(r), db.name
```
**5. `detect_circular_dependencies`** — ok
```json
{"level": "service"}
```
**6. `detect_circular_dependencies`** — ok
```json
{"level": "module"}
```
**7. `find_single_points_of_failure`** — ok
```json
{"min_fan_in": 1}
```
**8. `coupling_metrics`** — ok
```json
{"level": "service", "top": 10}
```
**9. `coupling_metrics`** — ok
```json
{"level": "module", "top": 10}
```
**10. `find_single_points_of_failure`** — ok
```json
{"min_fan_in": 3}
```
**11. `coupling_metrics`** — ok
```json
{"level": "service", "top": 15}
```
**12. `coupling_metrics`** — ok
```json
{"level": "module", "top": 15}
```
