import json
from pathlib import Path
from supervisor_agent.supervisor import run_supervisor
from audit_logs.audit_logger import log_transaction
BASE_DIR = Path(__file__).resolve().parent
EMAIL_FILE = BASE_DIR / "data" / "raw" / "sample_email_india.txt"
OUTPUT_DIR = BASE_DIR / "outputs"
def main():

    print("\n================================")
    print(" FINANCIAL TAX PROCESSING SYSTEM")
    print("================================")

    if not EMAIL_FILE.exists():
        print("Error: Sample email file not found!")
        return

    email_text = EMAIL_FILE.read_text(encoding="utf-8")

    try:
        result = run_supervisor(email_text)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        output_file = OUTPUT_DIR / "final_tax_report.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("\nFINAL REPORT GENERATED!")
        print(f"Report saved at: {output_file}")
        log_transaction(result)
        print("\nFinal Status:")
        print(result.get("calculation", {}).get("status"))

        print("\nManual Review Required:")
        print(result.get("requires_review"))

    except Exception as error:
        print("\nSYSTEM ERROR:")
        print(error)


if __name__ == "__main__":
    main()
