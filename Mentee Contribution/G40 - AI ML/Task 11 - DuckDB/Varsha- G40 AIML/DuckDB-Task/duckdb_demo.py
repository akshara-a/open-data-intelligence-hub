# ==========================================================
# Step 9 : Load Dataset
# ==========================================================

import pandas as pd

print("=" * 60)
print("STEP 9 : LOAD DATASET")
print("=" * 60)

# Load CSV file
df = pd.read_csv("data/Mall_Customers.csv")

# Display first 5 rows
print("\nFirst 5 Rows")
print("-" * 40)
print(df.head())

# Display last 5 rows
print("\nLast 5 Rows")
print("-" * 40)
print(df.tail())

# Display dataset shape
print("\nDataset Shape")
print("-" * 40)
print(df.shape)

# Display column names
print("\nColumn Names")
print("-" * 40)
print(df.columns.tolist())

# Display data types
print("\nData Types")
print("-" * 40)
print(df.dtypes)
# ==========================================================
# Step 10 : Exploratory Data Analysis (EDA)
# ==========================================================

print("\n" + "=" * 60)
print("STEP 10 : EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)

# ----------------------------------------------------------
# Dataset Information
# ----------------------------------------------------------
print("\n1. Dataset Information")
print("-" * 40)
df.info()

# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------
print("\n2. Missing Values")
print("-" * 40)
print(df.isnull().sum())

# ----------------------------------------------------------
# Duplicate Records
# ----------------------------------------------------------
print("\n3. Duplicate Records")
print("-" * 40)
print("Duplicate Rows :", df.duplicated().sum())

# ----------------------------------------------------------
# Statistical Summary
# ----------------------------------------------------------
print("\n4. Statistical Summary")
print("-" * 40)
print(df.describe())

# ----------------------------------------------------------
# Column Names
# ----------------------------------------------------------
print("\n5. Column Names")
print("-" * 40)
print(df.columns.tolist())

# ----------------------------------------------------------
# Data Types
# ----------------------------------------------------------
print("\n6. Data Types")
print("-" * 40)
print(df.dtypes)

# ----------------------------------------------------------
# Unique Values
# ----------------------------------------------------------
print("\n7. Unique Values in Each Column")
print("-" * 40)

for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")
# ==========================================================
# Step 11 : Data Cleaning
# ==========================================================

print("\n" + "=" * 60)
print("STEP 11 : DATA CLEANING")
print("=" * 60)

import os

# Create a copy of the dataset
clean_df = df.copy()

# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------
print("\n1. Missing Values Before Cleaning")
print("-" * 40)
print(clean_df.isnull().sum())

# Fill missing values only if they exist
if clean_df.isnull().sum().sum() > 0:
    clean_df = clean_df.ffill()

print("\nMissing Values After Cleaning")
print("-" * 40)
print(clean_df.isnull().sum())

# ----------------------------------------------------------
# Remove Duplicate Records
# ----------------------------------------------------------
print("\n2. Duplicate Records")
print("-" * 40)

print("Duplicate Rows Before :", clean_df.duplicated().sum())

clean_df = clean_df.drop_duplicates()

print("Duplicate Rows After :", clean_df.duplicated().sum())

# ----------------------------------------------------------
# Rename Columns
# ----------------------------------------------------------
print("\n3. Renaming Columns")
print("-" * 40)

clean_df.rename(columns={
    "Annual Income (k$)": "AnnualIncome",
    "Spending Score (1-100)": "SpendingScore"
}, inplace=True)

print(clean_df.columns.tolist())

# ----------------------------------------------------------
# Dataset Shape
# ----------------------------------------------------------
print("\n4. Dataset Shape")
print("-" * 40)
print(clean_df.shape)

# ----------------------------------------------------------
# Save Cleaned Dataset
# ----------------------------------------------------------
os.makedirs("output", exist_ok=True)

clean_df.to_csv(
    "output/Mall_Customers_Clean.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Location : output/Mall_Customers_Clean.csv")
# ==========================================================
# Step 12 : Create DuckDB Database
# ==========================================================

print("\n" + "=" * 60)
print("STEP 12 : CREATE DUCKDB DATABASE")
print("=" * 60)

import duckdb
import os

# Create output folder
os.makedirs("output", exist_ok=True)

# Database path
db_path = "output/mall_customers.duckdb"

# Connect to DuckDB
con = duckdb.connect(db_path)

print("\nDuckDB database created successfully!")
print("Database Location:", db_path)

# ----------------------------------------------------------
# Create Table from CSV
# ----------------------------------------------------------

con.execute("""
CREATE OR REPLACE TABLE customers AS
SELECT *
FROM read_csv_auto('output/Mall_Customers_Clean.csv');
""")

print("\nTable 'customers' created successfully!")

# ----------------------------------------------------------
# Verify Number of Records
# ----------------------------------------------------------

total_records = con.execute("""
SELECT COUNT(*) FROM customers;
""").fetchone()[0]

print(f"\nTotal Records Imported : {total_records}")

# ----------------------------------------------------------
# Display First Five Rows
# ----------------------------------------------------------

print("\nFirst 5 Records")
print("-" * 40)

result = con.execute("""
SELECT * FROM customers
LIMIT 5;
""").fetchdf()

print(result)
# ==========================================================
# Step 13 : Execute SQL Queries
# ==========================================================

print("\n" + "=" * 60)
print("STEP 13 : SQL QUERIES USING DUCKDB")
print("=" * 60)

# ----------------------------------------------------------
# Query 1 : Total Customers
# ----------------------------------------------------------

print("\n1. Total Customers")
print("-" * 40)

result = con.execute("""
SELECT COUNT(*) AS Total_Customers
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 2 : Average Age
# ----------------------------------------------------------

print("\n2. Average Age")
print("-" * 40)

result = con.execute("""
SELECT ROUND(AVG(Age),2) AS Average_Age
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 3 : Average Annual Income
# ----------------------------------------------------------

print("\n3. Average Annual Income")
print("-" * 40)

result = con.execute("""
SELECT ROUND(AVG(AnnualIncome),2) AS Average_Income
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 4 : Maximum Spending Score
# ----------------------------------------------------------

print("\n4. Maximum Spending Score")
print("-" * 40)

result = con.execute("""
SELECT MAX(SpendingScore) AS Maximum_Spending
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 5 : Minimum Spending Score
# ----------------------------------------------------------

print("\n5. Minimum Spending Score")
print("-" * 40)

result = con.execute("""
SELECT MIN(SpendingScore) AS Minimum_Spending
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 6 : Customers Older Than 30
# ----------------------------------------------------------

print("\n6. Customers Older Than 30")
print("-" * 40)

result = con.execute("""
SELECT *
FROM customers
WHERE Age > 30
LIMIT 10;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 7 : Female Customers
# ----------------------------------------------------------

print("\n7. Female Customers")
print("-" * 40)

result = con.execute("""
SELECT *
FROM customers
WHERE Gender='Female'
LIMIT 10;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 8 : Top 10 Spending Scores
# ----------------------------------------------------------

print("\n8. Top 10 Spending Scores")
print("-" * 40)

result = con.execute("""
SELECT CustomerID,
       Gender,
       SpendingScore
FROM customers
ORDER BY SpendingScore DESC
LIMIT 10;
""").fetchdf()

print(result)
# ==========================================================
# Step 14 : Advanced SQL Queries
# ==========================================================

print("\n" + "=" * 60)
print("STEP 14 : ADVANCED SQL QUERIES")
print("=" * 60)

# ----------------------------------------------------------
# Query 1 : Highest Annual Income
# ----------------------------------------------------------

print("\n1. Highest Annual Income")
print("-" * 40)

result = con.execute("""
SELECT MAX(AnnualIncome) AS Highest_Income
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 2 : Lowest Annual Income
# ----------------------------------------------------------

print("\n2. Lowest Annual Income")
print("-" * 40)

result = con.execute("""
SELECT MIN(AnnualIncome) AS Lowest_Income
FROM customers;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 3 : Average Spending Score by Gender
# ----------------------------------------------------------

print("\n3. Average Spending Score by Gender")
print("-" * 40)

result = con.execute("""
SELECT Gender,
       ROUND(AVG(SpendingScore),2) AS Average_Spending
FROM customers
GROUP BY Gender;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 4 : Number of Customers by Gender
# ----------------------------------------------------------

print("\n4. Number of Customers by Gender")
print("-" * 40)

result = con.execute("""
SELECT Gender,
       COUNT(*) AS Total_Customers
FROM customers
GROUP BY Gender;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 5 : Top 10 Highest Income Customers
# ----------------------------------------------------------

print("\n5. Top 10 Highest Income Customers")
print("-" * 40)

result = con.execute("""
SELECT CustomerID,
       Gender,
       Age,
       AnnualIncome
FROM customers
ORDER BY AnnualIncome DESC
LIMIT 10;
""").fetchdf()

print(result)

# ----------------------------------------------------------
# Query 6 : Customers with Annual Income > 70
# ----------------------------------------------------------

print("\n6. Customers with Annual Income Greater Than 70")
print("-" * 40)

result = con.execute("""
SELECT *
FROM customers
WHERE AnnualIncome > 70
LIMIT 10;
""").fetchdf()

print(result)
# ==========================================================
# Step 15 : Export Query Results
# ==========================================================

print("\n" + "=" * 60)
print("STEP 15 : EXPORT QUERY RESULTS")
print("=" * 60)

import os

# Create output folder
os.makedirs("output", exist_ok=True)

# ----------------------------------------------------------
# Query Result
# ----------------------------------------------------------

query_result = con.execute("""
SELECT *
FROM customers
WHERE AnnualIncome > 70
ORDER BY AnnualIncome DESC;
""").fetchdf()

print("\nQuery Result (First 10 Rows)")
print("-" * 40)
print(query_result.head(10))

# ----------------------------------------------------------
# Export to CSV
# ----------------------------------------------------------

csv_output = "output/query_results.csv"

query_result.to_csv(csv_output, index=False)

print("\nCSV exported successfully!")
print("Location :", csv_output)

# ----------------------------------------------------------
# Export to Parquet
# ----------------------------------------------------------

parquet_output = "output/query_results.parquet"

query_result.to_parquet(parquet_output, index=False)

print("\nParquet exported successfully!")
print("Location :", parquet_output)

# ----------------------------------------------------------
# Verify Exported Files
# ----------------------------------------------------------

print("\nExport Verification")
print("-" * 40)

print("CSV Exists      :", os.path.exists(csv_output))
print("Parquet Exists  :", os.path.exists(parquet_output))

print("\nNumber of Records Exported :", len(query_result))
# ==========================================================
# Step 16 : Compare Query Performance
# ==========================================================

print("\n" + "=" * 60)
print("STEP 16 : COMPARE QUERY PERFORMANCE")
print("=" * 60)

import time

# ----------------------------------------------------------
# Pandas Query
# ----------------------------------------------------------

start_time = time.perf_counter()

pandas_result = clean_df[
    clean_df["AnnualIncome"] > 70
].sort_values(by="AnnualIncome", ascending=False)

pandas_time = time.perf_counter() - start_time

print("\nPandas Query")
print("-" * 40)
print(pandas_result.head())

# ----------------------------------------------------------
# DuckDB Query
# ----------------------------------------------------------

start_time = time.perf_counter()

duckdb_result = con.execute("""
SELECT *
FROM customers
WHERE AnnualIncome > 70
ORDER BY AnnualIncome DESC;
""").fetchdf()

duckdb_time = time.perf_counter() - start_time

print("\nDuckDB Query")
print("-" * 40)
print(duckdb_result.head())

# ----------------------------------------------------------
# Performance Results
# ----------------------------------------------------------

print("\nPerformance Comparison")
print("-" * 40)

print(f"Pandas Query Time : {pandas_time:.6f} seconds")
print(f"DuckDB Query Time : {duckdb_time:.6f} seconds")

if duckdb_time < pandas_time:
    print("\nResult : DuckDB executed the query faster.")
elif pandas_time < duckdb_time:
    print("\nResult : Pandas executed the query faster.")
else:
    print("\nResult : Both executed in nearly the same time.")
# ==========================================================
# Step 17 : Data Visualization
# ==========================================================

print("\n" + "=" * 60)
print("STEP 17 : DATA VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt
import os

# Create images folder
os.makedirs("images", exist_ok=True)

# ----------------------------------------------------------
# 1. Gender Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
clean_df["Gender"].value_counts().plot(kind="bar")
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("images/gender_distribution.png")
plt.close()

print("✓ gender_distribution.png saved")

# ----------------------------------------------------------
# 2. Age Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(clean_df["Age"], bins=10)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/age_distribution.png")
plt.close()

print("✓ age_distribution.png saved")

# ----------------------------------------------------------
# 3. Annual Income Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(clean_df["AnnualIncome"], bins=10)
plt.title("Annual Income Distribution")
plt.xlabel("Annual Income")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/income_distribution.png")
plt.close()

print("✓ income_distribution.png saved")

# ----------------------------------------------------------
# 4. Spending Score Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(clean_df["SpendingScore"], bins=10)
plt.title("Spending Score Distribution")
plt.xlabel("Spending Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/spending_distribution.png")
plt.close()

print("✓ spending_distribution.png saved")

# ----------------------------------------------------------
# 5. Average Income by Gender
# ----------------------------------------------------------

avg_income = clean_df.groupby("Gender")["AnnualIncome"].mean()

plt.figure(figsize=(6,4))
avg_income.plot(kind="bar")
plt.title("Average Annual Income by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Annual Income")
plt.tight_layout()
plt.savefig("images/average_income_by_gender.png")
plt.close()

print("✓ average_income_by_gender.png saved")

print("\nAll charts generated successfully!")
print("Location : images/")
# ==========================================================
# Step 18 : Observations and Conclusion
# ==========================================================

print("\n" + "=" * 60)
print("STEP 18 : OBSERVATIONS AND CONCLUSION")
print("=" * 60)

print("\nPROJECT OBSERVATIONS")
print("-" * 40)

print(f"1. Total Records              : {clean_df.shape[0]}")
print(f"2. Total Columns              : {clean_df.shape[1]}")
print(f"3. DuckDB Database            : output/mall_customers.duckdb")
print(f"4. Pandas Query Time          : {pandas_time:.6f} seconds")
print(f"5. DuckDB Query Time          : {duckdb_time:.6f} seconds")

print("\nDATA ANALYSIS")
print("-" * 40)

print(f"Average Age                  : {clean_df['Age'].mean():.2f}")
print(f"Average Annual Income        : {clean_df['AnnualIncome'].mean():.2f}")
print(f"Average Spending Score       : {clean_df['SpendingScore'].mean():.2f}")

print("\nDUCKDB ADVANTAGES")
print("-" * 40)

print("✔ Fast SQL query execution")
print("✔ Easy integration with Python")
print("✔ Supports CSV, Parquet and DataFrames")
print("✔ No separate database server required")
print("✔ Excellent for analytics and data science")
print("✔ Lightweight and easy to use")

print("\nFINAL CONCLUSION")
print("-" * 40)

print("DuckDB is a high-performance analytical database designed")
print("for fast processing of structured data.")
print("In this project, customer data was successfully loaded,")
print("cleaned, analyzed using SQL, exported to CSV and Parquet,")
print("and visualized using Python.")
print("The comparison between Pandas and DuckDB demonstrates")
print("that DuckDB provides efficient SQL-based analytics,")
print("especially for large datasets.")

print("\nProject completed successfully!")
# ==========================================================
# Step 19 : Close Database Connection
# ==========================================================

print("\n" + "=" * 60)
print("STEP 19 : CLOSE DATABASE CONNECTION")
print("=" * 60)

# Close DuckDB connection
con.close()

print("\nDuckDB database connection closed successfully!")

print("\nGenerated Project Files")
print("-" * 40)

print("✓ output/Mall_Customers_Clean.csv")
print("✓ output/mall_customers.duckdb")
print("✓ output/query_results.csv")
print("✓ output/query_results.parquet")
print("✓ images/gender_distribution.png")
print("✓ images/age_distribution.png")
print("✓ images/income_distribution.png")
print("✓ images/spending_distribution.png")
print("✓ images/average_income_by_gender.png")

print("\nDuckDB Project Finished Successfully!")