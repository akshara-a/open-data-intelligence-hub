import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# PATHS
# ============================================================

BASE_DIR = "Mentee Contribution/Task 4 - Data Analysis using Pandas/SNITHINKUMAR"

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "retail_sales_dataset.csv"
)

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
CHART_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# PART A: DATA LOADING AND INITIAL INSPECTION
# ============================================================

print("\n" + "=" * 60)
print("RETAIL SALES DATA ANALYSIS USING PANDAS")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print("\nFIRST 10 ROWS")
print(df.head(10))

print("\nLAST 10 ROWS")
print(df.tail(10))

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATA TYPES")
print(df.dtypes)

print("\nDATASET INFORMATION")
df.info()

overview = pd.DataFrame({
    "Metric": [
        "Number of Rows",
        "Number of Columns",
        "File Format",
        "Numerical Columns",
        "Categorical Columns"
    ],
    "Value": [
        df.shape[0],
        df.shape[1],
        "CSV",
        len(df.select_dtypes(include="number").columns),
        len(df.select_dtypes(include=["object", "string"]).columns)
    ]
})

print("\nDATASET OVERVIEW")
print(overview)


# ============================================================
# PART B: DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nMISSING VALUE PERCENTAGE")
print((df.isnull().sum() / len(df) * 100).round(2))

duplicate_count = df.duplicated().sum()

print("\nDUPLICATE ROWS:", duplicate_count)

print("\nINVALID VALUE CHECK")
print("Invalid Quantity:", (df["Quantity"] <= 0).sum())
print("Invalid Unit Price:", (df["Unit_Price"] <= 0).sum())
print("Invalid Sales:", (df["Sales"] <= 0).sum())


# ============================================================
# PART C: DATA CLEANING
# ============================================================

print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)

rows_before = len(df)
missing_before = df.isnull().sum().sum()
duplicates_before = df.duplicated().sum()

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Clean text columns
text_columns = [
    "category",
    "region",
    "customer_type",
    "payment_method"
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.title()
    )

# Fill missing categorical values
df["customer_type"] = df["customer_type"].fillna("Unknown")

# Fill missing profit values using median
df["profit"] = df["profit"].fillna(df["profit"].median())

# Convert date
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove invalid records
df = df[
    (df["quantity"] > 0)
    & (df["unit_price"] > 0)
    & (df["sales"] > 0)
]

rows_after = len(df)
missing_after = df.isnull().sum().sum()
duplicates_after = df.duplicated().sum()

print("\nCLEANING COMPLETED")
print("Rows before cleaning:", rows_before)
print("Rows after cleaning:", rows_after)
print("Missing values before:", missing_before)
print("Missing values after:", missing_after)
print("Duplicate rows before:", duplicates_before)
print("Duplicate rows after:", duplicates_after)


# ============================================================
# PART D: EXPLORATORY DATA ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nNUMERICAL SUMMARY")
print(df.describe())

print("\nCATEGORICAL SUMMARY")
print(df.describe(include=["object", "string"]))

print("\nCATEGORY VALUE COUNTS")
print(df["category"].value_counts())

print("\nREGION VALUE COUNTS")
print(df["region"].value_counts())

print("\nCUSTOMER TYPE VALUE COUNTS")
print(df["customer_type"].value_counts())


# ============================================================
# FIVE MEANINGFUL FILTERS
# ============================================================

high_value_sales = df[df["sales"] > 10000]

south_region = df[df["region"] == "South"]

premium_customers = df[
    df["customer_type"] == "Premium"
]

high_profit_orders = df[
    df["profit"] > df["profit"].median()
]

high_discount_orders = df[
    df["discount"] >= 0.20
]

print("\nFILTER RESULTS")
print("High value sales:", len(high_value_sales))
print("South region orders:", len(south_region))
print("Premium customer orders:", len(premium_customers))
print("High profit orders:", len(high_profit_orders))
print("High discount orders:", len(high_discount_orders))


# ============================================================
# SORTING
# ============================================================

top_10_sales = (
    df.sort_values(
        by="sales",
        ascending=False
    )
    .head(10)
)

