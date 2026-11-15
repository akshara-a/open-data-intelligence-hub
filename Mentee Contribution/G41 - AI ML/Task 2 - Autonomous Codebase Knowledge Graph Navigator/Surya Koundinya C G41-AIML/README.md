# Autonomous Codebase Knowledge Graph Navigator

Natural-language question → **MCP tool-calling agent** → validated read-only **Cypher** on Neo4j →
deterministic graph reasoning (blast radius, cycles, single points of failure, coupling) →
**grounded Markdown report**.

```
 dev question ─► Agent (Gemini, provider-neutral tool-use loop) ──MCP/stdio──► kgnav.mcp_server ──► Neo4j (READ only)
                      │                                         ├ get_schema / find_nodes
                      │                                         ├ run_cypher  (guard + read tx + timeout + row cap)
                      │                                         ├ impact_analysis (blast radius + debt signals)
                      │                                         └ detect_circular_dependencies / find_single_points_of_failure / coupling_metrics
                      ▼
        evidence ledger ─► Synthesis LLM ─► Grounding verifier (every `identifier` must exist in evidence; auto-retry)
                                              ▼
                                   reports/<timestamp>-<slug>.md  (+ Cypher/evidence appendix)
```

## Requirement → implementation

| Requirement | Where |
|---|---|
| MCP tool integration | `src/kgnav/mcp_server.py` (FastMCP, stdio); the agent is an MCP client in `agent.py` |
| Safe DB access | `cypher_guard.py` (static validation) + `neo4j_client.py` (READ_ACCESS session, managed read transaction, timeout, row cap) |
| NL → Cypher + retrieval | The LLM calls `get_schema`, `find_nodes`, `run_cypher`; errors are returned as data so it can self-correct |
| Reasoning engine | `analysis.py` (reverse reachability, Tarjan SCC, articulation points, Ca/Ce/instability) |
| Generative synthesis | `agent.py::_synthesize` + `prompts.py` |
| No hallucination | `grounding.py` verifies every backticked entity against tool evidence; retries, otherwise flags it in the report |
| Exact-target safety | `agent.py::_mandatory_postflight` + `TargetNotFoundError`: impact analysis never runs for an unresolved target |
| Report content | Affected services / routes / components, architectural debt assessment, phased refactoring plan (`prompts.SYNTH_SYSTEM`) |

## Setup (macOS, Apple Silicon, VS Code)

```bash
brew install python@3.12 git
brew install --cask docker          # or: brew install orbstack
make setup && cp .env.example .env  # then add GEMINI_API_KEY from Google AI Studio
make up                             # Neo4j at http://localhost:7474 (neo4j / kgnav-password)
make seed                           # loads the demo graph
make test
kgnav doctor                        # verifies key, model IDs and Neo4j
make demo
```

Run `code .` and select the interpreter `.venv/bin/python`.
Debug via **Run and Debug → "kgnav: ask (demo)"**.

> If `kgnav` ever behaves differently from `pytest`, make sure it runs this project's code:
> `python -c "import kgnav; print(kgnav.__file__)"` must print a path under `src/kgnav`.
> If not, run `pip uninstall -y kgnav && pip install -e ".[dev]"`.

## LLM provider: Gemini free tier

The agent talks to models through a small provider interface (`src/kgnav/llm/`), so the MCP, Neo4j,
reasoning and grounding layers are vendor-neutral. The included adapter is Google Gemini (Developer API, REST).

```bash
# .env
KGNAV_PROVIDER=gemini
GEMINI_API_KEY=...                              # https://aistudio.google.com/apikey
KGNAV_MODEL_INVESTIGATE=gemini-3.5-flash-lite   # many small tool-use calls
KGNAV_MODEL_SYNTH=gemini-3.5-flash-lite         # 2-3 calls to write the report (a stronger Flash model improves prose if quota allows)
```

Run `kgnav doctor` first: it checks the key, confirms both model IDs exist **for your key**, and pings Neo4j.

