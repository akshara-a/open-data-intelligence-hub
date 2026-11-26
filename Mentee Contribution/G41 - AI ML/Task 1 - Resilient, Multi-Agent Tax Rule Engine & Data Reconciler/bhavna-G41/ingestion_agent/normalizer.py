
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "processed"

# India configuration
JURISDICTION = "India"
CURRENCY = "INR"


# Column mapping
COLUMN_MAPPING = {
    "asset": "asset_name",
    "asset name": "asset_name",
    "cost": "purchase_cost",
    "amount": "purchase_cost",
    "purchase amount": "purchase_cost",
    "date": "purchase_date",
    "purchase date": "purchase_date"
}


# Read CSV or Excel
def read_input_file(file_path):

    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif file_path.suffix.lower() == ".xlsx":
        return pd.read_excel(file_path, engine="openpyxl")

    else:
        raise ValueError("Unsupported file format")


# Normalize data
def normalize_data(file_path):

    df = read_input_file(file_path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
    )

    # Rename columns
    df = df.rename(columns=COLUMN_MAPPING)

    required_columns = [
        "asset_name",
        "purchase_cost",
        "purchase_date"
    ]

    # Check missing columns
    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Clean asset names
    df["asset_name"] = (
        df["asset_name"].astype("string").str.strip()
    )

    df["asset_name"] = df["asset_name"].replace("", pd.NA)

    # Convert cost to numeric
    df["purchase_cost"] = pd.to_numeric(
        df["purchase_cost"],
        errors="coerce"
    )

    # Convert dates
    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    # Add India jurisdiction and currency
    df["jurisdiction"] = JURISDICTION
    df["currency"] = CURRENCY

    # Generate validation reasons
    reasons = []

    for _, row in df.iterrows():

        record_reasons = []

        if pd.isna(row["asset_name"]):
            record_reasons.append("Missing asset name")

        if pd.isna(row["purchase_cost"]):
            record_reasons.append("Missing or invalid cost")

        elif row["purchase_cost"] <= 0:
            record_reasons.append("Cost must be greater than zero")

        if pd.isna(row["purchase_date"]):
            record_reasons.append("Missing or invalid purchase date")

        reasons.append("; ".join(record_reasons))

    df["validation_reason"] = reasons

    # Separate valid and invalid records
    valid_records = df[
        df["validation_reason"] == ""
    ].copy()

    invalid_records = df[
        df["validation_reason"] != ""
    ].copy()

    # Format dates
    valid_records["purchase_date"] = (
        valid_records["purchase_date"].dt.strftime("%Y-%m-%d")
    )

    invalid_records["purchase_date"] = (
        invalid_records["purchase_date"].dt.strftime("%Y-%m-%d")
    )

    return valid_records, invalid_records


# Main execution
if __name__ == "__main__":

    input_files = [
        BASE_DIR / "data" / "raw" / "client_data.csv",
        BASE_DIR / "data" / "raw" / "client_data.xlsx"
    ]

    all_valid = []
    all_invalid = []

    for input_file in input_files:

        if not input_file.exists():
            print(f"File not found: {input_file.name}")
            continue

        print(f"\nProcessing: {input_file.name}")

        valid, invalid = normalize_data(input_file)

        all_valid.append(valid)
        all_invalid.append(invalid)

        print("Valid records:", len(valid))
        print("Invalid records:", len(invalid))

    if not all_valid:
        raise FileNotFoundError(
            "No CSV or Excel input file found."
        )

    # Combine records
    valid_data = pd.concat(all_valid, ignore_index=True)
    invalid_data = pd.concat(all_invalid, ignore_index=True)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save valid records
    valid_data.to_json(
        OUTPUT_DIR / "normalized_data.json",
        orient="records",
        indent=4
    )

    # Save invalid records
    invalid_data.to_json(
        OUTPUT_DIR / "invalid_records.json",
        orient="records",
        indent=4
    )

    print("\nBATCH NORMALIZATION COMPLETED!")
    print("Total valid records:", len(valid_data))
    print("Total invalid records:", len(invalid_data))
    print("Jurisdiction: India")
    print("Currency: INR")
