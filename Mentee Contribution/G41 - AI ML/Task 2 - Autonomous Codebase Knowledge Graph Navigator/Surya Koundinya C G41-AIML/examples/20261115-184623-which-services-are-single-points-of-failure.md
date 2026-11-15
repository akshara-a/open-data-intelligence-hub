> **Query:** Which services are single points of failure?
> **Generated:** 2026-11-15 13:16 UTC · **Models:** `gemini-3.5-flash-lite` (investigate) / `gemini-3.5-flash-lite` (report) · **Grounding check:** PASSED

# Architectural Single Points of Failure & Dependency Analysis Report

## 1. Executive summary

This report assesses microservice single points of failure (SPOFs) and structural dependencies based on graph database evidence.

- **Assessed Question:** Which services are single points of failure?
- **Risk Level:** **HIGH**
- **Evidence-Based Justification:** The graph identifies `legacy-auth-service` with a high fan-in of 5 dependents (`api-gateway`, `auth-service-v2`, `order-service`, `payment-service`, `user-service`), making it a critical dependency bottleneck across the architecture. Additionally, `api-gateway` is identified as an articulation point whose removal splits the service graph.
- **Blast Radius Note:** The analysis of global SPOFs indicates structural vulnerabilities across multiple dependent services, though runtime failure depends on operational configurations and traffic patterns not captured purely in static graph topologies.

## 2. Scope & target resolution

- **Developer Question:** Which services are single points of failure?
- **Graph Nodes Mapped:** Global service inventory and structural coupling analysis (`Service` label).
- **Target's Graph Label:** `Service` (with properties `name`, `team`, `tier`, `language`, `deprecated`).
- **Tool Configuration:** The SPOF detection tool was executed with a configured threshold of `min_fan_in` set to `3`. A complementary Cypher query evaluated service fan-in across all `9` services in the graph schema (`Service` count = `9`, `Module` count = `10`, `APIRoute` count = `10`, `Database` count = `5`, `FrontendComponent` count = `5`).
- **Impact-Analysis Assumptions:** Graph connectivity assumes coarse, derived service-level coupling via `(Service)-[:DEPENDS_ON]->(Service)` relationships (`14` total counts in schema).
- **Missing Information:** Individual runtime failure probabilities, network partition behaviors, and asynchronous message queue topologies are not determinable from the graph.

## 3. Affected downstream components

*Note: The primary query investigates structural SPOFs across the service graph rather than an isolated single-service impact radius. Consequently, downstream dependencies for the identified SPOFs are detailed via global fan-in and dependency metrics.*

### 3.1 Microservices

The following table summarizes service-level fan-in and dependents across the architecture, as established by the global Cypher query and SPOF analysis:

| service | impact classification | why affected | service-level distance |
| :--- | :--- | :--- | :--- |
| `legacy-auth-service` | SPOF (High Fan-In) | High fan-in (5 dependents: `user-service`, `api-gateway`, `auth-service-v2`, `payment-service`, `order-service`) | Not determinable from the graph (global metric) |
| `api-gateway` | SPOF (Articulation Point) | Articulation point (removal splits the service graph into `[7]` components) | Not determinable from the graph (global metric) |
| `order-service` | Dependent / High Fan-In | 2 dependents (`api-gateway`, `notification-service`) | Not determinable from the graph (global metric) |
| `notification-service` | Dependent / High Fan-In | 2 dependents (`inventory-service`, `payment-service`) | Not determinable from the graph (global metric) |
| `auth-service-v2` | Dependent | 1 dependent (`api-gateway`) | Not determinable from the graph (global metric) |
| `user-service` | Dependent | 1 dependent (`api-gateway`) | Not determinable from the graph (global metric) |
| `inventory-service` | Dependent | 1 dependent (`order-service`) | Not determinable from the graph (global metric) |
| `payment-service` | Dependent | 1 dependent (`order-service`) | Not determinable from the graph (global metric) |
| `reporting-service` | Dependent | 1 dependent (`api-gateway`) | Not determinable from the graph (global metric) |

### 3.2 API routes

- Not directly scoped within the global SPOF tool output. (Schema contains `10` `APIRoute` nodes and `10` `EXPOSES` relationships).

### 3.3 Frontend components

- Not directly scoped within the global SPOF tool output. (Schema contains `5` `FrontendComponent` nodes and `7` `CONSUMES` relationships).

### 3.4 Modules and data stores

#### Affected Modules
- Module-level impact details are not determinable from the global service SPOF query results. (Schema contains `10` `Module` nodes and `14` `CALLS_ROUTE` relationships).

#### Data Stores & Shared Access
- Data store access details are not determinable from the global service SPOF query results. (Schema contains `5` `Database` nodes, `5` `WRITES_TO` relationships, and `2` `READS_FROM` relationships).

### 3.5 Not affected / exclusions

- The available evidence does not establish a reliable list of unaffected entities, as the analysis evaluated global structural single points of failure rather than an isolated target blast radius.

## 4. Architectural debt assessment

### Circular dependencies
- Module-level or service-level circular dependency paths were not explicitly returned by the evaluated tools. Individual cycle enumeration was not provided by the analysis.

