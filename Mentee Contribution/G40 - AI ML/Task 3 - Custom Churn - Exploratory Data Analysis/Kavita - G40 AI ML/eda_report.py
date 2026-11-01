# =====================================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# =====================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================================
# STEP 2: LOAD THE DATASET
# =====================================================================
# Load the CSV file into a pandas DataFrame
df = pd.read_csv("Customer-Churn.csv")

# Display basic structural information of the dataset
print("--- DATASET SHAPE ---")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n")

print("--- DATA TYPES AND INFORMATION ---")
print(df.info())
print("\n--- MISSING VALUES PER COLUMN ---")
print(df.isnull().sum())

# =====================================================================
# STEP 3: DATA CLEANING & PREPROCESSING
# =====================================================================
# 1. Handle potential incorrect data types (e.g., TotalCharges as object)
if 'TotalCharges' in df.columns:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# 2. Handle Missing Values by filling them with the median value
if 'TotalCharges' in df.columns and df['TotalCharges'].isnull().sum() > 0:
    median_value = df['TotalCharges'].median()
    df['TotalCharges'].fillna(median_value, inplace=True)
    print("\n[INFO] Missing values in 'TotalCharges' handled successfully.")

# 3. Remove duplicate records
duplicate_count = df.duplicated().sum()
if duplicate_count > 0:
    df.drop_duplicates(inplace=True)
    print(f"[INFO] Removed {duplicate_count} duplicate rows.")
else:
    print("\n[INFO] No duplicate rows found.")

# =====================================================================
# STEP 4: EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATIONS
# =====================================================================
# Set a clean style for all plots
sns.set_theme(style="whitegrid")

# Plot 1: Overall Churn Distribution (Target Variable)
plt.figure(figsize=(6, 4))
sns.countplot(x='Churn', data=df, palette='Set2')
plt.title('Overall Customer Churn Distribution')
plt.xlabel('Churn Status')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('churn_distribution.png') 
plt.show()

# Plot 2: Churn Breakdown by Contract Type (Categorical Feature)
if 'Contract' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.countplot(x='Contract', hue='Churn', data=df, palette='viridis')
    plt.title('Customer Churn Analysis by Contract Type')
    plt.xlabel('Contract Type')
    plt.ylabel('Customer Count')
    plt.xticks(rotation=0)
    plt.legend(title='Churned?')
    plt.tight_layout()
    plt.savefig('churn_by_contract.png')
    plt.show()

# Plot 3: Relationship between Tenure and Churn (Numerical Feature)
if 'tenure' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Churn', y='tenure', data=df, palette='pastel')
    plt.title('Impact of Customer Tenure on Churn')
    plt.xlabel('Churn Status')
    plt.ylabel('Tenure (Months)')
    plt.tight_layout()
    plt.savefig('tenure_vs_churn.png')
    plt.show()