"""
STEP 1 - Prepare the dataset

What this script does:
  1. Builds SYNTHETIC clauses (written by me with templates and made-up company names).
  2. Tries to download REAL clauses from LEDGAR (a public dataset of contract paragraphs from
     US SEC filings, part of the LexGLUE benchmark on Hugging Face).
     Real clauses are used for "Indemnification" and for the "Other" class.
  3. Combines both into data/dataset.csv. Every row has a 'source' column (real / synthetic).

Why synthetic data at all?
  LEDGAR does not seem to contain labels for Force Majeure or Limitation of Liability.
  This script prints the LEDGAR labels that match our classes, so you can check it yourself.
  If real labels for them exist, the script uses them automatically.

IMPORTANT: synthetic clauses are NOT real contracts. Never present them as a real dataset.

Run:  python 01_prepare_data.py
"""
import os
import random
import pandas as pd

from common import DATA_DIR, RANDOM_SEED, class_names

USE_LEDGAR = True             # set to False to skip the download and use synthetic data only
N_SYNTHETIC_PER_CLASS = 200   # synthetic clauses per class
N_REAL_PER_CLASS = 200        # real LEDGAR clauses per class (if available)

random.seed(RANDOM_SEED)

# %% ---------------------------------------------------------------------------------------------
# PART A: synthetic clauses
# Each template is a sentence with blanks like {p1} (company 1) or {amount}.
# We fill the blanks with random choices. All companies, dates and amounts are MADE UP.
# Some Force Majeure templates do NOT contain the words "force majeure", and one "Other" template
# contains "full force and effect", so the model cannot just look for a single keyword.

orgs = [
    "Alpha Solutions Private Limited", "Brightwave Technologies Inc.", "Crestline Logistics LLC",
    "Delta Manufacturing Co.", "Everpeak Software Ltd.", "Northgate Holdings Corporation",
    "Oakridge Consulting LLP", "Sunrise Foods Private Limited", "Titan Infrastructure Ltd.",
    "Union Pharma Inc.", "Vertex Retail Corporation", "Zenith Energy Limited",
]
dates = ["January 15, 2025", "30 June 2026", "March 1, 2024", "31 December 2025",
         "September 30, 2027", "15 August 2026", "April 10, 2025", "1 November 2026"]
amounts = ["$50,000", "$250,000", "$1,000,000", "USD 75,000", "EUR 120,000", "$10,000",
           "Rs. 10,00,000", "$500,000"]
day_counts = ["ten (10) days", "thirty (30) days", "sixty (60) days", "ninety (90) days",
              "fifteen (15) days", "seven (7) days"]
months = ["six (6)", "twelve (12)", "twenty-four (24)"]
causes = ["a breach of this Agreement", "negligence or wilful misconduct",
          "infringement of third party intellectual property rights",
          "violation of applicable law", "personal injury or damage to property"]
fm_events = ["floods, earthquakes, fire, war or terrorism", "pandemics, epidemics or government restrictions",
             "strikes, riots or civil unrest", "fire, explosion or natural disasters",
             "power failures, transport disruption or war"]
places = ["India", "the State of Delaware", "England and Wales", "Singapore", "the State of New York"]