### Single points of failure
The SPOF detection tool and Cypher validation identified two distinct structural single points of failure:
1. `legacy-auth-service`:
   - **Reason:** `high fan-in (5 dependents)`
   - **Fan-in:** `5`
   - **Dependents:** `api-gateway`, `auth-service-v2`, `order-service`, `payment-service`, `user-service`
   - **Graph components if removed:** Not applicable (reported as empty/omitted in tool output)
2. `api-gateway`:
   - **Reason:** `articulation point (removal splits the service graph)`
   - **Fan-in:** `0`
   - **Dependents:** None (`[]`)
   - **Graph components if removed:** `[7]`

*Distinction:* High fan-in (`legacy-auth-service`) and articulation-point status (`api-gateway`) represent different structural properties. High fan-in measures incoming dependency count, whereas an articulation point measures graph connectivity criticality (whose removal fragments graph components).

### Shared-database / hidden coupling
- Not determinable from the graph evidence provided for this query.

### Deprecated nodes still referenced
- The schema indicates support for a `deprecated` property on `Service` and `Module` nodes, but specific deprecated status flags for the SPOF nodes are not asserted in the SPOF tool output.

### Coupling metrics
- Global service fan-in distribution ranges from `0` (`api-gateway`) to `5` (`legacy-auth-service`). These metrics indicate severe structural centralization around authentication infrastructure and entry gateways.

**Debt Rating:** **HIGH**
**Prioritised Findings:**
1. `legacy-auth-service` represents a severe architectural bottleneck due to broad cross-service dependency (`5` dependents).
2. `api-gateway` represents a critical structural articulation point; its failure or removal partitions the service graph (`[7]` components if removed).

## 5. Refactoring strategy (step-by-step)

*Note: The following refactoring steps are engineering proposals designed to mitigate single points of failure. They are not established graph facts.*

### Step 1: Characterise existing behaviour and introduce contract tests
- **Goal:** Establish a baseline for interactions dependent on `legacy-auth-service` and `api-gateway`.
- **Concrete existing graph nodes involved:** `legacy-auth-service`, `api-gateway`, and all 5 dependent services (`user-service`, `auth-service-v2`, `payment-service`, `order-service`, `api-gateway`).
- **Proposed new artefacts:** *Contract test suite* (new), *Consumer-driven contract definitions* (new).
- **Verification:** Execute contract verification tests across all dependent callers.
- **Rollback:** Revert test configurations without altering runtime routing.

### Step 2: Identify and validate an approved replacement
- **Goal:** Define and validate a decentralized or redundant authentication mechanism to reduce reliance on `legacy-auth-service`.
- **Concrete existing graph nodes involved:** `legacy-auth-service`, `auth-service-v2`.
- **Proposed new artefacts:** *Authentication validation harness* (new).
- **Verification:** Verify parity of token validation and authorization logic.
- **Rollback:** Maintain `legacy-auth-service` as primary authority during validation.

### Step 3: Introduce an abstraction layer / facade
- **Goal:** Decouple direct service dependencies on `legacy-auth-service` by routing calls through a unified interface.
- **Concrete existing graph nodes involved:** `legacy-auth-service` and its dependents.
- **Proposed new artefacts:** *AuthFacade* (new).
- **Verification:** Monitor call routing through the new abstraction layer via integration tests.
- **Rollback:** Bypass *AuthFacade* (new) and revert direct calls to `legacy-auth-service`.

### Step 4: Migrate direct consumers iteratively
- **Goal:** Transition dependent services (`user-service`, `order-service`, `payment-service`, `auth-service-v2`, `api-gateway`) away from hard dependency on `legacy-auth-service` using verified dependency chains.
- **Concrete existing graph nodes involved:** `legacy-auth-service`, `api-gateway`, `user-service`, `order-service`, `payment-service`, `auth-service-v2`.
- **Proposed new artefacts:** None.
- **Verification:** Verify zero drop in successful authorization handshakes per migrating service.
- **Rollback:** Point service configuration back to `legacy-auth-service`.

## 6. Risks, assumptions & unknowns

| type | description |
| :--- | :--- |
| **Evidence-Backed Fact** | `legacy-auth-service` has a fan-in of 5 dependents (`api-gateway`, `auth-service-v2`, `order-service`, `payment-service`, `user-service`). |
| **Evidence-Backed Fact** | `api-gateway` is an articulation point whose removal splits the service graph into `[7]` components. |
| **Assumption** | Hard dependency assumptions (`DEPENDS_ON`) reflect structural coupling risks, though runtime failure is not guaranteed solely by graph connectivity. |
| **Unknown** | Individual runtime failure probabilities, asynchronous messaging decoupling, and actual network traffic volumes are not determinable from the graph. |
| **Unknown** | Complete cycle enumeration and module-level dependency chains were not provided in the tool output. |

---
## Appendix A — Evidence trail (tool calls executed)

**1. `get_schema`** — ok
**2. `find_nodes`** — ok
```json
{"text": "Which services are single points of failure?"}
```
**3. `find_single_points_of_failure`** — ok
**4. `run_cypher`** — ERROR
```cypher

```
**5. `run_cypher`** — ok
```cypher
MATCH (s:Service) OPTIONAL MATCH (s)<-[r:DEPENDS_ON]-(d:Service) RETURN s.name AS service, count(d) AS fanIn, collect(d.name) AS dependents ORDER BY fanIn DESC
```
