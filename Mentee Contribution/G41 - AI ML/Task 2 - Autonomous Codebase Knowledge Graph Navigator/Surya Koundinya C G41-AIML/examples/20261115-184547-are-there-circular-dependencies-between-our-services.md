> **Query:** Are there circular dependencies between our services?
> **Generated:** 2026-11-15 13:15 UTC · **Models:** `gemini-3.5-flash-lite` (investigate) / `gemini-3.5-flash-lite` (report) · **Grounding check:** PASSED

# Architectural Assessment: Circular Dependencies Between Services

## 1. Executive summary

- **Assessment Scope**: Evaluation of circular dependency patterns across the microservice graph topology and associated code modules.
- **Risk Level**: **HIGH**.
- **Evidence-Based Justification**: Graph analysis confirms the presence of a strongly connected component (SCC) spanning 4 core microservices (`inventory-service`, `notification-service`, `order-service`, `payment-service`) alongside a parallel module-level SCC of size 4 (`email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`). Additionally, critical infrastructure relies heavily on single points of failure such as `legacy-auth-service` (fan-in of 5) and `api-gateway` (articulation point).
- **Affected Downstream Services**: 4 microservices are directly implicated in the service-level circular dependency group.
- **Blast-Radius Interpretation**: Because these findings are derived from structural dependency graphs (`DEPENDS_ON`), blast radius calculations represent upper bounds based on hard-dependency assumptions. Graph reachability does not automatically guarantee immediate runtime failure, but indicates severe architectural coupling and coordination challenges during deployments or refactoring.

---

## 2. Scope & target resolution

- **Developer Question**: "Are there circular dependencies between our services?"
- **Graph Nodes Mapped**:
  - Service-level analysis target: All `Service` nodes connected via dependency paths.
  - Module-level analysis target: All `Module` nodes connected via internal dependency structures.
- **Graph Labels & Schema**: Schema contains `Service` (9 nodes), `Module` (10 nodes), `APIRoute` (10 nodes), `Database` (5 nodes), and `FrontendComponent` (5 nodes).
- **Assumptions**: Analysis relies on coarse, derived service-level coupling (`Service`-[:`DEPENDS_ON`]->`Service`) and fine-grained module call relationships (`Module`-[:`CALLS`]->`Module`).
- **Missing Information**: Individual cycles were not explicitly enumerated by the detection tool.

---

## 3. Affected downstream components

### 3.1 Microservices

Since the developer question queries global circular dependencies rather than a single starting target, affected services are those participating in the verified service-level strongly connected component.

| service | impact classification | why assessed | service-level distance |
| :--- | :--- | :--- | :--- |
| `order-service` | Affected (SCC Member) | Participates in service-level cycle via `order-service -> inventory-service -> notification-service -> order-service` and `order-service -> payment-service -> notification-service -> order-service` | Variable (Path dependent) |
| `inventory-service` | Affected (SCC Member) | Participates in service-level cycle via `inventory-service -> notification-service -> order-service -> inventory-service` | Variable (Path dependent) |
| `notification-service` | Affected (SCC Member) | Participates in service-level cycle via `notification-service -> order-service -> inventory-service -> notification-service` | Variable (Path dependent) |
| `payment-service` | Affected (SCC Member) | Participates in service-level cycle via `payment-service -> notification-service -> order-service -> payment-service` | Variable (Path dependent) |

*Note: Service-level distances are derived from runtime graph path traversals rather than a single fixed root.*

### 3.2 API routes

*Not applicable to this specific service-level circular dependency query scope; route-level impact analysis was not invoked.*

### 3.3 Frontend components

*Not applicable to this specific service-level circular dependency query scope; frontend component impact analysis was not invoked.*

### 3.4 Modules and data stores

#### Affected Modules

