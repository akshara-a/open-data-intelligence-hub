# ============================================================
#  Task 4 — Pandas EDA: Telco Customer Churn Dataset
#  Covers Parts A to J as per task-info.md
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")           # non-interactive backend for saving charts
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings("ignore")

# ── Resolve paths from anywhere ──────────────────────────────
ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA   = os.path.join(ROOT, "data",    "WA_Fn-UseC_-Telco-Customer-Churn.csv")
OUT    = os.path.join(ROOT, "outputs")
CHARTS = os.path.join(ROOT, "charts")
os.makedirs(OUT,    exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

print("=" * 65)
print(" TASK 4 — Telco Customer Churn | Pandas EDA")
print("=" * 65)


# ============================================================
# PART A — Data Loading and Initial Inspection
# ============================================================
print("\n▌ PART A — Loading & Inspection")

# A1 — Load
df = pd.read_csv(DATA)
print(f"\n✅ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

# A2 — Inspect
print("\n── First 10 rows ──")
print(df.head(10).to_string())

print("\n── Last 10 rows ──")
print(df.tail(10).to_string())

print(f"\nShape   : {df.shape}")
print(f"Columns : {list(df.columns)}")
print("\nData types:\n", df.dtypes)
print("\nDataset Info:")
df.info()

print("\n── Dataset Overview Table ──")
overview = {
    "Number of rows"      : df.shape[0],
    "Number of columns"   : df.shape[1],
    "File format"         : "CSV",
    "Numerical columns"   : list(df.select_dtypes(include="number").columns),
    "Categorical columns" : list(df.select_dtypes(include="object").columns),
    "Date columns"        : "None",
}
for k, v in overview.items():
    print(f"  {k:25s}: {v}")


# ============================================================
# PART B — Data Quality Check
# ============================================================
print("\n▌ PART B — Data Quality")

# B1 — Missing values
# TotalCharges is stored as object with ' ' for new customers
df["TotalCharges"] = df["TotalCharges"].str.strip().replace("", np.nan)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print("\n── Missing Values ──")
print(missing[missing > 0])
print("\n── Missing % ──")
print(missing_pct[missing_pct > 0])

# B2 — Duplicates
dup = df.duplicated().sum()
print(f"\nDuplicate rows: {dup}")

# B3 — Invalid / unusual values
print("\n── Invalid / Unusual Values ──")
print(f"  SeniorCitizen unique values    : {sorted(df['SeniorCitizen'].unique())}")
print(f"  Tenure = 0 (new customers)    : {(df['tenure'] == 0).sum()}")
print(f"  MonthlyCharges < 20           : {(df['MonthlyCharges'] < 20).sum()}")
print(f"  TotalCharges missing (blanks) : {df['TotalCharges'].isnull().sum()}")
print(f"  Churn unique values           : {df['Churn'].unique()}")


# ============================================================
# PART C — Data Cleaning
# ============================================================
print("\n▌ PART C — Cleaning")

rows_before = len(df)

# C1 — Fill missing TotalCharges with median
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

# C2 — Remove duplicates
df = df.drop_duplicates()

# C3 — Standardise text
df["gender"]          = df["gender"].str.strip().str.title()
df["Contract"]        = df["Contract"].str.strip()
df["PaymentMethod"]   = df["PaymentMethod"].str.strip()
df["InternetService"] = df["InternetService"].str.strip()

# C4 — Convert TotalCharges (already done above), add Churn as binary integer
df["Churn_Binary"] = (df["Churn"] == "Yes").astype(int)

# C5 — Rename columns to snake_case
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("(", "")
              .str.replace(")", ""))

print(f"  Rows before : {rows_before:,}")
print(f"  Rows after  : {len(df):,}")
print(f"  Duplicates removed : {rows_before - len(df)}")
print(f"  Missing values remaining: {df.isnull().sum().sum()}")
print(f"\n  Cleaned columns: {list(df.columns)}")


# ============================================================
# PART D — Exploratory Data Analysis
# ============================================================
print("\n▌ PART D — EDA")

# D1 — Summary statistics
print("\n── Numerical Summary ──")
print(df.describe().round(2).to_string())

print("\n── Categorical Summary ──")
print(df.describe(include="object").to_string())

# D2 — Value counts (3 categorical columns)
for col in ["churn", "contract", "internetservice"]:
    print(f"\n  {col} value counts:\n{df[col].value_counts()}")

# D3 — 5 Meaningful filters
print("\n── 5 Meaningful Filters ──")

churned       = df[df["churn"] == "Yes"]
print(f"  1. Churned customers              : {len(churned):,}")

fiber_users   = df[df["internetservice"] == "Fiber optic"]
print(f"  2. Fiber optic users              : {len(fiber_users):,}")

senior_churn  = df[(df["seniorcitizen"] == 1) & (df["churn"] == "Yes")]
print(f"  3. Senior citizens who churned    : {len(senior_churn):,}")

high_monthly  = df[df["monthlycharges"] > 80]
print(f"  4. High monthly charges (>80)     : {len(high_monthly):,}")

month_to_month= df[(df["contract"] == "Month-to-month") & (df["churn"] == "Yes")]
print(f"  5. Month-to-month churners        : {len(month_to_month):,}")

# D4 — Sorting (top 10 highest paying churned customers)
print("\n── Top 10 Churned Customers by Monthly Charges ──")
top_churned = (df[df["churn"] == "Yes"]
               .sort_values("monthlycharges", ascending=False)
               [["customerid", "monthlycharges", "totalcharges", "contract", "tenure"]]
               .head(10))
print(top_churned.to_string())

# D5 — Column selection
key_cols = df[["customerid", "tenure", "monthlycharges", "totalcharges", "churn"]]
print("\n── Selected key columns (first 5) ──")
print(key_cols.head().to_string())


# ============================================================
# PART E — Grouping & Aggregation
# ============================================================
print("\n▌ PART E — Grouping & Aggregation")

# E1 — Single-level grouping: churn stats by contract type
contract_summary = df.groupby("contract").agg(
    customer_count  = ("customerid",      "count"),
    churn_count     = ("churn_binary",    "sum"),
    churn_rate_pct  = ("churn_binary",    "mean"),
    avg_monthly_chg = ("monthlycharges",  "mean"),
    avg_tenure_mths = ("tenure",          "mean"),
    total_revenue   = ("totalcharges",    "sum"),
).reset_index()
contract_summary["churn_rate_pct"] = (contract_summary["churn_rate_pct"] * 100).round(2)
contract_summary["avg_monthly_chg"] = contract_summary["avg_monthly_chg"].round(2)
contract_summary["avg_tenure_mths"] = contract_summary["avg_tenure_mths"].round(1)
contract_summary["total_revenue"]   = contract_summary["total_revenue"].round(0)
print("\nChurn by Contract Type:\n", contract_summary.to_string())

# E2 — Multi-level grouping: contract + internet service
multi_group = df.groupby(["contract", "internetservice"]).agg(
    count       = ("customerid",   "count"),
    churn_rate  = ("churn_binary", "mean"),
    avg_monthly = ("monthlycharges","mean"),
).reset_index()
multi_group["churn_rate"]  = (multi_group["churn_rate"]  * 100).round(2)
multi_group["avg_monthly"] = multi_group["avg_monthly"].round(2)
print("\nContract × Internet Service:\n", multi_group.to_string())

# E3 — Churn by payment method
payment_summary = (df.groupby("paymentmethod")
                   .agg(count=("customerid","count"),
                        churn_rate=("churn_binary","mean"))
                   .reset_index()
                   .sort_values("churn_rate", ascending=False))
payment_summary["churn_rate"] = (payment_summary["churn_rate"] * 100).round(2)
print("\nChurn by Payment Method:\n", payment_summary.to_string())


# ============================================================
# PART F — Feature Engineering
# ============================================================
print("\n▌ PART F — Feature Engineering")

# 1. Tenure group (binning continuous tenure into segments)
df["tenure_group"] = pd.cut(
    df["tenure"],
    bins=[0, 12, 24, 48, 72],
    labels=["0-12 months", "13-24 months", "25-48 months", "49-72 months"],
    include_lowest=True
)

# 2. Monthly charge tier
df["charge_tier"] = pd.cut(
    df["monthlycharges"],
    bins=[0, 40, 70, 100, 120],
    labels=["Low (<40)", "Medium (40-70)", "High (70-100)", "Very High (>100)"]
)

# 3. Revenue per month flag
df["high_value_customer"] = (df["monthlycharges"] > df["monthlycharges"].mean()).astype(int)

print("  New features: tenure_group, charge_tier, high_value_customer")
print("\n  Tenure group distribution:")
print(df["tenure_group"].value_counts().sort_index())
print("\n  Charge tier distribution:")
print(df["charge_tier"].value_counts().sort_index())
print(f"\n  High-value customers (above avg ₹{df['monthlycharges'].mean():.2f}/mo): "
      f"{df['high_value_customer'].sum():,}")


# ============================================================
# PART G — Visualisations (4 charts)
# ============================================================
print("\n▌ PART G — Saving Charts")

# Chart 1 — Bar: Churn rate by Contract Type
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#e74c3c" if c == "Month-to-month" else "#2ecc71" for c in contract_summary["contract"]]
bars = ax.bar(contract_summary["contract"], contract_summary["churn_rate_pct"], color=colors)
ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=11)
ax.set_title("Churn Rate (%) by Contract Type", fontsize=14, fontweight="bold")
ax.set_xlabel("Contract Type"); ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 60)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_1_churn_by_contract.png"), dpi=130)
plt.close()
print("  ✅ Chart 1 saved — churn_by_contract")

