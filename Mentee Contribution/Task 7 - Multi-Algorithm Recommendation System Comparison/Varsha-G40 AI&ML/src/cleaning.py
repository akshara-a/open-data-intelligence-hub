# ==========================================================
# STEP 2 : DATA CLEANING
# E-Commerce Recommendation System
# ==========================================================

import pandas as pd

print("=" * 60)
print("STEP 2 : DATA CLEANING")
print("=" * 60)

# ----------------------------------------------------------
# Load Preprocessed Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/preprocessed_ecommerce.csv")

print("\nDataset Loaded Successfully")

print("\nShape Before Cleaning")
print(df.shape)

# ==========================================================
# Remove Duplicate Rows
# ==========================================================

duplicates = df.duplicated().sum()

print("\nDuplicate Records :", duplicates)

if duplicates > 0:

    df.drop_duplicates(inplace=True)

    print("Duplicates Removed Successfully")

# ==========================================================
# Handle Missing Values
# ==========================================================

print("\nMissing Values Before Cleaning")

print(df.isnull().sum())

# Numeric Columns

numeric_columns = df.select_dtypes(include=["int64","float64"]).columns

for column in numeric_columns:

    df[column] = df[column].fillna(df[column].median())

# Object Columns

object_columns = df.select_dtypes(include=["object"]).columns

for column in object_columns:

    df[column] = df[column].fillna(df[column].mode()[0])

print("\nMissing Values After Cleaning")

print(df.isnull().sum())

# ==========================================================
# Remove Negative Values
# ==========================================================

columns = [

    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "review_helpful_votes"

]

for column in columns:

    if column in df.columns:

        df[column] = df[column].clip(lower=0)

print("\nNegative Values Removed")

# ==========================================================
# Discount Validation
# ==========================================================

if "discount_percent" in df.columns:

    df["discount_percent"] = df["discount_percent"].clip(0,100)

print("\nDiscount Percentage Corrected")

# ==========================================================
# Rating Validation
# ==========================================================

if "rating" in df.columns:

    df["rating"] = df["rating"].clip(1,5)

print("\nRating Corrected")

# ==========================================================
# Purchased Column
# ==========================================================

if "purchased" in df.columns:

    df["purchased"] = df["purchased"].astype(int)

# ==========================================================
# Added To Cart
# ==========================================================

if "added_to_cart" in df.columns:

    df["added_to_cart"] = df["added_to_cart"].astype(int)

# ==========================================================
# Cart Abandoned
# ==========================================================

if "cart_abandoned" in df.columns:

    df["cart_abandoned"] = df["cart_abandoned"].astype(int)

# ==========================================================
# Review Text
# ==========================================================

if "review_text" in df.columns:

    df["review_text"] = df["review_text"].fillna("No Review")

# ==========================================================
# Visit Date
# ==========================================================

if "visit_date" in df.columns:

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        errors="coerce"
    )

print("\nVisit Date Converted")

# ==========================================================
# Dataset Information
# ==========================================================

print("\nDataset Shape After Cleaning")

print(df.shape)

print("\nDataset Information")

print(df.info())

print("\nFirst Five Rows")

print(df.head())

# ==========================================================
# Save Dataset
# ==========================================================

df.to_csv(

    "data/cleaned_ecommerce.csv",

    index=False

)

print("\nCleaned Dataset Saved Successfully")

print("Location : data/cleaned_ecommerce.csv")

print("\nSTEP 2 COMPLETED SUCCESSFULLY")