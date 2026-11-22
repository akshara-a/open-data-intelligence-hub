import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import neo4j

from .models import (
    EntityNode,
    RelationshipEdge,
    EntityEvidence,
    RelationshipEvidence,
    UnresolvedCallNode,
)

DEFAULT_NEO4J_URL = os.getenv("NEO4J_BOLT_URL", "bolt://localhost:7687")
DEFAULT_NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")


def get_neo4j_password() -> str:
    pwd_file = os.getenv("NEO4J_PASSWORD_FILE")
    if pwd_file and Path(pwd_file).is_file():
        return Path(pwd_file).read_text(encoding="utf-8").strip()

    # Fallback to local secrets directory
    local_sec = Path(__file__).resolve().parent.parent.parent / "secrets" / "neo4j_admin.password"
    if local_sec.is_file():
        return local_sec.read_text(encoding="utf-8").strip()

    if env_pwd := os.getenv("NEO4J_PASSWORD"):
        return env_pwd.strip()

    raise RuntimeError("Neo4j admin password secret not found in environment or secrets file")


class Neo4jGraphWriter:
    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.uri = uri or DEFAULT_NEO4J_URL
        self.user = user or DEFAULT_NEO4J_USER
        self.password = password or get_neo4j_password()
        self._driver: Optional[neo4j.Driver] = None

    def get_driver(self) -> neo4j.Driver:
        if self._driver is None:
            self._driver = neo4j.GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
            )
        return self._driver

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def ensure_schema_constraints(self):
        """
        Initializes uniqueness constraints and snapshot indices per Section 7.3.
        """
        driver = self.get_driver()
        queries = [
            # 1. Repository constraint
            "CREATE CONSTRAINT repo_pk IF NOT EXISTS FOR (r:Repo) REQUIRE r.repo_id IS UNIQUE;",
            # 2. Snapshot constraint
            "CREATE CONSTRAINT snapshot_pk IF NOT EXISTS FOR (s:Snapshot) REQUIRE s.snapshot_id IS UNIQUE;",
            # 3. Global Entity constraint across all code entities
            "CREATE CONSTRAINT entity_pk IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE;",
            # 4. Global Evidence constraint
            "CREATE CONSTRAINT evidence_pk IF NOT EXISTS FOR (ev:Evidence) REQUIRE ev.evidence_id IS UNIQUE;",
            # 5. Unresolved Call constraint
            "CREATE CONSTRAINT unresolved_call_pk IF NOT EXISTS FOR (uc:UnresolvedCall) REQUIRE uc.call_id IS UNIQUE;",
            # 6. Performance composite lookup index on snapshot scoping
            "CREATE INDEX entity_snapshot_idx IF NOT EXISTS FOR (e:Entity) ON (e.repo_id, e.commit_sha);",
            # 7. Logical entity index for cross-commit diffing
            "CREATE INDEX entity_logical_idx IF NOT EXISTS FOR (e:Entity) ON (e.logical_entity_id);",
            # 8. Unresolved calls snapshot index
            "CREATE INDEX unresolved_call_snapshot_idx IF NOT EXISTS FOR (uc:UnresolvedCall) ON (uc.repo_id, uc.commit_sha);",
            # 9. Evidence snapshot index
            "CREATE INDEX evidence_snapshot_idx IF NOT EXISTS FOR (ev:Evidence) ON (ev.repo_id, ev.commit_sha);",
            # 10. Entity name lookup index
            "CREATE INDEX entity_name_idx IF NOT EXISTS FOR (e:Entity) ON (e.name);",
            # 11. Entity file path lookup index
            "CREATE INDEX entity_file_idx IF NOT EXISTS FOR (e:Entity) ON (e.file_path);",
        ]
        with driver.session(database="neo4j") as session:
            for q in queries:
                session.run(q)

    def persist_snapshot(
        self,
        repo_id: str,
        commit_sha: str,
        entities: List[EntityNode],
        relationships: List[RelationshipEdge],
        entity_evidences: List[EntityEvidence],
        relationship_evidences: List[RelationshipEvidence],
        unresolved_calls: List[UnresolvedCallNode],
    ):
        """
        Batch transactional persistence of an immutable snapshot per Section 7 & 8.
        Uses pure Cypher batch parameter bindings with UNWIND.
        """
        driver = self.get_driver()
        snapshot_id = f"{repo_id}::{commit_sha}"

        with driver.session(database="neo4j") as session:
            # 1. Upsert Snapshot node
            session.run(
                """
                MERGE (s:Snapshot {snapshot_id: $snapshot_id})
                ON CREATE SET s.repo_id = $repo_id,
                              s.commit_sha = $commit_sha,
                              s.ingested_at = datetime()
                RETURN s
                """,
                {"snapshot_id": snapshot_id, "repo_id": repo_id, "commit_sha": commit_sha},
            )

            # 2. Upsert Entities grouped by concrete label
            entities_by_label: Dict[str, List[Dict[str, Any]]] = {}
            for e in entities:
                ent_dict = {
                    "entity_id": e.entity_id,
                    "logical_entity_id": e.logical_entity_id,
                    "repo_id": e.repo_id,
                    "commit_sha": e.commit_sha,
                    "file_path": e.file_path,
                    "name": e.name,
                    "content_hash": e.content_hash,
                    "line_start": e.line_start,
                    "line_end": e.line_end,
                    "signature_hash": e.signature_hash or "",
                }
                label = e.entity_type if e.entity_type in (
                    "File", "Module", "Class", "Function", "Interface", "Variable", "API"
                ) else "Entity"
                entities_by_label.setdefault(label, []).append(ent_dict)

            for label, items in entities_by_label.items():
                session.run(
                    f"""
                    UNWIND $items AS item
                    MERGE (n:Entity:{label} {{entity_id: item.entity_id}})
                    SET n += item
                    """,
                    {"items": items},
                )

            # 3. Upsert EntityEvidence and connect [:EVIDENCE_FOR {repo_id, commit_sha}]
            if entity_evidences:
                ev_items = [
                    {
                        "evidence_id": ev.evidence_id,
                        "repo_id": ev.repo_id,
                        "commit_sha": ev.commit_sha,
                        "evidence_type": ev.evidence_type,
                        "entity_id": ev.entity_id,
                        "file_path": ev.file_path,
                        "line_range": ev.line_range,
                        "extraction_rule": ev.extraction_rule,
                        "description": ev.description,
                    }
                    for ev in entity_evidences
                ]
                session.run(
                    """
                    UNWIND $items AS item
                    MERGE (ev:Evidence:EntityEvidence {evidence_id: item.evidence_id})
                    SET ev += item
                    WITH ev, item
                    MATCH (ent:Entity {entity_id: item.entity_id, repo_id: item.repo_id, commit_sha: item.commit_sha})
                    MERGE (ev)-[:EVIDENCE_FOR {repo_id: item.repo_id, commit_sha: item.commit_sha}]->(ent)
                    """,
                    {"items": ev_items},
                )

            # 4. Upsert Verified Relationships grouped by rel_type
            rels_by_type: Dict[str, List[Dict[str, Any]]] = {}
            for r in relationships:
                # Never persist AFFECTS per Section 7.4
                if r.rel_type == "AFFECTS":
                    continue
                rels_by_type.setdefault(r.rel_type, []).append({
                    "src": r.source_entity_id,
                    "tgt": r.target_entity_id,
                    "repo_id": r.repo_id,
                    "commit_sha": r.commit_sha,
                })

            for r_type, items in rels_by_type.items():
                if r_type in ("CONTAINS", "IMPORTS", "CALLS", "EXTENDS", "DEFINES"):
                    session.run(
                        f"""
                        UNWIND $items AS item
                        MATCH (src:Entity {{entity_id: item.src, repo_id: item.repo_id, commit_sha: item.commit_sha}})
                        MATCH (tgt:Entity {{entity_id: item.tgt, repo_id: item.repo_id, commit_sha: item.commit_sha}})
                        MERGE (src)-[r:{r_type} {{repo_id: item.repo_id, commit_sha: item.commit_sha}}]->(tgt)
                        """,
                        {"items": items},
                    )

            # 5. Upsert RelationshipEvidence and bi-directionally connect to source and target (Section 11.2)
            if relationship_evidences:
                rel_ev_items = [
                    {
                        "evidence_id": ev.evidence_id,
                        "repo_id": ev.repo_id,
                        "commit_sha": ev.commit_sha,
                        "evidence_type": ev.evidence_type,
                        "source_entity_id": ev.source_entity_id,
                        "target_entity_id": ev.target_entity_id,
                        "relationship_type": ev.relationship_type,
                        "file_path": ev.file_path,
                        "line_range": ev.line_range,
                        "extraction_rule": ev.extraction_rule,
                        "description": ev.description,
                    }
                    for ev in relationship_evidences
                ]
                session.run(
                    """
                    UNWIND $items AS item
                    MERGE (ev:Evidence:RelationshipEvidence {evidence_id: item.evidence_id})
                    SET ev += item
                    WITH ev, item
                    MATCH (src:Entity {entity_id: item.source_entity_id, repo_id: item.repo_id, commit_sha: item.commit_sha})
                    MATCH (tgt:Entity {entity_id: item.target_entity_id, repo_id: item.repo_id, commit_sha: item.commit_sha})
                    MERGE (ev)-[:SOURCE_OF {repo_id: item.repo_id, commit_sha: item.commit_sha}]->(src)
                    MERGE (ev)-[:TARGET_OF {repo_id: item.repo_id, commit_sha: item.commit_sha}]->(tgt)
                    """,
                    {"items": rel_ev_items},
                )

            # 6. Upsert UnresolvedCall nodes and connect [:HAS_UNRESOLVED_CALL]
            if unresolved_calls:
                uc_items = [
                    {
                        "call_id": uc.call_id,
                        "repo_id": uc.repo_id,
                        "commit_sha": uc.commit_sha,
                        "source_entity_id": uc.source_entity_id,
                        "invoked_symbol_name": uc.invoked_symbol_name,
                        "file_path": uc.file_path,
                        "line_range": uc.line_range,
                    }
                    for uc in unresolved_calls
                ]
                session.run(
                    """
                    UNWIND $items AS item
                    MERGE (uc:UnresolvedCall {call_id: item.call_id})
                    SET uc += item
                    WITH uc, item
                    MATCH (src:Entity {entity_id: item.source_entity_id, repo_id: item.repo_id, commit_sha: item.commit_sha})
                    MERGE (src)-[:HAS_UNRESOLVED_CALL {repo_id: item.repo_id, commit_sha: item.commit_sha}]->(uc)
                    """,
                    {"items": uc_items},
                )

    def purge_repository(self, repo_id: str):
        """
        Executes privileged detachment and deletion of all repository nodes per Section 8.1 / AC-5.3.
        """
        driver = self.get_driver()
        with driver.session(database="neo4j") as session:
            session.run(
                "MATCH (n {repo_id: $repo_id}) DETACH DELETE n;",
                {"repo_id": repo_id},
            )
