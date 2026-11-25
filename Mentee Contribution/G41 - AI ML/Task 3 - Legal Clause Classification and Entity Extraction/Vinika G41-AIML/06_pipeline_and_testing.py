"""
STEP 6 - Run the complete pipeline, JSON output and testing

IMPORTANT: everything below is a DEMONSTRATION.
  - The clauses are written by me. They are not real contracts and not an independent test set.
  - The "human expectation" is what a human reader would say. The predictions are produced live
    by the trained model. Nothing is hard-coded and some predictions may be wrong.
  - OCR robustness is NOT proven here. We only try two hand-made examples and a SIMULATED noise test.

JSON output = the structure from the project brief, plus two small extra fields:
  'start'/'end' of each clause and 'clauses_checked' (how many clauses were looked at).

Run:  python 06_pipeline_and_testing.py   (after steps 4; needs the spaCy model)
"""
import os
import json
import random
import pandas as pd
from sklearn.metrics import accuracy_score

from common import DATA_DIR, OUTPUT_DIR, RANDOM_SEED, class_names, class_to_id, clean_text
from model_tools import get_embeddings, predict_probs
from pipeline import load_models, analyze_contract

# %% Load everything (BERT + trained BiLSTM + spaCy)
models = load_models()

# %% 1) The complete pipeline on a small invented contract -> JSON
sample_file = os.path.join(DATA_DIR, "sample_contract.txt")
with open(sample_file, "r", encoding="utf-8") as f:
    contract_text = f.read()

result = analyze_contract(contract_text, "CONTRACT_001", models)
json_text = json.dumps(result, indent=2)
print(json_text)

with open(os.path.join(OUTPUT_DIR, "sample_output.json"), "w", encoding="utf-8") as f:
    f.write(json_text)

# check that every entity position really points to the same text in the contract
problems = 0
for clause in result["clauses"]:
    for ent in clause["entities"]:
        if contract_text[ent["start"]:ent["end"]] != ent["text"]:
            problems += 1
print()
print("Entities whose positions do NOT match the contract text:", problems)
print("Clauses checked:", result["clauses_checked"], "| flagged:", len(result["clauses"]))

# %% 2) Hand-written demonstration clauses (different wording from the templates)
demo_clauses = [
    ("Demo 1", "Indemnification",
     "Bluewater Trading Company Limited agrees to indemnify and defend Meridian Retail Corporation against all third party claims, losses and expenses arising out of the negligence of Bluewater Trading Company Limited. This obligation shall continue until 15 March 2027."),
    ("Demo 2", "Limitation of Liability",
     "Harbor Analytics LLC shall not be responsible for any indirect or consequential losses, and its total liability under this Agreement is restricted to $25,000."),
    ("Demo 3", "Force Majeure",
     "If a force majeure event such as a flood, strike or pandemic prevents Summit Energy Ltd. from delivering the goods by 1 September 2026, the delivery date shall be extended for as long as the event continues."),
    ("Demo 4 (harder: no keyword)", "Force Majeure",
     "Neither Delta Mining Corp. nor its customer will be held to blame for a failure to deliver caused by earthquakes, war or acts of government."),
    ("Demo 5 (not a risk clause)", "Other",
     "This Agreement shall be governed by the laws of India. Payment of Rs. 5,00,000 shall be made to Orion Software Inc. within 30 days of the invoice."),
    ("Demo 6 (tricky words 'force and effect')", "Other",
     "If any part of this Agreement is found to be unenforceable, the rest of the Agreement shall remain in full force and effect."),
]

print()
print("=" * 70)
print("DEMONSTRATION CLAUSES (written by me, not real contracts, not a test set)")
for name, expected, text in demo_clauses:
    emb, mask = get_embeddings([clean_text(text)], models["tokenizer"], models["bert_model"], models["device"])
    probs = predict_probs(models["clf_model"], emb, mask, models["device"])[0]
    print()
    print("-----", name, "| human expectation:", expected)
    for i in range(len(class_names)):
        print("    ", class_names[i], ":", round(float(probs[i]), 3))
    out = analyze_contract(text, "DEMO", models)
    if len(out["clauses"]) == 0:
        print("  -> pipeline: NOT flagged as a risk clause")
    else:
        c = out["clauses"][0]
        print("  -> pipeline:", c["classification"], "| confidence", c["confidence"])
        for e in c["entities"]:
            print("     entity:", e)

# %% 3) OCR-style input: spelling errors, missing punctuation, broken lines (two hand-made examples)
ocr_examples = [
    "2. LIMITATI0N OF LIABILITY. IN N0 EVENT SHALL HARB0R ANALYTICS LLC BE LIABLE FOR INDIRECT OR CONSEQUENTIAL\nDAMAGES AND ITS TOTAL Iiability SHALL NOT EXCEED $25,000",
    "Harbor Analytics LLC shall indemnifv and hold harmless Orion Software Inc from any claim loss or expense arising out of a breach of this Agree-\nment by Harbor Analytics LLC",
]

print()
print("=" * 70)
print("OCR-STYLE EXAMPLES (two hand-made examples, NOT a proper OCR evaluation)")
for text in ocr_examples:
    print()
    print("INPUT         :", repr(text))
    print("AFTER CLEANING:", clean_text(text))
    print(json.dumps(analyze_contract(text, "OCR_DEMO", models), indent=2))

# %% 4) Simulated OCR noise on the whole test set (random letter confusions: l->1, o->0, m->rn ...)
# This is SIMULATED noise. It is not the same as real scanned documents.
test_file = os.path.join(DATA_DIR, "test_set.csv")
if os.path.exists(test_file):
    test_df = pd.read_csv(test_file)
    y_test = [class_to_id[label] for label in test_df["label"]]

    random.seed(RANDOM_SEED)
    confusions = {"l": "1", "i": "l", "o": "0", "e": "c", "m": "rn"}
    noisy_texts = []
    for text in test_df["clean_text"]:
        chars = list(text)
        for k in range(len(chars)):
            if chars[k] in confusions and random.random() < 0.03:
                chars[k] = confusions[chars[k]]
        noisy_texts.append("".join(chars))

    clean_emb, clean_mask = get_embeddings(list(test_df["clean_text"]), models["tokenizer"], models["bert_model"], models["device"])
    noisy_emb, noisy_mask = get_embeddings(noisy_texts, models["tokenizer"], models["bert_model"], models["device"])
    clean_pred = predict_probs(models["clf_model"], clean_emb, clean_mask, models["device"]).argmax(axis=1)
    noisy_pred = predict_probs(models["clf_model"], noisy_emb, noisy_mask, models["device"]).argmax(axis=1)

    print()
    print("=" * 70)
    print("SIMULATED OCR NOISE on the test set (random letter swaps, NOT real scans)")
    print("Test accuracy on clean text        :", round(accuracy_score(y_test, clean_pred), 4))
    print("Test accuracy with simulated noise :", round(accuracy_score(y_test, noisy_pred), 4))
    print("Example noisy text:", noisy_texts[0][:150])
    print("This shows how the model reacts to this one type of noise. It does not prove OCR robustness.")
else:
    print("data/test_set.csv not found (created by step 4) -> noise test skipped.")
