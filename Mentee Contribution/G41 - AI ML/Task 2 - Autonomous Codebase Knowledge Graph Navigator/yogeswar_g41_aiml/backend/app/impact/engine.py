"""
Phase 6.1 - Change Impact Analysis Engine
Discovers direct and transitive callers, importers, and dependents using approved
Controlled Graph Gateway (CGG) operations with strict repository and commit snapshot isolation.
Never persists dynamic AFFECTS edges as static facts in Neo4j.
"""
import time
import logging
from typing import Dict, Any, List, Optional, Set

from ..agent.tools import (
    execute_cgg_entity_lookup,
    execute_cgg_entity_details,
    execute_cgg_direct_neighbors,
    execute_cgg_multihop_impact,
    execute_cgg_relationship_evidence,
    execute_cgg_unresolved_calls,
)
from .models import (
    ChangeImpactRequest,
    ChangeImpactResponse,
    ImpactedEntity,
)

logger = logging.getLogger("impact.engine")


async def run_change_impact_analysis(
    repo_id: str,
    commit_sha: str,
    req: Optional[ChangeImpactRequest] = None,
    request: Optional[ChangeImpactRequest] = None,
) -> ChangeImpactResponse:
    """
    Executes a bounded, evidence-grounded change impact analysis for a specified entity.
    """
    actual_req = req or request
    if actual_req is None:
        raise ValueError("Missing ChangeImpactRequest")

    start_time = time.time()
    depth = min(max(actual_req.max_depth, 1), 3)

    # 1. Target Entity Resolution
    root_entity = None
    target_id = actual_req.source_entity_id

    if not target_id and actual_req.symbol_name:
        lookup_res = await execute_cgg_entity_lookup(
            repo_id=repo_id,
            commit_sha=commit_sha,
            name=actual_req.symbol_name,
            file_path=actual_req.file_path,
        )
        entities = lookup_res.get("entities", [])
        if entities:
            root_entity = entities[0]
            target_id = root_entity.get("entity_id")

    if target_id and not root_entity:
        details_res = await execute_cgg_entity_details(
            repo_id=repo_id,
            commit_sha=commit_sha,
            entity_id=target_id,
        )
        root_entity = details_res.get("entity")

    if not target_id or not root_entity:
        exec_ms = round((time.time() - start_time) * 1000.0, 2)
        sym = actual_req.symbol_name or actual_req.source_entity_id or "unknown"
        return ChangeImpactResponse(
            repo_id=repo_id,
            commit_sha=commit_sha,
            root_entity=None,
            target_found=False,
            summary=f"No matching code entity found for symbol '{sym}' in snapshot context.",
            max_depth_analyzed=depth,
            direct_impacts=[],
            transitive_impacts=[],
            potential_impacts=[],
            unresolved_impacts=[],
            all_evidence_ids=[],
            recommendations=[
                f"Verify the symbol name '{sym}' exists in commit {commit_sha[:8]}.",
                "Ensure repository ingestion has completed static analysis for this snapshot.",
            ],
            execution_time_ms=exec_ms,
        )

    root_name = root_entity.get("name", "target_symbol")
    root_file = root_entity.get("file_path", "")

    direct_impacts: List[ImpactedEntity] = []
    transitive_impacts: List[ImpactedEntity] = []
    potential_impacts: List[ImpactedEntity] = []
    unresolved_impacts: List[ImpactedEntity] = []

    seen_entity_ids: Set[str] = {target_id}
    all_evidence_ids: List[str] = []

    # 2. Discover Direct Dependents (Incoming CALLS, IMPORTS, EXTENDS)
    neighbors_res = await execute_cgg_direct_neighbors(
        repo_id=repo_id,
        commit_sha=commit_sha,
        entity_id=target_id,
    )
    incoming = neighbors_res.get("incoming_dependents", [])

    for dep in incoming:
        dep_id = dep.get("entity_id")
        if not dep_id or dep_id in seen_entity_ids:
            continue
        seen_entity_ids.add(dep_id)

        # Retrieve relationship evidence for direct link
        rel_type = dep.get("relationship", "CALLS")
        rel_ev_res = await execute_cgg_relationship_evidence(
            repo_id=repo_id,
            commit_sha=commit_sha,
            source_entity_id=dep_id,
            target_entity_id=target_id,
        )
        ev_records = rel_ev_res.get("relationship_evidences", [])
        ev_ids = [r["evidence_id"] for r in ev_records if "evidence_id" in r]
        all_evidence_ids.extend(ev_ids)

        direct_impacts.append(
            ImpactedEntity(
                entity_id=dep_id,
                name=dep.get("name", "unnamed"),
                file_path=dep.get("file_path", ""),
                line_start=dep.get("line_start"),
                line_end=dep.get("line_end"),
                entity_type=dep.get("type", "Function"),
                impact_classification="direct_impact",
                hop_distance=1,
                relationship_types=[rel_type],
                traversal_path=[dep.get("name", "caller"), f"-[:{rel_type}]->", root_name],
                evidence_ids=ev_ids,
                confidence=1.0,
                rationale=f"Directly invokes or depends on '{root_name}' via static {rel_type} edge.",
                suggested_verification=f"Run unit tests for {dep.get('file_path')} and inspect caller contract.",
            )
        )

    # 3. Discover Transitive Dependents (Multi-hop impact)
    if depth >= 2:
        multihop_res = await execute_cgg_multihop_impact(
            repo_id=repo_id,
            commit_sha=commit_sha,
            start_entity_id=target_id,
            max_hops=depth,
        )
        records = multihop_res.get("records", [])
        for r in records:
            aff_id = r.get("entity_id")
            if not aff_id or aff_id in seen_entity_ids:
                continue
            seen_entity_ids.add(aff_id)

            hop_dist = int(r.get("hop_distance", 2))
            rel_types = r.get("relationship_types", [])

            transitive_impacts.append(
                ImpactedEntity(
                    entity_id=aff_id,
                    name=r.get("name", "unnamed"),
                    file_path=r.get("file_path", ""),
                    line_start=r.get("line_start"),
                    line_end=r.get("line_end"),
                    entity_type=(r.get("labels") or ["Entity"])[0],
                    impact_classification="transitive_impact",
                    hop_distance=hop_dist,
                    relationship_types=rel_types,
                    traversal_path=[r.get("name", "dependent"), f"-{hop_dist}hops->", root_name],
                    evidence_ids=[],
                    confidence=0.8,
                    rationale=f"Transitive dependent reached at hop distance {hop_dist} via {', '.join(rel_types)}.",
                    suggested_verification=f"Execute integration test suite covering {r.get('file_path')}.",
                )
            )

    # 4. Discover Dynamic / Unresolved Impact
    if actual_req.include_unresolved:
        unres_res = await execute_cgg_unresolved_calls(
            repo_id=repo_id,
            commit_sha=commit_sha,
            file_path=root_file if root_file else None,
        )
        unres_calls = unres_res.get("unresolved_calls", [])
        for u in unres_calls:
            call_id = u.get("call_id")
            inv_sym = u.get("invoked_symbol_name", "dynamic_call")
            # If dynamic call targets root name or is located in related file
            is_matching = (inv_sym == root_name) or (u.get("file_path") == root_file)
            if is_matching and call_id:
                all_evidence_ids.append(call_id)
                unresolved_impacts.append(
                    ImpactedEntity(
                        entity_id=call_id,
                        name=f"DynamicCall::{inv_sym}",
                        file_path=u.get("file_path", ""),
                        line_start=u.get("line_start"),
                        line_end=u.get("line_end"),
                        entity_type="UnresolvedCall",
                        impact_classification="unresolved_impact",
                        hop_distance=1,
                        relationship_types=["UNRESOLVED_CALL"],
                        traversal_path=[u.get("file_path", ""), f"-[:DYNAMIC_CALL]->", inv_sym],
                        evidence_ids=[call_id],
                        confidence=0.3,
                        rationale=f"Dynamic unresolvable invocation of '{inv_sym}' at {u.get('file_path')}:{u.get('line_range')}.",
                        suggested_verification="Inspect dynamic dispatch site and add explicit runtime assertions.",
                    )
                )

    # Filter by confidence threshold
    min_conf = actual_req.confidence_threshold
    direct_filtered = [d for d in direct_impacts if d.confidence >= min_conf]
    transitive_filtered = [t for t in transitive_impacts if t.confidence >= min_conf]
    unresolved_filtered = [u for u in unresolved_impacts if u.confidence >= min_conf]

    # De-duplicate evidence IDs
    unique_ev_ids = sorted(list(set(all_evidence_ids)))

    # Summary Generation
    total_impacted = len(direct_filtered) + len(transitive_filtered) + len(unresolved_filtered)
    summary = (
        f"Change Impact Analysis for '{root_name}' ({root_file}) across {depth} hop(s): "
        f"Identified {len(direct_filtered)} direct dependent(s), {len(transitive_filtered)} transitive dependent(s), "
        f"and {len(unresolved_filtered)} potential dynamic invocation site(s)."
    )

    recommendations = [
        f"Prioritize unit testing for {len(direct_filtered)} direct callers before merging changes to {root_name}.",
    ]
    if transitive_filtered:
        recommendations.append(f"Execute end-to-end integration tests across {len(transitive_filtered)} transitive dependents.")
    if unresolved_filtered:
        recommendations.append(f"Audit {len(unresolved_filtered)} unresolvable dynamic invocation site(s) for runtime contract compliance.")

    exec_ms = round((time.time() - start_time) * 1000.0, 2)

    return ChangeImpactResponse(
        repo_id=repo_id,
        commit_sha=commit_sha,
        target_entity=root_name,
        root_entity=root_entity,
        target_found=True,
        summary=summary,
        max_depth=depth,
        max_depth_analyzed=depth,
        direct_impacts=direct_filtered,
        direct_impacted=direct_filtered,
        transitive_impacts=transitive_filtered,
        transitive_impacted=transitive_filtered,
        potential_impacts=potential_impacts,
        unresolved_impacts=unresolved_filtered,
        unresolved_impacted=unresolved_filtered,
        all_evidence_ids=unique_ev_ids,
        recommendations=recommendations,
        total_impacted_count=total_impacted,
        graph_mutated=False,
        execution_time_ms=exec_ms,
    )