| module | owner service | module-level distance | dependency chain |
| :--- | :--- | :--- | :--- |
| `order-processing-module` | not determinable from the graph | not determinable from the graph | `order-processing-module -> payment-processor`, `order-processing-module -> stock-manager` |
| `email-dispatcher` | not determinable from the graph | not determinable from the graph | `email-dispatcher -> order-processing-module` |
| `payment-processor` | not determinable from the graph | not determinable from the graph | `payment-processor -> email-dispatcher` |
| `stock-manager` | not determinable from the graph | not determinable from the graph | `stock-manager -> email-dispatcher` |

#### Data Stores & Shared Access

*The provided evidence for circular dependencies does not list direct database access associations for the SCC members.*

### 3.5 Not affected / exclusions

The available evidence does not establish a reliable list of unaffected entities outside the reported service and module SCCs. Exclusion cannot be determined for remaining services without a broader impact sweep.

---

## 4. Architectural debt assessment

### Circular dependencies
- **Service-Level SCC**:
  - **Members**: `inventory-service`, `notification-service`, `order-service`, `payment-service`
  - **Size**: 4
  - **Internal Directed Edges**:
    - `inventory-service -> notification-service`
    - `notification-service -> order-service`
    - `order-service -> inventory-service`
    - `order-service -> payment-service`
    - `payment-service -> notification-service`
  - **Reachability Interpretation**: Every member is reachable from every other member through directed paths. This forms a strongly connected group containing multiple paths, but does not imply direct bidirectional edges between every pair of nodes. Individual cycle enumeration was not provided by the analysis. Cypher path queries confirm 6 distinct cyclical paths passing through these services.
- **Module-Level SCC**:
  - **Members**: `email-dispatcher`, `order-processing-module`, `payment-processor`, `stock-manager`
  - **Size**: 4
  - **Internal Directed Edges**:
    - `email-dispatcher -> order-processing-module`
    - `order-processing-module -> payment-processor`
    - `order-processing-module -> stock-manager`
    - `payment-processor -> email-dispatcher`
    - `stock-manager -> email-dispatcher`
  - **Reachability Interpretation**: Mirrors the service-level coupling at the code module level. Individual cycle enumeration was not provided.

### Single points of failure
Query executed with a threshold of fan-in 3:
- `legacy-auth-service`: `high fan-in (5 dependents)` (Fan-in = 5; dependents: `api-gateway`, `auth-service-v2`, `order-service`, `payment-service`, `user-service`). Component removal information is not reported (`graph_components_if_removed` is empty/absent).
- `api-gateway`: `articulation point (removal splits the service graph)` (Fan-in = 0; graph components if removed: `[7]`).

### Coupling metrics
- **Service Level**:
  - `legacy-auth-service`: $Ca = 5$, $Ce = 0$, $\text{instability} = 0.0$
  - `order-service`: $Ca = 2$, $Ce = 3$, $\text{instability} = 0.6$
  - `notification-service`: $Ca = 2$, $Ce = 1$, $\text{instability} = 0.33$
  - `payment-service`: $Ca = 1$, $Ce = 2$, $\text{instability} = 0.67$
  - `auth-service-v2`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `inventory-service`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `user-service`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `reporting-service`: $Ca = 1$, $Ce = 0$, $\text{instability} = 0.0$
  - `api-gateway`: $Ca = 0$, $Ce = 5$, $\text{instability} = 1.0$
- **Module Level**:
  - `legacy-token-validator`: $Ca = 5$, $Ce = 1$, $\text{instability} = 0.17$
  - `order-processing-module`: $Ca = 2$, $Ce = 3$, $\text{instability} = 0.6$
  - `email-dispatcher`: $Ca = 2$, $Ce = 1$, $\text{instability} = 0.33$
  - `legacy-auth-module`: $Ca = 2$, $Ce = 0$, $\text{instability} = 0.0$
  - `payment-processor`: $Ca = 1$, $Ce = 2$, $\text{instability} = 0.67$
  - `session-manager`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `stock-manager`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `user-profile-module`: $Ca = 1$, $Ce = 1$, $\text{instability} = 0.5$
  - `report-builder`: $Ca = 1$, $Ce = 0$, $\text{instability} = 0.0$
  - `gateway-router`: $Ca = 0$, $Ce = 6$, $\text{instability} = 1.0$

