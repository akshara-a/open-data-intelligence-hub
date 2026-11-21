"""
Merge CUAD data (Limitation of Liability) with synthetic data
(Indemnification, Force Majeure, Other) for balanced training.
"""
import json
import os
import random


def generate_synthetic():
    random.seed(42)
    ORGS = ["Acme Corp", "Beta LLC", "Gamma Inc", "Delta Co", "Epsilon Ltd",
            "Zenith Holdings", "Omega Partners", "Alpha Industries"]
    DATES = ["31 December 2024", "1 January 2025", "15 March 2024",
             "30 June 2025", "10 October 2026", "20 February 2025"]
    MONEYS = ["$10,000", "$250,000", "€5,000", "$1,000,000",
              "$500,000", "£75,000", "$2,500,000"]

    INDEMNIFICATION = [
        "{org1} shall indemnify and hold harmless {org2} from any and all claims, damages, losses, and expenses arising out of or related to this Agreement, subject to the limitations set forth herein.",
        "{org1} agrees to indemnify, defend, and hold {org2} harmless from and against any liabilities, costs, or expenses (including reasonable attorneys' fees) resulting from any breach of this Agreement.",
        "Each party shall indemnify the other party against any third-party claims arising from its negligence or willful misconduct under this Agreement, up to a maximum of {money}.",
        "{org1} shall defend, indemnify, and hold harmless {org2} and its officers, directors, and employees from and against all claims arising from {org1}'s performance of the Services.",
        "The indemnification obligations of {org1} shall survive termination of this Agreement and shall not be limited by any cap on liability.",
        "{org1} hereby indemnifies {org2} for all losses, damages, and expenses incurred as a result of {org1}'s breach of its obligations under this Agreement.",
        "Notwithstanding anything to the contrary, {org1} shall indemnify {org2} for any and all claims relating to intellectual property infringement arising from the use of the Deliverables.",
        "{org1} shall indemnify {org2} against all losses arising from third-party claims, effective {date}, up to {money}.",
    ]
    FORCE_MAJEURE = [
        "Neither party shall be liable for any failure or delay in performing its obligations under this Agreement if such failure or delay is caused by an event of force majeure, including but not limited to acts of God, war, terrorism, or natural disasters.",
        "If a force majeure event continues for more than thirty (30) days, either party may terminate this Agreement upon written notice to the other party.",
        "{org1} shall notify {org2} promptly upon becoming aware of any force majeure event affecting its performance, and shall use reasonable efforts to mitigate the impact of such event.",
        "Neither party shall be considered in breach of this Agreement due to any delay or failure to perform caused by circumstances beyond its reasonable control, including force majeure events as defined herein.",
        "In the event of force majeure, the affected party shall be excused from performance for the duration of the event, provided that it gives prompt written notice to the other party.",
        "Force majeure events shall include, without limitation, earthquakes, floods, fires, pandemics, governmental actions, and any other events beyond the reasonable control of the affected party.",
        "A force majeure event affecting {org1} as of {date} shall not relieve {org2} of its payment obligations accrued prior to such event.",
    ]
    OTHER = [
        "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.",
        "This Agreement constitutes the entire agreement between the parties and supersedes all prior agreements, understandings, and representations, whether written or oral.",
        "Any notice required or permitted under this Agreement shall be in writing and shall be deemed given when delivered personally or sent by certified mail.",
        "The parties agree that this Agreement may be executed in counterparts, each of which shall be deemed an original and all of which together shall constitute one instrument.",
        "{org1} shall pay {org2} the sum of {money} within thirty days of the Effective Date.",
        "This Agreement shall commence on {date} and shall continue for a period of one year unless terminated earlier in accordance with its terms.",
        "Either party may terminate this Agreement upon thirty (30) days' prior written notice to the other party.",
        "The parties acknowledge that the Effective Date of this Agreement is {date}, and all obligations shall commence as of that date.",
    ]

    def build(templates, label, count):
        rows = []
        for _ in range(count):
            t = random.choice(templates)
            org1, org2 = random.sample(ORGS, 2)
            date = random.choice(DATES)
            money = random.choice(MONEYS)
            text = t.format(org1=org1, org2=org2, date=date, money=money)
            entities = []
            for org in ORGS:
                if org in text:
                    start = text.find(org)
                    entities.append({"type": "ORG", "start": start,
                                     "end": start + len(org), "text": org})
            for date_v in DATES:
                if date_v in text:
                    start = text.find(date_v)
                    entities.append({"type": "DATE", "start": start,
                                     "end": start + len(date_v), "text": date_v})
            for money_v in MONEYS:
                if money_v in text:
                    start = text.find(money_v)
                    entities.append({"type": "MONEY", "start": start,
                                     "end": start + len(money_v), "text": money_v})
            rows.append({"text": text, "clause": label, "entities": entities})
        return rows

    return (build(INDEMNIFICATION, "Indemnification", 400) +
            build(FORCE_MAJEURE, "Force Majeure", 400) +
            build(OTHER, "Other", 200))


def main():
    CUAD_FILE = "data/annotated/train.jsonl"
    cuad_rows = []
    if os.path.exists(CUAD_FILE):
        with open(CUAD_FILE, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r["clause"] == "Limitation of Liability":
                    cuad_rows.append(r)
    print(f"CUAD LoL rows: {len(cuad_rows)}")

    synthetic = generate_synthetic()
    print(f"Synthetic rows generated: {len(synthetic)}")

    all_rows = cuad_rows + synthetic
    random.seed(42)
    random.shuffle(all_rows)

    os.makedirs("data/annotated", exist_ok=True)
    with open(CUAD_FILE, "w", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    from collections import Counter
    dist = Counter(r["clause"] for r in all_rows)
    print(f"\n✅ Wrote {len(all_rows)} rows to {CUAD_FILE}")
    print("Label distribution:")
    for k, v in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()