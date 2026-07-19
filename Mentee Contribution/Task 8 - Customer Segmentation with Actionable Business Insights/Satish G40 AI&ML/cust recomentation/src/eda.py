"""Exploratory Data Analysis functions: basic plots and summaries."""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def basic_summary(df: pd.DataFrame, out_dir: str = "outputs/plots"):
    os.makedirs(out_dir, exist_ok=True)
    summary = df.describe(include='all')
    summary.to_csv(os.path.join(out_dir, "summary.csv"))

    plt.figure(figsize=(8, 5))
    sns.histplot(df["AnnualIncome"].dropna(), kde=True)
    plt.title("Annual Income Distribution")
    plt.savefig(os.path.join(out_dir, "annual_income_dist.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(df["TotalSpending"].dropna(), kde=True)
    plt.title("Total Spending Distribution")
    plt.savefig(os.path.join(out_dir, "total_spending_dist.png"))
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(y=df["ProductCategory"])
    plt.title("Product Category Counts")
    plt.savefig(os.path.join(out_dir, "product_category_counts.png"))
    plt.close()

    return summary
