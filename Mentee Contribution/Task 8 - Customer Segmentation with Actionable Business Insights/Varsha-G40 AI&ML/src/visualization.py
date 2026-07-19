# ==========================================
# Data Visualization
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("reports/customer_segments.csv")

print("=" * 60)
print("DATA VISUALIZATION")
print("=" * 60)

# ------------------------------------------
# Create Total Spending if not present
# ------------------------------------------

if "TotalSpending" not in df.columns:
    df["TotalSpending"] = (
        df["MntWines"]
        + df["MntFruits"]
        + df["MntMeatProducts"]
        + df["MntFishProducts"]
        + df["MntSweetProducts"]
        + df["MntGoldProds"]
    )

# ------------------------------------------
# Income Distribution
# ------------------------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["Income"], bins=30, kde=True)
plt.title("Income Distribution")
plt.xlabel("Income")
plt.ylabel("Count")
plt.savefig("visualizations/income_distribution.png")
plt.show()

# ------------------------------------------
# Age Distribution
# ------------------------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["Age"], bins=20, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Customers")
plt.savefig("visualizations/age_distribution.png")
plt.show()

# ------------------------------------------
# RFM Distribution
# ------------------------------------------

plt.figure(figsize=(8,5))
sns.histplot(df["R"], bins=20)
plt.title("Recency Distribution")
plt.savefig("visualizations/recency_distribution.png")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["F"], bins=20)
plt.title("Frequency Distribution")
plt.savefig("visualizations/frequency_distribution.png")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["M"], bins=20)
plt.title("Monetary Distribution")
plt.savefig("visualizations/monetary_distribution.png")
plt.show()

# ------------------------------------------
# Correlation Heatmap
# ------------------------------------------

plt.figure(figsize=(14,10))

sns.heatmap(
    df.select_dtypes(include="number").corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig("visualizations/correlation_heatmap.png")

plt.show()

# ------------------------------------------
# Cluster Count
# ------------------------------------------

plt.figure(figsize=(8,5))

sns.countplot(x="Cluster", data=df)

plt.title("Customer Count by Cluster")

plt.savefig("visualizations/cluster_count.png")

plt.show()

# ------------------------------------------
# Cluster vs Income
# ------------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Cluster",
    y="Income",
    data=df
)

plt.title("Income by Cluster")

plt.savefig("visualizations/income_cluster.png")

plt.show()

# ------------------------------------------
# Cluster vs Monetary
# ------------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Cluster",
    y="M",
    data=df
)

plt.title("Monetary Value by Cluster")

plt.savefig("visualizations/monetary_cluster.png")

plt.show()

# ------------------------------------------
# Cluster vs Frequency
# ------------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Cluster",
    y="F",
    data=df
)

plt.title("Frequency by Cluster")

plt.savefig("visualizations/frequency_cluster.png")

plt.show()

# ------------------------------------------
# Cluster vs Recency
# ------------------------------------------

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Cluster",
    y="R",
    data=df
)

plt.title("Recency by Cluster")

plt.savefig("visualizations/recency_cluster.png")

plt.show()

# ------------------------------------------
# Scatter Plot
# ------------------------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x="Income",
    y="M",
    hue="Cluster",
    palette="Set2"
)

plt.title("Income vs Monetary")

plt.savefig("visualizations/income_vs_monetary.png")

plt.show()

print("\nVisualization Completed Successfully!")