# ==========================================================
# STEP 1 : DATA PREPROCESSING
# E-Commerce Recommendation System
# ==========================================================

import os
import pandas as pd

print("=" * 60)
print("STEP 1 : DATA PREPROCESSING")
print("=" * 60)

# ----------------------------------------------------------
# Create Required Folders
# ----------------------------------------------------------

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("images", exist_ok=True)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

dataset_path = "data/ecommerce.csv"

df = pd.read_csv(dataset_path)

print("\nDataset Loaded Successfully")

# ----------------------------------------------------------
# Basic Information
# ----------------------------------------------------------

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------------------------------------
# Duplicate Records
# ----------------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate Records :", duplicates)

# ----------------------------------------------------------
# Remove Duplicates
# ----------------------------------------------------------

if duplicates > 0:

    df = df.drop_duplicates()

    print("\nDuplicates Removed Successfully")

# ----------------------------------------------------------
# Convert visit_date into datetime
# ----------------------------------------------------------

if "visit_date" in df.columns:

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        dayfirst=True,
        errors="coerce"
    )

    print("\nvisit_date Converted to Datetime")

# ----------------------------------------------------------
# Fill Missing Numeric Values
# ----------------------------------------------------------

numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

for col in numeric_columns:

    df[col] = df[col].fillna(df[col].median())

# ----------------------------------------------------------
# Fill Missing Object Values
# ----------------------------------------------------------

categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:

    df[col] = df[col].fillna(df[col].mode()[0])

# ----------------------------------------------------------
# Dataset Information
# ----------------------------------------------------------

print("\nDataset Info")

print(df.info())

print("\nFirst Five Rows")

print(df.head())

# ----------------------------------------------------------
# Save Preprocessed Dataset
# ----------------------------------------------------------

output_path = "data/preprocessed_ecommerce.csv"

df.to_csv(output_path, index=False)

print("\nPreprocessed Dataset Saved Successfully")

print("Location :", output_path)

print("\nFinal Dataset Shape")

print(df.shape)

print("\nSTEP 1 COMPLETED SUCCESSFULLY")