"""
STEP 2 - Data exploration

What this script does:
  - shows the structure, column names and sample records
  - checks missing values and duplicates (and removes them)
  - shows the class balance (real vs synthetic) and clause lengths
  - saves two simple plots in the outputs folder
  - saves the cleaned table as data/dataset_clean.csv

Run:  python 02_explore_data.py   (after step 1)
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # save plots as files instead of opening windows
import matplotlib.pyplot as plt
import seaborn as sns

from common import DATA_DIR, OUTPUT_DIR, class_names

# %% Load the dataset made in step 1
data_file = os.path.join(DATA_DIR, "dataset.csv")
if not os.path.exists(data_file):
    print("data/dataset.csv not found. Please run 01_prepare_data.py first.")
    raise SystemExit

df = pd.read_csv(data_file)

# %% Structure and sample records
pd.set_option("display.max_colwidth", 100)
pd.set_option("display.width", 200)
print("Shape (rows, columns):", df.shape)
print("Column names:", list(df.columns))
print()
print(df.dtypes)
print()
print("Sample records:")
sample_rows = df.sample(8, random_state=1)[["label", "source", "text"]].copy()
sample_rows["text"] = sample_rows["text"].str[:90]       # shorten long texts for printing
print(sample_rows.to_string())

# %% Missing values and duplicates
print()
print("Missing values per column:")
print(df.isnull().sum())
df["text"] = df["text"].fillna("")
print("Empty texts:", (df["text"].str.strip() == "").sum())
print("Duplicate texts:", df.duplicated(subset="text").sum())

# remove empty texts and duplicates, then renumber the rows
df = df[df["text"].str.strip() != ""]
df = df.drop_duplicates(subset="text").reset_index(drop=True)
print("Rows after cleaning:", len(df))

# %% Class balance
print()
print("Clauses per class and source:")
print(pd.crosstab(df["label"], df["source"]))

plt.figure(figsize=(8, 4))
sns.countplot(data=df, x="label", hue="source", order=class_names)
plt.title("Number of clauses per class (real vs synthetic)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "class_balance.png"))
plt.close()

# %% Clause length (number of words)
df["word_count"] = df["text"].str.split().str.len()
print()
print("Clause length in words:")
print(df.groupby("source")["word_count"].describe()[["count", "mean", "50%", "max"]])

plt.figure(figsize=(8, 4))
sns.histplot(data=df, x="word_count", hue="source", bins=40)
plt.xlim(0, 400)
plt.title("Clause length in words")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "clause_length.png"))
plt.close()

# %% Save the cleaned table for the next step
df = df.drop(columns=["word_count"])
df.to_csv(os.path.join(DATA_DIR, "dataset_clean.csv"), index=False)

print()
print("Saved: data/dataset_clean.csv, outputs/class_balance.png, outputs/clause_length.png")
print()
print("What to notice:")
print(" - Limitation of Liability and Force Majeure exist ONLY as synthetic data (unless LEDGAR had them).")
print(" - Real LEDGAR paragraphs are usually longer and messier than the short synthetic clauses.")
print(" - LEDGAR gives one label per paragraph, so some 'Other' paragraphs may still mention")
print("   words like 'liability'. This is label noise from the dataset.")
