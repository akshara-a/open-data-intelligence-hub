"""Read-only Neo4j access layer."""
from __future__ import annotations

from itertools import islice

from neo4j import READ_ACCESS, GraphDatabase, unit_of_work

from .config import Config
from .cypher_guard import UnsafeCypherError, validate_cypher


class GraphClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.driver = GraphDatabase.driver(cfg.neo4j_uri, auth=(cfg.neo4j_user, cfg.neo4j_password))

    def run_read(self, cypher: str, params: dict | None = None, max_rows: int | None = None):
        """Validate, then execute in a READ transaction. Returns (rows, truncated)."""
        verdict = validate_cypher(cypher)
        if not verdict.ok:
            raise UnsafeCypherError(verdict.reason)
        limit = max_rows or self.cfg.max_rows

        @unit_of_work(timeout=self.cfg.query_timeout_s)
        def work(tx):
            result = tx.run(cypher, params or {})
            rows = [r.data() for r in islice(result, limit + 1)]
            result.consume()
            return rows

        with self.driver.session(database=self.cfg.neo4j_database, default_access_mode=READ_ACCESS) as s:
            rows = s.execute_read(work)
        return rows[:limit], len(rows) > limit

    def query(self, cypher: str, params: dict | None = None, max_rows: int | None = None) -> list[dict]:
        return self.run_read(cypher, params, max_rows)[0]

    def close(self):
        self.driver.close()
