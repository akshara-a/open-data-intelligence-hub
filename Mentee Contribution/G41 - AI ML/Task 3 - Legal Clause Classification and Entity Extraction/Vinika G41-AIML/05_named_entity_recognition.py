"""
STEP 5 - Named Entity Recognition (NER) with spaCy

NER finds names of real-world things in text and gives each a label.
We keep only three labels:
  ORG   - organizations
  DATE  - dates (spaCy also labels durations like "thirty (30) days" as DATE)
  MONEY - money amounts

How spaCy does it (simple version): the text is split into tokens, and a small neural network
(trained on many labelled news/web texts) predicts for every token whether it is the start of an
entity, inside an entity, or outside any entity.

Character indices: 'start' is the position of the first character of the entity and 'end' is the
position just AFTER the last character (Python slicing style). Counting starts at 0 and spaces count.
Example: text = "Pay $50,000 now"  ->  text[4:11] is "$50,000", so start = 4 and end = 11.

Validation: for every entity we check   original_text[start:end] == entity_text
If this fails, the entity is dropped. We never invent or repair entities.

Limits of pretrained NER on contracts (NER accuracy is NOT measured in this project):
  - Defined terms like "the Company" or "Supplier" are usually NOT recognised as ORG.
  - Text in ALL CAPITALS often confuses the model.
  - Wrong labels and missed entities are possible.

Run:  python 05_named_entity_recognition.py
(first time only:  python -m spacy download en_core_web_sm)
"""
import os
import re
import pandas as pd
import spacy

from common import DATA_DIR, SPACY_MODEL, wanted_labels

# %% Load the pretrained spaCy model
try:
    nlp = spacy.load(SPACY_MODEL)
except OSError:
    print("The spaCy model is not installed. Run:  python -m spacy download", SPACY_MODEL)
    raise SystemExit

# %% Run NER on one clause and show everything spaCy finds
sample_clause = "Bluewater Trading Company Limited shall pay Meridian Retail Corporation $50,000 before 15 March 2027."
doc = nlp(sample_clause)

print("All entities spaCy found:")
for ent in doc.ents:
    print("  ", ent.text, "|", ent.label_, "| start:", ent.start_char, "| end:", ent.end_char)

# %% Keep only ORG, DATE, MONEY and validate the positions
valid_entities = []
for ent in doc.ents:
    if ent.label_ in wanted_labels:
        if sample_clause[ent.start_char:ent.end_char] == ent.text:
            valid_entities.append({"text": ent.text, "label": ent.label_,
                                   "start": ent.start_char, "end": ent.end_char})
        else:
            print("Dropped (positions do not match):", ent.text)

print()
print("Valid entities (ORG, DATE, MONEY only):")
for entity in valid_entities:
    print("  ", entity)

# %% Why we run NER on the ORIGINAL text and not on the cleaned text
messy = "Bluewater   Trading Company Limited\nshall pay $50,000."
cleaned_messy = re.sub(r"\s+", " ", messy)       # extra spaces removed -> the positions shift!
doc_clean = nlp(cleaned_messy)
print()
print("Entities found in the CLEANED text, checked against the ORIGINAL text:")
for ent in doc_clean.ents:
    same = messy[ent.start_char:ent.end_char] == ent.text
    print("  ", ent.text, ent.start_char, ent.end_char, "| positions valid in the original text?", same)
print("If the answer is False, the positions point to the wrong place. That is why the pipeline")
print("runs NER on the original text, and why the validation check exists.")

# %% Try NER on a few clauses from our dataset (needs steps 1 and 2)
data_file = os.path.join(DATA_DIR, "dataset_clean.csv")
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    print()
    print("NER on 5 random clauses from the dataset:")
    for text in df.sample(5, random_state=3)["text"]:
        doc = nlp(text)
        print()
        print("Clause:", text[:150].replace("\n", " "))
        found = [(e.text, e.label_) for e in doc.ents if e.label_ in wanted_labels]
        print("  ORG/DATE/MONEY found:", found if found else "nothing")
