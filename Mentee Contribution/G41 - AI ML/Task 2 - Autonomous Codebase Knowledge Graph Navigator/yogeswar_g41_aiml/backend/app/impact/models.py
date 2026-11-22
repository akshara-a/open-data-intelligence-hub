"""
Phase 6.1 - Change Impact Analysis Data Models
Strictly snapshot-isolated, evidence-backed impact analysis schemas.
"""
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


class ImpactedEntity(BaseModel):
    """An individual entity identified as potentially affected by a change."""
    entity_id: str
    name: str
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    entity_type: Optional[str] = "Function"
    impact_classification: Literal[
        "direct_impact",
        "transitive_impact",
        "potential_impact",
        "unresolved_impact",
    ] = "direct_impact"
    impact_level: Optional[str] = None
    hop_distance: int = 1
    depth: Optional[int] = None
    relationship_types: List[str] = Field(default_factory=list)
    traversal_path: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    is_uncertain: bool = False
    rationale: str = ""
    suggested_verification: str = ""

    def model_post_init(self, __context: Any) -> None:
        if self.impact_level is None:
            self.impact_level = self.impact_classification
        if self.depth is None:
            self.depth = self.hop_distance
        if not self.is_uncertain and self.confidence < 0.5:
            self.is_uncertain = True


class ChangeImpactRequest(BaseModel):
    """Request payload for change impact analysis."""
    source_entity_id: Optional[str] = None
    symbol_name: Optional[str] = None
    target_entity: Optional[str] = None
    file_path: Optional[str] = None
    change_description: Optional[str] = None
    max_depth: int = Field(default=2, ge=1, le=3)
    confidence_threshold: float = 0.5
    include_unresolved: bool = True

    def model_post_init(self, __context: Any) -> None:
        if self.target_entity and not self.symbol_name:
            self.symbol_name = self.target_entity
        elif self.symbol_name and not self.target_entity:
            self.target_entity = self.symbol_name


class ChangeImpactResponse(BaseModel):
    """Structured response for change impact analysis."""
    repo_id: str
    commit_sha: str
    target_entity: Optional[str] = None
    root_entity: Optional[Dict[str, Any]] = None
    target_found: bool = True
    summary: str = ""
    max_depth: Optional[int] = None
    max_depth_analyzed: int = 2
    direct_impacts: List[ImpactedEntity] = Field(default_factory=list)
    direct_impacted: List[ImpactedEntity] = Field(default_factory=list)
    transitive_impacts: List[ImpactedEntity] = Field(default_factory=list)
    transitive_impacted: List[ImpactedEntity] = Field(default_factory=list)
    potential_impacts: List[ImpactedEntity] = Field(default_factory=list)
    unresolved_impacts: List[ImpactedEntity] = Field(default_factory=list)
    unresolved_impacted: List[ImpactedEntity] = Field(default_factory=list)
    all_evidence_ids: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    total_impacted_count: int = 0
    graph_mutated: bool = False
    execution_time_ms: float = 0.0

    def model_post_init(self, __context: Any) -> None:
        if not self.direct_impacted and self.direct_impacts:
            self.direct_impacted = self.direct_impacts
        elif not self.direct_impacts and self.direct_impacted:
            self.direct_impacts = self.direct_impacted

        if not self.transitive_impacted and self.transitive_impacts:
            self.transitive_impacted = self.transitive_impacts
        elif not self.transitive_impacts and self.transitive_impacted:
            self.transitive_impacts = self.transitive_impacted

        if not self.unresolved_impacted and self.unresolved_impacts:
            self.unresolved_impacted = self.unresolved_impacts
        elif not self.unresolved_impacts and self.unresolved_impacted:
            self.unresolved_impacts = self.unresolved_impacted

        if self.max_depth is None:
            self.max_depth = self.max_depth_analyzed
        if self.total_impacted_count == 0:
            self.total_impacted_count = len(self.direct_impacts) + len(self.transitive_impacts) + len(self.unresolved_impacts)
