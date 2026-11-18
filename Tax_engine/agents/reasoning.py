"""Apply explicit, deterministic depreciation assumptions to normalized assets."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from agents.ingestion import AssetInput
from tax_lib.depreciation import MACRS_METHOD, RULESET_ID, calculate_macrs_gds


class ReasoningError(ValueError):
    """Raised when an asset lacks supported calculation inputs."""


def calculate_assets(assets: list[AssetInput], tax_year: int = 2025) -> list[dict[str, object]]:
    """Calculate the configured limited MACRS estimate for each asset."""
    results: list[dict[str, object]] = []
    for asset in assets:
        if asset.method is None:
            raise ReasoningError(f"asset {asset.asset_id!r} is missing depreciation method")
        if asset.recovery_period_years is None:
            raise ReasoningError(
                f"asset {asset.asset_id!r} is missing recovery period in years"
            )
        if asset.method not in {MACRS_METHOD, "macrs"}:
            raise ReasoningError(
                f"asset {asset.asset_id!r} uses unsupported method {asset.method!r}; "
                f"supported method: {MACRS_METHOD}"
            )
        if (
            asset.cost is None
            or asset.business_use_pct is None
            or asset.special_depreciation_pct is None
            or asset.placed_in_service_date is None
        ):
            raise ReasoningError(
                f"asset {asset.asset_id!r} is missing normalized cost, "
                "business-use, special-depreciation, or placed-in-service date data"
            )

        try:
            placed_in_service_year = int(asset.placed_in_service_date[:4])
        except ValueError as exc:
            raise ReasoningError(
                f"asset {asset.asset_id!r} has an invalid placed-in-service date"
            ) from exc
        if asset.residual_value not in {None, Decimal("0")}:
            raise ReasoningError(
                f"asset {asset.asset_id!r}: MACRS does not use residual value; "
                "provide 0 for this limited demonstration"
            )

        try:
            result = calculate_macrs_gds(
                cost=asset.cost,
                business_use_pct=asset.business_use_pct,
                recovery_period_years=asset.recovery_period_years,
                special_depreciation_pct=asset.special_depreciation_pct,
                placed_in_service_year=placed_in_service_year,
                tax_year=tax_year,
            )
        except ValueError as exc:
            raise ReasoningError(f"asset {asset.asset_id!r}: {exc}") from exc
        special_amount = _decimal_text(result["special_depreciation_amount"])
        macrs_amount = _decimal_text(result["macrs_depreciation_amount"])
        results.append({
            "asset_id": asset.asset_id,
            "description": asset.description,
            "region": asset.region,
            "placed_in_service_date": asset.placed_in_service_date,
            "method": MACRS_METHOD,
            "ruleset_id": RULESET_ID,
            "tax_year": tax_year,
            "recovery_period_years": _decimal_text(asset.recovery_period_years),
            "cost": _decimal_text(asset.cost),
            "business_use_pct": _decimal_text(asset.business_use_pct),
            "special_depreciation_pct": _decimal_text(asset.special_depreciation_pct),
            "business_depreciable_basis": _decimal_text(
                result["business_depreciable_basis"]
            ),
            "macrs_table_rate_pct": _decimal_text(result["table_rate_pct"]),
            "special_depreciation_amount": _decimal_text(
                result["special_depreciation_amount"]
            ),
            "macrs_basis_after_special_depreciation": _decimal_text(
                result["macrs_basis_after_special_depreciation"]
            ),
            "macrs_depreciation_amount": macrs_amount,
            "annual_depreciation_estimate": _decimal_text(
                Decimal(special_amount) + Decimal(macrs_amount)
            ),
            "source_files": list(asset.sources),
        })
    return results


def _decimal_text(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(rounded, "f")
