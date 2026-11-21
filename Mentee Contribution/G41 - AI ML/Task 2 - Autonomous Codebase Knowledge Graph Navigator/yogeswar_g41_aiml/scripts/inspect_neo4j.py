import os
from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "testpassword123")

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN labels(n) as lbl, count(n) as cnt")
        print("Neo4j Labels & Counts:")
        for r in result:
            print(" ", r["lbl"], r["cnt"])

        print("\nDistinct Repositories in Neo4j:")
        result2 = session.run("MATCH (n) WHERE n.repo_id IS NOT NULL RETURN DISTINCT n.repo_id as repo_id, count(n) as cnt")
        for r in result2:
            print("  Repo:", r["repo_id"], "Count:", r["cnt"])

        print("\nDistinct Commit SHAs in Neo4j:")
        result3 = session.run("MATCH (n) WHERE n.commit_sha IS NOT NULL RETURN DISTINCT n.repo_id as repo_id, n.commit_sha as commit_sha, count(n) as cnt")
        for r in result3:
            print(f"  Repo: {r['repo_id']} | Commit: {r['commit_sha']} | Count: {r['cnt']}")

        print("\nSample real nodes with properties:")
        sample_nodes = session.run("MATCH (n:Entity) RETURN n.entity_id as id, n.name as name, n.file_path as file, n.line_start as line_start, n.line_end as line_end, n.repo_id as repo_id LIMIT 5")
        for r in sample_nodes:
            print(" ", dict(r))

        print("\nSample relationships:")
        sample_rels = session.run("MATCH (a)-[r]->(b) RETURN type(r) as rel_type, a.name as src, b.name as tgt, r.evidence_id as ev_id, a.repo_id as repo_id LIMIT 5")
        for r in sample_rels:
            print(" ", dict(r))

    driver.close()
except Exception as e:
    print("Neo4j connection error:", e)
