# Step 10: Load the Dataset

import pandas as pd

# Load the CSV dataset
df = pd.read_csv("data/Mall_Customers.csv")

# Display first 5 rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head())

# Display last 5 rows
print("\n========== LAST 5 ROWS ==========")
print(df.tail())

# Display dataset shape
print("\n========== DATASET SHAPE ==========")
print(df.shape)

# Display column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# Display data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)
# ==========================================================
# Step 11: Exploratory Data Analysis (EDA)
# ==========================================================

print("\n" + "="*60)
print("STEP 11 : EXPLORATORY DATA ANALYSIS (EDA)")
print("="*60)

# Dataset Information
print("\n1. Dataset Information")
print("-"*40)
df.info()

# Missing Values
print("\n2. Missing Values")
print("-"*40)
print(df.isnull().sum())

# Duplicate Records
print("\n3. Duplicate Records")
print("-"*40)
print("Duplicate Rows :", df.duplicated().sum())

# Statistical Summary
print("\n4. Statistical Summary")
print("-"*40)
print(df.describe())

# Column Names
print("\n5. Column Names")
print("-"*40)
print(df.columns.tolist())

# Data Types
print("\n6. Data Types")
print("-"*40)
print(df.dtypes)

# Unique Values
print("\n7. Unique Values in Each Column")
print("-"*40)

for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")
# ==========================================================
# Step 12 : Data Cleaning
# ==========================================================

import os

print("\n" + "="*60)
print("STEP 12 : DATA CLEANING")
print("="*60)

# Create a copy of the dataset
clean_df = df.copy()

# ----------------------------------------------------------
# 1. Check Missing Values
# ----------------------------------------------------------
print("\n1. Missing Values Before Cleaning")
print("-"*40)
print(clean_df.isnull().sum())

# Fill missing values only if any exist
if clean_df.isnull().sum().sum() > 0:
    clean_df = clean_df.ffill()

print("\nMissing Values After Cleaning")
print("-"*40)
print(clean_df.isnull().sum())

# ----------------------------------------------------------
# 2. Remove Duplicate Records
# ----------------------------------------------------------
print("\n2. Duplicate Records")
print("-"*40)

duplicates_before = clean_df.duplicated().sum()
print("Duplicate Rows Before :", duplicates_before)

clean_df = clean_df.drop_duplicates()

duplicates_after = clean_df.duplicated().sum()
print("Duplicate Rows After :", duplicates_after)

# ----------------------------------------------------------
# 3. Data Types
# ----------------------------------------------------------
print("\n3. Data Types")
print("-"*40)
print(clean_df.dtypes)

# ----------------------------------------------------------
# 4. Rename Columns
# ----------------------------------------------------------
print("\n4. Renaming Columns")
print("-"*40)

clean_df.rename(columns={
    "Annual Income (k$)": "AnnualIncome",
    "Spending Score (1-100)": "SpendingScore"
}, inplace=True)

print(clean_df.columns.tolist())

# ----------------------------------------------------------
# 5. Dataset Shape
# ----------------------------------------------------------
print("\n5. Dataset Shape After Cleaning")
print("-"*40)
print(clean_df.shape)

# ----------------------------------------------------------
# 6. Save Cleaned Dataset
# ----------------------------------------------------------
os.makedirs("output", exist_ok=True)

clean_df.to_csv("output/Mall_Customers_Clean.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Saved as : output/Mall_Customers_Clean.csv")
# ==========================================================
# Step 13 : Convert CSV to Apache Parquet
# ==========================================================

print("\n" + "="*60)
print("STEP 13 : CONVERT CSV TO APACHE PARQUET")
print("="*60)

import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Save as Parquet
parquet_file = "output/Mall_Customers.parquet"

clean_df.to_parquet(
    parquet_file,
    engine="pyarrow",
    index=False
)

print("\nParquet file created successfully!")
print("Saved at :", parquet_file)

# Read the Parquet file
parquet_df = pd.read_parquet(
    parquet_file,
    engine="pyarrow"
)

