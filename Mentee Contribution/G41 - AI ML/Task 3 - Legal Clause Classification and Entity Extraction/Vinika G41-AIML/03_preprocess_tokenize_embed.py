"""
STEP 3 - Preprocessing, tokenization and embeddings

What this script does:
  1. Makes a cleaned COPY of every clause (the original text stays in the 'text' column).
  2. Shows word tokenization (NLTK) versus BERT subword tokenization.
  3. Creates pretrained BERT embeddings for every clause and saves them to outputs/embeddings.pt
     (so you do not have to run BERT again every time you retrain the classifier).

Why not clean more? Removing stop words would delete 'not' and 'no'. Removing numbers would delete
money and dates. Removing punctuation can change what a sentence applies to. In law, small words matter.

Why do we need numbers? Neural networks do arithmetic, they cannot read letters.
  - Tokenization: cut text into small pieces (tokens).
  - Subword tokenization: unknown words are split into smaller known pieces, e.g.
    'indemnification' -> 'indem', '##ni', '##fication'. So legal words and OCR typos are still understood.
  - Embedding: every token becomes a list of 768 numbers that captures its meaning in context.

Run:  python 03_preprocess_tokenize_embed.py   (after step 2; needs internet the first time for BERT)
"""
import os
import time
import numpy as np
import pandas as pd
import torch
from nltk.tokenize import TreebankWordTokenizer

from common import DATA_DIR, OUTPUT_DIR, MAX_LEN, class_to_id, clean_text
from model_tools import load_bert, get_embeddings

# %% Load the cleaned table from step 2
data_file = os.path.join(DATA_DIR, "dataset_clean.csv")
if not os.path.exists(data_file):
    print("data/dataset_clean.csv not found. Please run 02_explore_data.py first.")
    raise SystemExit
df = pd.read_csv(data_file)
print("Rows:", len(df))

# %% Preprocessing: try the cleaning function on a messy OCR-style example
messy = "The Supplier shall indemnifv the Buyer against all claims arising out of any breach of this Agree-\nment, and the total Iiability of the Supplier shall not\nexceed  $50,000."
print()
print("ORIGINAL:", repr(messy))
print("CLEANED :", clean_text(messy))

# apply the cleaning to all clauses (column 'text' stays untouched)
df["clean_text"] = [clean_text(t) for t in df["text"]]

# %% Word tokenization with NLTK (just to compare with BERT subword tokens)
# TreebankWordTokenizer is the word tokenizer used inside NLTK's word_tokenize (needs no download)
word_tokenizer = TreebankWordTokenizer()
example = "The Supplier shall indemnify the Buyer up to $50,000."
print()
print("Word tokens   :", word_tokenizer.tokenize(example))

# %% BERT subword tokenization
tokenizer, bert_model, device = load_bert()
print("Using device  :", device)
print()
for word in ["indemnification", "subrogation", "indemnifv", "force majeure"]:
    print(word, "->", tokenizer.tokenize(word))

encoded = tokenizer(example, padding="max_length", truncation=True, max_length=16)
print()
print("input_ids     :", encoded["input_ids"])
print("tokens        :", tokenizer.convert_ids_to_tokens(encoded["input_ids"]))
print("attention_mask:", encoded["attention_mask"], "(1 = real token, 0 = padding)")

# how long are our clauses in BERT tokens? (clauses longer than MAX_LEN are cut)
df["token_count"] = [len(tokenizer.tokenize(t)) for t in df["clean_text"]]
print()
print(df.groupby("source")["token_count"].describe()[["mean", "50%", "max"]])
print("Clauses longer than", MAX_LEN, "tokens (will be cut):", (df["token_count"] > MAX_LEN - 2).sum(), "of", len(df))

# %% Look at the embedding of ONE clause
one = tokenizer(df["clean_text"][0], return_tensors="pt", truncation=True, max_length=MAX_LEN)
one = {key: value.to(device) for key, value in one.items()}
with torch.no_grad():
    out = bert_model(**one)
print()
print("Embedding shape [batch, tokens, 768]:", tuple(out.last_hidden_state.shape))

# %% Create embeddings for the whole dataset (a few minutes on CPU, much faster on GPU)
print()
print("Creating BERT embeddings for", len(df), "clauses ...")
start_time = time.time()
X_all, mask_all = get_embeddings(list(df["clean_text"]), tokenizer, bert_model, device, show_progress=True)
print("Done in", round(time.time() - start_time), "seconds")

# turn the class names into numbers
y_all = np.array([class_to_id[label] for label in df["label"]])

# %% Save everything for step 4
# (embeddings are saved as float16 to halve the file size, step 4 converts them back to float32)
df.to_csv(os.path.join(DATA_DIR, "dataset_ready.csv"), index=False)
torch.save({"X": X_all.half(), "mask": mask_all, "y": torch.tensor(y_all)},
           os.path.join(OUTPUT_DIR, "embeddings.pt"))

print()
print("Embeddings:", tuple(X_all.shape), "(clauses, tokens, 768)")
print("Saved: data/dataset_ready.csv and outputs/embeddings.pt")
