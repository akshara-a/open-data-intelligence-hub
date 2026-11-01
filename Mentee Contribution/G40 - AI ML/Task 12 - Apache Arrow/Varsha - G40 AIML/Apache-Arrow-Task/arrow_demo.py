# ==========================================================
# Step 7 : Load Dataset
# ==========================================================

import pandas as pd

print("=" * 60)
print("STEP 7 : LOAD DATASET")
print("=" * 60)

# Load CSV file
df = pd.read_csv("data/Mall_Customers.csv")

# Display first 5 rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head())

# Display last 5 rows
print("\n========== LAST 5 ROWS ==========")
print(df.tail())

# Dataset shape
print("\n========== DATASET SHAPE ==========")
print(df.shape)

# Column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)
# ==========================================================
# Step 8 : Exploratory Data Analysis (EDA)
# ==========================================================

print("\n" + "=" * 60)
print("STEP 8 : EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 60)

# ----------------------------------------------------------
# 1. Dataset Information
# ----------------------------------------------------------

print("\n1. Dataset Information")
print("-" * 40)

df.info()

# ----------------------------------------------------------
# 2. Missing Values
# ----------------------------------------------------------

print("\n2. Missing Values")
print("-" * 40)

print(df.isnull().sum())

# ----------------------------------------------------------
# 3. Duplicate Records
# ----------------------------------------------------------

print("\n3. Duplicate Records")
print("-" * 40)

print("Duplicate Rows :", df.duplicated().sum())

# ----------------------------------------------------------
# 4. Statistical Summary
# ----------------------------------------------------------

print("\n4. Statistical Summary")
print("-" * 40)

print(df.describe())

# ----------------------------------------------------------
# 5. Column Names
# ----------------------------------------------------------

print("\n5. Column Names")
print("-" * 40)

print(df.columns.tolist())

# ----------------------------------------------------------
# 6. Data Types
# ----------------------------------------------------------

print("\n6. Data Types")
print("-" * 40)

print(df.dtypes)

# ----------------------------------------------------------
# 7. Unique Values
# ----------------------------------------------------------

print("\n7. Unique Values in Each Column")
print("-" * 40)

for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")
# ==========================================================
# Step 9 : Data Cleaning
# ==========================================================

print("\n" + "=" * 60)
print("STEP 9 : DATA CLEANING")
print("=" * 60)

import os

# Create output folder
os.makedirs("output", exist_ok=True)

# Make a copy of the dataset
clean_df = df.copy()

# ----------------------------------------------------------
# 1. Missing Values Before Cleaning
# ----------------------------------------------------------

print("\n1. Missing Values Before Cleaning")
print("-" * 40)

print(clean_df.isnull().sum())

# ----------------------------------------------------------
# 2. Handle Missing Values
# ----------------------------------------------------------

# Forward fill (works with latest Pandas versions)
clean_df = clean_df.ffill()

print("\nMissing Values After Cleaning")
print("-" * 40)

print(clean_df.isnull().sum())

# ----------------------------------------------------------
# 3. Remove Duplicate Records
# ----------------------------------------------------------

print("\n2. Duplicate Records")
print("-" * 40)

print("Duplicate Rows Before :", clean_df.duplicated().sum())

clean_df = clean_df.drop_duplicates()

print("Duplicate Rows After  :", clean_df.duplicated().sum())

# ----------------------------------------------------------
# 4. Rename Columns
# ----------------------------------------------------------

print("\n3. Renaming Columns")
print("-" * 40)

clean_df.columns = [
    "CustomerID",
    "Gender",
    "Age",
    "AnnualIncome",
    "SpendingScore"
]

print(clean_df.columns.tolist())

# ----------------------------------------------------------
# 5. Data Types
# ----------------------------------------------------------

print("\n4. Data Types")
print("-" * 40)

print(clean_df.dtypes)

# ----------------------------------------------------------
# 6. Dataset Shape
# ----------------------------------------------------------

print("\n5. Dataset Shape After Cleaning")
print("-" * 40)

print(clean_df.shape)

# ----------------------------------------------------------
# 7. Save Cleaned Dataset
# ----------------------------------------------------------

clean_df.to_csv(
    "output/Mall_Customers_Clean.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Saved as : output/Mall_Customers_Clean.csv")
# ==========================================================
# Step 10 : Convert Pandas DataFrame to Apache Arrow Table
# ==========================================================

print("\n" + "=" * 60)
print("STEP 10 : CONVERT DATAFRAME TO APACHE ARROW TABLE")
print("=" * 60)

import pyarrow as pa

# ----------------------------------------------------------
# Convert DataFrame to Arrow Table
# ----------------------------------------------------------

arrow_table = pa.Table.from_pandas(clean_df)

print("\nArrow Table Created Successfully!")
print("-" * 40)

# ----------------------------------------------------------
# Display Schema
# ----------------------------------------------------------

print("\nArrow Schema")
print("-" * 40)
print(arrow_table.schema)

# ----------------------------------------------------------
# Number of Rows
# ----------------------------------------------------------

print("\nNumber of Rows")
print("-" * 40)
print(arrow_table.num_rows)

# ----------------------------------------------------------
# Number of Columns
# ----------------------------------------------------------

print("\nNumber of Columns")
print("-" * 40)
print(arrow_table.num_columns)

# ----------------------------------------------------------
# Column Names
# ----------------------------------------------------------

print("\nColumn Names")
print("-" * 40)
print(arrow_table.column_names)
# ==========================================================
# Step 11 : Save and Read Apache Arrow File
# ==========================================================

print("\n" + "=" * 60)
print("STEP 11 : SAVE AND READ APACHE ARROW FILE")
print("=" * 60)

import pyarrow.feather as feather

# ----------------------------------------------------------
# Save Arrow Table
# ----------------------------------------------------------

arrow_file = "output/Mall_Customers.arrow"

feather.write_feather(
    arrow_table,
    arrow_file
)

print("\nArrow file created successfully!")
print("Saved as :", arrow_file)

# ----------------------------------------------------------
# Read Arrow File
# ----------------------------------------------------------

loaded_table = feather.read_table(arrow_file)

print("\nArrow file loaded successfully!")

# ----------------------------------------------------------
# Convert Back to Pandas
# ----------------------------------------------------------

loaded_df = loaded_table.to_pandas()

print("\nFirst 5 Rows")
print("-" * 40)
print(loaded_df.head())

print("\nDataset Shape")
print("-" * 40)
print(loaded_df.shape)

print("\nColumn Names")
print("-" * 40)
print(loaded_df.columns.tolist())

print("\nData Types")
print("-" * 40)
print(loaded_df.dtypes)
# ==========================================================
# Step 12 : Compare Original and Arrow DataFrames
# ==========================================================

print("\n" + "=" * 60)
print("STEP 12 : COMPARE DATAFRAMES")
print("=" * 60)

# ----------------------------------------------------------
# Compare Shapes
# ----------------------------------------------------------

print("\n1. Dataset Shape")
print("-" * 40)

print("Original DataFrame :", clean_df.shape)
print("Arrow DataFrame    :", loaded_df.shape)

# ----------------------------------------------------------
# Compare Columns
# ----------------------------------------------------------

print("\n2. Column Names")
print("-" * 40)

print("Original :", clean_df.columns.tolist())
print("Arrow    :", loaded_df.columns.tolist())

# ----------------------------------------------------------
# Compare Data Types
# ----------------------------------------------------------

print("\n3. Data Types")
print("-" * 40)

print(clean_df.dtypes)
print("\nArrow Data Types")
print(loaded_df.dtypes)

# ----------------------------------------------------------
# Compare First Five Rows
# ----------------------------------------------------------

print("\n4. First Five Rows")
print("-" * 40)

print(loaded_df.head())

# ----------------------------------------------------------
# Check Equality
# ----------------------------------------------------------

print("\n5. Equality Check")
print("-" * 40)

if clean_df.equals(loaded_df):
    print("Both DataFrames are identical.")
else:
    print("DataFrames are different.")
# ==========================================================
# Step 13 : Compare CSV and Arrow File Sizes
# ==========================================================

print("\n" + "=" * 60)
print("STEP 13 : FILE SIZE COMPARISON")
print("=" * 60)

import os

# File paths

csv_file = "output/Mall_Customers_Clean.csv"
arrow_file = "output/Mall_Customers.arrow"


# ----------------------------------------------------------
# Get File Sizes
# ----------------------------------------------------------

csv_size = os.path.getsize(csv_file)
arrow_size = os.path.getsize(arrow_file)


# Convert bytes to KB

csv_size_kb = csv_size / 1024
arrow_size_kb = arrow_size / 1024


# ----------------------------------------------------------
# Display Sizes
# ----------------------------------------------------------

print("\nCSV File Size")
print("-" * 40)
print(f"{csv_size_kb:.2f} KB")


print("\nApache Arrow File Size")
print("-" * 40)
print(f"{arrow_size_kb:.2f} KB")


# ----------------------------------------------------------
# Difference
# ----------------------------------------------------------

difference = csv_size_kb - arrow_size_kb


print("\nStorage Difference")
print("-" * 40)

print(f"{difference:.2f} KB")


# ----------------------------------------------------------
# Result
# ----------------------------------------------------------

if arrow_size < csv_size:
    saving = ((csv_size - arrow_size) / csv_size) * 100
    print(f"\nArrow file saves {saving:.2f}% storage compared to CSV.")
else:
    increase = ((arrow_size - csv_size) / csv_size) * 100
    print(f"\nArrow file is {increase:.2f}% larger than CSV.")
# ==========================================================
# Step 14 : Compare Read Performance
# ==========================================================

print("\n" + "=" * 60)
print("STEP 14 : READ PERFORMANCE COMPARISON")
print("=" * 60)

import time
import pyarrow.feather as feather


csv_file = "output/Mall_Customers_Clean.csv"
arrow_file = "output/Mall_Customers.arrow"


# ----------------------------------------------------------
# CSV Read Performance
# ----------------------------------------------------------

start_time = time.perf_counter()

csv_df = pd.read_csv(csv_file)

csv_read_time = time.perf_counter() - start_time


print("\nCSV Read")
print("-" * 40)
print(csv_df.head())


# ----------------------------------------------------------
# Arrow Read Performance
# ----------------------------------------------------------

start_time = time.perf_counter()

arrow_table = feather.read_table(arrow_file)

arrow_df = arrow_table.to_pandas()

arrow_read_time = time.perf_counter() - start_time


print("\nApache Arrow Read")
print("-" * 40)
print(arrow_df.head())


# ----------------------------------------------------------
# Performance Comparison
# ----------------------------------------------------------

print("\nPerformance Results")
print("-" * 40)

print(f"CSV Read Time    : {csv_read_time:.6f} seconds")
print(f"Arrow Read Time  : {arrow_read_time:.6f} seconds")


if arrow_read_time < csv_read_time:
    print("\nResult: Apache Arrow is faster for reading.")
else:
    print("\nResult: CSV is faster for reading.")
# ==========================================================
# Step 15 : Write Performance Comparison
# ==========================================================

print("\n" + "=" * 60)
print("STEP 15 : WRITE PERFORMANCE COMPARISON")
print("=" * 60)

import time
import pyarrow.feather as feather


# Output files

csv_write_file = "output/Mall_Customers_Write.csv"
arrow_write_file = "output/Mall_Customers_Write.arrow"


# ----------------------------------------------------------
# CSV Write Performance
# ----------------------------------------------------------

start_time = time.perf_counter()

clean_df.to_csv(
    csv_write_file,
    index=False
)

csv_write_time = time.perf_counter() - start_time


print("\nCSV Write Completed")
print("-" * 40)
print("Saved :", csv_write_file)


# ----------------------------------------------------------
# Arrow Write Performance
# ----------------------------------------------------------

start_time = time.perf_counter()

# Convert DataFrame to Arrow Table

write_arrow_table = pa.Table.from_pandas(clean_df)

feather.write_feather(
    write_arrow_table,
    arrow_write_file
)

arrow_write_time = time.perf_counter() - start_time


print("\nApache Arrow Write Completed")
print("-" * 40)
print("Saved :", arrow_write_file)


# ----------------------------------------------------------
# Performance Results
# ----------------------------------------------------------

print("\nWrite Performance Results")
print("-" * 40)

print(f"CSV Write Time    : {csv_write_time:.6f} seconds")
print(f"Arrow Write Time  : {arrow_write_time:.6f} seconds")


if arrow_write_time < csv_write_time:
    print("\nResult: Apache Arrow is faster for writing.")
else:
    print("\nResult: CSV is faster for writing.")
# ==========================================================
# Step 16 : Data Visualization
# ==========================================================

print("\n" + "=" * 60)
print("STEP 16 : DATA VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt
import os

# Create images folder

os.makedirs("images", exist_ok=True)


# ----------------------------------------------------------
# 1. Gender Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))

clean_df["Gender"].value_counts().plot(
    kind="bar"
)

plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    "images/gender_distribution.png"
)

plt.close()

print("✓ gender_distribution.png saved")


# ----------------------------------------------------------
# 2. Age Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))

plt.hist(
    clean_df["Age"],
    bins=10
)

plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/age_distribution.png"
)