print("\nTOP 10 SALES RECORDS")
print(
    top_10_sales[
        [
            "order_id",
            "category",
            "region",
            "sales",
            "profit"
        ]
    ]
)


# ============================================================
# PART E: GROUPING AND AGGREGATION
# ============================================================

print("\n" + "=" * 60)
print("GROUPING AND AGGREGATION")
print("=" * 60)

category_summary = (
    df.groupby("category")
    .agg(
        record_count=("category", "count"),
        total_sales=("sales", "sum"),
        average_sales=("sales", "mean"),
        total_profit=("profit", "sum"),
        average_profit=("profit", "mean")
    )
    .reset_index()
    .sort_values("total_sales", ascending=False)
)

print("\nCATEGORY SUMMARY")
print(category_summary)

region_category_summary = (
    df.groupby(["region", "category"])
    .agg(
        record_count=("sales", "count"),
        total_sales=("sales", "sum"),
        average_sales=("sales", "mean")
    )
    .reset_index()
)

print("\nREGION AND CATEGORY SUMMARY")
print(region_category_summary)


# ============================================================
# PART F: FEATURE ENGINEERING
# ============================================================

print("\n" + "=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

# Feature 1: Sales Category
df["sales_category"] = pd.cut(
    df["sales"],
    bins=[0, 5000, 10000, float("inf")],
    labels=["Low", "Medium", "High"]
)

# Feature 2: Year
df["year"] = df["order_date"].dt.year

# Feature 3: Month
df["month"] = df["order_date"].dt.month

# Feature 4: Profit Margin
df["profit_margin"] = (
    df["profit"] / df["sales"]
).round(4)

print("\nNEW FEATURES CREATED")
print([
    "sales_category",
    "year",
    "month",
    "profit_margin"
])


# ============================================================
# PART G: VISUALIZATION
# ============================================================

print("\nCREATING VISUALIZATIONS...")

# Chart 1: Total Sales by Category
plt.figure(figsize=(10, 6))

plt.bar(
    category_summary["category"],
    category_summary["total_sales"]
)

plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "chart_1_sales_by_category.png"
    )
)

plt.close()


# Chart 2: Sales Distribution
plt.figure(figsize=(10, 6))

plt.hist(
    df["sales"],
    bins=30
)

plt.title("Distribution of Sales")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "chart_2_sales_distribution.png"
    )
)

plt.close()


# Chart 3: Monthly Sales Trend
monthly_summary = (
    df.groupby("month")
    .agg(
        total_sales=("sales", "sum")
    )
    .reset_index()
    .sort_values("month")
)

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_summary["month"],
    monthly_summary["total_sales"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(range(1, 13))
plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "chart_3_monthly_sales_trend.png"
    )
)

plt.close()


# ============================================================
# PART H: CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CORRELATION ANALYSIS")
print("=" * 60)

numeric_df = df.select_dtypes(include="number")

correlation_matrix = numeric_df.corr()

print(correlation_matrix)

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "chart_4_correlation_heatmap.png"
    )
)

plt.close()


# ============================================================
# PART I: EXPORT OUTPUTS
# ============================================================

print("\n" + "=" * 60)
print("EXPORTING OUTPUTS")
print("=" * 60)

# Cleaned dataset CSV
df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "cleaned_dataset.csv"
    ),
    index=False
)

# Cleaned dataset Excel
df.to_excel(
    os.path.join(
        OUTPUT_DIR,
        "cleaned_dataset.xlsx"
    ),
    index=False
)

# Category summary
category_summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "category_summary.csv"
    ),
    index=False
)

# Region and category summary
region_category_summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "region_category_summary.csv"
    ),
    index=False
)

# Dataset overview
overview.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "dataset_overview.csv"
    ),
    index=False
)

print("\nFILES EXPORTED SUCCESSFULLY!")

print("\nGenerated charts:")
print("1. Sales by Category")
print("2. Sales Distribution")
print("3. Monthly Sales Trend")
print("4. Correlation Heatmap")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)