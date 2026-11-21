import os
from neo4j import GraphDatabase

uri = os.getenv("NEO4J_BOLT_URL", "bolt://neo4j:7687")
user = os.getenv("NEO4J_USER", "neo4j")
pwd_file = os.getenv("NEO4J_PASSWORD_FILE", "/run/secrets/neo4j_admin_password")
if os.path.exists(pwd_file):
    with open(pwd_file, "r") as f:
        password = f.read().strip()
else:
    password = os.getenv("NEO4J_PASSWORD", "testpassword123")

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session() as s:
    print("=== NODES ===")
    records = s.run(
        "MATCH (n {repo_id: $repo_id}) RETURN labels(n) as lbl, n.name as name, n.file_path as fp, n.line_start as ls, n.line_end as le, n.declaration_evidence_id as dev, n.evidence_id as ev",
        repo_id="12fac9bd-0ebb-4844-a239-e518e812b6bb"
    ).data()
    for r in records:
        print(r)

    print("\n=== RELATIONSHIPS ===")
    rels = s.run(
        "MATCH (a {repo_id: $repo_id})-[r]->(b {repo_id: $repo_id}) RETURN type(r) as rel_type, a.name as src, b.name as dst, r.evidence_id as ev, r.classification as cls",
        repo_id="12fac9bd-0ebb-4844-a239-e518e812b6bb"
    ).data()
    for r in rels:
        print(r)

    print("\n=== ALL EVIDENCE RECORDS ===")
    evs = s.run(
        "MATCH (e:EvidenceRecord {repo_id: $repo_id}) RETURN e.evidence_id as eid, e.file_path as fp, e.line_start as ls, e.line_end as le, e.classification as cls, e.description as desc",
        repo_id="12fac9bd-0ebb-4844-a239-e518e812b6bb"
    ).data()
    for e in evs:
        print(e)

driver.close()