- **Debt Rating**: **HIGH**. The existence of multi-service and multi-module SCCs severely restricts independent deployment pipelines and increases blast radii across the commerce and notification domains.

---

## 5. Refactoring strategy (step-by-step)

To safely decouple the verified circular dependencies without disrupting runtime availability, the following phased refactoring strategy is proposed:

### Phase 1: Characterise existing behaviour and introduce contract tests
- **Goal**: Establish safety nets around the services involved in the circular dependency chain before breaking edges.
- **Concrete existing nodes involved**: `order-service`, `inventory-service`, `notification-service`, `payment-service`.
- **Proposed new artefacts**: *ContractTestsuites* (new) for boundary interactions.
- **Verification**: Run integration test suites verifying current request-response contracts across service boundaries.
- **Rollback**: Not applicable (test-only addition).

### Phase 2: Introduce an abstraction to break direct coupling
- **Goal**: Invert or mediate dependencies using an event-driven pattern or asynchronous message broker to eliminate synchronous circular edges (e.g., removing direct synchronous calls from `order-service` to `inventory-service` or `payment-service` to `notification-service`).
- **Concrete existing nodes involved**: `order-service`, `inventory-service`, `notification-service`, `payment-service`.
- **Proposed new artefacts**: *AsyncEventBusAdapter* (new).
- **Verification**: Verify via contract tests that synchronous `DEPENDS_ON` edges can be replaced with asynchronous event publication.
- **Rollback**: Revert code changes to restore direct synchronous API calls if message delivery validation fails.

### Phase 3: Coordinate changes for the strongly connected components
- **Goal**: Refactor internal module dependencies within the module SCC (`order-processing-module`, `payment-processor`, `stock-manager`, `email-dispatcher`) to remove internal cycles.
- **Concrete existing nodes involved**: `order-processing-module`, `payment-processor`, `stock-manager`, `email-dispatcher`.
- **Proposed new artefacts**: *SharedModuleInterfaceContracts* (new).
- **Verification**: Run module-level static analysis and unit tests to ensure unidirectionality of module calls.
- **Rollback**: Revert module interface definitions and reinstate prior call structures.

---

## 6. Risks, assumptions & unknowns

| type | description |
| :--- | :--- |
| **Evidence-Backed Fact** | A 4-node service SCC exists containing `inventory-service`, `notification-service`, `order-service`, and `payment-service`. |
| **Evidence-Backed Fact** | A 4-node module SCC exists containing `email-dispatcher`, `order-processing-module`, `payment-processor`, and `stock-manager`. |
| **Evidence-Backed Fact** | `legacy-auth-service` has a high fan-in of 5 dependents, and `api-gateway` acts as a graph articulation point. |
| **Assumption** | Hard-dependency assumptions apply to graph reachability; structural cycles indicate tight coupling but do not guarantee immediate runtime deadlock without traffic concurrency evidence. |
| **Unknown** | Individual exact cycles were not explicitly enumerated by the detection tool. |
| **Unknown** | Exact database access paths for the services within the service SCC are not fully detailed in the circular dependency graph tool output. |

---
## Appendix A — Evidence trail (tool calls executed)

**1. `get_schema`** — ok
**2. `find_nodes`** — ok
```json
{"text": "Are there circular dependencies between our services?"}
```
**3. `detect_circular_dependencies`** — ok
```json
{"level": "service"}
```
**4. `run_cypher`** — ok
```cypher
MATCH path = (s:Service)-[:DEPENDS_ON*]->(s) RETURN path
```
**5. `detect_circular_dependencies`** — ok
```json
{"level": "module"}
```
**6. `find_single_points_of_failure`** — ok
```json
{"min_fan_in": 3}
```
**7. `coupling_metrics`** — ok
```json
{"level": "service", "top": 15}
```
**8. `coupling_metrics`** — ok
```json
{"level": "module", "top": 15}
```
