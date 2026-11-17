"""Seed the demo graph into Neo4j (needs WRITE access - uses the admin credentials in .env)."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from neo4j import GraphDatabase  # noqa: E402

from kgnav.config import load_config  # noqa: E402
from kgnav.sample_data import EDGES, NODES  # noqa: E402


def main(wipe: bool = True):
    cfg = load_config()
    driver = GraphDatabase.driver(cfg.neo4j_uri, auth=(cfg.neo4j_user, cfg.neo4j_password))
    with driver.session(database=cfg.neo4j_database) as s:
        if wipe:
            s.run("MATCH (n) DETACH DELETE n").consume()
        for label in NODES:
            s.run(f"CREATE CONSTRAINT {label.lower()}_name IF NOT EXISTS FOR (n:{label}) REQUIRE n.name IS UNIQUE").consume()
            s.run(f"UNWIND $rows AS r MERGE (n:{label} {{name: r.name}}) SET n += r", rows=NODES[label]).consume()
        grouped = defaultdict(list)
        for sl, src, rel, dl, dst in EDGES:
            grouped[(sl, rel, dl)].append({"src": src, "dst": dst})
        for (sl, rel, dl), rows in grouped.items():
            s.run(
                f"UNWIND $rows AS r MATCH (a:{sl} {{name:r.src}}) MATCH (b:{dl} {{name:r.dst}}) MERGE (a)-[:{rel}]->(b)",
                rows=rows,
            ).consume()
        n = s.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        e = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    driver.close()
    print(f"Seeded {n} nodes and {e} relationships into '{cfg.neo4j_database}'.")


if __name__ == "__main__":
    main()
