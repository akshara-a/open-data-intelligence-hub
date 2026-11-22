"""In-memory NetworkX implementation of the codebase knowledge graph client."""

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import networkx as nx

from src.config import TASK_ROOT_DIR, get_settings
from src.graph.base import BaseGraphClient
from src.graph.schema import extract_graph_schema


class MockGraphClient(BaseGraphClient):
    """In-memory graph client powered by NetworkX and seeded from mock_graph_seed.json.
    
    Provides deterministic graph querying, dependency traversal, cycle detection,
    and blast-radius analysis without external database dependencies.
    """

    def __init__(self, seed_path: Optional[Path] = None):
        """Initialize and load the graph from JSON seed.
        
        Args:
            seed_path: Optional custom path to JSON seed. Defaults to settings.MOCK_SEED_PATH.
        """
        self.settings = get_settings()
        self.seed_path = seed_path or self.settings.MOCK_SEED_PATH
        self._graph: nx.DiGraph = nx.DiGraph()
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []
        self.load_graph()

    def load_graph(self) -> None:
        """Load and validate nodes and edges from the JSON seed file.
        
        Raises:
            FileNotFoundError: If the seed file does not exist.
            ValueError: If JSON is invalid, duplicate node IDs exist, or edges reference missing nodes.
        """
        if not self.seed_path.exists():
            raise FileNotFoundError(f"Mock seed file not found at: {self.seed_path}")

        try:
            with open(self.seed_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as err:
            raise ValueError(f"Malformed JSON seed file: {err}") from err

        raw_nodes = data.get("nodes", [])
        raw_edges = data.get("edges", []) or data.get("relationships", [])

        # Reset in-memory structures
        self._graph.clear()
        self._nodes.clear()
        self._edges.clear()

        # Step 1: Validate unique node IDs and load nodes
        seen_node_ids = set()
        for idx, item in enumerate(raw_nodes):
            if "id" not in item:
                raise ValueError(f"Node at index {idx} is missing required 'id' attribute.")
            node_id = str(item["id"])
            if node_id in seen_node_ids:
                raise ValueError(f"Duplicate node ID detected: '{node_id}'")
            seen_node_ids.add(node_id)

            node_type = item.get("type", "Generic")
            node_name = item.get("name", node_id)
            node_desc = item.get("description", "")
            properties = item.get("properties", {})

            node_record: Dict[str, Any] = {
                "id": node_id,
                "type": node_type,
                "name": node_name,
                "description": node_desc,
                "properties": properties,
            }
            self._nodes[node_id] = node_record
            self._graph.add_node(
                node_id,
                id=node_id,
                type=node_type,
                name=node_name,
                description=node_desc,
                properties=properties,
            )

        # Step 2: Validate edge referential integrity and load edges
        for idx, edge in enumerate(raw_edges):
            if "source" not in edge or "target" not in edge:
                raise ValueError(f"Edge at index {idx} must have 'source' and 'target'.")

            source_id = str(edge["source"])
            target_id = str(edge["target"])
            edge_type = str(edge.get("type", "DEPENDS_ON"))
            edge_props = edge.get("properties", {})

            if source_id not in seen_node_ids:
                raise ValueError(f"Edge index {idx} references nonexistent source node: '{source_id}'")
            if target_id not in seen_node_ids:
                raise ValueError(f"Edge index {idx} references nonexistent target node: '{target_id}'")

            edge_record: Dict[str, Any] = {
                "source": source_id,
                "target": target_id,
                "type": edge_type,
                "properties": edge_props,
            }
            self._edges.append(edge_record)
            self._graph.add_edge(
                source_id,
                target_id,
                type=edge_type,
                properties=edge_props,
            )

    def get_nodes(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all nodes, optionally filtered by category (case-insensitive)."""
        if category is None:
            return [copy.deepcopy(n) for n in self._nodes.values()]

        target_cat = category.strip().lower()
        return [
            copy.deepcopy(n)
            for n in self._nodes.values()
            if n.get("type", "").lower() == target_cat
        ]

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single node by ID, or None if it does not exist."""
        node = self._nodes.get(node_id)
        return copy.deepcopy(node) if node else None

    def get_relationships(self, relationship_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all relationships (edges), optionally filtered by edge type."""
        if relationship_type is None:
            return [copy.deepcopy(e) for e in self._edges]

        target_rel = relationship_type.strip().lower()
        return [
            copy.deepcopy(e)
            for e in self._edges
            if e.get("type", "").lower() == target_rel
        ]

    def get_schema(self) -> Dict[str, Any]:
        """Return the extracted graph schema dictionary."""
        return extract_graph_schema(list(self._nodes.values()), self._edges)

    def get_direct_dependencies(self, node_id: str) -> List[str]:
        """Find components that node_id directly depends on (outgoing edges: node_id -> target).
        
        Raises:
            KeyError: If node_id does not exist in the graph.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")
        return sorted(list(self._graph.successors(node_id)))

    def get_direct_dependents(self, node_id: str) -> List[str]:
        """Find components that directly depend on node_id (incoming edges: source -> node_id).
        
        Raises:
            KeyError: If node_id does not exist in the graph.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")
        return sorted(list(self._graph.predecessors(node_id)))

    def get_transitive_dependents(self, node_id: str) -> List[str]:
        """Find all upstream components that transitively depend on node_id.
        
        In the directed graph where (A -> B) means A depends on B, if B is modified or
        deprecated, any node A that has a directed path to B will be affected.
        
        Important: The starting target node is strictly EXCLUDED from the returned set.
        
        Raises:
            KeyError: If node_id does not exist in the graph.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")

        # Reversing graph gives reachability from target back to all upstream callers
        reversed_g = self._graph.reverse(copy=False)
        transitive_set = set(nx.descendants(reversed_g, node_id))

        # Explicitly ensure the starting node is not included in its own dependents
        transitive_set.discard(node_id)
        return sorted(list(transitive_set))

    def calculate_blast_radius(self, node_id: str) -> Dict[str, Any]:
        """Calculate the blast radius if node_id is modified or deprecated.
        
        Evaluation details:
            - Direct dependents: Immediate callers (in-degree neighbors).
            - Transitive dependents: All upstream callers across all dependency depths.
            - Starting node exclusion: The starting target node itself is strictly
              EXCLUDED from the affected counts and dependent lists.
        
        Raises:
            KeyError: If node_id does not exist in the graph.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")

        target_node = self._nodes[node_id]
        direct = self.get_direct_dependents(node_id)
        transitive = self.get_transitive_dependents(node_id)
        indirect = [n for n in transitive if n not in direct]

        # Categorize affected nodes
        by_category: Dict[str, List[str]] = {}
        affected_services: List[str] = []
        affected_api_routes: List[str] = []
        affected_frontend_components: List[str] = []

        for dep_id in transitive:
            dep_node = self._nodes.get(dep_id, {})
            cat = dep_node.get("type", "Unknown")
            by_category.setdefault(cat, []).append(dep_id)

            cat_lower = cat.lower()
            if "service" in cat_lower and "frontend" not in cat_lower and "gateway" not in cat_lower:
                affected_services.append(dep_id)
            elif "route" in cat_lower or ("api" in cat_lower and "gateway" not in cat_lower):
                affected_api_routes.append(dep_id)
            elif "frontend" in cat_lower:
                affected_frontend_components.append(dep_id)

        # Compute shortest traversal paths from each affected node to the target
        traversal_paths: List[List[str]] = []
        for dep_id in transitive:
            try:
                path = nx.shortest_path(self._graph, source=dep_id, target=node_id)
                traversal_paths.append(path)
            except nx.NetworkXNoPath:
                pass

        # Sort traversal paths by length then node name for determinism
        traversal_paths.sort(key=lambda p: (len(p), p))

        return {
            "target_id": node_id,
            "target_name": target_node.get("name", node_id),
            "target_type": target_node.get("type", "Generic"),
            "starting_node_included": False,
            "total_affected_count": len(transitive),
            "direct_dependents": direct,
            "indirect_dependents": indirect,
            "affected_by_category": {k: sorted(v) for k, v in sorted(by_category.items())},
            "affected_services": sorted(affected_services),
            "affected_api_routes": sorted(affected_api_routes),
            "affected_frontend_components": sorted(affected_frontend_components),
            "traversal_paths": traversal_paths,
            "notes": "Blast-radius counts strictly exclude the target node itself.",
        }

    def detect_cycles(self) -> List[List[str]]:
        """Identify circular dependency loops in the architecture.
        
        Returns:
            Deterministically sorted list of cycle paths.
        """
        raw_cycles = list(nx.simple_cycles(self._graph))
        normalized_cycles: List[List[str]] = []

        for cycle in raw_cycles:
            # Rotate cycle so minimum element is at index 0 for consistent ordering
            min_idx = cycle.index(min(cycle))
            canonical = cycle[min_idx:] + cycle[:min_idx]
            normalized_cycles.append(canonical)

        normalized_cycles.sort()
        return normalized_cycles

    def calculate_coupling_metrics(self, node_id: str) -> Dict[str, Any]:
        """Calculate afferent coupling (Ca), efferent coupling (Ce), and instability index.
        
        Definitions:
            - Afferent Coupling (Ca): In-degree. Number of components depending on this node.
            - Efferent Coupling (Ce): Out-degree. Number of components this node depends upon.
            - Instability (I): Ce / (Ca + Ce).
                - I = 0: Maximally stable/rigid (many depend on it, it depends on none). Hard to change.
                - I = 1: Maximally unstable (it depends on many, none depend on it). Easy to change.
        
        Raises:
            KeyError: If node_id does not exist in the graph.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in knowledge graph.")

        node = self._nodes[node_id]
        ca = int(self._graph.in_degree(node_id))
        ce = int(self._graph.out_degree(node_id))
        total = ca + ce
        instability = round(float(ce) / float(total), 4) if total > 0 else 0.0

        # Evaluate potential failure concentration risk based on structural in-degree (Ca >= 3) and architectural category.
        # Note: Static graph coupling is an indicator of failure concentration, not an absolute proof of a runtime single point of failure (SPOF).
        is_spof = ca >= 3 and node.get("type") in [
            "Microservice",
            "Shared module",
            "API gateway",
            "Database",
            "Cache",
        ]

        return {
            "node_id": node_id,
            "node_name": node.get("name", node_id),
            "node_type": node.get("type", "Generic"),
            "afferent_coupling": ca,
            "efferent_coupling": ce,
            "instability": instability,
            "is_single_point_of_failure": is_spof,
            "potential_failure_concentration_risk": is_spof,
        }
