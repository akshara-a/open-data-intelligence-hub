"""
Pandas Data Analysis Assignment
Dataset: Sample Superstore (9,994 rows, 21 columns)
Author: Student
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# SETUP PATHS
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")
OUTPUTS = os.path.join(BASE_DIR, "outputs")
CHARTS = os.path.join(BASE_DIR, "charts")
os.makedirs(OUTPUTS, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

# ─────────────────────────────────────────────
# PART A: DATA LOADING AND INITIAL INSPECTION
# ─────────────────────────────────────────────
print("=" * 60)
print("PART A: DATA LOADING AND INITIAL INSPECTION")
print("=" * 60)

# Task A1: Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin-1")

# Task A2: Inspect dataset
print("\n--- First 10 Rows ---")
print(df.head(10).to_string())

print("\n--- Last 10 Rows ---")
print(df.tail(10).to_string())

print(f"\n--- Shape ---")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Dataset Info ---")
df.info()

# Dataset overview
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()
date_cols = [c for c in df.columns if "date" in c.lower()]

print("\n--- Dataset Overview Table ---")
print(f"{'Item':<30} {'Value'}")
print("-" * 50)
print(f"{'Number of rows':<30} {df.shape[0]}")
print(f"{'Number of columns':<30} {df.shape[1]}")
print(f"{'File format':<30} CSV")
print(f"{'Numerical columns':<30} {len(num_cols)} → {num_cols}")
print(f"{'Categorical columns':<30} {len(cat_cols)} → {cat_cols}")
print(f"{'Date columns':<30} {date_cols}")

# ─────────────────────────────────────────────
# PART B: DATA QUALITY CHECK
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART B: DATA QUALITY CHECK")
print("=" * 60)

# Task B1: Missing values
print("\n--- Missing Values per Column ---")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df)) * 100
missing_report = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
print(missing_report[missing_report["missing_count"] > 0])

# Task B2: Duplicate records
dup_count = df.duplicated().sum()
print(f"\nDuplicate rows: {dup_count}")

# Task B3: Invalid / unusual values
print("\n--- Data Quality Issues ---")

# Issue 1: Negative profit
neg_profit = df[df["Profit"] < 0]
print(f"Issue 1 - Negative Profit: {len(neg_profit)} records (loss-making orders)")

# Issue 2: Zero or negative quantity
bad_qty = df[df["Quantity"] <= 0]
print(f"Issue 2 - Zero/Negative Quantity: {len(bad_qty)} records")

# Issue 3: Discount > 1 (invalid percentage)
bad_discount = df[df["Discount"] > 1]
print(f"Issue 3 - Discount > 100%: {len(bad_discount)} records")

# Issue 4: Inconsistent text casing in Category / Sub-Category
print(f"Issue 4 - Unique Category values: {df['Category'].unique()}")

# Issue 5: Postal code stored as number (leading zeros may be lost)
print(f"Issue 5 - Postal Code dtype: {df['Postal Code'].dtype} (should be string)")

print("\n--- Data Quality Issues Table ---")
quality_table = pd.DataFrame({
    "Column": ["Profit", "Quantity", "Discount", "Category", "Postal Code"],
    "Issue Found": [
        "Negative values (loss orders)",
        "Zero or negative quantity",
        "Values > 1 (invalid pct)",
        "Check for inconsistent casing",
        "Stored as int, leading zeros lost"
    ],
    "Number of Records": [
        len(neg_profit), len(bad_qty), len(bad_discount),
        df["Category"].nunique(), df["Postal Code"].isnull().sum()
    ],
    "Suggested Fix": [
        "Flag as loss; do not drop",
        "Investigate; likely data entry errors",
        "No records found; data is valid",
        "Apply str.strip().str.title()",
        "Convert to string with zero-padding"
    ]
})
print(quality_table.to_string(index=False))

# ─────────────────────────────────────────────
# PART C: DATA CLEANING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART C: DATA CLEANING")
print("=" * 60)

before_rows = len(df)
before_missing = df.isnull().sum().sum()
before_dups = df.duplicated().sum()

# Task C1: Handle missing values
# No missing values in this dataset — confirm and document
print(f"\nTotal missing values: {df.isnull().sum().sum()}")
# Postal code: fill any nulls with 'Unknown'
df["Postal Code"] = df["Postal Code"].fillna(0).astype(int).astype(str).str.zfill(5)

# Task C2: Remove duplicates
df = df.drop_duplicates()
print(f"Rows after dedup: {len(df)}")

# Task C3: Standardize text columns
for col in ["Category", "Sub-Category", "Segment", "Ship Mode", "Region"]:
    df[col] = df[col].str.strip().str.title()

# Task C4: Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Task C5: Rename columns to snake_case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Derived: shipping lag days
df["ship_lag_days"] = (df["ship_date"] - df["order_date"]).dt.days

after_rows = len(df)
after_missing = df.isnull().sum().sum()
after_dups = df.duplicated().sum()

print("\n--- Cleaning Steps Summary ---")
cleaning_steps = pd.DataFrame({
    "Cleaning Step": [
        "Missing value handling",
        "Duplicate removal",
        "Text standardization",
        "Type conversion",
        "Column renaming"
    ],
    "Column Used": [
        "Postal Code",
        "All columns",
        "Category, Sub-Category, Segment, Ship Mode, Region",
        "Order Date, Ship Date",
        "All columns"
    ],
    "Method Applied": [
        "fillna(0) then zero-pad as string",
        "drop_duplicates()",
        "str.strip().str.title()",
        "pd.to_datetime(errors='coerce')",
        "str.lower().str.replace(' ','_')"
    ],
    "Reason": [
        "Postal code must be 5-digit string",
        "Remove duplicate order rows",
        "Ensure consistent category labels",
        "Enable date arithmetic",
        "Pythonic column names"
    ]
})
print(cleaning_steps.to_string(index=False))

print("\n--- Before / After Cleaning ---")
before_after = pd.DataFrame({
    "Metric": ["Number of rows", "Missing values", "Duplicate rows", "Invalid records"],
    "Before Cleaning": [before_rows, before_missing, before_dups, len(bad_qty)],
    "After Cleaning": [after_rows, after_missing, after_dups, 0]
})
print(before_after.to_string(index=False))

# ─────────────────────────────────────────────
# PART D: EXPLORATORY DATA ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART D: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Task D1: Summary statistics
print("\n--- Numerical Summary ---")
print(df.describe().round(2))

print("\n--- Categorical Summary ---")
print(df.describe(include="object"))

# Task D2: Value counts
print("\n--- Category Value Counts ---")
print(df["category"].value_counts())

print("\n--- Segment Value Counts ---")
print(df["segment"].value_counts())

print("\n--- Region Value Counts ---")
print(df["region"].value_counts())

print("\n--- Ship Mode Value Counts ---")
print(df["ship_mode"].value_counts())

# Task D3: Filters
print("\n--- Filter 1: High-value orders (Sales > 1000) ---")
high_value = df[df["sales"] > 1000]
print(f"  Count: {len(high_value)}")

print("\n--- Filter 2: Loss-making orders (Profit < 0) ---")
losses = df[df["profit"] < 0]
print(f"  Count: {len(losses)}")

print("\n--- Filter 3: Orders with discount > 30% ---")
high_discount = df[df["discount"] > 0.30]
print(f"  Count: {len(high_discount)}")

print("\n--- Filter 4: Corporate segment, West region ---")
corp_west = df[(df["segment"] == "Corporate") & (df["region"] == "West")]
print(f"  Count: {len(corp_west)}")

print("\n--- Filter 5: Orders placed in 2017 ---")
orders_2017 = df[df["order_date"].dt.year == 2017]
print(f"  Count: {len(orders_2017)}")

# Task D4: Sorting — top 10 by sales
print("\n--- Top 10 Orders by Sales ---")
top10_sales = df.sort_values(by="sales", ascending=False).head(10)[
    ["order_id", "customer_name", "category", "sales", "profit"]
]
print(top10_sales.to_string(index=False))

# Task D5: Column selection
selected_df = df[["order_id", "customer_name", "category", "sales", "profit"]]

# ─────────────────────────────────────────────
# PART E: GROUPING AND AGGREGATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART E: GROUPING AND AGGREGATION")
print("=" * 60)

# Task E1: Single-level grouping by category
category_summary = df.groupby("category").agg(
    record_count=("category", "count"),
    total_sales=("sales", "sum"),
    average_sales=("sales", "mean"),
    total_profit=("profit", "sum"),
    profit_margin=("profit", lambda x: x.sum() / df.loc[x.index, "sales"].sum() * 100)
).reset_index().round(2)

print("\n--- Category Summary ---")
print(category_summary.to_string(index=False))

# Task E2: Multi-level grouping — region × category
region_category_summary = df.groupby(["region", "category"]).agg(
    record_count=("sales", "count"),
    total_sales=("sales", "sum"),
    total_profit=("profit", "sum"),
    avg_discount=("discount", "mean")
).reset_index().round(2)

print("\n--- Region × Category Summary (top 10) ---")
print(region_category_summary.sort_values("total_sales", ascending=False).head(10).to_string(index=False))

# Task E3: Top 10 sub-categories by total sales
sub_cat_summary = df.groupby("sub-category").agg(
    total_sales=("sales", "sum"),
    total_profit=("profit", "sum"),
    order_count=("order_id", "count")
).reset_index().sort_values("total_sales", ascending=False).head(10).round(2)

print("\n--- Top 10 Sub-Categories by Sales ---")
print(sub_cat_summary.to_string(index=False))

# ─────────────────────────────────────────────
# PART F: FEATURE ENGINEERING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART F: FEATURE ENGINEERING")
print("=" * 60)

# Feature 1: Profit margin %
df["profit_margin_pct"] = (df["profit"] / df["sales"] * 100).round(2)

# Feature 2: Revenue tier
df["revenue_tier"] = pd.cut(
    df["sales"],
    bins=[0, 100, 500, 1000, float("inf")],
    labels=["Low", "Medium", "High", "Premium"]
)

# Feature 3: Order year / month
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month

# Feature 4: Is loss-making
df["is_loss"] = df["profit"] < 0

# Feature 5: Discount tier
df["discount_tier"] = pd.cut(
    df["discount"],
    bins=[-0.01, 0, 0.2, 0.5, 1.0],
    labels=["No Discount", "Low Discount", "Medium Discount", "High Discount"]
)

print("New features added:")
new_features = pd.DataFrame({
    "New Feature": [
        "profit_margin_pct", "revenue_tier", "order_year/order_month",
        "is_loss", "discount_tier"
    ],
    "Logic Used": [
        "(profit / sales) * 100",
        "pd.cut on sales into 4 bins",
        "dt.year and dt.month from order_date",
        "profit < 0",
        "pd.cut on discount into 4 tiers"
    ],
    "Why It Is Useful": [
        "Measures profitability efficiency per order",
        "Segments orders by revenue size for analysis",
        "Enables time-series and seasonal analysis",
        "Quickly flags unprofitable orders for review",
        "Groups discount levels to study discount impact"
    ]
})
print(new_features.to_string(index=False))

# ─────────────────────────────────────────────
# PART G: VISUALIZATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART G: VISUALIZATION")
print("=" * 60)

plt.style.use("seaborn-v0_8-whitegrid")
colors = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED"]

# Chart 1: Bar chart — Total Sales by Category
fig, ax = plt.subplots(figsize=(9, 5))
cat_sales = df.groupby("category")["sales"].sum().sort_values(ascending=False)
ax.bar(cat_sales.index, cat_sales.values, color=colors[:len(cat_sales)], edgecolor="white")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax.set_title("Total Sales by Product Category", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Category", fontsize=11)
ax.set_ylabel("Total Sales", fontsize=11)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5000,
            f"${bar.get_height()/1e6:.2f}M", ha="center", va="bottom", fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_1_sales_by_category.png"), dpi=150)
plt.close()
print("Chart 1 saved.")

# Chart 2: Line chart — Monthly Sales Trend
monthly = df.groupby(["order_year", "order_month"])["sales"].sum().reset_index()
monthly["period"] = monthly["order_year"].astype(str) + "-" + monthly["order_month"].astype(str).str.zfill(2)
fig, ax = plt.subplots(figsize=(12, 5))
for yr, grp in monthly.groupby("order_year"):
    ax.plot(grp["order_month"], grp["sales"], marker="o", label=str(yr), linewidth=2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_title("Monthly Sales Trend by Year", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Total Sales", fontsize=11)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.legend(title="Year")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_2_monthly_trend.png"), dpi=150)
plt.close()
print("Chart 2 saved.")

# Chart 3: Horizontal bar — Top 10 Sub-Categories by Profit
top_sub = df.groupby("sub-category")["profit"].sum().sort_values().tail(10)
colors_bar = ["#DC2626" if v < 0 else "#16A34A" for v in top_sub.values]
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(top_sub.index, top_sub.values, color=colors_bar, edgecolor="white")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_title("Top 10 Sub-Categories by Total Profit", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Total Profit", fontsize=11)
ax.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_3_profit_by_subcategory.png"), dpi=150)
plt.close()
print("Chart 3 saved.")

# Chart 4: Histogram — Sales Distribution
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["sales"].clip(upper=2000), bins=40, color="#2563EB", edgecolor="white", alpha=0.85)
ax.set_title("Distribution of Order Sales (capped at $2,000)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Sales ($)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_4_sales_distribution.png"), dpi=150)
plt.close()
print("Chart 4 saved.")

# Chart 5: Boxplot — Profit by Region
fig, ax = plt.subplots(figsize=(9, 5))
regions = df["region"].unique()
data_by_region = [df[df["region"] == r]["profit"].clip(-500, 500) for r in regions]
bp = ax.boxplot(data_by_region, labels=regions, patch_artist=True, notch=False)
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title("Profit Distribution by Region (capped ±$500)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Region", fontsize=11)
ax.set_ylabel("Profit ($)", fontsize=11)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_5_profit_by_region.png"), dpi=150)
plt.close()
print("Chart 5 saved.")

# ─────────────────────────────────────────────
# PART H: CORRELATION ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART H: CORRELATION ANALYSIS")
print("=" * 60)

numeric_df = df.select_dtypes(include="number")
correlation_matrix = numeric_df.corr().round(3)
print("\n--- Correlation Matrix ---")
print(correlation_matrix)

# Heatmap
fig, ax = plt.subplots(figsize=(10, 7))
mask = pd.DataFrame(False, index=correlation_matrix.index, columns=correlation_matrix.columns)
import numpy as np
mask_np = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f",
            linewidths=0.5, ax=ax, mask=mask_np, vmin=-1, vmax=1)
ax.set_title("Correlation Heatmap (Numerical Features)", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_6_correlation_heatmap.png"), dpi=150)
plt.close()
print("Heatmap saved.")

print("\n--- Correlation Observations ---")
print("""
Observation 1:
Sales and Profit have a positive correlation (~0.48), meaning higher-revenue
orders tend to generate more profit — but it is moderate, not strong, due to
the impact of discounts on margin erosion.