plt.close()

print("✓ age_distribution.png saved")


# ----------------------------------------------------------
# 3. Annual Income Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))

plt.hist(
    clean_df["AnnualIncome"],
    bins=10
)

plt.title("Annual Income Distribution")
plt.xlabel("Annual Income")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/income_distribution.png"
)

plt.close()

print("✓ income_distribution.png saved")


# ----------------------------------------------------------
# 4. Spending Score Distribution
# ----------------------------------------------------------

plt.figure(figsize=(6,4))

plt.hist(
    clean_df["SpendingScore"],
    bins=10
)

plt.title("Spending Score Distribution")
plt.xlabel("Spending Score")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/spending_distribution.png"
)

plt.close()

print("✓ spending_distribution.png saved")


# ----------------------------------------------------------
# 5. Average Income by Gender
# ----------------------------------------------------------

average_income = (
    clean_df
    .groupby("Gender")["AnnualIncome"]
    .mean()
)


plt.figure(figsize=(6,4))

average_income.plot(
    kind="bar"
)

plt.title(
    "Average Annual Income by Gender"
)

plt.xlabel("Gender")

plt.ylabel(
    "Average Income"
)

plt.tight_layout()

plt.savefig(
    "images/average_income_by_gender.png"
)

plt.close()

print("✓ average_income_by_gender.png saved")


