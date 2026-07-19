# ==========================================
# Customer Personality Analysis
# Data Preprocessing
# ==========================================

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("data/marketing_campaign.csv", sep="\t")

print("=" * 60)
print("DATA PREPROCESSING")
print("=" * 60)

# ------------------------------------------
# Dataset Information
# ------------------------------------------

print("\nDataset Shape Before Cleaning:")
print(df.shape)

# ------------------------------------------
# Missing Values
# ------------------------------------------

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

# Fill missing Income values with median

df["Income"] = df["Income"].fillna(df["Income"].median())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# ------------------------------------------
# Remove Duplicate Records
# ------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate Rows:", duplicates)

df = df.drop_duplicates()

print("\nDataset Shape After Removing Duplicates:")
print(df.shape)

# ------------------------------------------
# Remove Unnecessary Columns
# ------------------------------------------

df = df.drop(columns=["ID"])

print("\nID Column Removed")

# ------------------------------------------
# Convert Dt_Customer to Date
# ------------------------------------------

df["Dt_Customer"] = pd.to_datetime(
    df["Dt_Customer"],
    format="%d-%m-%Y"
)

print("\nDate Converted Successfully")

# ------------------------------------------
# Encode Education
# ------------------------------------------

education_encoder = LabelEncoder()

df["Education"] = education_encoder.fit_transform(df["Education"])

# ------------------------------------------
# Encode Marital Status
# ------------------------------------------

marital_encoder = LabelEncoder()

df["Marital_Status"] = marital_encoder.fit_transform(
    df["Marital_Status"]
)

print("\nCategorical Columns Encoded")

# ------------------------------------------
# Create Customer Age
# ------------------------------------------

current_year = 2026

df["Age"] = current_year - df["Year_Birth"]

# ------------------------------------------
# Create Total Children
# ------------------------------------------

df["Children"] = df["Kidhome"] + df["Teenhome"]

# ------------------------------------------
# Create Total Spending
# ------------------------------------------

df["TotalSpending"] = (
    df["MntWines"]
    + df["MntFruits"]
    + df["MntMeatProducts"]
    + df["MntFishProducts"]
    + df["MntSweetProducts"]
    + df["MntGoldProds"]
)

# ------------------------------------------
# Create Total Purchases
# ------------------------------------------

df["TotalPurchases"] = (
    df["NumWebPurchases"]
    + df["NumCatalogPurchases"]
    + df["NumStorePurchases"]
)

# ------------------------------------------
# Scale Numerical Features
# ------------------------------------------

columns_to_scale = [
    "Income",
    "Age",
    "Recency",
    "TotalSpending",
    "TotalPurchases",
    "Children"
]

scaler = StandardScaler()

df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

print("\nNumerical Features Scaled Successfully")

# ------------------------------------------
# Save Cleaned Dataset
# ------------------------------------------

df.to_csv(
    "data/preprocessed_data.csv",
    index=False
)

print("\nPreprocessed Dataset Saved Successfully!")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFirst 5 Rows")
print(df.head())