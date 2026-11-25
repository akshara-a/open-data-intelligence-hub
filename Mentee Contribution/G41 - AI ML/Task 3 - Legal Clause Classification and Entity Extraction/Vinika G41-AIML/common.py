"""
common.py - shared settings and the text-cleaning function used by all scripts.

No heavy libraries (torch, transformers) are imported here,
so scripts 01, 02 and 05 start quickly.
"""
import os
import re

# ---------- folders (always relative to this file, so it works from any terminal location) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- settings ----------
RANDOM_SEED = 42
BERT_NAME = "bert-base-uncased"      # pretrained BERT used for tokenizing and embeddings (not generative)
SPACY_MODEL = "en_core_web_sm"       # pretrained spaCy model used for NER
MAX_LEN = 128                        # maximum number of BERT tokens per clause (longer clauses are cut)
CONFIDENCE_THRESHOLD = 0.60          # clauses below this confidence are NOT flagged as risk clauses

# The 3 classes asked in the project + an extra "Other" class (see README for why)
class_names = ["Indemnification", "Limitation of Liability", "Force Majeure", "Other"]
risk_classes = ["Indemnification", "Limitation of Liability", "Force Majeure"]

# give every class a number (models need numbers, not names)
class_to_id = {}
for i in range(len(class_names)):
    class_to_id[class_names[i]] = i
other_id = class_to_id["Other"]

# entity types we keep from spaCy
wanted_labels = ["ORG", "DATE", "MONEY"]

# A small dictionary of KNOWN OCR mistakes (only a few examples; real OCR makes many more kinds of errors)
ocr_fixes = {
    "indemnifv": "indemnify",
    "indemnitv": "indemnity",
    "liabilitv": "liability",
    "iiability": "liability",
    "iiable": "liable",
    "agrcement": "agreement",
}


def clean_text(text):
    """Make a cleaned COPY of a clause. The original text is never changed.

    We only do safe changes. We do NOT remove stop words, numbers or punctuation,
    because words like 'not' and amounts like '$50,000' change legal meaning.
    """
    # join words that were split with a hyphen at the end of a line
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    # fancy quotes and dashes -> normal ones
    text = text.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'").replace("\u2013", "-")
    # line breaks and multiple spaces -> one space
    text = re.sub(r"\s+", " ", text).strip()
    # fix known OCR mistakes
    for wrong, right in ocr_fixes.items():
        text = re.sub(r"\b" + wrong + r"\b", right, text, flags=re.IGNORECASE)
    return text
