from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load Clean Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "clean_customers.csv"

df = pd.read_csv(DATA_PATH)

# Create output folder if it doesn't exist
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Set plot style
sns.set_style("whitegrid")

# -----------------------------
# Age Distribution
# -----------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["Age"], bins=20, kde=True)
plt.title("Age Distribution")
plt.savefig(OUTPUT_DIR / "age_distribution.png")
plt.show()

# -----------------------------
# Gender Distribution
# -----------------------------

plt.figure(figsize=(6,5))
sns.countplot(data=df, x="Gender")
plt.title("Gender Distribution")
plt.savefig(OUTPUT_DIR / "gender_distribution.png")
plt.show()

# -----------------------------
# Annual Income Distribution
# -----------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["Annual_Income"], bins=20, kde=True)
plt.title("Annual Income Distribution")
plt.savefig(OUTPUT_DIR / "income_distribution.png")
plt.show()

# -----------------------------
# Spending Score Distribution
# -----------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["Spending_Score"], bins=20, kde=True)
plt.title("Spending Score Distribution")
plt.savefig(OUTPUT_DIR / "spending_distribution.png")
plt.show()

# -----------------------------
# Correlation Heatmap
# -----------------------------

plt.figure(figsize=(8,6))

numeric_df = df.select_dtypes(include=["number"])

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.savefig(OUTPUT_DIR / "correlation_heatmap.png")
plt.show()

print("✅ All EDA charts saved successfully!")