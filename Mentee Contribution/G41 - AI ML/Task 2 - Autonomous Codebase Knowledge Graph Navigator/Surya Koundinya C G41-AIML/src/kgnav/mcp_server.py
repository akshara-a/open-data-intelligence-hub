
"""MCP server exposing safe, read-only graph tools over stdio.

Run standalone: python -m kgnav.mcp_server

(The agent spawns it automatically; it can also be plugged into
Claude Desktop / Claude Code.)
"""
from __future__ import annotations

import functools
import json
import re
from collections import deque

from mcp.server.fastmcp import FastMCP

from .analysis import (
    blast_radius,
    coupling_metrics,
    find_cycles,
    single_points_of_failure,
)
from .config import load_config
from .graph_data import (
    fetch_dependency_edges,
    fetch_module_pairs,
    fetch_service_pairs,
)
from .neo4j_client import GraphClient
from .schema import SCHEMA_GUIDE


mcp = FastMCP("codebase-graph")

_client: GraphClient | None = None


def graph() -> GraphClient:
    global _client

    if _client is None:
        _client = GraphClient(load_config())

    return _client


def safe(fn):
    """Return tool errors to the LLM as data so it can self-correct."""

    @functools.wraps(fn)
    def wrapper(*a, **k):
        try:
            return json.dumps(fn(*a, **k), default=str, indent=1)
        except Exception as e:  # noqa: BLE001
            return json.dumps(
                {
                    "error": type(e).__name__,
                    "message": str(e)[:1500],
                    "hint": (
                        "Fix the input/Cypher and retry. "
                        "Only read-only, single-statement Cypher is allowed."
                    ),
                }
            )

    return wrapper


# ---------------------------------------------------------------------------
# Service-level downstream dependency propagation


def downstream_service_distances(
    pairs: list[tuple[str, str]],
    targets: set[str],
) -> dict[str, int]:
    """Return shortest DEPENDS_ON distance from target services.

    DEPENDS_ON direction:

        (dependent)-[:DEPENDS_ON]->(dependency)

    Reverse traversal therefore finds dependent services.

    Distances count Service-to-Service DEPENDS_ON relationships only.
    Target services are excluded from the returned mapping.
    """
    reverse: dict[str, set[str]] = {}

    for dependent, dependency in pairs:
        reverse.setdefault(dependency, set()).add(dependent)

    distances: dict[str, int] = {}
    visited = set(targets)
    queue = deque((target, 0) for target in sorted(targets))

    while queue:
        current, distance = queue.popleft()

        for dependent in sorted(reverse.get(current, set())):
            if dependent in visited:
                continue

            visited.add(dependent)
            distances[dependent] = distance + 1
            queue.append((dependent, distance + 1))

    return distances


def downstream_services(
    pairs: list[tuple[str, str]],
    targets: set[str],
) -> set[str]:
    """Find services that transitively depend on target services.

    DEPENDS_ON direction:

        (dependent)-[:DEPENDS_ON]->(dependency)

    Therefore, reverse traversal finds services affected when a
    dependency service is changed or removed.
    """
    reverse: dict[str, set[str]] = {}

    for dependent, dependency in pairs:
        reverse.setdefault(dependency, set()).add(dependent)

    affected: set[str] = set()
    visited = set(targets)
    queue = deque(targets)

    while queue:
        current = queue.popleft()

        for dependent in reverse.get(current, set()):
            if dependent in visited:
                continue

            visited.add(dependent)
            affected.add(dependent)
            queue.append(dependent)

    return affected


# ---------------------------------------------------------------------------
# Schema


@mcp.tool()
@safe
def get_schema() -> dict:
    """Return the live graph schema.

    Includes labels, properties, relationship patterns and direction guide.
    ALWAYS call this first.
    """
    g = graph()

    labels = g.query(
        "MATCH (n) "
        "UNWIND labels(n) AS label "
        "RETURN label, count(*) AS count "
        "ORDER BY count DESC"
    )

    props = g.query(
        "MATCH (n) "
        "WITH labels(n)[0] AS label, n "
        "UNWIND keys(n) AS k "
        "RETURN label, collect(DISTINCT k) AS properties"
    )

    patterns = g.query(
        "MATCH (a)-[r]->(b) "
        "RETURN labels(a)[0] AS src, "
        "type(r) AS rel, "
        "labels(b)[0] AS dst, "
        "count(*) AS count "
        "ORDER BY count DESC"
    )

    return {
        "labels": labels,
        "properties": props,
        "relationship_patterns": patterns,
        "guide": SCHEMA_GUIDE,
    }


