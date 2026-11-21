import json
from pathlib import Path
from datetime import datetime, timezone
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_FILE = BASE_DIR / "audit_logs" / "audit_log.json"
def log_transaction(result):

    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    audit_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "asset_name": result.get("asset_data", {}).get("asset_name"),
        "jurisdiction": result.get("asset_data", {}).get("jurisdiction"),
        "rule_id": result.get("calculation", {}).get("rule_id"),
        "status": result.get("calculation", {}).get("status"),
        "requires_review": result.get("requires_review", False)
    }

    existing_records = []

    if AUDIT_FILE.exists():
        try:
            with open(AUDIT_FILE, "r", encoding="utf-8") as file:
                existing_records = json.load(file)

            if not isinstance(existing_records, list):
                raise ValueError("Audit log must contain a JSON list.")

        except (json.JSONDecodeError, ValueError):
            raise ValueError("Existing audit log is invalid. Backup and inspect it first.")

    existing_records.append(audit_record)

    temp_file = AUDIT_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(existing_records, file, indent=4)

    temp_file.replace(AUDIT_FILE)

    print("[5] Audit log saved")

    return audit_record
