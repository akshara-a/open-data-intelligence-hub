
import json
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Tax rules directory
TAX_RULES_DIR = BASE_DIR / "tax_rules"


def load_tax_rules(jurisdiction):
    """
    Load jurisdiction-specific tax rules.
    Supported jurisdictions: India and US.
    """

    jurisdiction = jurisdiction.strip().lower()

    jurisdiction_map = {
        "india": "india",
        "in": "india",
        "us": "us",
        "usa": "us"
    }

    if jurisdiction not in jurisdiction_map:
        raise ValueError(
            f"Unsupported jurisdiction: {jurisdiction}"
        )

    country_folder = jurisdiction_map[jurisdiction]

    rules_file = (
        TAX_RULES_DIR / country_folder / "tax_rules.json"
    )

    if not rules_file.exists():
        raise FileNotFoundError(
            f"Tax rules file not found: {rules_file}"
        )

    with open(rules_file, "r", encoding="utf-8") as file:
        rules = json.load(file)

    if not isinstance(rules, dict):
        raise ValueError("Tax rules must be a JSON object")

    if rules.get("jurisdiction") != country_folder:
        raise ValueError("Jurisdiction mismatch in tax rules")

    if not isinstance(rules.get("rules"), list):
        raise ValueError("Rules must be stored as a list")

    return rules
