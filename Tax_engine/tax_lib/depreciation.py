"""Limited 2025 US MACRS GDS reference schedules for education and testing.

The percentage tables implement 200% declining balance, switching to
straight-line, with the half-year convention for 5- and 7-year property.
"""

from __future__ import annotations

from decimal import Decimal

RULESET_ID = "US-FEDERAL-2025-PUB946-MACRS-GDS-HY-DEMO-v1"
RULE_SOURCE = "https://www.irs.gov/publications/p946"
MACRS_TABLES: dict[int, tuple[Decimal, ...]] = {
    5: tuple(map(Decimal, ("20.00", "32.00", "19.20", "11.52", "11.52", "5.76"))),
    7: tuple(map(Decimal, (
        "14.29", "24.49", "17.49", "12.49", "8.93", "8.92", "8.93", "4.46",
    ))),
}
MACRS_METHOD = "macrs_gds_200_db_half_year"


def calculate_macrs_gds(
    *,
    cost: Decimal,
    business_use_pct: Decimal,
    recovery_period_years: Decimal,
    special_depreciation_pct: Decimal,
    placed_in_service_year: int,
    tax_year: int = 2025,
) -> dict[str, Decimal | int | str]:
    """Calculate one year from the limited 2025 MACRS percentage schedules.

    The caller must supply a tax-professional-determined special allowance
    percentage; this function does not determine legal eligibility or elections.
    """
    if tax_year != 2025:
        raise ValueError(f"{RULESET_ID} supports tax year 2025 only")
    if cost < 0:
        raise ValueError("cost cannot be negative")
    if not Decimal("0") <= business_use_pct <= Decimal("100"):
        raise ValueError("business use percentage must be between zero and 100")
    if not Decimal("0") <= special_depreciation_pct <= Decimal("100"):
        raise ValueError("special depreciation percentage must be between zero and 100")
    if recovery_period_years not in {Decimal("5"), Decimal("7")}:
        raise ValueError("supported MACRS recovery periods are 5 or 7 years")
    if placed_in_service_year != tax_year:
        raise ValueError("this demonstration supports property placed in service in 2025")

    recovery_period = int(recovery_period_years)
    year_in_schedule = tax_year - placed_in_service_year + 1
    schedule = MACRS_TABLES[recovery_period]
    rate = schedule[year_in_schedule - 1]
    business_basis = cost * business_use_pct / Decimal("100")
    special_allowance = business_basis * special_depreciation_pct / Decimal("100")
    remaining_basis = business_basis - special_allowance
    macrs_rate = rate / Decimal("100")
    macrs_amount = remaining_basis * macrs_rate
    return {
        "ruleset_id": RULESET_ID,
        "tax_year": tax_year,
        "year_in_recovery_schedule": year_in_schedule,
        "table_rate_pct": rate,
        "business_depreciable_basis": business_basis,
        "special_depreciation_pct": special_depreciation_pct,
        "special_depreciation_amount": special_allowance,
        "macrs_basis_after_special_depreciation": remaining_basis,
        "macrs_depreciation_amount": macrs_amount,
        "annual_depreciation": special_allowance + macrs_amount,
    }