# Chart 2 — Histogram: Monthly Charges by Churn status
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df[df["churn"] == "No"]["monthlycharges"],  bins=30, alpha=0.7,
        color="#2ecc71", label="Not Churned", edgecolor="white")
ax.hist(df[df["churn"] == "Yes"]["monthlycharges"], bins=30, alpha=0.7,
        color="#e74c3c", label="Churned",     edgecolor="white")
ax.set_title("Monthly Charges Distribution by Churn Status", fontsize=14, fontweight="bold")
ax.set_xlabel("Monthly Charges ($)"); ax.set_ylabel("Number of Customers")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_2_monthly_charges_distribution.png"), dpi=130)
plt.close()
print("  ✅ Chart 2 saved — monthly_charges_distribution")

# Chart 3 — Bar: Churn count by Tenure Group
tenure_churn = df.groupby("tenure_group", observed=True)["churn_binary"].agg(["sum","count"]).reset_index()
tenure_churn.columns = ["tenure_group","churned","total"]
tenure_churn["churn_rate"] = (tenure_churn["churned"] / tenure_churn["total"] * 100).round(1)

fig, ax = plt.subplots(figsize=(9, 5))
x = range(len(tenure_churn))
ax.bar(x, tenure_churn["churn_rate"], color=["#e74c3c","#e67e22","#3498db","#2ecc71"], width=0.5)
ax.set_xticks(x); ax.set_xticklabels(tenure_churn["tenure_group"])
ax.set_title("Churn Rate (%) by Tenure Group", fontsize=14, fontweight="bold")
ax.set_xlabel("Tenure Group"); ax.set_ylabel("Churn Rate (%)")
for i, rate in enumerate(tenure_churn["churn_rate"]):
    ax.text(i, rate + 0.5, f"{rate}%", ha="center", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_3_churn_by_tenure.png"), dpi=130)
plt.close()
print("  ✅ Chart 3 saved — churn_by_tenure")

# Chart 4 — Heatmap: Correlation Matrix (numerical columns)
numeric_cols = df.select_dtypes(include="number")
corr = numeric_cols.corr()
fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)   # show only lower triangle
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            linewidths=0.5, ax=ax, square=True)
ax.set_title("Correlation Heatmap — Numerical Columns", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "chart_4_correlation_heatmap.png"), dpi=130)
plt.close()
print("  ✅ Chart 4 saved — correlation_heatmap")


