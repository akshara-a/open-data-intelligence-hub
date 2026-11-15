"""Cypher fetchers that feed the deterministic analysis layer."""
from __future__ import annotations

from .analysis import Edge
from .neo4j_client import GraphClient
from .schema import DEPENDENCY_RELS, SERVICE_LABEL, SERVICE_REL


def fetch_dependency_edges(g: GraphClient, max_rows: int = 100_000) -> list[Edge]:
    rels = "|".join(DEPENDENCY_RELS)
    rows = g.query(
        f"MATCH (a)-[r:{rels}]->(b) "
        "RETURN a.name AS src, labels(a)[0] AS sl, type(r) AS rel, b.name AS dst, labels(b)[0] AS dl",
        max_rows=max_rows,
    )
    return [Edge(r["src"], r["sl"], r["rel"], r["dst"], r["dl"]) for r in rows]


def fetch_service_pairs(g: GraphClient) -> list[tuple[str, str]]:
    rows = g.query(
        f"MATCH (a:{SERVICE_LABEL})-[:{SERVICE_REL}]->(b:{SERVICE_LABEL}) RETURN a.name AS src, b.name AS dst",
        max_rows=100_000,
    )
    return [(r["src"], r["dst"]) for r in rows]


def fetch_module_pairs(g: GraphClient) -> list[tuple[str, str]]:
    rows = g.query(
        "MATCH (a:Module)-[:CALLS]->(b:Module) RETURN a.name AS src, b.name AS dst "
        "UNION "
        "MATCH (a:Module)-[:CALLS_ROUTE]->(:APIRoute)-[:IMPLEMENTED_BY]->(b:Module) RETURN a.name AS src, b.name AS dst",
        max_rows=100_000,
    )
    return [(r["src"], r["dst"]) for r in rows]
