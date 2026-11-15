import pytest
from kgnav.cypher_guard import validate_cypher

OK = [
    "MATCH (n:Service) RETURN n.name LIMIT 5",
    "MATCH (a)-[:CALLS_ROUTE*1..4]->(b) WHERE b.name = 'x' RETURN a.name",
    "MATCH (n) WHERE n.name = 'DELETE ME' RETURN n.name",           # keyword inside string literal
    "MATCH (n) RETURN n.created_at, n.set AS s",                    # keyword-like property names
    "CALL db.labels() YIELD label RETURN label",
    "MATCH (n) RETURN n.name;",
    "MATCH (n) CALL { WITH n MATCH (n)-[:CALLS]->(m) RETURN count(m) AS c } RETURN n.name, c",
]
BAD = [
    "MATCH (n) DETACH DELETE n",
    "MATCH (n) SET n.x = 1 RETURN n",
    "CREATE (n:Service {name:'x'}) RETURN n",
    "MERGE (n:Service {name:'x'}) RETURN n",
    "MATCH (n) RETURN n; MATCH (m) DELETE m",
    "CALL apoc.cypher.doIt('CREATE (n)', {}) YIELD value RETURN value",
    "CALL dbms.security.createUser('a','b',false)",
    "LOAD CSV FROM 'file:///x.csv' AS r RETURN r",
    "CREATE INDEX foo FOR (n:Service) ON (n.name)",
    "MATCH (n) REMOVE n.name RETURN n",
    "",
    "MATCH (n:Service)",   # no RETURN
]


@pytest.mark.parametrize("q", OK)
def test_allowed(q):
    assert validate_cypher(q).ok, validate_cypher(q).reason


@pytest.mark.parametrize("q", BAD)
def test_blocked(q):
    assert not validate_cypher(q).ok
