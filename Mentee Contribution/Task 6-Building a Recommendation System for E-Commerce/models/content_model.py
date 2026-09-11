import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/products.csv")

print("Dataset Shape:", df.shape)
print(df.head())

# -----------------------------
# Select Text Columns
# -----------------------------
possible_cols = [
    "name",
    "product_name",
    "title",
    "description",
    "brand",
    "category"
]

available_cols = [c for c in possible_cols if c in df.columns]

if len(available_cols) == 0:
    raise Exception(
        "No suitable text columns found in products.csv"
    )

print("Using columns:", available_cols)

# -----------------------------
# Handle Missing Values
# -----------------------------
for col in available_cols:
    df[col] = df[col].fillna("")

# -----------------------------
# Create Combined Feature
# -----------------------------
df["combined_features"] = ""

for col in available_cols:
    df["combined_features"] += df[col].astype(str) + " "

# -----------------------------
# TF-IDF Vectorization
# -----------------------------
tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(df["combined_features"])

print("TF-IDF Shape:", tfidf_matrix.shape)

# -----------------------------
# Cosine Similarity
# -----------------------------
similarity = cosine_similarity(tfidf_matrix)

print("Similarity Matrix Shape:", similarity.shape)

# -----------------------------
# Save Models
# -----------------------------
os.makedirs("notebook", exist_ok=True)

pickle.dump(df, open("notebook/products.pkl", "wb"))
pickle.dump(similarity, open("notebook/similarity.pkl", "wb"))
pickle.dump(tfidf, open("notebook/tfidf.pkl", "wb"))

print("\nFiles Saved Successfully!")
print("products.pkl")
print("similarity.pkl")
print("tfidf.pkl")