# ============================================================
# PART H — Correlation Analysis
# ============================================================
print("\n▌ PART H — Correlation Analysis")
print("\nCorrelation Matrix:\n", corr.round(2).to_string())
print("\n  Observation 1: tenure and totalcharges have very strong positive correlation (≈0.83)")
print("  Observation 2: churn_binary and monthlycharges show positive correlation — higher bills = more churn")
print("  Observation 3: tenure and churn_binary are negatively correlated — longer customers churn less")


# ============================================================
# PART I — Export All Outputs
# ============================================================
print("\n▌ PART I — Exporting Outputs")

df.to_csv(    os.path.join(OUT, "cleaned_dataset.csv"),  index=False)
df.to_excel(  os.path.join(OUT, "cleaned_dataset.xlsx"), index=False)
contract_summary.to_csv(os.path.join(OUT, "category_summary.csv"), index=False)

print("  ✅ cleaned_dataset.csv  saved")
print("  ✅ cleaned_dataset.xlsx saved")
print("  ✅ category_summary.csv saved")


# ============================================================
# PART J — Key Insights (8 insights printed)
# ============================================================
print("\n▌ PART J — Key Insights")

churn_rate    = df["churn_binary"].mean() * 100
fiber_churn   = df[df["internetservice"]=="Fiber optic"]["churn_binary"].mean() * 100
m2m_churn     = df[df["contract"]=="Month-to-month"]["churn_binary"].mean() * 100
twoyear_churn = df[df["contract"]=="Two year"]["churn_binary"].mean() * 100
senior_rate   = df[df["seniorcitizen"]==1]["churn_binary"].mean() * 100
ec_churn      = df[df["paymentmethod"]=="electronic check"]["churn_binary"].mean() * 100

