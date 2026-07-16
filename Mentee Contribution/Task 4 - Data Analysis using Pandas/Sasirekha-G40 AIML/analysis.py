## Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

## Create Output Folders
os.makedirs("outputs", exist_ok=True)
os.makedirs("charts", exist_ok=True)

## Load Dataset
df = pd.read_csv("customer_churn_1M.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)

# Part A – Dataset Inspection

print("\nFIRST 10 ROWS")
print(df.head(10))

print("\nLAST 10 ROWS")
print(df.tail(10))

print("\nDATA TYPES")
print(df.dtypes)

print("\nINFO")
print(df.info())

# Dataset Overview
num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nNumerical Columns")
print(list(num_cols))

print("\nCategorical Columns")
print(list(cat_cols))

# Part B – Data Quality Checks

## Missing Values
missing_values = df.isnull().sum()

print("\nMissing Values")
print(missing_values)

missing_percentage = (
    df.isnull().sum() /
    len(df)
) * 100

print("\nMissing Percentage")
print(missing_percentage)

## Duplicate Rows
duplicates = df.duplicated().sum()

print("\nDuplicate Rows:", duplicates)

## Invalid Records
print("\nNegative Age Records")
print((df["age"] < 0).sum())

print("\nNegative Income Records")
print((df["annual_income"] < 0).sum())

print("\nNegative Monthly Charges")
print((df["monthlycharges"] < 0).sum())


# Part C – Data Cleaning

## Convert Date
df["signup_date"] = pd.to_datetime(
    df["signup_date"],
    errors="coerce"
)

#Remove Duplicates
before_rows = len(df)

df = df.drop_duplicates()

after_rows = len(df)

print(
    "Duplicates Removed:",
    before_rows - after_rows
)

## Fill Numerical Missing Values

numeric_columns = df.select_dtypes(
    include=np.number
).columns

for col in numeric_columns:
    df[col] = df[col].fillna(
        df[col].median()
    )
    
## Fill Categorical Missing Values

categorical_columns = df.select_dtypes(
    include="object"
).columns

for col in categorical_columns:
    df[col] = df[col].fillna(
        "Unknown"
    )
    
 ## Standardize Text
 
for col in categorical_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
    )
    
 # Part D – Exploratory Data Analysis
   
   
   ## Summary Statistics

print(df.describe())

print(
    df.describe(
        include="object"
    )
)

## Value Counts

print(df["gender"].value_counts())

print(df["contract"].value_counts())

print(df["education"].value_counts())

print(df["marital_status"].value_counts())

print(df["churn"].value_counts())


# Filtering Examples

high_income = df[
    df["annual_income"] > 100000
]

print(
    "High Income Customers:",
    len(high_income)
)

senior = df[
    df["senior_citizen"] == 1
]

print(
    "Senior Citizens:",
    len(senior)
)

high_charges = df[
    df["monthlycharges"] > 100
]

print(
    "High Monthly Charges:",
    len(high_charges)
)

churned = df[
    df["churn"] == 1
]

print(
    "Churned Customers:",
    len(churned)
)

long_tenure = df[
    df["tenure"] > 24
]

print(
    "Long Tenure Customers:",
    len(long_tenure)
)

# Sorting

top_income = (
    df.sort_values(
        by="annual_income",
        ascending=False
    )
    .head(10)
)

print(top_income)

# Part E – GroupBy Analysis

## Contract Summary
contract_summary = (
    df.groupby("contract")
      .agg(
          customer_count=(
              "customer_id",
              "count"
          ),
          avg_income=(
              "annual_income",
              "mean"
          ),
          avg_charge=(
              "monthlycharges",
              "mean"
          )
      )
      .reset_index()
)

print(contract_summary)

## Gender + Contract Analysis

gender_contract = (
    df.groupby(
        ["gender","contract"]
    )
    .agg(
        customers=(
            "customer_id",
            "count"
        ),
        avg_income=(
            "annual_income",
            "mean"
        )
    )
    .reset_index()
)

print(gender_contract)


# Part F – Feature Engineering
## Age Group

df["age_group"] = pd.cut(
    df["age"],
    bins=[0,18,30,45,60,100],
    labels=[
        "Teen",
        "Young Adult",
        "Adult",
        "Middle Age",
        "Senior"
    ]
)

## Income Category

def income_category(x):

    if x < 50000:
        return "Low"

    elif x < 100000:
        return "Medium"

    return "High"

df["income_category"] = (
    df["annual_income"]
    .apply(income_category)
)

## Revenue Estimate
df["estimated_revenue"] = (
    df["monthlycharges"] *
    df["tenure"]
)

## Signup Year
df["signup_year"] = (
    df["signup_date"]
    .dt.year
)

# Part G – Visualizations
## Churn Distribution

plt.figure(figsize=(8,5))

df["churn"].value_counts().plot(
    kind="bar"
)

plt.title(
    "Customer Churn Distribution"
)

plt.savefig(
    "charts/churn_distribution.png"
)

plt.close()

## Contract Distribution
plt.figure(figsize=(8,5))

df["contract"].value_counts().plot(
    kind="bar"
)

plt.title(
    "Contract Type Distribution"
)

plt.savefig(
    "charts/contract_distribution.png"
)

plt.close()

## Age Histogram
plt.figure(figsize=(8,5))

plt.hist(
    df["age"],
    bins=30
)

plt.title(
    "Age Distribution"
)

plt.savefig(
    "charts/age_distribution.png"
)

plt.close()

## Income Distribution
plt.figure(figsize=(8,5))

plt.hist(
    df["annual_income"],
    bins=30
)

plt.title(
    "Income Distribution"
)

plt.savefig(
    "charts/income_distribution.png"
)

plt.close()

# Part H – Correlation Analysis
numeric_df = df.select_dtypes(
    include=np.number
)

corr_matrix = numeric_df.corr()

# Part I – Export Files
df.to_csv(
    "outputs/cleaned_dataset.csv",
    index=False
)

df.to_excel(
    "outputs/cleaned_dataset.xlsx",
    index=False
)

contract_summary.to_csv(
    "outputs/category_summary.csv",
    index=False
)

print(
    "All Files Exported Successfully"
)