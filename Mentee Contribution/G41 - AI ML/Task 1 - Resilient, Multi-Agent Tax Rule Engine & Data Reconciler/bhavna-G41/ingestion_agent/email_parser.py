
import re
import json
from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
EMAIL_FILE = BASE_DIR / "data" / "raw" / "sample_email.txt"

OUTPUT_DIR = BASE_DIR / "data" / "processed"


def extract_email_data(email_text):

    result = {
        "asset_name": None,
        "quantity": None,
        "purchase_cost": None,
        "purchase_date": None,
        "jurisdiction": None,
        "region": None,
        "review_required": False,
        "currency": None,
        "missing_fields": []
    }

    # 1. Extract quantity and asset name
    asset_match = re.search(
        r"purchased\s+(\d+)\s+([a-zA-Z]+)",
        email_text,
        re.IGNORECASE
    )

    if asset_match:
        result["quantity"] = int(asset_match.group(1))
        result["asset_name"] = asset_match.group(2)

    # 2. Extract total purchase amount
    amount_match = re.search(
        r"total amount of\s*[$₹]?\s*([\d,]+(?:\.\d{1,2})?)",
        email_text,
        re.IGNORECASE
    )

    if amount_match:
        result["purchase_cost"] = float(
            amount_match.group(1).replace(",", "")
        )

    # 3. Detect currency
    currency_match = re.search(
        r"([$₹]|\bUSD\b|\bINR\b)",
        email_text,
        re.IGNORECASE
    )

    if currency_match:
        symbol = currency_match.group(1)

        if symbol in ["$", "USD"]:
            result["currency"] = "USD"

        elif symbol in ["₹", "INR"]:
            result["currency"] = "INR"

    # 4. Extract purchase date
    date_match = re.search(
        r"on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        email_text,
        re.IGNORECASE
    )

    if date_match:
        parsed_date = pd.to_datetime(
            date_match.group(1),
            format="%d %B %Y",
            errors="coerce"
        )

        if not pd.isna(parsed_date):
            result["purchase_date"] = parsed_date.strftime("%Y-%m-%d")

    # 5. Extract location
    location_match = re.search(
        r"located in\s+([A-Za-z ]+),\s*(USA|US|India)",
        email_text,
        re.IGNORECASE
    )

    if location_match:
        result["region"] = location_match.group(1).strip()

        country = location_match.group(2).lower()

        if country in ["usa", "us"]:
            result["jurisdiction"] = "US"

        elif country == "india":
            result["jurisdiction"] = "India"

    # 6. Check missing information
    required_fields = [
        "asset_name",
        "quantity",
        "purchase_cost",
        "purchase_date",
        "jurisdiction"
    ]

    for field in required_fields:
        if result[field] is None:
            result["missing_fields"].append(field)

    # 7. Flag incomplete emails
    result["review_required"] = (
        len(result["missing_fields"]) > 0
    )

    return result


# Main execution
if __name__ == "__main__":

    email_text = EMAIL_FILE.read_text(encoding="utf-8")

    extracted_data = extract_email_data(email_text)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "email_extracted.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(extracted_data, file, indent=4)

    print("\nEMAIL EXTRACTION COMPLETED!")

    print(json.dumps(extracted_data, indent=4))

    print(f"\nOutput saved at: {output_file}")
