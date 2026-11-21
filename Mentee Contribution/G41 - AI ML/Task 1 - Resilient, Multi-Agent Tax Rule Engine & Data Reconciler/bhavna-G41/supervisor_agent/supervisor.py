
from ingestion_agent.email_parser import extract_email_data

from reasoning_agent.rule_loader import load_tax_rules
from reasoning_agent.tax_engine import calculate_depreciation
from reasoning_agent.reasoning import generate_reasoning


def run_supervisor(email_text, year_number=1):

    print("\n===== SUPERVISOR AGENT STARTED =====")

    # STEP 1: Ingestion Agent
    try:
        asset_data = extract_email_data(email_text)

        if not isinstance(asset_data, dict):
            raise ValueError("Invalid data received from Ingestion Agent")

    except Exception as error:
        return {
            "status": "error",
            "reason": f"Ingestion Agent failed: {error}",
            "requires_review": True
        }

    print("\n[1] Ingestion Agent completed")

    # STEP 2: Validate jurisdiction
    jurisdiction = asset_data.get("jurisdiction")

    if isinstance(jurisdiction, str):
        jurisdiction = jurisdiction.strip()

        if jurisdiction.lower() == "india":
            jurisdiction = "India"
        elif jurisdiction.lower() in ["us", "usa", "united states"]:
            jurisdiction = "US"

        asset_data["jurisdiction"] = jurisdiction

    if jurisdiction not in ["India", "US"]:
        return {
            "status": "needs_information",
            "reason": "Missing or unsupported jurisdiction.",
            "asset_data": asset_data,
            "requires_review": True
        }

    # STEP 3: Validate required information
    required_fields = [
        "asset_name",
        "purchase_cost",
        "purchase_date"
    ]

    missing_fields = [
        field for field in required_fields
        if asset_data.get(field) is None
        or asset_data.get(field) == ""
    ]

    # Include missing fields reported by Ingestion Agent
    ingestion_missing = asset_data.get("missing_fields", [])

    missing_fields = list(
        dict.fromkeys(missing_fields + ingestion_missing)
    )

    if missing_fields:
        return {
            "status": "needs_information",
            "reason": "Required asset information is incomplete.",
            "missing_fields": missing_fields,
            "asset_data": asset_data,
            "requires_review": True
        }

    # STEP 4: Load jurisdiction-specific rules
    try:
        rules_data = load_tax_rules(jurisdiction)

        if not isinstance(rules_data, dict):
            raise ValueError("Invalid tax rules format.")

        if not isinstance(rules_data.get("rules"), list):
            raise ValueError("Tax rules list is missing.")

    except Exception as error:
        return {
            "status": "error",
            "reason": f"Tax rules loading failed: {error}",
            "asset_data": asset_data,
            "requires_review": True
        }

    print("\n[2] Tax rules loaded")

    # STEP 5: Calculate depreciation
    try:
        calculation_result = calculate_depreciation(
            asset_data,
            rules_data,
            year_number=year_number
        )

        if not isinstance(calculation_result, dict):
            raise ValueError("Invalid calculation result.")

    except Exception as error:
        return {
            "status": "error",
            "reason": f"Tax calculation failed: {error}",
            "asset_data": asset_data,
            "requires_review": True
        }

    print("\n[3] Tax calculation completed")

    # STEP 6: Generate reasoning
    try:
        reasoning_result = generate_reasoning(
            asset_data,
            rules_data,
            calculation_result
        )

        if not isinstance(reasoning_result, dict):
            raise ValueError("Invalid reasoning result.")

    except Exception as error:
        reasoning_result = {
            "agent": "Reasoning Agent",
            "status": "error",
            "summary": "Reasoning generation failed.",
            "reasoning": [str(error)],
            "requires_review": True
        }

    print("\n[4] Reasoning Agent completed")

    # STEP 7: Prepare final output
    requires_review = (
        calculation_result.get("status") != "calculated"
        or calculation_result.get("requires_review", False)
        or reasoning_result.get("requires_review", False)
    )

    final_output = {
        "status": calculation_result.get("status"),
        "asset_data": asset_data,
        "calculation": calculation_result,
        "reasoning": reasoning_result,
        "requires_review": requires_review
    }

    print("\n===== SUPERVISOR AGENT COMPLETED =====")

    return final_output