print("\nFirst 5 Rows of Parquet File")
print("-"*40)
print(parquet_df.head())

print("\nDataset Shape")
print("-"*40)
print(parquet_df.shape)

print("\nColumn Names")
print("-"*40)
print(parquet_df.columns.tolist())

print("\nData Types")
print("-"*40)
print(parquet_df.dtypes)
# ==========================================================
# Step 14 : Compare CSV and Parquet File Sizes
# ==========================================================

print("\n" + "="*60)
print("STEP 14 : COMPARE FILE SIZES")
print("="*60)

import os

# File paths
csv_file = "data/Mall_Customers.csv"
parquet_file = "output/Mall_Customers.parquet"

# Get file sizes in bytes
csv_size = os.path.getsize(csv_file)
parquet_size = os.path.getsize(parquet_file)

# Convert bytes to KB
csv_size_kb = csv_size / 1024
parquet_size_kb = parquet_size / 1024

print(f"\nCSV File Size      : {csv_size_kb:.2f} KB")
print(f"Parquet File Size  : {parquet_size_kb:.2f} KB")

# Calculate size difference
difference = csv_size_kb - parquet_size_kb
print(f"\nStorage Saved      : {difference:.2f} KB")

# Calculate compression percentage
compression = (difference / csv_size_kb) * 100
print(f"Compression        : {compression:.2f}%")

# Determine which file is smaller
if parquet_size < csv_size:
    print("\nResult: Parquet file occupies less storage space than CSV.")
elif parquet_size > csv_size:
    print("\nResult: CSV file is smaller than the Parquet file for this dataset.")
else:
    print("\nResult: Both files have the same size.")
# ==========================================================
# Step 15 : Compare Read Performance
# ==========================================================

print("\n" + "="*60)
print("STEP 15 : COMPARE READ PERFORMANCE")
print("="*60)

import time
import pandas as pd

# File paths
csv_file = "data/Mall_Customers.csv"
parquet_file = "output/Mall_Customers.parquet"

# -----------------------------
# Measure CSV Read Time
# -----------------------------
start_time = time.perf_counter()

csv_df = pd.read_csv(csv_file)

end_time = time.perf_counter()

csv_read_time = end_time - start_time

# -----------------------------
# Measure Parquet Read Time
# -----------------------------
start_time = time.perf_counter()

parquet_df = pd.read_parquet(parquet_file, engine="pyarrow")

end_time = time.perf_counter()

parquet_read_time = end_time - start_time

# -----------------------------
# Display Results
# -----------------------------
print(f"\nCSV Read Time      : {csv_read_time:.6f} seconds")
print(f"Parquet Read Time  : {parquet_read_time:.6f} seconds")

# -----------------------------
# Compare Performance
# -----------------------------
if parquet_read_time < csv_read_time:
    print("\nResult: Parquet is faster to read than CSV.")
elif parquet_read_time > csv_read_time:
    print("\nResult: CSV is faster to read than Parquet.")
else:
    print("\nResult: Both formats have similar read performance.")
# ==========================================================
# Step 16 : Compare Write Performance
# ==========================================================

print("\n" + "="*60)
print("STEP 16 : COMPARE WRITE PERFORMANCE")
print("="*60)

import time
import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

csv_output = "output/Mall_Customers_Write.csv"
parquet_output = "output/Mall_Customers_Write.parquet"

# -----------------------------
# Measure CSV Write Time
# -----------------------------
start_time = time.perf_counter()

clean_df.to_csv(csv_output, index=False)

end_time = time.perf_counter()

csv_write_time = end_time - start_time

# -----------------------------
# Measure Parquet Write Time
# -----------------------------
start_time = time.perf_counter()

clean_df.to_parquet(
    parquet_output,
    engine="pyarrow",
    index=False
)

end_time = time.perf_counter()

parquet_write_time = end_time - start_time

# -----------------------------
# Display Results
# -----------------------------
print(f"\nCSV Write Time      : {csv_write_time:.6f} seconds")
print(f"Parquet Write Time  : {parquet_write_time:.6f} seconds")

