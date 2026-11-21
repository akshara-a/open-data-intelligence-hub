from datetime import datetime, date
def parse_date(value):
    """Convert date string into Python date object."""
    if isinstance(value, date):
        return value

    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

def find_asset_rule(asset_name, rules_data):
    """Find matching depreciation rule for an asset."""

    if not asset_name:
        return None

    asset_name = asset_name.lower()

    for rule in rules_data.get("rules", []):
        keywords = rule.get("asset_keywords", [])

        for keyword in keywords:
            if keyword.lower() in asset_name:
                return rule

    return None
def calculate_india_depreciation(
    cost,
    purchase_date,
    rule,
    opening_wdv=None
):
    """Calculate first-year or subsequent-year Indian WDV depreciation."""

    rate = rule.get("depreciation_rate")

    if rate is None:
        return {
            "status": "manual_review",
            "reason": "Depreciation rate is not configured for this asset."
        }

    if not 0 < rate <= 1:
        return {
            "status": "error",
            "reason": "Invalid depreciation rate."
        }

    year_start = date(purchase_date.year, 4, 1)

    if purchase_date < year_start:
        year_start = date(purchase_date.year - 1, 4, 1)

    financial_year_end = date(year_start.year + 1, 3, 31)

    days_used = (financial_year_end - purchase_date).days + 1

    half_rate = (
        rule.get("half_rate_if_used_below_threshold", False)
        and days_used < rule.get("first_year_usage_threshold_days", 180)
    )

    applicable_rate = rate / 2 if half_rate else rate

    opening_value = (
        opening_wdv if opening_wdv is not None else cost
    )

    depreciation = round(opening_value * applicable_rate, 2)

    closing_value = round(opening_value - depreciation, 2)

    return {
        "status": "calculated",
        "method": "WDV",
        "original_cost": cost,
        "opening_wdv": opening_value,
        "depreciation_rate": applicable_rate,
        "days_used": days_used,
        "depreciation_amount": depreciation,
        "closing_wdv": closing_value,
        "financial_year": f"{year_start.year}-{year_start.year + 1}",
        "half_rate_applied": half_rate
    }
def calculate_us_depreciation(cost, rule, year_number=1):
    """Calculate standard MACRS 5-year half-year depreciation."""

    recovery_period = rule.get("recovery_period_years")

    if recovery_period != 5:
        return {
            "status": "manual_review",
            "reason": "MACRS table for this recovery period is not configured."
        }

    if rule.get("convention") != "Half-Year":
        return {
            "status": "manual_review",
            "reason": "Unsupported MACRS convention."
        }

    if not 1 <= year_number <= 6:
        return {
            "status": "error",
            "reason": "Invalid MACRS recovery year."
        }
    # Standard 5-year GDS MACRS percentages.
    macrs_rates = [
        0.20,
        0.32,
        0.192,
        0.1152,
        0.1152,
        0.0576
    ]
    rate = macrs_rates[year_number - 1]
    depreciation = round(cost * rate, 2)
    return {
        "status": "calculated",
        "method": "MACRS",
        "recovery_period_years": 5,
        "year_number": year_number,
        "depreciation_rate": rate,
        "depreciation_amount": depreciation,
        "remaining_basis": round(cost - depreciation, 2),
        "bonus_depreciation": "Not included",
        "section_179": "Not included",
        "requires_review": True
    }
def calculate_depreciation(asset_data, rules_data, year_number=1):
    """Main depreciation engine."""
    asset_name = asset_data.get("asset_name")
    cost = asset_data.get("purchase_cost")
    jurisdiction = asset_data.get("jurisdiction")
    purchase_date = parse_date(
        asset_data.get("placed_in_service_date")
        or asset_data.get("purchase_date")
    )
    if not asset_name or cost is None or not jurisdiction:
        return {
            "status": "manual_review",
            "reason": "Missing asset name, purchase cost or jurisdiction."
        }
    try:
        cost = float(cost)
    except (TypeError, ValueError):
        return {
            "status": "error",
            "reason": "Invalid purchase cost."
        }
    if cost <= 0:
        return {
            "status": "error",
            "reason": "Purchase cost must be greater than zero."
        }

    if not purchase_date:
        return {
            "status": "manual_review",
            "reason": "Valid placed-in-service date is required."
        }
    if jurisdiction not in ["India", "US"]:
        return {
            "status": "manual_review",
            "reason": "Unsupported tax jurisdiction."
        }
    rule = find_asset_rule(asset_name, rules_data)
    if not rule:
        return {
            "status": "manual_review",
            "reason": f"No depreciation rule found for {asset_name}."
        }
    if rule.get("requires_review", False):
        return {
            "status": "manual_review",
            "asset_name": asset_name,
            "reason": "This asset requires tax classification verification.",
            "rule_id": rule.get("rule_id")
        }
    if jurisdiction == "India":
        result = calculate_india_depreciation(
            cost,
            purchase_date,
            rule,
            asset_data.get("opening_wdv")
        )
    else:
        result = calculate_us_depreciation(
            cost,
            rule,
            year_number
        )
    result["asset_name"] = asset_name
    result["jurisdiction"] = jurisdiction
    result["rule_id"] = rule.get("rule_id")
    result["currency"] = asset_data.get("currency")
    # Purchase date is not necessarily the date the asset
    # was actually placed in service.
    if not asset_data.get("placed_in_service_date"):
        result["requires_review"] = True
        result["review_reason"] = (
            "Purchase date used as a provisional placed-in-service date."
        )

    return result