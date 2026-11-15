"""Deterministic graph reasoning (pure Python, no DB needed -> unit-testable).

Provides: blast radius (reverse reachability), cycles (Tarjan SCC), single points
of failure (articulation points + fan-in) and coupling metrics (Ca/Ce/instability).
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable, NamedTuple


class Edge(NamedTuple):
    src: str
    src_label: str
    rel: str
    dst: str
    dst_label: str


# ---------------------------------------------------------------- blast radius
def blast_radius(edges: Iterable[Edge], targets: Iterable[str], max_depth: int = 8) -> dict[str, dict]:
    """Everything that (transitively) depends on `targets`.

    Returns {name: {label, distance, chain}}; chain is the shortest dependency path
    from the affected node down to the changed target, e.g. [web-page, route, module].
    """
    targets = set(targets)
    rev: dict[str, list[Edge]] = defaultdict(list)
    for e in edges:
        rev[e.dst].append(e)
    seen = {t: 0 for t in targets}
    parent: dict[str, str] = {}
    label: dict[str, str] = {}
    rel_to_parent: dict[str, str] = {}
    q = deque(targets)
    while q:
        cur = q.popleft()
        if seen[cur] >= max_depth:
            continue
        for e in rev.get(cur, []):
            if e.src in seen:
                continue
            seen[e.src] = seen[cur] + 1
            parent[e.src] = cur
            label[e.src] = e.src_label
            rel_to_parent[e.src] = e.rel
            q.append(e.src)
    out: dict[str, dict] = {}
    for n, d in seen.items():
        if n in targets:
            continue
        chain, hops, c = [n], [], n
        while c in parent:
            hops.append(rel_to_parent[c])
            c = parent[c]
            chain.append(c)
        out[n] = {"label": label[n], "distance": d, "chain": chain, "relations": hops}
    return out


# ---------------------------------------------------------------- cycles (SCC)
def strongly_connected_components(pairs: Iterable[tuple[str, str]]) -> list[list[str]]:
    adj: dict[str, list[str]] = defaultdict(list)
    for a, b in pairs:
        adj[a].append(b)
        adj.setdefault(b, [])
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on: set[str] = set()
    stack: list[str] = []
    comps: list[list[str]] = []
    counter = 0
    for root in list(adj):
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        work = [(root, iter(adj[root]))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(adj[w])))
                    pushed = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                comps.append(sorted(comp))
    return comps


def find_cycles(pairs: list[tuple[str, str]]) -> list[dict]:
    """Circular dependencies = SCCs with >1 node, plus self-loops."""
    result = []
    for comp in strongly_connected_components(pairs):
        if len(comp) > 1:
            members = set(comp)
            internal = sorted({(a, b) for a, b in pairs if a in members and b in members})
            result.append({"members": comp, "size": len(comp), "internal_edges": [f"{a} -> {b}" for a, b in internal]})
    for a, b in set(pairs):
        if a == b:
            result.append({"members": [a], "size": 1, "internal_edges": [f"{a} -> {a}"]})
    return sorted(result, key=lambda c: -c["size"])


# ---------------------------------------------------------------- SPOF
def articulation_points(pairs: Iterable[tuple[str, str]]) -> set[str]:
    adj: dict[str, set[str]] = defaultdict(set)
    for a, b in pairs:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    disc: dict[str, int] = {}
    low: dict[str, int] = {}
    aps: set[str] = set()
    t = 0
    for root in list(adj):
        if root in disc:
            continue
        disc[root] = low[root] = t
        t += 1
        children = 0
        stack = [(root, None, iter(adj[root]))]
        while stack:
            v, parent, it = stack[-1]
            for w in it:
                if w == parent:
                    continue
                if w in disc:
                    low[v] = min(low[v], disc[w])
                else:
                    disc[w] = low[w] = t
                    t += 1
                    if v == root:
                        children += 1
                    stack.append((w, v, iter(adj[w])))
                    break
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[v])
                    if p != root and low[v] >= disc[p]:
                        aps.add(p)
        if children > 1:
            aps.add(root)
    return aps


def _components_without(pairs, removed: str) -> list[int]:
    adj: dict[str, set[str]] = defaultdict(set)
    for a, b in pairs:
        if removed in (a, b) or a == b:
            continue
        adj[a].add(b)
        adj[b].add(a)
    seen, sizes = set(), []
    for n in adj:
        if n in seen:
            continue
        size, q = 0, [n]
        seen.add(n)
        while q:
            c = q.pop()
            size += 1
            for w in adj[c]:
                if w not in seen:
                    seen.add(w)
                    q.append(w)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def coupling_metrics(pairs: Iterable[tuple[str, str]]) -> list[dict]:
    """Ca = unique dependents (fan-in), Ce = unique dependencies (fan-out), I = Ce/(Ca+Ce)."""
    fan_in: dict[str, set[str]] = defaultdict(set)
    fan_out: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set()
    for a, b in pairs:
        if a == b:
            continue
        fan_out[a].add(b)
        fan_in[b].add(a)
        nodes |= {a, b}
    rows = []
    for n in nodes:
        ca, ce = len(fan_in[n]), len(fan_out[n])
        rows.append({
            "name": n,
            "afferent_ca": ca,
            "efferent_ce": ce,
            "instability": round(ce / (ca + ce), 2) if ca + ce else 0.0,
            "dependents": sorted(fan_in[n]),
            "dependencies": sorted(fan_out[n]),
        })
    return sorted(rows, key=lambda r: (-r["afferent_ca"], -r["efferent_ce"], r["name"]))


def single_points_of_failure(pairs: list[tuple[str, str]], min_fan_in: int = 3) -> list[dict]:
    aps = articulation_points(pairs)
    metrics = {m["name"]: m for m in coupling_metrics(pairs)}
    out = []
    for n, m in metrics.items():
        is_ap = n in aps
        if is_ap or m["afferent_ca"] >= min_fan_in:
            reasons = []
            if is_ap:
                reasons.append("articulation point (removal splits the service graph)")
            if m["afferent_ca"] >= min_fan_in:
                reasons.append(f"high fan-in ({m['afferent_ca']} dependents)")
            out.append({
                "name": n,
                "reasons": reasons,
                "fan_in": m["afferent_ca"],
                "dependents": m["dependents"],
                "graph_components_if_removed": _components_without(pairs, n) if is_ap else None,
            })
    return sorted(out, key=lambda r: -r["fan_in"])
