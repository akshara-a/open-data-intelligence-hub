
import json
from pathlib import Path

from reasoning_agent.rule_loader import load_tax_rules
from reasoning_agent.tax_engine import calculate_depreciation
from reasoning_agent.reasoning import generate_reasoning


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "normalized_data.json"
OUTPUT_DIR = BASE_DIR / "outputs"


def process_batch():

    print("\n===== BATCH PROCESSOR STARTED =====")

    if not INPUT_FILE.exists():
        raise FileNotFoundError("Normalized data not found.")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Input JSON must contain a list of records.")

    final_results = []
    rules_cache = {}

    for index, asset_data in enumerate(records, start=1):

        print(f"\nProcessing Asset {index}: {asset_data.get('asset_name')}")

        try:
            jurisdiction = asset_data.get("jurisdiction")

            if not jurisdiction:
                raise ValueError("Jurisdiction is missing.")

            # STEP 1: Load tax rules
            if jurisdiction not in rules_cache:
                rules_cache[jurisdiction] = load_tax_rules(jurisdiction)

            rules_data = rules_cache[jurisdiction]

            # STEP 2: Calculate depreciation
            calculation_result = calculate_depreciation(
                asset_data,
                rules_data,
                year_number=1
            )

            # STEP 3: Generate reasoning
            reasoning_result = generate_reasoning(
                asset_data,
                rules_data,
                calculation_result
            )

            # STEP 4: Check human review requirement
            requires_review = (
                calculation_result.get("requires_review", False)
                or reasoning_result.get("requires_review", False)
                or calculation_result.get("status") == "manual_review"
            )

            final_results.append({
                "record_number": index,
                "asset_data": asset_data,
                "calculation": calculation_result,
                "reasoning": reasoning_result,
                "requires_review": requires_review
            })

            print("Status:", calculation_result.get("status"))
            print("Requires Review:", requires_review)

        except Exception as error:

            final_results.append({
                "record_number": index,
                "asset_data": asset_data,
                "status": "error",
                "error": str(error),
                "requires_review": True
            })

            print("Processing Error:", error)

    # STEP 5: Prepare summary

    calculated = sum(
        1 for item in final_results
        if item.get("calculation", {}).get("status") == "calculated"
    )

    manual_review = sum(
        1 for item in final_results
        if item.get("calculation", {}).get("status") == "manual_review"
    )

    requires_review = sum(
        1 for item in final_results
        if item.get("requires_review", False)
    )

    errors = sum(
        1 for item in final_results
        if item.get("status") == "error"
        or item.get("calculation", {}).get("status") == "error"
    )

    # STEP 6: Generate final report

    report = {
        "project": "Financial Tax Processing System",
        "jurisdiction": "India",
        "total_records": len(records),
        "successfully_calculated": calculated,
        "manual_review": manual_review,
        "requires_review": requires_review,
        "errors": errors,
        "results": final_results
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "batch_tax_report.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    # STEP 7: Display final summary

    print("\n===== BATCH PROCESSING COMPLETED =====")
    print("Total records:", len(records))
    print("Calculated:", calculated)
    print("Manual review:", manual_review)
    print("Requires review:", requires_review)
    print("Errors:", errors)

    print("\nReport saved at:", output_file)

    return report


if __name__ == "__main__":
    process_batch()