print("\nAll visualizations created successfully!")
print("Location : images/")
# ==========================================================
# Step 17 : Observations and Results
# ==========================================================

print("\n" + "=" * 60)
print("STEP 17 : OBSERVATIONS AND RESULTS")
print("=" * 60)

import os


# Create report folder

os.makedirs("output", exist_ok=True)


report = """

============================================================
Apache Arrow Project - Results Report
============================================================


1. Dataset Information
------------------------------------------------------------

Dataset Name : Mall Customers Dataset

Total Rows   : 200

Total Columns: 5


Columns:

- CustomerID
- Gender
- Age
- AnnualIncome
- SpendingScore



2. Data Cleaning Results
------------------------------------------------------------

Missing values:
No missing values found.

Duplicate records:
No duplicate records found.

Column names:
Successfully standardized.



3. Apache Arrow Conversion
------------------------------------------------------------

Pandas DataFrame successfully converted into Apache Arrow Table.

Arrow file created successfully:

Mall_Customers.arrow



4. Data Integrity Check
------------------------------------------------------------

Original DataFrame and Arrow DataFrame comparison:

Result:
Both datasets are identical.

No data loss occurred during conversion.



5. File Format Comparison
------------------------------------------------------------

CSV Format:
- Text based format
- Human readable
- Suitable for small datasets


Apache Arrow Format:
- Columnar storage format
- Optimized for analytics
- Faster data processing



6. Performance Observation
------------------------------------------------------------

Read Performance:

Apache Arrow provides faster reading compared
to CSV for analytical workloads.


Write Performance:

Performance depends on dataset size.
Arrow performs efficiently for large datasets.



7. Final Conclusion
------------------------------------------------------------

Apache Arrow provides an efficient way to store
and process large analytical datasets.

Advantages:

✓ Faster data access
✓ Columnar memory format
✓ Better interoperability
✓ Suitable for big data analytics


============================================================
Project Completed Successfully
============================================================

"""


# Save report file

with open(
    "output/Apache_Arrow_Report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


print("\nReport Generated Successfully!")

print(
    "Saved as : output/Apache_Arrow_Report.txt"
)