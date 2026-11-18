"""Coordinate ingestion, reconciliation, calculations, and file exports."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from agents.ingestion import AssetInput, IngestionError, load_inputs, reconcile
from agents.reasoning import ReasoningError, calculate_assets
from llm.router import LLMRouter, RouterError


class EngineError(RuntimeError):
    """Raised when the engine cannot complete a safe processing run."""


@dataclass(frozen=True)
class RunResult:
    asset_count: int
    json_path: Path
    audit_path: Path


def run(
    data_dir: Path,
    output_dir: Path,
    router: LLMRouter | None = None,
    tax_year: int = 2025,
) -> RunResult:
    """Process inputs and write normalized tax inputs and an audit log."""
    try:
        records = load_inputs(data_dir)
        if not records:
            raise EngineError(
                f"no .txt emails, .csv attachments, or .xlsx workbooks found under {data_dir}"
            )
        assets = reconcile(records)
        calculations = calculate_assets(assets, tax_year=tax_year)
    except (IngestionError, ReasoningError) as exc:
        raise EngineError(str(exc)) from exc

    export = {
        "schema_version": "1.0",
        "jurisdiction": "US federal",
        "tax_year": tax_year,
        "ruleset_id": calculations[0]["ruleset_id"],
        "rule_source": "https://www.irs.gov/publications/p946",
        "calculation_basis": "Limited MACRS GDS educational demonstration.",
        "assets": calculations,
    }
    export_text = json.dumps(export, indent=2, ensure_ascii=False) + "\n"

    generated_note = "No generated narrative was requested."
    generation_route = "deterministic template only"
    try:
        generation = (router or LLMRouter()).generate(
            "Write a brief, neutral introduction for an audit report describing "
            "a deterministic asset-data reconciliation and MACRS educational "
            "calculation workflow. Do not claim tax compliance, do not interpret "
            "tax law, and do not invent facts."
        )
        generated_note = generation.text
        generation_route = generation.provider
        if generation.fallback_reason:
            generation_route += " (cloud unavailable; local fallback used)"
    except RouterError as exc:
        generated_note = (
            "The optional language-model narrative was unavailable; the "
            "mathematical audit below was generated deterministically."
        )
        generation_route = "deterministic fallback (cloud/local generation unavailable)"

    audit_text = _build_audit(
        assets, calculations, generated_note, generation_route, tax_year
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "tax_inputs.json"
    audit_path = output_dir / "audit_log.md"
    staged_paths: list[Path] = []
    try:
        for prefix, content in (
            (".tax-inputs-", export_text),
            (".audit-log-", audit_text),
        ):
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=output_dir,
                prefix=prefix,
                suffix=".tmp",
                delete=False,
            ) as staged:
                staged.write(content)
                staged_paths.append(Path(staged.name))
        os.replace(staged_paths[0], json_path)
        os.replace(staged_paths[1], audit_path)
    finally:
        for staged_path in staged_paths:
            if staged_path.exists():
                staged_path.unlink()
    return RunResult(len(assets), json_path, audit_path)


def _build_audit(
    assets: list[AssetInput],
    calculations: list[dict[str, object]],
    generated_note: str,
    generation_route: str,
    tax_year: int,
) -> str:
    lines = [
        "# Tax Input Reconciliation Audit",
        "",
        "> Educational example only. Not a tax filing, tax advice, or a "
        "determination of property classification, bonus-depreciation eligibility, "
        "or elections.",
        "",
        "## Processing summary",
        "",
        f"- Normalized assets: {len(assets)}",
        "- Jurisdiction/tax year: US federal / 2025",
        "- Rule source: IRS Publication 946 (2025), MACRS percentage tables "
        "(Table A-1): https://www.irs.gov/publications/p946",
        f"- Ruleset ID: {calculations[0]['ruleset_id'] if calculations else 'none'}",
        "- Reconciliation key: exact asset ID",
        "- Conflicting non-empty source values: rejected; no precedence was guessed",
        "- Special-depreciation percentage: supplied as an explicit assumption; "
        "eligibility and elections are not determined by this tool",
        f"- Optional narrative route: {generation_route}",
        "",
        "## Generated overview",
        "",
        "If present, the optional model-generated narrative is non-authoritative; "
        "use the source records and calculations below for verification.",
        "",
        _format_generated_note(generated_note),
        "",
        "## Calculation details",
        "",
        f"The bundled demonstration implements the IRS Publication 946 (2025) "
        f"MACRS GDS half-year percentage table for explicitly supplied 5- or "
        f"7-year recovery classes. Reported year: {tax_year}. It does not "
        "classify assets or determine bonus eligibility, section 179, listed "
        "property limits, business-use qualification, or other elections.",
        "",
        "`business depreciable basis = cost x business use %`",
        "",
        "`special allowance = business depreciable basis x supplied special-depreciation %`",
        "",
        "`MACRS amount = (business depreciable basis - special allowance) x Table A-1 rate`",
        "",
        "Amounts are rounded to two decimal places using round-half-up for this "
        "demonstration. The supplied residual value is not used by MACRS. "
        "Calculations reject non-zero residual values rather than silently "
        "applying straight-line salvage assumptions.",
        "",
    ]
    for calculation in calculations:
        lines.extend([
            f"### Asset {calculation['asset_id']}",
            "",
            f"- Description: {calculation['description'] or 'not supplied'}",
            f"- Source files: {', '.join(calculation['source_files'])}",
            f"- Region (informational only): {calculation['region'] or 'not supplied'}",
            f"- Placed-in-service date (informational): "
            f"{calculation['placed_in_service_date'] or 'not supplied'}",
            f"- Cost: {calculation['cost']}",
            f"- Business use: {calculation['business_use_pct']}%",
            f"- Recovery period: {calculation['recovery_period_years']} years",
            f"- Supplied special-depreciation rate: "
            f"{calculation['special_depreciation_pct']}%",
            f"- Business depreciable basis: "
            f"{calculation['business_depreciable_basis']}",
            f"- Table A-1 MACRS rate for tax year: "
            f"{calculation['macrs_table_rate_pct']}%",
            f"- Special-depreciation amount: "
            f"{calculation['special_depreciation_amount']}",
            f"- MACRS basis after special depreciation: "
            f"{calculation['macrs_basis_after_special_depreciation']}",
            f"- MACRS depreciation amount: {calculation['macrs_depreciation_amount']}",
            f"- Total annual depreciation estimate: "
            f"{calculation['annual_depreciation_estimate']}",
            "",
        ])
    annual_total = sum(
        (Decimal(str(item["annual_depreciation_estimate"])) for item in calculations),
        start=Decimal("0"),
    )
    lines.extend([
        "## Total",
        "",
        f"- Sum of displayed annual estimates: {annual_total:.2f}",
        "",
    ])
    return "\n".join(lines)


def _format_generated_note(note: str) -> str:
    """Keep optional model prose visually separate and non-authoritative."""
    escaped = (
        note.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("`", "\\`")
    )
    return "\n".join(f"> {line}" for line in escaped.splitlines()) or "> "
