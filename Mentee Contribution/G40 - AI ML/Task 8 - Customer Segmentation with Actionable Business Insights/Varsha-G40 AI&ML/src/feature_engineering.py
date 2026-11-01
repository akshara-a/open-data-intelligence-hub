# ==========================================
# Customer Personality Analysis
# Feature Engineering (RFM)
# ==========================================

import pandas as pd

# ------------------------------------------
# Load Preprocessed Dataset
# ------------------------------------------

df = pd.read_csv("data/preprocessed_data.csv")

print("=" * 60)
print("FEATURE ENGINEERING (RFM)")
print("=" * 60)

print("\nDataset Shape")
print(df.shape)

# ------------------------------------------
# Recency
# ------------------------------------------

# Already available in the dataset
df["R"] = df["Recency"]

# ------------------------------------------
# Frequency
# ------------------------------------------

df["F"] = (
    df["NumWebPurchases"]
    + df["NumCatalogPurchases"]
    + df["NumStorePurchases"]
)

# ------------------------------------------
# Monetary
# ------------------------------------------

df["M"] = (
    df["MntWines"]
    + df["MntFruits"]
    + df["MntMeatProducts"]
    + df["MntFishProducts"]
    + df["MntSweetProducts"]
    + df["MntGoldProds"]
)

# ------------------------------------------
# Customer Age
# ------------------------------------------

current_year = 2026

# If Age already exists from preprocessing, keep it.
if "Age" not in df.columns:
    df["Age"] = current_year - df["Year_Birth"]

# ------------------------------------------
# Total Children
# ------------------------------------------

if "Children" not in df.columns:
    df["Children"] = df["Kidhome"] + df["Teenhome"]

# ------------------------------------------
# Total Campaign Acceptance
# ------------------------------------------

df["CampaignsAccepted"] = (
    df["AcceptedCmp1"]
    + df["AcceptedCmp2"]
    + df["AcceptedCmp3"]
    + df["AcceptedCmp4"]
    + df["AcceptedCmp5"]
)

# ------------------------------------------
# Web Activity
# ------------------------------------------

df["WebActivity"] = (
    df["NumWebVisitsMonth"]
    + df["NumWebPurchases"]
)

# ------------------------------------------
# Family Size
# ------------------------------------------

df["FamilySize"] = (
    df["Kidhome"]
    + df["Teenhome"]
    + 2
)

# ------------------------------------------
# Display New Features
# ------------------------------------------

print("\nRFM Features")

print(df[[
    "R",
    "F",
    "M",
    "Age",
    "Children",
    "CampaignsAccepted",
    "WebActivity",
    "FamilySize"
]].head())

# ------------------------------------------
# Save Dataset
# ------------------------------------------

df.to_csv(
    "data/rfm_features.csv",
    index=False
)

print("\nRFM Feature Dataset Saved Successfully!")

print("\nFinal Dataset Shape")
print(df.shape)