**Free-tier notes** (check your own limits at https://aistudio.google.com/rate-limit):
- Quotas are per model and per project. One question costs roughly 8-20 requests; the full eval (4 questions) roughly 60.
- The adapter retries 429/5xx using the server's suggested delay, fails fast with a clear message when the
  *daily* quota is gone, and supports `GEMINI_MIN_INTERVAL_S` to pace requests.
- `gemini-2.5-flash` / `2.5-pro` are deprecated (shutdown set for 2026-12-01): do not use them.
- **Privacy:** free-tier prompts may be used by Google to improve its products. The demo graph is synthetic;
  do not point this at a proprietary codebase graph on the free tier.

## Use

```bash
kgnav ask "If I deprecate the legacy-auth-module, which downstream API routes and frontend components will break?" -v --print
kgnav ask "Are there circular dependencies between our services?"
kgnav ask "Which services are single points of failure?"
kgnav ask "What is impacted if we change the schema of orders-db?"
```

Reports are written to `reports/<timestamp>-<slug>.md` with an evidence appendix listing every tool call and Cypher query.

## Target resolution (safety behaviour)

Impact questions that propose changing a component (deprecate, remove, delete, change, migrate)
must name an **exact graph node**. The agent never guesses between fuzzy matches.

```
$ kgnav ask "What happens if I deprecate nonexistent-payment-service?"

KG Navigator — Target validation failed
Status: TARGET NOT FOUND
Requested target: nonexistent-payment-service
Graph verification: No exact matching node was found.
Possible matches (not selected automatically): payment-service, payment-processor, ...
Impact analysis: NOT EXECUTED
Report: NOT GENERATED
```

- Exit code is `2`, and **no report is written**.
- Suggestions are informational only and are never passed to `impact_analysis`.
- Natural-language names that are not exact node names (for example "the legacy authentication module")
  are treated the same way: use the exact name, here `legacy-auth-module`.
- Architecture-wide questions that name no component and propose no change (for example
  "Are there circular dependencies between our services?") need no target. They run the independent
  architecture analysis (cycles, single points of failure, coupling) without a single-target impact step.

## Testing and evaluation

```bash
pytest -q                    # 85 tests: Cypher guard, MCP server, analysis, grounding, agent recovery, Gemini adapter
python eval/run_eval.py      # golden-set evaluation against the live seeded graph (needs Neo4j + GEMINI_API_KEY)
```

The golden set (`eval/golden.json`) has four questions. Each case checks that:
1. every required entity appears in the report (`must_include`);
2. forbidden entities are not **claimed** as affected or as part of a cycle (`must_not_include`);
3. the grounding check found no invented identifiers;
4. no Cypher executed by the agent was blocked as unsafe.

`must_not_include` is checked only in claim-bearing sections (affected components, circular dependencies).
Entities may legitimately be named in coupling-metric tables or "Not affected" lists, so those are not counted as claims.

The eval is a regression check, not a proof of correctness. LLM wording varies between runs, so an
occasional borderline failure is possible; re-run before drawing conclusions.

**Latest verified results:** 85 tests passed; golden-set eval 4/4.

## Verifying a report against the live graph

Run these in Neo4j Browser (http://localhost:7474) and compare with the report.

```cypher
// Blast radius of legacy-auth-module, grouped by node type
MATCH (t:Module {name:'legacy-auth-module'})
MATCH (d)-[:CALLS|IMPLEMENTED_BY|CALLS_ROUTE|CONSUMES|READS_FROM|WRITES_TO*1..]->(t)
RETURN labels(d)[0] AS type, collect(DISTINCT d.name) AS names ORDER BY type;

// Service-level cycles
MATCH p=(a:Service)-[:DEPENDS_ON*2..6]->(a)
RETURN DISTINCT [n IN nodes(p) | n.name] AS cycle LIMIT 10;

// Fan-in (single-point-of-failure candidates)
MATCH (s:Service)<-[:DEPENDS_ON]-(x)
RETURN s.name, count(DISTINCT x) AS fan_in ORDER BY fan_in DESC;
```

Expected on the demo graph:
- **Blast radius of `legacy-auth-module`:** 9 API routes, 4 frontend components, 8 modules, no databases.
- **Cycles:** only `order-service`, `inventory-service`, `notification-service` and `payment-service`
  (two distinct cycles through `notification-service`).
- **Fan-in:** `legacy-auth-service` is highest with 5; `order-service` and `notification-service` follow with 2.

The latest legacy-auth report matched the live graph on all 29 affected items
(9 routes, 4 frontend components, 8 modules, 8 services).

## When Gemini is overloaded (503) or out of quota

- Transient 429/5xx errors are retried with exponential backoff and jitter (`GEMINI_MAX_RETRIES`).
- If the report model stays unavailable, the agent tries `KGNAV_SYNTH_FALLBACKS`
  (default: the investigation model).
- Graph evidence is **checkpointed** to `reports/.checkpoints/*.json` right after the investigation.
  If report generation still fails, nothing is lost: run `kgnav resume` (newest checkpoint) or
  `kgnav resume <file>` to redo only the report step. No Neo4j/MCP work is repeated.
- `GEMINI_MIN_INTERVAL_S` paces requests and helps with 429 (rate limit); it does not help 503 (server capacity).

## Using your own graph

Edit `src/kgnav/schema.py` (labels, relationship names; direction = "depends on").
Everything else adapts via `get_schema`.

## Read-only hardening

Layers: Cypher guard → READ_ACCESS session → (recommended) database level.
Neo4j Community has no RBAC; after seeding you can set `server.databases.default_to_read_only=true`.
On Enterprise, create a `reader` role and use that user in `.env`.

## Security

- `.env` holds your API key and database password. It is listed in `.gitignore`: never commit it or include it in a zip.
- If a key was ever shared or committed by accident, revoke it and generate a new one.
- Share `.env.example` instead.

## Plug the MCP server into other clients

```json
{"mcpServers":{"codebase-graph":{"command":"/abs/path/.venv/bin/python","args":["-m","kgnav.mcp_server"],"env":{"NEO4J_URI":"bolt://localhost:7687","NEO4J_USER":"neo4j","NEO4J_PASSWORD":"kgnav-password"}}}}
```

## Notes and limits

- Blast radius is an upper bound (it assumes hard dependencies).
- The graph is static analysis only: runtime fallbacks, feature flags and traffic volume are not visible.
- Reports are grounded in graph evidence; the grounding check covers backticked identifiers,
  so read the refactoring plan with normal engineering judgement.