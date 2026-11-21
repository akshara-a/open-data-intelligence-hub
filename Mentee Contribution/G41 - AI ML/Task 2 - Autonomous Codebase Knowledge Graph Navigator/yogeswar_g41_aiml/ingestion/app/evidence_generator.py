import uuid
from typing import List, Tuple, Dict, Set
from .models import (
    EntityNode,
    RelationshipEdge,
    EntityEvidence,
    RelationshipEvidence,
    UnresolvedCallNode,
)


def generate_entity_evidence(entity: EntityNode) -> EntityEvidence:
    """
    Generates declaration provenance for an Entity per Section 11.1.
    Uses deterministic UUIDv5 based on snapshot entity_id for idempotent re-ingestion.
    """
    e_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"ENTITY::{entity.entity_id}"))
    line_range = (
        f"{entity.line_start}-{entity.line_end}"
        if entity.line_start != entity.line_end
        else f"{entity.line_start}"
    )
    rule = f"tree_sitter_{entity.entity_type.lower()}_declaration"
    desc = f"Syntactic declaration of {entity.entity_type} {entity.name}"

    return EntityEvidence(
        evidence_id=f"E-{e_uuid}",
        repo_id=entity.repo_id,
        commit_sha=entity.commit_sha,
        evidence_type="ENTITY",
        entity_id=entity.entity_id,
        file_path=entity.file_path,
        line_range=line_range,
        extraction_rule=rule,
        description=desc,
    )


def generate_relationship_evidence(
    rel: RelationshipEdge,
    source_entity: EntityNode,
    target_entity: EntityNode,
) -> RelationshipEvidence:
    """
    Generates coupling provenance for a verified relationship per Section 11.1.
    Uses deterministic UUIDv5 based on snapshot relationship endpoints for idempotent re-ingestion.
    """
    rel_key = f"REL::{rel.repo_id}::{rel.commit_sha}::{rel.source_entity_id}::{rel.rel_type}::{rel.target_entity_id}"
    e_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, rel_key))
    line_range = (
        f"{source_entity.line_start}-{source_entity.line_end}"
        if source_entity.line_start != source_entity.line_end
        else f"{source_entity.line_start}"
    )
    rule = f"tree_sitter_{rel.rel_type.lower()}_coupling"
    desc = f"Verified {rel.rel_type} relationship from {source_entity.name} to {target_entity.name}"

    return RelationshipEvidence(
        evidence_id=f"E-{e_uuid}",
        repo_id=rel.repo_id,
        commit_sha=rel.commit_sha,
        evidence_type="RELATIONSHIP",
        source_entity_id=rel.source_entity_id,
        target_entity_id=rel.target_entity_id,
        relationship_type=rel.rel_type,
        file_path=source_entity.file_path,
        line_range=line_range,
        extraction_rule=rule,
        description=desc,
    )


def resolve_and_filter_relationships(
    entities: List[EntityNode],
    relationships: List[RelationshipEdge],
    unresolved_calls: List[UnresolvedCallNode],
    repo_id: str,
    commit_sha: str,
) -> Tuple[List[RelationshipEdge], List[EntityEvidence], List[RelationshipEvidence], List[UnresolvedCallNode]]:
    """
    1. Validates that source and target of all relationships belong to the current snapshot (Section 7.4).
    2. Resolves intra-snapshot calls where possible: if an unresolved call matches a unique function name in the snapshot,
       it can be upgraded to a CALLS relationship; otherwise it remains in unresolved_calls.
    3. Generates 100% evidence for all entities and verified relationships (Section 11.2).
    """
    entity_map: Dict[str, EntityNode] = {e.entity_id: e for e in entities}
    functions_by_name: Dict[str, List[EntityNode]] = {}
    for e in entities:
        if e.entity_type in ("Function", "API"):
            functions_by_name.setdefault(e.name, []).append(e)

    # Resolve some unresolved calls if there's a deterministic match
    remaining_unresolved: List[UnresolvedCallNode] = []
    upgraded_rels: List[RelationshipEdge] = []

    for uc in unresolved_calls:
        candidates = functions_by_name.get(uc.invoked_symbol_name, [])
        if len(candidates) == 1:
            target = candidates[0]
            # Verify snapshot match
            if target.repo_id == repo_id and target.commit_sha == commit_sha:
                upgraded_rels.append(
                    RelationshipEdge(
                        source_entity_id=uc.source_entity_id,
                        target_entity_id=target.entity_id,
                        rel_type="CALLS",
                        repo_id=repo_id,
                        commit_sha=commit_sha,
                    )
                )
                continue
        remaining_unresolved.append(uc)

    all_candidate_rels = relationships + upgraded_rels
    valid_relationships: List[RelationshipEdge] = []

    # Enforce Section 7.4 Precondition: source and target must exist in snapshot
    for rel in all_candidate_rels:
        # Ignore inferred impact (AFFECTS is NEVER persisted)
        if rel.rel_type == "AFFECTS":
            continue

        src = entity_map.get(rel.source_entity_id)
        tgt = entity_map.get(rel.target_entity_id)
        if src and tgt:
            if (
                src.repo_id == repo_id
                and src.commit_sha == commit_sha
                and tgt.repo_id == repo_id
                and tgt.commit_sha == commit_sha
            ):
                valid_relationships.append(rel)

    # Generate Entity Evidence for 100% of entities
    entity_evidences: List[EntityEvidence] = [
        generate_entity_evidence(e) for e in entities
    ]

    # Generate Relationship Evidence for 100% of persisted relationships
    rel_evidences: List[RelationshipEvidence] = [
        generate_relationship_evidence(r, entity_map[r.source_entity_id], entity_map[r.target_entity_id])
        for r in valid_relationships
    ]

    return valid_relationships, entity_evidences, rel_evidences, remaining_unresolved