templates = {
    "Indemnification": [
        "{p1} shall indemnify, defend and hold harmless {p2} from and against all claims, losses, damages and expenses arising out of {cause}.",
        "{p1} agrees to indemnify {p2} and its officers and employees against any third party claim, including reasonable legal fees, resulting from {cause}.",
        "The indemnifying party, {p1}, shall compensate {p2} for all liabilities and costs incurred because of {cause}, and this obligation shall survive until {date}.",
        "{p2} shall be entitled to be indemnified by {p1} for any loss suffered as a result of {cause}, provided that {p2} gives written notice of the claim within {days}.",
        "Each party shall indemnify the other against claims made by third parties arising from {cause}, and shall pay all amounts finally awarded by a court.",
        "{p1} will defend {p2} against any action brought by a third party alleging {cause}, and will pay the damages and costs finally awarded.",
    ],
    "Limitation of Liability": [
        "In no event shall {p1} be liable to {p2} for any indirect, incidental, special or consequential damages, including loss of profits or loss of data.",
        "The total aggregate liability of {p1} arising out of this Agreement shall not exceed {amount}.",
        "{p1} shall not be liable for any loss of revenue, loss of goodwill or loss of business opportunity, and its liability shall be limited to the fees paid by {p2} in the {months} months before the claim arose.",
        "Except in cases of fraud or wilful misconduct, the liability of either party under this Agreement shall in no case exceed {amount}, whether in contract, tort or otherwise.",
        "Neither party shall be responsible to the other for special or punitive damages, and the maximum liability of {p1} for direct damages is capped at {amount}.",
        "{p1} excludes all liability for consequential losses to the fullest extent permitted by law, and any claim by {p2} must be brought within {days} of the event giving rise to it.",
    ],
    "Force Majeure": [
        "Neither party shall be liable for any delay or failure to perform its obligations under this Agreement if the delay is caused by a force majeure event, including {fm_event}.",
        "If a force majeure event continues for more than {days}, {p2} may terminate this Agreement by giving written notice to {p1}.",
        "{p1} shall notify {p2} within {days} after the start of any force majeure event and shall make reasonable efforts to resume performance as soon as possible.",
        "{p1} will not be in breach of this Agreement for events beyond its reasonable control, such as {fm_event}, and the time for performance shall be extended until {date}.",
        "Performance by {p1} shall be suspended while it is prevented from performing by acts of God or {fm_event}, and the delivery date for {p2} shall be extended accordingly.",
        "Any failure by {p1} to meet its obligations resulting from circumstances outside its control, including {fm_event}, shall not be treated as a default.",
    ],
    "Other": [
        "This Agreement shall be governed by and construed in accordance with the laws of {place}, and the courts of {place} shall have exclusive jurisdiction.",
        "All notices under this Agreement shall be in writing and shall be delivered by hand or by registered post to the registered office of the receiving party.",
        "{p1} may not assign or transfer any of its rights under this Agreement without the prior written consent of {p2}.",
        "{p2} shall pay {p1} the sum of {amount} within {days} of receiving a valid invoice.",
        "Each party shall keep confidential all non-public information received from the other party until {date}.",
        "This Agreement shall come into effect on {date} and shall continue for a term of {months} months unless terminated earlier in accordance with its terms.",
        "If any provision of this Agreement is held to be invalid, the remaining provisions shall continue in full force and effect.",
        "Either party may terminate this Agreement for convenience by giving the other party {days} prior written notice.",
        "This Agreement constitutes the entire agreement between {p1} and {p2} and replaces all earlier discussions and understandings.",
        "{p1} shall maintain insurance coverage of at least {amount} throughout the term of this Agreement.",
        "{p1} represents and warrants that it has full power and authority to enter into this Agreement.",
        "No failure or delay by either party in exercising any right shall operate as a waiver of that right.",
    ],
}

# %% Generate the synthetic clauses (every clause is unique)
synthetic_rows = []
for label, template_list in templates.items():
    seen = set()
    clauses_for_label = []
    tries = 0
    while len(clauses_for_label) < N_SYNTHETIC_PER_CLASS and tries < 20000:
        tries += 1
        p1, p2 = random.sample(orgs, 2)
        clause = random.choice(template_list).format(
            p1=p1, p2=p2,
            amount=random.choice(amounts), date=random.choice(dates),
            days=random.choice(day_counts), months=random.choice(months),
            cause=random.choice(causes), fm_event=random.choice(fm_events),
            place=random.choice(places))
        # real liability clauses are often written in CAPITAL LETTERS, so we do that sometimes
        if label == "Limitation of Liability" and random.random() < 0.2:
            clause = clause.upper()
        if clause not in seen:
            seen.add(clause)
            clauses_for_label.append(clause)
    for clause in clauses_for_label:
        synthetic_rows.append({"text": clause, "label": label, "source": "synthetic (written by me)"})

synthetic_df = pd.DataFrame(synthetic_rows)
synthetic_df.to_csv(os.path.join(DATA_DIR, "synthetic_clauses.csv"), index=False)
print("Synthetic clauses created:", len(synthetic_df), "-> data/synthetic_clauses.csv")

# %% ---------------------------------------------------------------------------------------------
# PART B: real clauses from LEDGAR (needs internet and the 'datasets' library)
# The first source is the Hugging Face repository you chose (lighteval/lexglue, folder 'ledgar').
# If that fails we try the original LexGLUE repository. If everything fails, we continue
# with synthetic data only (nothing is faked).

