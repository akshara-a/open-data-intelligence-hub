"""
Phase 6.2 - Evidence-Backed Technical Report Models
"""
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


ReportTypeLiteral = Literal[
    "architecture",
    "impact",
    "migration",
    "onboarding",
    "vulnerability",
    "repository_architecture",
    "dependency_analysis",
    "change_impact",
    "security_risk",
    "refactoring_recommendation",
]


class GenerateReportRequest(BaseModel):
    """Request payload to generate a persistent technical report."""
    report_type: ReportTypeLiteral = Field(
        default="architecture",
        description="Type of technical report to generate.",
    )
    title: Optional[str] = None
    user_query: Optional[str] = None
    target_symbol: Optional[str] = None
    target_symbols: Optional[List[str]] = None
    source_file: Optional[str] = None
    focus_areas: Optional[List[str]] = None
    include_impact: bool = True


class ReportSummary(BaseModel):
    """Metadata summary of a generated report."""
    report_id: str
    repo_id: str
    commit_sha: str
    report_type: str
    title: str
    query_text: str = ""
    status: str
    created_at: str


class ReportDetail(BaseModel):
    """Full detail view of an immutable snapshot-pinned technical report."""
    report_id: str
    query_id: str = ""
    repo_id: str
    commit_sha: str
    report_type: str
    title: str
    query_text: str = ""
    executive_summary: str
    verified_findings: List[Dict[str, Any]] = Field(default_factory=list)
    uncertain_findings: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[Any] = Field(default_factory=list)
    risk_assessment: Any = Field(default_factory=dict)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_references: List[Dict[str, Any]] = Field(default_factory=list)
    limitations: str = ""
    markdown_body: str = ""
    status: str
    created_by: str = "usr_admin_default"
    created_at: str