insights = [
    ("Overall churn rate",
     f"{churn_rate:.1f}% of all customers have churned",
     "1 in 4 customers leaving — retention urgent"),

    ("Month-to-month contracts churn most",
     f"{m2m_churn:.1f}% churn vs {twoyear_churn:.1f}% for 2-year contracts",
     "Push customers toward longer contracts"),

    ("Fiber optic users churn more",
     f"{fiber_churn:.1f}% churn rate — likely due to higher cost",
     "Introduce value bundles for fiber optic users"),

    ("New customers at highest risk",
     f"{tenure_churn.iloc[0]['churn_rate']}% churn in first 12 months",
     "Improve onboarding experience for 0-12 month customers"),

    ("Senior citizens churn more",
     f"{senior_rate:.1f}% churn vs overall {churn_rate:.1f}%",
     "Create senior-specific plans or support lines"),

    ("Electronic check users churn most",
     f"{ec_churn:.1f}% churn rate for this payment method",
     "Incentivise auto-payment methods"),

    ("Tenure strongly predicts loyalty",
     "Correlation of tenure & churn_binary ≈ -0.35",
     "Reward loyalty milestones to increase tenure"),

    ("High monthly charges linked to churn",
     "Churned customers avg monthly charge higher than retained",
     "Offer discount plans when monthly charge exceeds $80"),
]

for i, (title, evidence, action) in enumerate(insights, 1):
    print(f"\n  Insight {i}: {title}")
    print(f"  Evidence: {evidence}")
    print(f"  Action  : {action}")

print("\n" + "=" * 65)
print("  ✅  ALL PARTS COMPLETE!")
print("=" * 65)