real_df = pd.DataFrame(columns=["text", "label", "source"])
ledgar_file = os.path.join(DATA_DIR, "ledgar_sample.csv")

if USE_LEDGAR and os.path.exists(ledgar_file):
    real_df = pd.read_csv(ledgar_file)
    print("Re-using the saved LEDGAR sample:", ledgar_file, "(delete this file to download again)")

elif USE_LEDGAR:
    try:
        from datasets import load_dataset
    except ImportError:
        load_dataset = None
        print("The 'datasets' library is not installed -> skipping LEDGAR (pip install datasets).")

    ledgar = None
    attempts = [
        ("lighteval/lexglue", {"data_dir": "ledgar"}),
        ("coastalcph/lex_glue", {"name": "ledgar"}),
        ("coastalcph/lex_glue", {"name": "ledgar", "revision": "refs/convert/parquet"}),
    ]
    if load_dataset is not None:
        for repo, options in attempts:
            try:
                ledgar = load_dataset(repo, split="train", **options)
                print("Loaded LEDGAR from:", repo)
                break
            except Exception as error:
                print("Could not load from", repo, "->", str(error)[:120])

    if ledgar is None:
        print("LEDGAR not available -> continuing with SYNTHETIC data only.")
    else:
        try:
            ledgar_df = ledgar.to_pandas()
            print("LEDGAR rows:", len(ledgar_df), "| columns:", list(ledgar_df.columns))

            # find the name of each label (LEDGAR stores labels as numbers + a list of names)
            label_feature = ledgar.features["label"]
            if hasattr(label_feature, "names"):
                ledgar_df["label_name"] = [label_feature.names[i] for i in ledgar_df["label"]]
            else:
                ledgar_df["label_name"] = ledgar_df["label"].astype(str)

            print("LEDGAR labels that look like our target classes:")
            for name in sorted(ledgar_df["label_name"].unique()):
                lower = name.lower()
                if "indemn" in lower or "liabil" in lower or "force majeure" in lower:
                    print("    ", name)

            # map LEDGAR labels to our classes
            our_label = []
            for name in ledgar_df["label_name"]:
                lower = name.lower()
                if "indemn" in lower:
                    our_label.append("Indemnification")
                elif "liabil" in lower:
                    our_label.append("Limitation of Liability")
                elif "force majeure" in lower:
                    our_label.append("Force Majeure")
                else:
                    our_label.append("Other")
            ledgar_df["our_label"] = our_label
            print("How LEDGAR rows map to our classes:")
            print(ledgar_df["our_label"].value_counts())

            if (ledgar_df["our_label"] == "Indemnification").sum() == 0:
                # safety check: without label names every row would become "Other"
                print("No Indemnification rows found (label names missing?) -> real data skipped.")
            else:
                # drop very short paragraphs (like 'Reserved.') and take a sample of every class
                ledgar_df = ledgar_df[ledgar_df["text"].str.split().str.len() >= 8]
                parts = []
                for cls in class_names:
                    subset = ledgar_df[ledgar_df["our_label"] == cls]
                    if len(subset) > 0:
                        subset = subset.sample(n=min(N_REAL_PER_CLASS, len(subset)), random_state=RANDOM_SEED)
                        parts.append(pd.DataFrame({"text": subset["text"].values, "label": cls,
                                                   "source": "real (LEDGAR)"}))
                real_df = pd.concat(parts, ignore_index=True)
                real_df.to_csv(ledgar_file, index=False)
                print("Saved the real sample to data/ledgar_sample.csv")
        except Exception as error:
            print("Something unexpected happened with LEDGAR:", str(error)[:150])
            print("-> continuing with SYNTHETIC data only.")
            real_df = pd.DataFrame(columns=["text", "label", "source"])

# %% ---------------------------------------------------------------------------------------------
# PART C: combine real + synthetic and save

dataset = pd.concat([real_df, synthetic_df], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)   # shuffle
dataset.to_csv(os.path.join(DATA_DIR, "dataset.csv"), index=False)

print()
print("Final dataset saved to data/dataset.csv")
print("Total rows:", len(dataset))
print(pd.crosstab(dataset["label"], dataset["source"]))
if len(real_df) == 0:
    print()
    print("NOTE: this dataset is 100% SYNTHETIC. Scores on it do not show real-world performance.")