# ---------------------------------------------------------------------------
# Node search


@mcp.tool()
@safe
def find_nodes(text: str, limit: int = 10) -> dict:
    """Fuzzy-resolve a human phrase to exact node names.

    Use before impact_analysis / run_cypher.
    """
    g = graph()

    words = [
        w
        for w in re.split(r"[\s_\-/]+", text.lower())
        if len(w) > 2
    ]

    rows = g.query(
        "MATCH (n) "
        "WHERE toLower(n.name) CONTAINS $full "
        "OR any(w IN $words WHERE toLower(n.name) CONTAINS w) "
        "WITH n, CASE "
        "WHEN toLower(n.name) CONTAINS $full THEN 0 "
        "ELSE 1 END AS rank "
        "RETURN labels(n)[0] AS label, "
        "n.name AS name, "
        "properties(n) AS properties "
        "ORDER BY rank, name LIMIT $limit",
        {
            "full": text.lower(),
            "words": words,
            "limit": max(1, min(limit, 50)),
        },
    )

    return {"matches": rows}


# ---------------------------------------------------------------------------
# Read-only Cypher


@mcp.tool()
@safe
def run_cypher(query: str, parameters_json: str = "") -> dict:
    """Execute ONE read-only Cypher statement.

    parameters_json must be a JSON object string.
    """
    params = json.loads(parameters_json) if parameters_json.strip() else None

    if params is not None and not isinstance(params, dict):
        raise ValueError("parameters_json must be a JSON object")

    rows, truncated = graph().run_read(query, params)

    return {
        "row_count": len(rows),
        "truncated": truncated,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Impact analysis


@mcp.tool()
@safe
def impact_analysis(target: str, max_depth: int = 8) -> dict:
    """Calculate the blast radius of changing, deprecating or removing a node.

    Supports Service, Module, APIRoute, Database and FrontendComponent.

    Returns:
      - Transitively affected nodes
      - Shortest dependency chains
      - Owning services
      - Transitive downstream services
      - Service-level shortest dependency distances
      - Architectural debt signals
    """
    g = graph()

    # 1. Resolve the exact target node.

    head = g.query(
        "MATCH (n {name:$t}) "
        "RETURN labels(n)[0] AS label, "
        "n.name AS name, "
        "properties(n) AS properties "
        "LIMIT 1",
        {"t": target},
    )

    if not head:
        near = g.query(
            "MATCH (n) "
            "WHERE toLower(n.name) CONTAINS toLower($t) "
            "RETURN labels(n)[0] AS label, "
            "n.name AS name "
            "LIMIT 10",
            {"t": target},
        )

        return {
            "error": f"No node named '{target}'.",
            "did_you_mean": near,
        }

    label = head[0]["label"]

    # 2. Expand service ownership.

    targets = [target]

    if label == "Service":
        kids = g.query(
            "MATCH (:Service {name:$t})-[:CONTAINS|EXPOSES]->(c) "
            "RETURN c.name AS name",
            {"t": target},
        )

        targets += [k["name"] for k in kids]

    max_depth = max(1, min(int(max_depth), 25))

    # 3. Calculate module/API/frontend blast radius.

    edges = fetch_dependency_edges(g)

    radius = blast_radius(
        edges,
        targets,
        max_depth,
    )

    names = list(radius) + targets

    # 4. Resolve service ownership.

    owner_rows = g.query(
        "MATCH (s:Service)-[:CONTAINS|EXPOSES]->(x) "
        "WHERE x.name IN $n "
        "RETURN x.name AS name, s.name AS service",
        {"n": names},
    )

    owner = {
        r["name"]: r["service"]
        for r in owner_rows
    }

    target_owners = sorted(
        {owner[t] for t in targets if t in owner}
        | ({target} if label == "Service" else set())
    )

    # 5. Group affected nodes by label.

    grouped: dict[str, list] = {}

    for n, info in sorted(
        radius.items(),
        key=lambda kv: (kv[1]["distance"], kv[0]),
    ):
        item = {
            "name": n,
            "distance": info["distance"],
            "chain": info["chain"],
            "owner_service": owner.get(n),
        }

        grouped.setdefault(info["label"], []).append(item)

    # 6. Identify services owning affected modules/routes.

    affected_services = {
        item["owner_service"]
        for kind in ("Module", "APIRoute")
        for item in grouped.get(kind, [])
        if item["owner_service"]
    }

    affected_services -= set(target_owners)

    # 7. Propagate impact through DEPENDS_ON relationships.

    svc_pairs = fetch_service_pairs(g)

    # Include both original target services and services
    # discovered through module/API impact analysis.

    service_seeds = set(target_owners) | affected_services

    downstream = downstream_services(
        svc_pairs,
        service_seeds,
    )

    # Calculate distances from the original target-owning services.

    target_service_distances = downstream_service_distances(
        svc_pairs,
        set(target_owners),
    )

    # Also calculate distances from all service seeds.

    propagated_service_distances = downstream_service_distances(
        svc_pairs,
        service_seeds,
    )

    # Merge module-level and service-level impact results.
    # Exclude original target services from downstream results.

    affected_services = sorted(
        (affected_services | downstream) - set(target_owners)
    )

    # Include downstream services when checking deprecated nodes.

    scope_names = sorted(
        set(names) | set(affected_services)
    )

    # 8. Architectural debt signals.

    relevant_services = set(affected_services) | set(target_owners)

    cycles = [
        c
        for c in find_cycles(svc_pairs)
        if set(c["members"]) & relevant_services
    ]

    spofs = [
        s
        for s in single_points_of_failure(svc_pairs)
        if s["name"] in relevant_services
    ]

    # Shared database coupling.

    shared = g.query(
        "MATCH (t)-[:READS_FROM|WRITES_TO]->(d:Database)"
        "<-[r:READS_FROM|WRITES_TO]-(o) "
        "WHERE t.name IN $t "
        "AND NOT o.name IN $t "
        "RETURN d.name AS database, "
        "o.name AS other_accessor, "
        "type(r) AS access "
        "ORDER BY database, other_accessor",
        {"t": targets},
    )

    # Deprecated nodes in the complete impact scope.

    dep = g.query(
        "MATCH (n) "
        "WHERE n.deprecated = true "
        "AND n.name IN $n "
        "RETURN labels(n)[0] AS label, "
        "n.name AS name",
        {"n": scope_names},
    )

    # 9. Final response.

    return {
        "target": {
            "name": target,
            "label": label,
            "owner_services": target_owners,
            "treated_as_removed": targets,
        },
        "assumption": (
            "Upper bound: assumes each dependency is a hard runtime "
            "dependency (no fallback/circuit breaker)."
        ),
        "counts": {
            k: len(v)
            for k, v in grouped.items()
        },
        "affected_downstream_services": affected_services,
        "downstream_service_distances": dict(
            sorted(target_service_distances.items())
        ),
        "propagated_service_distances": dict(
            sorted(propagated_service_distances.items())
        ),
        "affected_nodes": grouped,
        "debt_signals": {
            "circular_dependencies_touching_radius": cycles,
            "single_points_of_failure_in_radius": spofs,
            "shared_database_coupling": shared,
            "deprecated_nodes_in_scope": dep,
        },
    }


# ---------------------------------------------------------------------------
# Circular dependencies


@mcp.tool()
@safe
def detect_circular_dependencies(level: str = "service") -> dict:
    """Find strongly connected components representing circular dependencies.

    level='service' uses Service-DEPENDS_ON->Service.
    level='module' uses Module CALLS / CALLS_ROUTE->IMPLEMENTED_BY.

    Returns SCC groups, not an enumeration of every possible simple cycle.
    """
    if level not in {"service", "module"}:
        raise ValueError(
            "Invalid level. Expected 'service' or 'module'."
        )

    g = graph()

    pairs = (
        fetch_module_pairs(g)
        if level == "module"
        else fetch_service_pairs(g)
    )

    components = find_cycles(pairs)

    return {
        "level": level,
        "scc_count": len(components),
        "strongly_connected_components": components,
        "individual_cycles_enumerated": False,
    }


# ---------------------------------------------------------------------------
# Single points of failure


@mcp.tool()
@safe
def find_single_points_of_failure(min_fan_in: int = 3) -> dict:
    """Find services that are articulation points or have high fan-in."""

    return {
        "min_fan_in": min_fan_in,
        "single_points_of_failure": single_points_of_failure(
            fetch_service_pairs(graph()),
            min_fan_in,
        ),
    }


# ---------------------------------------------------------------------------
# Coupling metrics


@mcp.tool(name="coupling_metrics")
@safe
def coupling_metrics_tool(level: str = "service", top: int = 15) -> dict:
    """Calculate afferent/efferent coupling and instability."""

    g = graph()

    pairs = (
        fetch_module_pairs(g)
        if level == "module"
        else fetch_service_pairs(g)
    )

    return {
        "level": level,
        "metrics": coupling_metrics(pairs)[:max(1, top)],
    }


# ---------------------------------------------------------------------------


if __name__ == "__main__":
    mcp.run()
