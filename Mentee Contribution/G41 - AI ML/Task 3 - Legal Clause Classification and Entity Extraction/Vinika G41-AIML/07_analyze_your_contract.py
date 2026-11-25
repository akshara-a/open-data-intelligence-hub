"""
STEP 7 - Analyze your own contract text file

Usage:
    python 07_analyze_your_contract.py                     (uses data/sample_contract.txt)
    python 07_analyze_your_contract.py path/to/contract.txt

The file must be plain text (.txt). Separate clauses with a BLANK LINE, because that is how the
simple clause splitter finds clause boundaries. The result is printed and saved in
outputs/your_contract_output.json

Notes:
  - Start/end positions are counted in the text as Python reads the file
    (Windows line endings are read as a single newline character).
  - The output is a SUGGESTION for a human reviewer, never a legal decision.
"""
import os
import sys
import json

from common import DATA_DIR, OUTPUT_DIR
from pipeline import load_models, analyze_contract

# %% Choose the file
if len(sys.argv) > 1:
    contract_file = sys.argv[1]
else:
    contract_file = os.path.join(DATA_DIR, "sample_contract.txt")

if not os.path.exists(contract_file):
    print("File not found:", contract_file)
    raise SystemExit

with open(contract_file, "r", encoding="utf-8") as f:
    contract_text = f.read()

# %% Run the pipeline
models = load_models()
contract_id = os.path.splitext(os.path.basename(contract_file))[0].upper()
result = analyze_contract(contract_text, contract_id, models)

# %% Print and save the JSON
json_text = json.dumps(result, indent=2)
print(json_text)

output_file = os.path.join(OUTPUT_DIR, "your_contract_output.json")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(json_text)

print()
print("Clauses checked:", result["clauses_checked"], "| flagged:", len(result["clauses"]))
print("Saved to:", output_file)
print("Reminder: a lawyer must review these results.")
