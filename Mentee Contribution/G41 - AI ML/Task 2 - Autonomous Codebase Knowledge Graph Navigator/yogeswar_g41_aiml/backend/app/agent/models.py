"""
Phase 5 - Agent State and Structured Data Models
Strictly scoped to (repo_id, commit_sha) snapshot contexts.
"""
from typing import TypedDict, List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


# ============================================================================
# Pydantic Schemas for Structured LLM Outputs & Validation
# ============================================================================

class IntentOutput(BaseModel):
    """Structured representation of interpreted user intent."""
    intent_category: Literal[
        "entity_lookup",
        "architecture_exploration",
        "dependency_analysis",
        "api_discovery",
        "code_explanation",
        "unresolved_investigation",
        "general",
    ] = Field(
        description="The primary architectural intent category of the user query."
    )
    target_symbols: List[str] = Field(
        default_factory=list,
        description="Identified function, class, module, or variable symbol names."
    )
    target_files: List[str] = Field(
        default_factory=list,
        description="Identified file paths or extensions mentioned or implied."
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Specific constraints or filters requested (e.g., max hops, specific language)."
    )
    reasoning: str = Field(
        default="",
        description="Concise rationale for the selected intent and targeted symbols."
    )


class ToolCallSpec(BaseModel):
    """Specification of an approved tool call to be executed."""
    tool_name: Literal[
        "graph_rag_retrieve",
        "cgg_entity_lookup",
        "cgg_entity_details",
        "cgg_direct_neighbors",
        "cgg_relationship_evidence",
        "cgg_multihop_impact",
        "cgg_unresolved_calls",
        "cgg_evidence_lookup",
        "repo_read_file",
    ]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""


class Finding(BaseModel):
    """An individual finding extracted during evidence validation."""
    statement: str
    finding_type: Literal["verified_static", "potential_uncertain"] = "verified_static"
    evidence_ids: List[str] = Field(default_factory=list)
    entity_id: Optional[str] = None
    file_path: Optional[str] = None
    line_range: Optional[str] = None
    confidence: float = 1.0


class AnswerOutput(BaseModel):
    """Synthesized engineering answer grounded in snapshot evidence."""
    summary: str = Field(description="High-level engineering overview addressing the user query.")
    verified_findings: List[Finding] = Field(
        default_factory=list,
        description="Syntactically verified facts backed by static analysis evidence."
    )
    uncertain_findings: List[Finding] = Field(
        default_factory=list,
        description="Dynamic or unresolved relationships flagged with uncertainty."
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable engineering or refactoring recommendations."
    )
    evidence_references: List[str] = Field(
        default_factory=list,
        description="Unique evidence citation IDs (e.g. E-xxxx) supporting the answer."
    )
    insufficient_evidence: bool = Field(
        default=False,
        description="Flag indicating whether available evidence is insufficient to answer the query."
    )
    insufficient_evidence_reason: Optional[str] = None
    markdown_response: str = Field(
        default="",
        description="Full polished Markdown presentation rendered for the developer dashboard."
    )


class ValidationOutput(BaseModel):
    """Final audit output of evidence validation."""
    is_valid: bool = True
    purged_claims_count: int = 0
    validated_evidence_count: int = 0
    snapshot_match_confirmed: bool = True
    validation_notes: List[str] = Field(default_factory=list)


# ============================================================================
# LangGraph Workflow State Schema (TypedDict)
# ============================================================================

class AgentState(TypedDict, total=False):
    """State maintained across the supervisor LangGraph workflow nodes."""
    # Context
    repo_id: str
    commit_sha: str
    user_id: str
    thread_id: str
    question: str

    # Status
    status: str
    error: Optional[str]
    is_cancelled: bool

    # Progress & Limits
    iterations_count: int
    tool_calls_count: int

    # Workflow Artifacts
    intent: Optional[IntentOutput]
    plan: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]
    retrieved_evidence: List[Dict[str, Any]]
    retrieved_chunks: List[Dict[str, Any]]
    retrieved_entities: List[Dict[str, Any]]
    unresolved_calls: List[Dict[str, Any]]
    evidence_class_map: Dict[str, str]
    answer: Optional[AnswerOutput]
    validation_result: Optional[ValidationOutput]

    # Metrics
    execution_time_ms: float


# ============================================================================
# API Request / Response Models
# ============================================================================

class AssistantChatRequest(BaseModel):
    """HTTP request payload for asking a question to the assistant."""
    question: str = Field(..., min_length=1, max_length=2000, description="Natural language codebase question.")
    thread_id: Optional[str] = Field(
        default=None,
        description="Optional conversation thread ID to continue an existing context."
    )


class AssistantChatResponse(BaseModel):
    """HTTP response payload with grounded answer, evidence, and tool trace."""
    thread_id: str
    repo_id: str
    commit_sha: str
    question: str
    status: str
    answer: AnswerOutput
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    tool_trace: List[Dict[str, Any]] = Field(default_factory=list)
    execution_time_ms: float = 0.0


class AssistantThreadSummary(BaseModel):
    """Thread summary for conversation history listings."""
    thread_id: str
    repo_id: str
    commit_sha: str
    user_id: str
    title: str
    message_count: int
    created_at: str
    updated_at: str
