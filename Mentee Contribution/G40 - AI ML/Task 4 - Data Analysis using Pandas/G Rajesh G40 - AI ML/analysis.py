import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folders if they don't exist
os.makedirs("outputs", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Load dataset
df = pd.read_csv("data/tips.csv")

# Basic inspection
print("First 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicates
df = df.drop_duplicates()

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Group by day
summary = df.groupby("day").agg({
    "total_bill": "mean",
    "tip": "mean"
}).reset_index()

print("\nDay-wise Summary:")
print(summary)

# Save outputs
df.to_csv("outputs/cleaned_dataset.csv", index=False)
summary.to_csv("outputs/category_summary.csv", index=False)

# Chart 1
df.groupby("day")["total_bill"].mean().plot(kind="bar")
plt.title("Average Total Bill by Day")
plt.tight_layout()
plt.savefig("charts/chart1.png")
plt.close()

# Chart 2
df["total_bill"].hist()
plt.title("Distribution of Total Bill")
plt.tight_layout()
plt.savefig("charts/chart2.png")
plt.close()

# Chart 3
df.groupby("day")["tip"].mean().plot(kind="line", marker="o")
plt.title("Average Tip by Day")
plt.tight_layout()
plt.savefig("charts/chart3.png")
plt.close()

print("\nAnalysis Completed Successfully!")