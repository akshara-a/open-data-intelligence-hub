"""
Downloads CUAD_v1.json, extracts category from 'id' field using '__' separator,
writes data/annotated/train.jsonl with ORG/DATE/MONEY entities.
"""
import json
import os
import random
import re
import urllib.request

CUAD_JSON_URL = "https://huggingface.co/datasets/theatticusproject/cuad/resolve/main/CUAD_v1/CUAD_v1.json"
LOCAL_JSON = "data/raw/CUAD_v1.json"

# Substring → our label (case-insensitive)
CATEGORY_MAP = [
    ("indemnification", "Indemnification"),
    ("limitation of liability", "Limitation of Liability"),
    ("limitation of liab", "Limitation of Liability"),
    ("cap on liability", "Limitation of Liability"),
    ("uncapped liability", "Limitation of Liability"),
    ("liquidated damages", "Limitation of Liability"),
    ("force majeure", "Force Majeure"),
]

DATE_PATTERN = re.compile(
    r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}"
    r"|\d{1,2}/\d{1,2}/\d{2,4}"
    r"|\d{4}-\d{2}-\d{2})\b"
)
MONEY_PATTERN = re.compile(r"[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand))?")
ORG_PATTERN = re.compile(
    r"\b(?:[A-Z][A-Za-z&.'-]+\s+){1,4}(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Corporation|Company|Co\.|LP|LLP|GmbH|plc|PLC)\b"
)


def extract_entities(text):
    spans = []
    for pat, kind in [(ORG_PATTERN, "ORG"), (DATE_PATTERN, "DATE"), (MONEY_PATTERN, "MONEY")]:
        for m in pat.finditer(text):
            spans.append({"type": kind, "start": m.start(), "end": m.end(), "text": m.group()})
    spans.sort(key=lambda x: x["start"])
    clean, last_end = [], -1
    for s in spans:
        if s["start"] >= last_end:
            clean.append(s)
            last_end = s["end"]
    return clean


def category_from_id(qa_id):
    """Extract category = text after last '__' in the id."""
    if "__" not in qa_id:
        return None
    return qa_id.rsplit("__", 1)[-1].strip()


def map_category(raw):
    if not raw:
        return None
    low = raw.lower()
    for key, mapped in CATEGORY_MAP:
        if key in low:
            return mapped
    return None


def download_json():
    os.makedirs("data/raw", exist_ok=True)
    if os.path.exists(LOCAL_JSON) and os.path.getsize(LOCAL_JSON) > 10_000_000:
        print(f"Using cached {LOCAL_JSON}")
        return LOCAL_JSON
    print(f"Downloading {CUAD_JSON_URL}")
    urllib.request.urlretrieve(CUAD_JSON_URL, LOCAL_JSON)
    print(f"Saved ({os.path.getsize(LOCAL_JSON)/1e6:.1f} MB)")
    return LOCAL_JSON


def main():
    path = download_json()
    print("Parsing CUAD JSON...")
    with open(path, encoding="utf-8") as f:
        cuad = json.load(f)

    rows = []
    label_counts = {}
    other_candidates = []

    for contract in cuad["data"]:
        for para in contract["paragraphs"]:
            for qa in para["qas"]:
                raw_cat = category_from_id(qa["id"])
                mapped = map_category(raw_cat)
                for ans in qa["answers"]:
                    clause_text = ans["text"].strip()
                    if not (20 <= len(clause_text) <= 500):
                        continue
                    if mapped is not None:
                        rows.append({
                            "text": clause_text,
                            "clause": mapped,
                            "entities": extract_entities(clause_text),
                        })
                        label_counts[mapped] = label_counts.get(mapped, 0) + 1
                    elif mapped is None:
                        other_candidates.append(clause_text)

    print(f"Target rows: {len(rows)}; candidate Other: {len(other_candidates)}")

    # Balance: add up to len(rows) "Other" examples (or 2000 max)
    random.seed(42)
    random.shuffle(other_candidates)
    target_other = min(len(rows), len(other_candidates), 2000)
    for t in other_candidates[:target_other]:
        rows.append({
            "text": t,
            "clause": "Other",
            "entities": extract_entities(t),
        })
        label_counts["Other"] = label_counts.get("Other", 0) + 1

    random.shuffle(rows)
    os.makedirs("data/annotated", exist_ok=True)
    with open("data/annotated/train.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n✅ Wrote {len(rows)} rows to data/annotated/train.jsonl")
    print("Label distribution:")
    for k, v in sorted(label_counts.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()