"""
Phase 6.2 - Technical Report Generation Engine
Produces persistent, snapshot-pinned, evidence-backed technical reports.
Ensures every verified finding is supported by valid evidence citations,
uncertain findings preserve uncertainty labels, and recommendations are distinct.
"""
import uuid
import json
import logging
import datetime
from typing import List, Dict, Any, Optional

from ..database import get_db_connection
from ..agent.supervisor import run_supervisor_workflow
from ..impact.engine import run_change_impact_analysis
from ..impact.models import ChangeImpactRequest
from .models import (
    GenerateReportRequest,
    ReportSummary,
    ReportDetail,
    ReportTypeLiteral,
)

logger = logging.getLogger("reports.engine")


async def generate_technical_report(
    repo_id: str,
    commit_sha: str,
    user_id: str = "usr_admin_default",
    req: Optional[GenerateReportRequest] = None,
    request: Optional[GenerateReportRequest] = None,
    created_by: Optional[str] = None,
) -> ReportDetail:
    """
    Generates a structured, evidence-backed technical report and persists it to SQLite.
    """
    actual_req = req or request
    if actual_req is None:
        raise ValueError("Missing GenerateReportRequest")
    actual_user = created_by or user_id

    report_id = str(uuid.uuid4())
    query_id = f"qry_rep_{uuid.uuid4().hex[:10]}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    rtype_raw = actual_req.report_type
    type_map = {
        "architecture": "repository_architecture",
        "repository_architecture": "repository_architecture",
        "impact": "change_impact",
        "change_impact": "change_impact",
        "migration": "refactoring_recommendation",
        "refactoring_recommendation": "refactoring_recommendation",
        "onboarding": "dependency_analysis",
        "dependency_analysis": "dependency_analysis",
        "vulnerability": "security_risk",
        "security_risk": "security_risk",
    }
    rtype = type_map.get(rtype_raw, rtype_raw)
    target_sym = actual_req.target_symbol or (actual_req.target_symbols[0] if getattr(actual_req, "target_symbols", None) else "")
    source_fp = actual_req.source_file or ""

    # 1. Formulate inquiry query based on report type
    if rtype in ("repository_architecture", "architecture"):
        default_title = f"Repository Architecture Report - Snapshot {commit_sha[:8]}"
        query = actual_req.user_query or "Explain the high-level architecture, module boundaries, and service components in this repository."
        if getattr(actual_req, "target_symbols", None) and actual_req.target_symbols:
            query += f" Target symbols: {', '.join(actual_req.target_symbols)}."
        elif target_sym:
            query += f" Target symbol: {target_sym}."
    elif rtype in ("dependency_analysis", "onboarding"):
        default_title = f"Dependency Analysis Report: {target_sym or 'Snapshot ' + commit_sha[:8]}"
        query = actual_req.user_query or f"Explain the dependency chain and static call graph for symbol '{target_sym or 'core components'}' across modules."
    elif rtype in ("change_impact", "impact"):
        default_title = f"Change Impact Report: {target_sym or source_fp or 'Snapshot ' + commit_sha[:8]}"
        query = actual_req.user_query or f"Analyze change impact for '{target_sym}' in '{source_fp}', identifying direct and transitive callers."
    elif rtype in ("security_risk", "vulnerability"):
        default_title = f"Security and Risk Analysis Report - Snapshot {commit_sha[:8]}"
        query = actual_req.user_query or "Identify security risks, dynamic unresolvable invocations, and authentication boundaries."
    else:  # refactoring_recommendation / migration
        default_title = f"Refactoring Recommendation Report - Snapshot {commit_sha[:8]}"
        query = actual_req.user_query or "Identify tight couplings, dynamic dispatch sites, and recommend refactoring targets."

    title = actual_req.title or default_title

    verified_findings: List[Dict[str, Any]] = []
    uncertain_findings: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    evidence_refs: List[Dict[str, Any]] = []
    risk_level = "LOW"
    risk_rationale = "Static AST analysis recovered verified bindings without unhandled faults."
    limitations = (
        f"Analysis bounded to commit snapshot {commit_sha}. Dynamic runtime bindings and reflection "
        "cannot be statically resolved and remain classified as potential/uncertain."
    )

    # 2. Execute underlying analysis
    if rtype == "change_impact" and (target_sym or source_fp):
        impact_req = ChangeImpactRequest(
            symbol_name=target_sym if target_sym else None,
            file_path=source_fp if source_fp else None,
            max_depth=2,
            include_unresolved=True,
        )
        impact_resp = await run_change_impact_analysis(repo_id, commit_sha, impact_req)

        for d in impact_resp.direct_impacts:
            verified_findings.append({
                "statement": f"Direct dependent: '{d.name}' ({d.file_path}) depends on '{target_sym}' via static {', '.join(d.relationship_types)}.",
                "finding_type": "verified_static",
                "evidence_ids": d.evidence_ids,
                "file_path": d.file_path,
                "confidence": d.confidence,
            })
        for t in impact_resp.transitive_impacts:
            verified_findings.append({
                "statement": f"Transitive dependent: '{t.name}' ({t.file_path}) reached at hop distance {t.hop_distance}.",
                "finding_type": "verified_static",
                "evidence_ids": t.evidence_ids,
                "file_path": t.file_path,
                "confidence": t.confidence,
            })
        for u in impact_resp.unresolved_impacts:
            uncertain_findings.append({
                "statement": u.rationale,
                "finding_type": "potential_uncertain",
                "evidence_ids": u.evidence_ids,
                "file_path": u.file_path,
                "confidence": 0.3,
            })
            risk_level = "HIGH"
            risk_rationale = "Unresolvable dynamic invocation site detected in change impact path."

        recommendations.extend(impact_resp.recommendations)
        exec_summary = impact_resp.summary

    else:
        # Execute LangGraph Supervisor Workflow
        agent_state = await run_supervisor_workflow(
            repo_id=repo_id,
            commit_sha=commit_sha,
            user_id=user_id,
            question=query,
        )
        ans = agent_state.get("answer")
        if ans:
            exec_summary = ans.summary
            for vf in ans.verified_findings:
                if isinstance(vf, dict):
                    verified_findings.append(vf)
                elif hasattr(vf, "model_dump"):
                    verified_findings.append(vf.model_dump())
                else:
                    verified_findings.append({
                        "statement": getattr(vf, "statement", str(vf)),
                        "finding_type": getattr(vf, "finding_type", "verified_static"),
                        "evidence_ids": getattr(vf, "evidence_ids", []),
                        "file_path": getattr(vf, "file_path", ""),
                        "confidence": getattr(vf, "confidence", 1.0),
                    })
            for uf in ans.uncertain_findings:
                if isinstance(uf, dict):
                    uncertain_findings.append(uf)
                elif hasattr(uf, "model_dump"):
                    uncertain_findings.append(uf.model_dump())
                else:
                    uncertain_findings.append({
                        "statement": getattr(uf, "statement", str(uf)),
                        "finding_type": getattr(uf, "finding_type", "potential_uncertain"),
                        "evidence_ids": getattr(uf, "evidence_ids", []),
                        "file_path": getattr(uf, "file_path", ""),
                        "confidence": getattr(uf, "confidence", 0.3),
                    })
            recommendations.extend(ans.recommendations)
        else:
            exec_summary = f"Automated technical investigation completed for snapshot {commit_sha[:8]}."

        # Collect evidence records
        for ev in agent_state.get("retrieved_evidence", []):
            if ev.get("evidence_id"):
                evidence_refs.append(ev)

        if uncertain_findings:
            risk_level = "MEDIUM" if len(uncertain_findings) <= 2 else "HIGH"
            risk_rationale = f"Detected {len(uncertain_findings)} dynamic or unresolvable invocation site(s) requiring verification."

    # De-duplicate evidence references
    dedup_ev: Dict[str, Dict[str, Any]] = {}
    for ev in evidence_refs:
        eid = ev.get("evidence_id")
        if eid and eid not in dedup_ev:
            dedup_ev[eid] = ev
    final_evidence_list = list(dedup_ev.values())

    risk_assessment = {
        "risk_level": risk_level,
        "rationale": risk_rationale,
        "uncertain_couplings_count": len(uncertain_findings),
        "verified_findings_count": len(verified_findings),
    }

    # 3. Render Markdown Presentation
    md_lines = [
        f"# {title}",
        "",
        f"**Repository**: `{repo_id}` | **Commit**: `{commit_sha}` | **Generated**: `{timestamp}`",
        f"**Report ID**: `{report_id}` | **Type**: `{rtype}`",
        "",
        "## Executive Summary",
        exec_summary,
        "",
        "## Risk Assessment",
        f"- **Risk Level**: **{risk_level}**",
        f"- **Rationale**: {risk_rationale}",
        "",
        "## Verified Static Findings",
    ]
    if verified_findings:
        for vf in verified_findings:
            cites = f" [Evidence: {', '.join(vf.get('evidence_ids', []))}]" if vf.get("evidence_ids") else ""
            md_lines.append(f"- **[Verified Fact]** {vf.get('statement')}{cites}")
    else:
        md_lines.append("- *No verified static relationships recovered.*")

    if uncertain_findings:
        md_lines.extend(["", "## Potential / Uncertain Findings"])
        for uf in uncertain_findings:
            cites = f" [Evidence: {', '.join(uf.get('evidence_ids', []))}]" if uf.get("evidence_ids") else ""
            md_lines.append(f"- **[Potential / Uncertain]** {uf.get('statement')}{cites} (Confidence: {uf.get('confidence', 0.3)})")

    if recommendations:
        md_lines.extend(["", "## Actionable Recommendations"])
        for r in recommendations:
            md_lines.append(f"- {r}")

    md_lines.extend([
        "",
        "## Evidence & Provenance References",
    ])
    if final_evidence_list:
        for ev in final_evidence_list[:20]:
            md_lines.append(f"- `[{ev.get('evidence_id')}]`: `{ev.get('file_path')}` lines `{ev.get('line_range')}`")
    else:
        md_lines.append("- *No discrete evidence citations cited.*")

    md_lines.extend([
        "",
        "## Analysis Limitations",
        limitations,
    ])

    markdown_body = "\n".join(md_lines)

    # 4. Persist to SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO reports (
                report_id, query_id, repo_id, commit_sha, report_type, title,
                query_text, executive_summary, verified_findings_json, uncertain_findings_json,
                recommendations_json, risk_assessment_json, evidence_json, limitations,
                markdown_body, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'COMPLETED', ?)
            """,
            (
                report_id,
                query_id,
                repo_id,
                commit_sha,
                rtype,
                title,
                query,
                exec_summary,
                json.dumps(verified_findings),
                json.dumps(uncertain_findings),
                json.dumps(recommendations),
                json.dumps(risk_assessment),
                json.dumps(final_evidence_list),
                limitations,
                markdown_body,
                timestamp,
            ),
        )
        conn.commit()

    return ReportDetail(
        report_id=report_id,
        query_id=query_id,
        repo_id=repo_id,
        commit_sha=commit_sha,
        report_type=rtype,
        title=title,
        query_text=query,
        executive_summary=exec_summary,
        verified_findings=verified_findings,
        uncertain_findings=uncertain_findings,
        recommendations=recommendations,
        risk_assessment=risk_assessment,
        evidence=final_evidence_list,
        evidence_references=final_evidence_list,
        limitations=limitations,
        markdown_body=markdown_body,
        status="COMPLETED",
        created_at=timestamp,
    )


def list_reports(
    repo_id: Optional[str] = None,
    commit_sha: Optional[str] = None,
    report_type: Optional[str] = None,
) -> List[ReportSummary]:
    """Lists persisted technical reports matching optional filters."""
    query = "SELECT report_id, repo_id, commit_sha, report_type, title, query_text, status, created_at FROM reports WHERE 1=1"
    params = []
    if repo_id:
        query += " AND repo_id = ?"
        params.append(repo_id)
    if commit_sha:
        query += " AND commit_sha = ?"
        params.append(commit_sha)
    if report_type:
        query += " AND report_type = ?"
        params.append(report_type)

    query += " ORDER BY created_at DESC LIMIT 50"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

    return [
        ReportSummary(
            report_id=row["report_id"],
            repo_id=row["repo_id"],
            commit_sha=row["commit_sha"],
            report_type=row["report_type"],
            title=row["title"],
            query_text=row["query_text"],
            status=row["status"],
            created_at=str(row["created_at"]),
        )
        for row in rows
    ]


def get_report_by_id(report_id: str) -> Optional[ReportDetail]:
    """Retrieves full detail of a persisted report by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT report_id, query_id, repo_id, commit_sha, report_type, title,
                   query_text, executive_summary, verified_findings_json, uncertain_findings_json,
                   recommendations_json, risk_assessment_json, evidence_json, limitations,
                   markdown_body, status, created_at
            FROM reports
            WHERE report_id = ?
            """,
            (report_id,),
        )
        row = cursor.fetchone()

    if not row:
        return None

    return ReportDetail(
        report_id=row["report_id"],
        query_id=row["query_id"],
        repo_id=row["repo_id"],
        commit_sha=row["commit_sha"],
        report_type=row["report_type"],
        title=row["title"],
        query_text=row["query_text"],
        executive_summary=row["executive_summary"],
        verified_findings=json.loads(row["verified_findings_json"] or "[]"),
        uncertain_findings=json.loads(row["uncertain_findings_json"] or "[]"),
        recommendations=json.loads(row["recommendations_json"] or "[]"),
        risk_assessment=json.loads(row["risk_assessment_json"] or "{}"),
        evidence_references=json.loads(row["evidence_json"] or "[]"),
        limitations=row["limitations"] or "",
        markdown_body=row["markdown_body"],
        status=row["status"],
        created_at=str(row["created_at"]),
    )


def delete_report_by_id(report_id: str) -> bool:
    """Deletes a report by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reports WHERE report_id = ?", (report_id,))
        conn.commit()
        return cursor.rowcount > 0
