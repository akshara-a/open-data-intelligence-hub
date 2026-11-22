from typing import Dict, Any, Optional

# Approved Parameterized Cypher Templates per ARCHITECTURE.md Section 6.4, 10.1, 12.1

QUERY_TEMPLATES: Dict[str, str] = {
    # 1. Snapshot Information
    "snapshot_info": """
        MATCH (s:Snapshot {repo_id: $repo_id, commit_sha: $commit_sha})
        OPTIONAL MATCH (r:Repo {repo_id: $repo_id})
        RETURN s.snapshot_id AS snapshot_id,
               s.repo_id AS repo_id,
               s.commit_sha AS commit_sha,
               toString(s.ingested_at) AS ingested_at,
               r.name AS repo_name,
               r.git_url AS git_url
        LIMIT 1;
    """,

    # 2. Entity Lookup by name, type, or stable/logical ID
    "entity_lookup": """
        MATCH (e:Entity {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE ($entity_id IS NULL OR e.entity_id = $entity_id OR e.logical_entity_id = $entity_id)
          AND ($name IS NULL OR e.name = $name)
          AND ($file_path IS NULL OR e.file_path = $file_path)
          AND ($entity_type IS NULL OR $entity_type IN labels(e))
        RETURN e.entity_id AS entity_id,
               e.logical_entity_id AS logical_entity_id,
               e.name AS name,
               e.file_path AS file_path,
               e.line_start AS line_start,
               e.line_end AS line_end,
               e.signature_hash AS signature_hash,
               [lbl IN labels(e) WHERE lbl <> 'Entity'] AS entity_types
        ORDER BY e.file_path, e.line_start
        SKIP coalesce($skip, 0)
        LIMIT coalesce($limit, 500);
    """,

    # 3. Entity Details & Source Provenance
    "entity_details": """
        MATCH (e:Entity {entity_id: $entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        OPTIONAL MATCH (ev:Evidence:EntityEvidence {repo_id: $repo_id, commit_sha: $commit_sha})-[:EVIDENCE_FOR]->(e)
        RETURN e.entity_id AS entity_id,
               e.logical_entity_id AS logical_entity_id,
               e.name AS name,
               e.file_path AS file_path,
               e.line_start AS line_start,
               e.line_end AS line_end,
               e.content_hash AS content_hash,
               e.signature_hash AS signature_hash,
               [lbl IN labels(e) WHERE lbl <> 'Entity'] AS entity_types,
               ev.evidence_id AS declaration_evidence_id,
               ev.line_range AS declaration_line_range,
               ev.extraction_rule AS extraction_rule,
               ev.description AS description
        LIMIT 1;
    """,

    # 4. Direct Dependencies and Dependents
    "direct_neighbors": """
        MATCH (e:Entity {entity_id: $entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        OPTIONAL MATCH (e)-[r_out {repo_id: $repo_id, commit_sha: $commit_sha}]->(dep:Entity {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE type(r_out) IN ['CALLS', 'IMPORTS', 'EXTENDS', 'CONTAINS', 'DEFINES']
        OPTIONAL MATCH (depender:Entity {repo_id: $repo_id, commit_sha: $commit_sha})-[r_in {repo_id: $repo_id, commit_sha: $commit_sha}]->(e)
        WHERE type(r_in) IN ['CALLS', 'IMPORTS', 'EXTENDS', 'CONTAINS', 'DEFINES']
        RETURN
            collect(DISTINCT {
                entity_id: dep.entity_id,
                name: dep.name,
                file_path: dep.file_path,
                entity_types: [lbl IN labels(dep) WHERE lbl <> 'Entity'],
                relationship: type(r_out),
                direction: 'OUTGOING'
            }) AS outgoing_dependencies,
            collect(DISTINCT {
                entity_id: depender.entity_id,
                name: depender.name,
                file_path: depender.file_path,
                entity_types: [lbl IN labels(depender) WHERE lbl <> 'Entity'],
                relationship: type(r_in),
                direction: 'INCOMING'
            }) AS incoming_dependents;
    """,

    # 5. Discrete Bounded Multi-Hop Traversals per Section 10.1 (1, 2, and 3 hops)
    "impact_downstream_1hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)<-[:CALLS|IMPORTS|EXTENDS*1..1]-(affected:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            affected.entity_id AS entity_id,
            affected.file_path AS file_path,
            affected.name AS name,
            [lbl IN labels(affected) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    "impact_downstream_2hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)<-[:CALLS|IMPORTS|EXTENDS*1..2]-(affected:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            affected.entity_id AS entity_id,
            affected.file_path AS file_path,
            affected.name AS name,
            [lbl IN labels(affected) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    "impact_downstream_3hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)<-[:CALLS|IMPORTS|EXTENDS*1..3]-(affected:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            affected.entity_id AS entity_id,
            affected.file_path AS file_path,
            affected.name AS name,
            [lbl IN labels(affected) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    "dependencies_upstream_1hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)-[:CALLS|IMPORTS|EXTENDS*1..1]->(dependency:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            dependency.entity_id AS entity_id,
            dependency.file_path AS file_path,
            dependency.name AS name,
            [lbl IN labels(dependency) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    "dependencies_upstream_2hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)-[:CALLS|IMPORTS|EXTENDS*1..2]->(dependency:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            dependency.entity_id AS entity_id,
            dependency.file_path AS file_path,
            dependency.name AS name,
            [lbl IN labels(dependency) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    "dependencies_upstream_3hop": """
        MATCH (start:Entity {entity_id: $start_entity_id, repo_id: $repo_id, commit_sha: $commit_sha})
        MATCH path = (start)-[:CALLS|IMPORTS|EXTENDS*1..3]->(dependency:Entity)
        WHERE all(n IN nodes(path) WHERE n.repo_id = $repo_id AND n.commit_sha = $commit_sha)
          AND all(r IN relationships(path) WHERE r.repo_id = $repo_id AND r.commit_sha = $commit_sha)
        RETURN
            dependency.entity_id AS entity_id,
            dependency.file_path AS file_path,
            dependency.name AS name,
            [lbl IN labels(dependency) WHERE lbl <> 'Entity'] AS labels,
            length(path) AS hop_distance,
            [r IN relationships(path) | type(r)] AS relationship_types
        LIMIT 501;
    """,

    # 6. Relationship Evidence Retrieval (with bi-directional traversal guarantee)
    "get_evidence": """
        MATCH (ev:Evidence {evidence_id: $evidence_id, repo_id: $repo_id, commit_sha: $commit_sha})
        RETURN ev.evidence_id AS evidence_id,
               ev.repo_id AS repo_id,
               ev.commit_sha AS commit_sha,
               ev.evidence_type AS evidence_type,
               ev.file_path AS file_path,
               ev.line_range AS line_range,
               ev.extraction_rule AS extraction_rule,
               ev.description AS description,
               ev.entity_id AS entity_id,
               ev.source_entity_id AS source_entity_id,
               ev.target_entity_id AS target_entity_id,
               ev.relationship_type AS relationship_type
        LIMIT 1;
    """,

    "evidence_for_entities": """
        MATCH (e:Entity {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE e.entity_id IN $entity_ids
        OPTIONAL MATCH (ev_ent:EntityEvidence {repo_id: $repo_id, commit_sha: $commit_sha})-[:EVIDENCE_FOR]->(e)
        OPTIONAL MATCH (ev_rel:RelationshipEvidence {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE (ev_rel)-[:SOURCE_OF]->(e) OR (ev_rel)-[:TARGET_OF]->(e)
        RETURN
            e.entity_id AS entity_id,
            collect(DISTINCT ev_ent.evidence_id) AS entity_evidence_ids,
            collect(DISTINCT ev_rel.evidence_id) AS relationship_evidence_ids;
    """,

    "relationship_evidence_lookup": """
        MATCH (ev:Evidence:RelationshipEvidence {
            source_entity_id: $source_entity_id,
            target_entity_id: $target_entity_id,
            repo_id: $repo_id,
            commit_sha: $commit_sha
        })
        RETURN ev.evidence_id AS evidence_id,
               ev.relationship_type AS relationship_type,
               ev.file_path AS file_path,
               ev.line_range AS line_range,
               ev.extraction_rule AS extraction_rule,
               ev.description AS description
        LIMIT 501;
    """,

    # 7. Unresolved Dynamic Call Lookup per Section 12.1
    "unresolved_calls": """
        MATCH (uc:UnresolvedCall {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE ($source_entity_id IS NULL OR uc.source_entity_id = $source_entity_id)
          AND ($file_path IS NULL OR uc.file_path = $file_path)
        OPTIONAL MATCH (cand:Entity:Function {repo_id: $repo_id, commit_sha: $commit_sha, name: uc.invoked_symbol_name})
        RETURN
            uc.call_id AS call_id,
            uc.source_entity_id AS source_entity_id,
            uc.invoked_symbol_name AS invoked_symbol_name,
            uc.file_path AS file_path,
            uc.line_range AS line_range,
            collect(DISTINCT {
                candidate_entity_id: cand.entity_id,
                candidate_name: cand.name,
                candidate_file: cand.file_path,
                classification: 'potential_uncertain'
            }) AS candidate_targets
        ORDER BY uc.file_path, uc.line_range
        SKIP coalesce($skip, 0)
        LIMIT coalesce($limit, 500);
    """,

    # 8. Graph Statistics for Snapshot
    "graph_statistics": """
        MATCH (s:Snapshot {repo_id: $repo_id, commit_sha: $commit_sha})
        OPTIONAL MATCH (e:Entity {repo_id: $repo_id, commit_sha: $commit_sha})
        WITH s, count(e) AS total_entities
        OPTIONAL MATCH ()-[r {repo_id: $repo_id, commit_sha: $commit_sha}]->()
        WHERE type(r) IN ['CALLS', 'IMPORTS', 'EXTENDS', 'CONTAINS', 'DEFINES']
        WITH s, total_entities, count(r) AS total_relationships
        OPTIONAL MATCH (ev:Evidence {repo_id: $repo_id, commit_sha: $commit_sha})
        WITH s, total_entities, total_relationships, count(ev) AS total_evidence
        OPTIONAL MATCH (uc:UnresolvedCall {repo_id: $repo_id, commit_sha: $commit_sha})
        RETURN
            s.snapshot_id AS snapshot_id,
            s.repo_id AS repo_id,
            s.commit_sha AS commit_sha,
            total_entities,
            total_relationships,
            total_evidence,
            count(uc) AS total_unresolved_calls;
    """,

    # 9. All Verified Relationships in Snapshot
    "snapshot_relationships": """
        MATCH (src:Entity {repo_id: $repo_id, commit_sha: $commit_sha})-[r {repo_id: $repo_id, commit_sha: $commit_sha}]->(tgt:Entity {repo_id: $repo_id, commit_sha: $commit_sha})
        WHERE ($relationship_type IS NULL OR type(r) = $relationship_type)
          AND type(r) IN ['CALLS', 'IMPORTS', 'EXTENDS', 'CONTAINS', 'DEFINES']
        RETURN
            elementId(r) AS id,
            src.entity_id AS source_id,
            src.name AS source_name,
            tgt.entity_id AS target_id,
            tgt.name AS target_name,
            type(r) AS relationship,
            'OUTGOING' AS direction
        ORDER BY src.name, tgt.name
        SKIP coalesce($skip, 0)
        LIMIT coalesce($limit, 500);
    """,
}


def get_template(operation: str) -> Optional[str]:
    return QUERY_TEMPLATES.get(operation)
