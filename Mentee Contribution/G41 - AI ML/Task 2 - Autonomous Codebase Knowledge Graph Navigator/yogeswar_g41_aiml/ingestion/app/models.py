from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class EntityNode(BaseModel):
    entity_id: str = Field(..., description="Snapshot-specific entity ID (<repo_id>::<commit_sha>::<type>::<name>)")
    logical_entity_id: str = Field(..., description="Cross-commit stable logical ID (<repo_id>::<type>::<name>)")
    repo_id: str
    commit_sha: str
    file_path: str
    name: str
    entity_type: str = Field(..., description="File, Module, Class, Function, Interface, Variable, API")
    content_hash: str = Field(..., description="SHA-256 hash (or head 16 hex chars) of source body")
    line_start: int
    line_end: int
    signature_hash: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationshipEdge(BaseModel):
    source_entity_id: str
    target_entity_id: str
    rel_type: str = Field(..., description="CONTAINS, IMPORTS, CALLS, EXTENDS, DEFINES")
    repo_id: str
    commit_sha: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class EntityEvidence(BaseModel):
    evidence_id: str = Field(..., description="Format E-<uuid>")
    repo_id: str
    commit_sha: str
    evidence_type: str = "ENTITY"
    entity_id: str
    file_path: str
    line_range: str = Field(..., description="Format 'start-end'")
    extraction_rule: str
    description: str


class RelationshipEvidence(BaseModel):
    evidence_id: str = Field(..., description="Format E-<uuid>")
    repo_id: str
    commit_sha: str
    evidence_type: str = "RELATIONSHIP"
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    file_path: str
    line_range: str = Field(..., description="Format 'start-end'")
    extraction_rule: str
    description: str


class UnresolvedCallNode(BaseModel):
    call_id: str = Field(..., description="Format <repo_id>::<commit_sha>::UnresolvedCall::<uuid>")
    repo_id: str
    commit_sha: str
    source_entity_id: str
    invoked_symbol_name: str
    file_path: str
    line_range: str = Field(..., description="Format 'start-end'")
