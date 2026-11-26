
import json
from pathlib import Path
from datetime import date

from pydantic import BaseModel, Field, ConfigDict, ValidationError


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "normalized_data.json"


class FinancialAsset(BaseModel):

    model_config = ConfigDict(extra="ignore")

    asset_name: str = Field(min_length=1)

    purchase_cost: float = Field(gt=0)

    purchase_date: date

    jurisdiction: str = Field(min_length=1)

    currency: str = Field(min_length=1)


def validate_financial_data():

    # Read normalized JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    valid_records = []
    invalid_records = []

    # Validate each record
    for index, record in enumerate(records):

        try:
            asset = FinancialAsset.model_validate(record)

            valid_records.append(
                asset.model_dump(mode="json")
            )

        except ValidationError as error:

            invalid_records.append({
                "record_number": index + 1,
                "original_data": record,
                "errors": error.errors(
                    include_url=False
                )
            })

    # Display results
    print("\nPYDANTIC VALIDATION RESULTS")

    print("\nValid Records:")
    print(json.dumps(valid_records, indent=4))

    print("\nInvalid Records:")
    print(json.dumps(invalid_records, indent=4))

    print("\nValidation Summary:")
    print("Valid:", len(valid_records))
    print("Invalid:", len(invalid_records))


if __name__ == "__main__":
    validate_financial_data()
