"""Abstract base class and interface for codebase knowledge graph engines."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseGraphClient(ABC):
    """Abstract interface defining standard capabilities for graph storage and analysis."""

    @abstractmethod
    def load_graph(self) -> None:
        """Load and validate the graph from underlying storage or seed file."""
        pass

    @abstractmethod
    def get_nodes(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all nodes, optionally filtered by category/type."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single node by its unique ID. Returns None if not found."""
        pass

    @abstractmethod
    def get_relationships(self, relationship_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all relationships (edges), optionally filtered by edge type."""
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Return the graph schema including node types, relationship types, and counts."""
        pass

    @abstractmethod
    def get_direct_dependencies(self, node_id: str) -> List[str]:
        """Find nodes that the specified node directly depends on (outgoing edges)."""
        pass

    @abstractmethod
    def get_direct_dependents(self, node_id: str) -> List[str]:
        """Find nodes that directly depend on the specified node (incoming edges)."""
        pass

    @abstractmethod
    def get_transitive_dependents(self, node_id: str) -> List[str]:
        """Find all upstream/caller nodes that transitively depend on this node.
        
        The starting node itself is strictly excluded from the returned dependents.
        """
        pass

    @abstractmethod
    def calculate_blast_radius(self, node_id: str) -> Dict[str, Any]:
        """Calculate the full blast radius if the target node is modified or deprecated.
        
        Note: The starting target node is excluded from the affected dependents count.
        """
        pass

    @abstractmethod
    def detect_cycles(self) -> List[List[str]]:
        """Detect circular dependency loops within the codebase architecture."""
        pass

    @abstractmethod
    def calculate_coupling_metrics(self, node_id: str) -> Dict[str, Any]:
        """Calculate afferent coupling (Ca), efferent coupling (Ce), and instability index."""
        pass
