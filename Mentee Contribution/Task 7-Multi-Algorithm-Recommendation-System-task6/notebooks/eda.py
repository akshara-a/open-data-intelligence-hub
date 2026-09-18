from pathlib import Path
import pandas as pd

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "amazon.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("Original Dataset Shape:", df.shape)

# Select useful columns
df = df[
    [
        "asins",
        "name",
        "brand",
        "categories",
        "reviews.username",
        "reviews.rating",
        "reviews.text",
    ]
]

# Rename columns
df.columns = [
    "product_id",
    "product_name",
    "brand",
    "category",
    "user",
    "rating",
    "review",
]

# Remove missing values
df.dropna(inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

print("\nCleaned Dataset Shape:", df.shape)

print("\nFirst Five Rows")
print(df.head())

print("\nMissing Values")
print(df.isnull().sum())

print("\nRating Distribution")
print(df["rating"].value_counts().sort_index())
# Save cleaned dataset
output_path = BASE_DIR / "data" / "clean_amazon.csv"

df.to_csv(output_path, index=False)

print("\n✅ Cleaned dataset saved as clean_amazon.csv")