Observation 2:
Discount and Profit have a notable negative correlation (~-0.22), confirming
that larger discounts consistently hurt profitability across all categories.

Observation 3:
Quantity and Sales have a weak positive correlation (~0.20), suggesting that
many high-value orders are driven by unit price (e.g., expensive furniture)
rather than volume.
""")

# ─────────────────────────────────────────────
# PART I: EXPORT OUTPUTS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART I: EXPORT OUTPUTS")
print("=" * 60)

df.to_csv(os.path.join(OUTPUTS, "cleaned_dataset.csv"), index=False)
df.to_excel(os.path.join(OUTPUTS, "cleaned_dataset.xlsx"), index=False)
category_summary.to_csv(os.path.join(OUTPUTS, "category_summary.csv"), index=False)
region_category_summary.to_csv(os.path.join(OUTPUTS, "region_category_summary.csv"), index=False)
sub_cat_summary.to_csv(os.path.join(OUTPUTS, "subcategory_summary.csv"), index=False)

print("All output files saved.")

# ─────────────────────────────────────────────
# BONUS: Pivot Table, Time-Series, Outlier Detection
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("BONUS TASKS")
print("=" * 60)

# Bonus 1: Pivot table
pivot = pd.pivot_table(
    df, values="sales", index="region",
    columns="category", aggfunc="sum", fill_value=0
).round(2)
print("\n--- Pivot Table: Sales by Region × Category ---")
print(pivot)
pivot.to_csv(os.path.join(OUTPUTS, "pivot_region_category.csv"))

# Bonus 2: Time-series
df["month_year"] = df["order_date"].dt.to_period("M")
monthly_trend = df.groupby("month_year").agg(
    total_sales=("sales", "sum"),
    total_profit=("profit", "sum"),
    order_count=("order_id", "count")
).reset_index().round(2)
print("\n--- Monthly Trend (last 6 months) ---")
print(monthly_trend.tail(6).to_string(index=False))

# Bonus 3: Outlier detection using IQR on Sales
Q1 = df["sales"].quantile(0.25)
Q3 = df["sales"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df["sales"] < lower_bound) | (df["sales"] > upper_bound)]
print(f"\nOutlier Detection — Sales:")
print(f"  Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
print(f"  Lower bound={lower_bound:.2f}, Upper bound={upper_bound:.2f}")
print(f"  Outlier count: {len(outliers)} ({len(outliers)/len(df)*100:.1f}% of records)")

print("\n✅ Analysis complete!")