# -----------------------------
# Compare Performance
# -----------------------------
if parquet_write_time < csv_write_time:
    print("\nResult: Parquet is faster to write than CSV.")
elif parquet_write_time > csv_write_time:
    print("\nResult: CSV is faster to write than Parquet.")
else:
    print("\nResult: Both formats have similar write performance.")
# ==========================================================
# Step 17 : Create Visualizations
# ==========================================================

print("\n" + "="*60)
print("STEP 17 : DATA VISUALIZATION")
print("="*60)

import os
import matplotlib.pyplot as plt

# Create images folder
os.makedirs("images", exist_ok=True)

# ==========================================================
# Chart 1 : File Size Comparison
# ==========================================================

plt.figure(figsize=(6,5))

plt.bar(
    ["CSV", "Parquet"],
    [csv_size_kb, parquet_size_kb]
)

plt.title("CSV vs Parquet File Size")
plt.xlabel("File Format")
plt.ylabel("Size (KB)")

plt.savefig("images/file_size_comparison.png")

plt.show()

# ==========================================================
# Chart 2 : Read Time Comparison
# ==========================================================

plt.figure(figsize=(6,5))

plt.bar(
    ["CSV", "Parquet"],
    [csv_read_time, parquet_read_time]
)

plt.title("CSV vs Parquet Read Time")
plt.xlabel("File Format")
plt.ylabel("Time (Seconds)")

plt.savefig("images/read_time_comparison.png")

plt.show()

# ==========================================================
# Chart 3 : Write Time Comparison
# ==========================================================

plt.figure(figsize=(6,5))

plt.bar(
    ["CSV", "Parquet"],
    [csv_write_time, parquet_write_time]
)

plt.title("CSV vs Parquet Write Time")
plt.xlabel("File Format")
plt.ylabel("Time (Seconds)")

plt.savefig("images/write_time_comparison.png")

plt.show()

print("\nCharts saved successfully!")
print("Location : images/")
# ==========================================================
# Step 18 : Observations and Conclusion
# ==========================================================

print("\n" + "="*60)
print("STEP 18 : OBSERVATIONS AND CONCLUSION")
print("="*60)

print("\nPROJECT OBSERVATIONS")
print("-" * 40)

print(f"1. Total Records                : {clean_df.shape[0]}")
print(f"2. Total Columns                : {clean_df.shape[1]}")
print(f"3. CSV File Size                : {csv_size_kb:.2f} KB")
print(f"4. Parquet File Size            : {parquet_size_kb:.2f} KB")
print(f"5. CSV Read Time                : {csv_read_time:.6f} seconds")
print(f"6. Parquet Read Time            : {parquet_read_time:.6f} seconds")
print(f"7. CSV Write Time               : {csv_write_time:.6f} seconds")
print(f"8. Parquet Write Time           : {parquet_write_time:.6f} seconds")

print("\nCONCLUSION")
print("-" * 40)

if parquet_size_kb < csv_size_kb:
    print("✔ Parquet file occupies less storage than CSV.")
else:
    print("✔ For this small dataset, CSV occupies less storage than Parquet.")

if parquet_read_time < csv_read_time:
    print("✔ Parquet provides faster read performance.")
else:
    print("✔ CSV provides faster read performance for this dataset.")

if parquet_write_time < csv_write_time:
    print("✔ Parquet provides faster write performance.")
else:
    print("✔ CSV provides faster write performance for this dataset.")

print("\nFINAL CONCLUSION")
print("-" * 40)
print("Apache Parquet is a columnar storage format optimized for")
print("large-scale analytics and big data processing.")
print("For very small datasets like Mall Customers (200 records),")
print("CSV may require less storage and may write faster due to")
print("lower metadata overhead.")
print("However, for large datasets containing millions of rows,")
print("Parquet generally offers:")
print("• Better compression")
print("• Faster read performance")
print("• Efficient column-based queries")
print("• Reduced storage requirements")
print("• Better compatibility with Spark, Hadoop, Hive and cloud analytics.")

print("\nProject completed successfully!")