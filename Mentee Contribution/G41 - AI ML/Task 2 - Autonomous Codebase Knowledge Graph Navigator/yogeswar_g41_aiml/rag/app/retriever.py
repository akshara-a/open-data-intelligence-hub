import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import numpy as np

from .models import (
    RetrievalRequest,
    RetrievalResultItem,
    RankingExplanation,
    HybridRetrievalResponse,
)
from .embedding_engine import get_embedding_engine
from .sqlite_storage import SQLiteChunkStorage
from .cgg_client import get_cgg_client, CGGClient


class GraphRAGRetriever:
    """
    Hybrid GraphRAG Retrieval Engine combining SQLite semantic search
    with structural graph traversals through the Controlled Graph Gateway (CGG).
    """

    def __init__(self, db_path: Optional[str] = None, cgg_client: Optional[CGGClient] = None):
        self.storage = SQLiteChunkStorage(db_path)
        self.cgg = cgg_client or get_cgg_client()
        self.engine = get_embedding_engine()

    def retrieve(self, request: RetrievalRequest) -> HybridRetrievalResponse:
        repo_id = request.repo_id.strip()
        commit_sha = request.commit_sha.strip()
        query_text = request.query.strip()

        if not repo_id or not commit_sha:
            raise ValueError("Both repo_id and commit_sha are mandatory for snapshot isolation")
        if not query_text:
            return HybridRetrievalResponse(
                repo_id=repo_id,
                commit_sha=commit_sha,
                query=query_text,
                total_candidates_scanned=0,
                results_returned=0,
                model_version=self.engine.model_version,
                model_status=self.engine.status,
                backend=self.engine.backend,
                fallback_mode=self.engine.fallback_mode,
                results=[],
            )

        # 1. Semantic Retrieval: embed query and scan SQLite candidates
        query_vec = self.engine.embed_text(query_text)
        # Scan initial top 2x pool for hybrid ranking
        initial_k = min(request.top_k * 3, 50)
        semantic_candidates = self.storage.scan_semantic_candidates(
            repo_id=repo_id,
            commit_sha=commit_sha,
            query_vector=query_vec,
            top_k=initial_k,
        )

        total_scanned = len(semantic_candidates)
        if not semantic_candidates and not request.include_graph:
            return HybridRetrievalResponse(
                repo_id=repo_id,
                commit_sha=commit_sha,
                query=query_text,
                total_candidates_scanned=total_scanned,
                results_returned=0,
                model_version=self.engine.model_version,
                model_status=self.engine.status,
                backend=self.engine.backend,
                fallback_mode=self.engine.fallback_mode,
                results=[],
            )

        # 2. Graph Retrieval via CGG Interface
        CODE_DEPENDENCY_TYPES = {"CALLS", "IMPORTS", "EXTENDS"}
        graph_entities: Dict[str, Dict[str, Any]] = {}
        unresolved_by_entity: Dict[str, List[Dict[str, Any]]] = {}
        file_unresolved_cache: Dict[str, List[Dict[str, Any]]] = {}

        if request.include_graph:
            # Prefetch all unresolved calls for this snapshot up front to avoid N+1 queries
            try:
                snap_unres = self.cgg.get_unresolved_calls(repo_id, commit_sha)
                for u in snap_unres:
                    s_id = u.get("source_entity_id")
                    if s_id:
                        unresolved_by_entity.setdefault(s_id, []).append(u)
                    u_fp = u.get("file_path")
                    if u_fp:
                        file_unresolved_cache.setdefault(u_fp, []).append(u)
            except Exception:
                pass

            # Query CGG for entities matching extracted tokens or prominent query words
            query_tokens = [w for w in re.split(r"[^\w_]+", query_text) if len(w) >= 3]
            for token in query_tokens[:3]:
                try:
                    ents = self.cgg.lookup_entities(repo_id, commit_sha, name=token)
                    for e in ents:
                        graph_entities[e["entity_id"]] = {
                            "entity": e,
                            "hop_distance": 0,
                            "relationship_type": "DIRECT_MATCH",
                            "classification": "verified_static",
                        }
                except Exception:
                    pass

            # Also inspect graph neighbors for top semantic candidates that possess an entity_id
            for cand in semantic_candidates[:5]:
                ent_id = cand.get("entity_id")
                if ent_id:
                    # Direct verified code dependencies (excluding containment)
                    try:
                        neighbors = self.cgg.get_direct_neighbors(repo_id, commit_sha, ent_id)
                        outgoing = [
                            d for d in neighbors.get("outgoing_dependencies", [])
                            if d.get("entity_id") and d.get("relationship") in CODE_DEPENDENCY_TYPES
                        ]
                        incoming = [
                            d for d in neighbors.get("incoming_dependents", [])
                            if d.get("entity_id") and d.get("relationship") in CODE_DEPENDENCY_TYPES
                        ]
                        if outgoing or incoming:
                            if ent_id not in graph_entities:
                                first_dep = outgoing[0] if outgoing else incoming[0]
                                f_id = first_dep.get("entity_id")
                                p = [ent_id, f_id] if outgoing else [f_id, ent_id]
                                graph_entities[ent_id] = {
                                    "entity": {"entity_id": ent_id},
                                    "hop_distance": 0,
                                    "relationship_type": first_dep.get("relationship", "DEPENDENCY"),
                                    "classification": "verified_static",
                                    "path": [x for x in p if x],
                                }
                        for dep in outgoing:
                            target_id = dep.get("entity_id")
                            if target_id and target_id not in graph_entities:
                                graph_entities[target_id] = {
                                    "entity": dep,
                                    "hop_distance": 1,
                                    "relationship_type": dep.get("relationship", "DEPENDENCY"),
                                    "classification": "verified_static",
                                    "path": [x for x in [ent_id, target_id] if x],
                                }
                        for dep in incoming:
                            src_id = dep.get("entity_id")
                            if src_id and src_id not in graph_entities:
                                graph_entities[src_id] = {
                                    "entity": dep,
                                    "hop_distance": 1,
                                    "relationship_type": dep.get("relationship", "DEPENDENT"),
                                    "classification": "verified_static",
                                    "path": [x for x in [src_id, ent_id] if x],
                                }
                    except Exception:
                        pass

                    # Unresolved dynamic calls for entity
                    try:
                        unres = self.cgg.get_unresolved_calls(repo_id, commit_sha, source_entity_id=ent_id)
                        if unres:
                            unresolved_by_entity[ent_id] = unres
                    except Exception:
                        pass

        # 3. Hybrid Ranking and Deduplication
        ranked_results: List[RetrievalResultItem] = []
        seen_chunk_ids: Set[str] = set()

        # Score semantic candidates
        for cand in semantic_candidates:
            cid = cand["chunk_id"]
            if cid in seen_chunk_ids:
                continue
            seen_chunk_ids.add(cid)

            s_score = float(cand.get("semantic_similarity", 0.0))
            ent_id = cand.get("entity_id")

            # Determine graph topological signal
            g_score = 0.0
            hop_dist: Optional[int] = None
            rel_type: Optional[str] = None
            classification = "none"
            rel_path: List[str] = []
            evidence_ids: List[str] = []

            # Check if candidate represents or contains an unresolved dynamic call site
            unres_calls = []
            if ent_id and ent_id in unresolved_by_entity:
                unres_calls.extend([u for u in unresolved_by_entity[ent_id] if u.get("source_entity_id") in (None, ent_id)])

            if not unres_calls and cand.get("file_path"):
                fp = cand["file_path"]
                if fp not in file_unresolved_cache:
                    try:
                        file_unresolved_cache[fp] = self.cgg.get_unresolved_calls(repo_id, commit_sha, file_path=fp)
                    except Exception:
                        file_unresolved_cache[fp] = []
                for u in file_unresolved_cache[fp]:
                    u_fp = u.get("file_path")
                    if u_fp and u_fp != fp:
                        continue
                    u_lr = str(u.get("line_range", ""))
                    if u_lr.isdigit():
                        u_line = int(u_lr)
                        if cand["line_start"] <= u_line <= cand["line_end"]:
                            unres_calls.append(u)
                    elif not u_lr:
                        unres_calls.append(u)

            if unres_calls:
                u = unres_calls[0]
                hop_dist = 1
                rel_type = "UNRESOLVED_CALL"
                classification = "potential_uncertain"
                # Architecture Section 12.1: lower confidence weight 0.3
                g_score = 0.3 * (1.0 / (float(hop_dist) + 1.0))
                inv_sym = u.get("invoked_symbol_name", "dynamic_call")
                rel_path = [ent_id or cand["file_path"], f"UnresolvedCall::{inv_sym}"]
                if u.get("call_id"):
                    evidence_ids.append(u["call_id"])
            elif ent_id and ent_id in graph_entities:
                g_info = graph_entities[ent_id]
                hop_dist = g_info.get("hop_distance", 0)
                rel_type = g_info.get("relationship_type")
                classification = "verified_static"
                rel_path = [str(x) for x in g_info.get("path", [ent_id]) if x]
                # Graph topological score per Section 12.2: 1 / (hop_distance + 1)
                g_score = 1.0 / (float(hop_dist) + 1.0)

            # Retrieve declaration evidence if entity known
            if ent_id:
                try:
                    details = self.cgg.get_entity_details(repo_id, commit_sha, ent_id)
                    if details and details.get("declaration_evidence_id"):
                        evidence_ids.append(details["declaration_evidence_id"])
                except Exception:
                    pass

            # Hybrid Score formula: 0.6 * semantic + 0.4 * graph (Section 12.2)
            if g_score > 0.0:
                combined = 0.6 * s_score + 0.4 * g_score
                expl = f"Hybrid match: semantic={s_score:.3f}, graph={g_score:.3f} (hop={hop_dist}, {classification})"
            else:
                combined = s_score
                expl = f"Semantic match: score={s_score:.3f}"

            ranked_results.append(
                RetrievalResultItem(
                    chunk_id=cid,
                    repo_id=repo_id,
                    commit_sha=commit_sha,
                    file_path=cand["file_path"],
                    line_start=cand["line_start"],
                    line_end=cand["line_end"],
                    entity_id=cand.get("entity_id"),
                    entity_name=Path(cand["file_path"]).stem,
                    entity_type="CodeChunk",
                    content=cand["content"],
                    semantic_similarity=round(s_score, 4),
                    graph_relevance=round(g_score, 4),
                    combined_score=round(combined, 4),
                    evidence_ids=evidence_ids,
                    relationship_path=rel_path,
                    relationship_classification=classification,
                    ranking_explanation=RankingExplanation(
                        semantic_score=round(s_score, 4),
                        graph_score=round(g_score, 4),
                        combined_score=round(combined, 4),
                        hop_distance=hop_dist,
                        relationship_type=rel_type,
                        relationship_classification=classification,
                        explanation=expl,
                    ),
                    provenance_status="evidence_grounded" if (evidence_ids or ent_id) else "unsupported",
                )
            )

        # Deterministic sorting: combined_score DESC, file_path ASC, line_start ASC
        ranked_results.sort(
            key=lambda x: (-x.combined_score, x.file_path, x.line_start)
        )
        final_results = ranked_results[: request.top_k]

        return HybridRetrievalResponse(
            repo_id=repo_id,
            commit_sha=commit_sha,
            query=query_text,
            total_candidates_scanned=total_scanned,
            results_returned=len(final_results),
            model_version=self.engine.model_version,
            model_status=self.engine.status,
            backend=self.engine.backend,
            fallback_mode=self.engine.fallback_mode,
            results=final_results,
        )
