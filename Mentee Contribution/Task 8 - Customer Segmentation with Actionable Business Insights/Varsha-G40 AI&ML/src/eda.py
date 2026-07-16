# ================================
# Customer Personality Analysis
# Exploratory Data Analysis (EDA)
# ================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------
# Load Dataset
# --------------------------------

df = pd.read_csv("data/marketing_campaign.csv", sep="\t")

print("=" * 60)
print("CUSTOMER PERSONALITY ANALYSIS DATASET")
print("=" * 60)

# --------------------------------
# First & Last Rows
# --------------------------------

print("\nFirst 5 Rows")
print(df.head())

print("\nLast 5 Rows")
print(df.tail())

# --------------------------------
# Dataset Shape
# --------------------------------

print("\nDataset Shape")
print(df.shape)

# --------------------------------
# Column Names
# --------------------------------

print("\nColumn Names")
print(df.columns.tolist())

# --------------------------------
# Dataset Information
# --------------------------------

print("\nDataset Information")
print(df.info())

# --------------------------------
# Missing Values
# --------------------------------

print("\nMissing Values")
print(df.isnull().sum())

# --------------------------------
# Duplicate Records
# --------------------------------

print("\nDuplicate Rows")
print(df.duplicated().sum())

# --------------------------------
# Summary Statistics
# --------------------------------

print("\nSummary Statistics")
print(df.describe())

# --------------------------------
# Unique Values
# --------------------------------

print("\nEducation Levels")
print(df["Education"].unique())

print("\nMarital Status")
print(df["Marital_Status"].unique())

# --------------------------------
# Create Age Feature
# --------------------------------

current_year = 2026

df["Age"] = current_year - df["Year_Birth"]

# --------------------------------
# Create Total Spending
# --------------------------------

df["TotalSpending"] = (
    df["MntWines"]
    + df["MntFruits"]
    + df["MntMeatProducts"]
    + df["MntFishProducts"]
    + df["MntSweetProducts"]
    + df["MntGoldProds"]
)

# --------------------------------
# Income Distribution
# --------------------------------

plt.figure(figsize=(8,5))
plt.hist(df["Income"].dropna(), bins=30)
plt.title("Income Distribution")
plt.xlabel("Income")
plt.ylabel("Number of Customers")
plt.grid(True)
plt.show()

# --------------------------------
# Age Distribution
# --------------------------------

plt.figure(figsize=(8,5))
plt.hist(df["Age"], bins=20)
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.grid(True)
plt.show()

# --------------------------------
# Recency Distribution
# --------------------------------

plt.figure(figsize=(8,5))
plt.hist(df["Recency"], bins=20)
plt.title("Recency Distribution")
plt.xlabel("Recency")
plt.ylabel("Number of Customers")
plt.grid(True)
plt.show()

# --------------------------------
# Total Spending Distribution
# --------------------------------

plt.figure(figsize=(8,5))
plt.hist(df["TotalSpending"], bins=30)
plt.title("Total Spending Distribution")
plt.xlabel("Total Spending")
plt.ylabel("Number of Customers")
plt.grid(True)
plt.show()

# --------------------------------
# Income Boxplot
# --------------------------------

plt.figure(figsize=(6,5))
plt.boxplot(df["Income"].dropna())
plt.title("Income Boxplot")
plt.show()

# --------------------------------
# Age Boxplot
# --------------------------------

plt.figure(figsize=(6,5))
plt.boxplot(df["Age"])
plt.title("Age Boxplot")
plt.show()

# --------------------------------
# Total Spending Boxplot
# --------------------------------

plt.figure(figsize=(6,5))
plt.boxplot(df["TotalSpending"])
plt.title("Total Spending Boxplot")
plt.show()

# --------------------------------
# Gender/Marital Status Count (Example)
# --------------------------------

plt.figure(figsize=(8,5))
sns.countplot(x="Education", data=df)
plt.title("Education Level Distribution")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,5))
sns.countplot(x="Marital_Status", data=df)
plt.title("Marital Status Distribution")
plt.xticks(rotation=45)
plt.show()

# --------------------------------
# Correlation Heatmap
# --------------------------------

numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(16,12))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.show()

# --------------------------------
# Scatter Plot
# --------------------------------

plt.figure(figsize=(8,6))
plt.scatter(df["Income"], df["TotalSpending"])
plt.title("Income vs Total Spending")
plt.xlabel("Income")
plt.ylabel("Total Spending")
plt.grid(True)
plt.show()

# --------------------------------
# Purchase Type Comparison
# --------------------------------

purchase_columns = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases"
]

df[purchase_columns].sum().plot(
    kind="bar",
    figsize=(7,5)
)

plt.title("Purchase Type Comparison")
plt.ylabel("Total Purchases")
plt.xticks(rotation=0)
plt.show()

# --------------------------------
# Correlation with Total Spending
# --------------------------------

print("\nCorrelation with Total Spending")

print(
    numeric_df.corr()["TotalSpending"].sort_values(ascending=False)
)

print("\nEDA Completed Successfully!")