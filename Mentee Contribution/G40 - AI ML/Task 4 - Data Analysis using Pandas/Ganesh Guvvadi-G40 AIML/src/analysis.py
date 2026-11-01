import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/dataset.csv")

print("===== DATASET OVERVIEW =====")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

print("\nSummary Statistics:")
print(df.describe())

# Value counts
print("\nGender Count:")
print(df["sex"].value_counts())

print("\nDay Count:")
print(df["day"].value_counts())

# Grouping
summary = df.groupby("day").agg(
    total_bill=("total_bill", "sum"),
    avg_tip=("tip", "mean")
)

print("\nDay Summary:")
print(summary)

# Create chart
plt.figure(figsize=(8,5))
summary["total_bill"].plot(kind="bar")
plt.title("Total Bill by Day")
plt.tight_layout()
plt.savefig("total_bill_by_day.png")

# Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

print("\nAnalysis Completed Successfully!")