"""Graph schema extraction and inspection utilities."""

from typing import Any, Dict, List, Set
from pydantic import BaseModel, Field


class GraphSchemaSummary(BaseModel):
    """Structured representation of the codebase knowledge graph schema."""

    total_nodes: int = Field(..., description="Total number of nodes in the graph")
    total_edges: int = Field(..., description="Total number of relationships in the graph")
    node_types: List[str] = Field(..., description="Unique categories/labels of nodes")
    relationship_types: List[str] = Field(..., description="Unique relationship types/edge labels")
    node_ids: List[str] = Field(..., description="List of all unique node identifiers")
    node_type_counts: Dict[str, int] = Field(..., description="Frequency count per node type")
    relationship_type_counts: Dict[str, int] = Field(..., description="Frequency count per relationship type")
    properties_by_type: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Available property keys discovered for each node type",
    )


def extract_graph_schema(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inspect raw nodes and edges to extract graph schema metadata.

    Args:
        nodes: List of node dictionaries with id, type, name, description, properties.
        edges: List of edge dictionaries with source, target, type, properties.

    Returns:
        Dictionary containing schema summary statistics, categories, and property keys.
    """
    node_types_set: Set[str] = set()
    node_ids: List[str] = []
    node_type_counts: Dict[str, int] = {}
    properties_by_type: Dict[str, Set[str]] = {}

    for n in nodes:
        nid = str(n.get("id", ""))
        ntype = str(n.get("type", "Generic"))
        node_ids.append(nid)
        node_types_set.add(ntype)
        node_type_counts[ntype] = node_type_counts.get(ntype, 0) + 1

        props = properties_by_type.setdefault(ntype, set())
        for k in n.keys():
            props.add(k)
        if "properties" in n and isinstance(n["properties"], dict):
            for pk in n["properties"].keys():
                props.add(pk)

    rel_types_set: Set[str] = set()
    rel_type_counts: Dict[str, int] = {}
    for e in edges:
        rtype = str(e.get("type", "RELATED_TO"))
        rel_types_set.add(rtype)
        rel_type_counts[rtype] = rel_type_counts.get(rtype, 0) + 1

    schema_dict: Dict[str, Any] = {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "node_types": sorted(list(node_types_set)),
        "relationship_types": sorted(list(rel_types_set)),
        "node_ids": sorted(node_ids),
        "node_type_counts": dict(sorted(node_type_counts.items())),
        "relationship_type_counts": dict(sorted(rel_type_counts.items())),
        "properties_by_type": {k: sorted(list(v)) for k, v in sorted(properties_by_type.items())},
    }
    return schema_dict
