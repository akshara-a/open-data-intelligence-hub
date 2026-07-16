# ==========================================================
# STEP 3 : EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("STEP 3 : EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# Create Images Folder
# ----------------------------------------------------------

os.makedirs("images", exist_ok=True)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/cleaned_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("Shape :", df.shape)

# ----------------------------------------------------------
# Dataset Information
# ----------------------------------------------------------

print("\nDataset Information")

print(df.info())

print("\nStatistical Summary")

print(df.describe())

# ==========================================================
# Revenue Distribution
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(df["revenue"], bins=30)

plt.title("Revenue Distribution")

plt.xlabel("Revenue")

plt.ylabel("Count")

plt.grid(True)

plt.savefig("images/revenue_distribution.png")

plt.close()

print("Revenue Distribution Saved")

# ==========================================================
# Rating Distribution
# ==========================================================

plt.figure(figsize=(7,5))

df["rating"].value_counts().sort_index().plot(kind="bar")

plt.title("Rating Distribution")

plt.xlabel("Rating")

plt.ylabel("Count")

plt.grid(True)

plt.savefig("images/rating_distribution.png")

plt.close()

print("Rating Distribution Saved")

# ==========================================================
# Product Category
# ==========================================================

plt.figure(figsize=(10,5))

df["product_category"].value_counts().head(10).plot(kind="bar")

plt.title("Top Product Categories")

plt.xlabel("Category")

plt.ylabel("Count")

plt.grid(True)

plt.savefig("images/product_category.png")

plt.close()

print("Product Category Chart Saved")

# ==========================================================
# Payment Method
# ==========================================================

plt.figure(figsize=(8,5))

df["payment_method"].value_counts().plot(kind="bar")

plt.title("Payment Method")

plt.xlabel("Payment")

plt.ylabel("Count")

plt.grid(True)

plt.savefig("images/payment_method.png")

plt.close()

print("Payment Method Chart Saved")

# ==========================================================
# Device Type
# ==========================================================

plt.figure(figsize=(8,5))

df["device_type"].value_counts().plot(kind="bar")

plt.title("Device Type")

plt.xlabel("Device")

plt.ylabel("Users")

plt.grid(True)

plt.savefig("images/device_type.png")

plt.close()

print("Device Type Chart Saved")

# ==========================================================
# Revenue vs Quantity
# ==========================================================

plt.figure(figsize=(8,6))

plt.scatter(

    df["quantity"],

    df["revenue"]

)

plt.title("Revenue vs Quantity")

plt.xlabel("Quantity")

plt.ylabel("Revenue")

plt.grid(True)

plt.savefig("images/revenue_quantity.png")

plt.close()

print("Revenue vs Quantity Saved")

# ==========================================================
# Revenue by Month
# ==========================================================

plt.figure(figsize=(10,5))

df.groupby("visit_month")["revenue"].sum().plot(kind="bar")

plt.title("Monthly Revenue")

plt.xlabel("Month")

plt.ylabel("Revenue")

plt.grid(True)

plt.savefig("images/monthly_revenue.png")

plt.close()

print("Monthly Revenue Chart Saved")

# ==========================================================
# Pages Viewed
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(df["pages_viewed"], bins=25)

plt.title("Pages Viewed")

plt.xlabel("Pages")

plt.ylabel("Customers")

plt.grid(True)

plt.savefig("images/pages_viewed.png")

plt.close()

print("Pages Viewed Chart Saved")

# ==========================================================
# Time On Site
# ==========================================================

plt.figure(figsize=(8,5))

plt.hist(df["time_on_site_sec"], bins=30)

plt.title("Time On Site")

plt.xlabel("Seconds")

plt.ylabel("Customers")

plt.grid(True)

plt.savefig("images/time_on_site.png")

plt.close()

print("Time On Site Chart Saved")

# ==========================================================
# Correlation Matrix
# ==========================================================

numeric = df.select_dtypes(include=["int64","float64"])

corr = numeric.corr()

plt.figure(figsize=(12,10))

plt.imshow(corr)

plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)

plt.yticks(range(len(corr.columns)), corr.columns)

plt.title("Correlation Matrix")

plt.savefig("images/correlation_matrix.png")

plt.close()

print("Correlation Matrix Saved")

# ==========================================================
# Purchased Customers
# ==========================================================

plt.figure(figsize=(6,5))

df["purchased"].value_counts().plot(kind="bar")

plt.title("Purchase Distribution")

plt.xlabel("Purchased")

plt.ylabel("Customers")

plt.grid(True)

plt.savefig("images/purchased.png")

plt.close()

print("Purchase Distribution Saved")

# ==========================================================
# Summary
# ==========================================================

print("\nEDA COMPLETED SUCCESSFULLY")

print("\nGenerated Images:")

print("""
1. revenue_distribution.png
2. rating_distribution.png
3. product_category.png
4. payment_method.png
5. device_type.png
6. revenue_quantity.png
7. monthly_revenue.png
8. pages_viewed.png
9. time_on_site.png
10. correlation_matrix.png
11. purchased.png
""")

print("\nSTEP 3 COMPLETED SUCCESSFULLY")