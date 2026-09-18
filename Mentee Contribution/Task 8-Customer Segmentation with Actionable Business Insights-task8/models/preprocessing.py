from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clean_customers.csv"

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Encode Gender
# -----------------------------

df["Gender"] = df["Gender"].map({
    "Male": 0,
    "Female": 1
})

# -----------------------------
# Select Features
# -----------------------------

features = df[
    [
        "Gender",
        "Age",
        "Annual_Income",
        "Spending_Score"
    ]
]

# -----------------------------
# Feature Scaling
# -----------------------------

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

scaled_df = pd.DataFrame(
    scaled_features,
    columns=features.columns
)

# -----------------------------
# Save Scaled Data
# -----------------------------

OUTPUT_PATH = BASE_DIR / "data" / "scaled_customers.csv"

scaled_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("✅ Feature Scaling Completed!\n")

print(scaled_df.head())