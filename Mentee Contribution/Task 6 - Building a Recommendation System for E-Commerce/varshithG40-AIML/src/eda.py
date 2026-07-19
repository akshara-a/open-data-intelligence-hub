"""
Exploratory Data Analysis Module
=================================
Generates and saves visualizations to understand patterns in the
e-commerce dataset before model building.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# Set consistent style
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")


def run_eda(df, output_dir="outputs/plots"):
    """
    Perform Exploratory Data Analysis and save visualizations.

    Parameters
    ----------
    df : pd.DataFrame
        The e-commerce dataset.
    output_dir : str
        Directory to save plot images.
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # --- 1. Dataset Overview ---
    print("\n--- Dataset Overview ---")
    print(f"Shape: {df.shape}")
    print(f"\nColumn Types:\n{df.dtypes}")
    print(f"\nBasic Statistics:\n{df.describe().round(2)}")
    print(f"\nPurchase Rate: {df['Purchase_Status'].mean():.2%}")
    print(f"Average Rating: {df['Rating'].mean():.2f}")
    print(f"Average Price: ${df['Price'].mean():.2f}")

    # --- 2. Rating Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Rating"], bins=20, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Product Ratings", fontsize=14, fontweight="bold")
    ax.axvline(df["Rating"].mean(), color="#C44E52", linestyle="--", linewidth=2,
               label=f'Mean: {df["Rating"].mean():.2f}')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "rating_distribution.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: rating_distribution.png")

    # --- 3. Price Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Price"], bins=30, color="#55A868", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Price ($)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Product Prices", fontsize=14, fontweight="bold")
    ax.axvline(df["Price"].mean(), color="#C44E52", linestyle="--", linewidth=2,
               label=f'Mean: ${df["Price"].mean():.2f}')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "price_distribution.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: price_distribution.png")

    # --- 4. Most Purchased Product Categories ---
    fig, ax = plt.subplots(figsize=(10, 6))
    purchase_by_cat = df[df["Purchase_Status"] == 1]["Category"].value_counts()
    purchase_by_cat.plot(kind="bar", ax=ax, color=sns.color_palette("husl", len(purchase_by_cat)),
                          edgecolor="white")
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Number of Purchases", fontsize=12)
    ax.set_title("Most Purchased Product Categories", fontsize=14, fontweight="bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "purchases_by_category.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: purchases_by_category.png")

    # --- 5. Average Rating by Category ---
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_rating = df.groupby("Category")["Rating"].mean().sort_values(ascending=False)
    avg_rating.plot(kind="bar", ax=ax, color=sns.color_palette("coolwarm", len(avg_rating)),
                     edgecolor="white")
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.set_title("Average Rating by Product Category", fontsize=14, fontweight="bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylim(0, 5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "avg_rating_by_category.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: avg_rating_by_category.png")

    # --- 6. Browsing Time vs Purchase Status ---
    fig, ax = plt.subplots(figsize=(10, 6))
    df_box = df.copy()
    df_box["Purchase_Status_Label"] = df_box["Purchase_Status"].map({0: "Not Purchased", 1: "Purchased"})
    sns.boxplot(x="Purchase_Status_Label", y="Browsing_Time", data=df_box, ax=ax,
                palette=["#DD8452", "#55A868"])
    ax.set_xlabel("Purchase Status", fontsize=12)
    ax.set_ylabel("Browsing Time (minutes)", fontsize=12)
    ax.set_title("Browsing Time vs Purchase Status", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "browsing_vs_purchase.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: browsing_vs_purchase.png")

    # --- 7. Customer Spending Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Total_Spending"], bins=40, color="#8172B2", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Total Spending ($)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Customer Total Spending", fontsize=14, fontweight="bold")
    ax.axvline(df["Total_Spending"].mean(), color="#C44E52", linestyle="--", linewidth=2,
               label=f'Mean: ${df["Total_Spending"].mean():.2f}')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "spending_distribution.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: spending_distribution.png")

    # --- 8. Purchase Rate by Discount Usage ---
    fig, ax = plt.subplots(figsize=(8, 6))
    discount_purchase = df.groupby("Discount_Applied")["Purchase_Status"].mean()
    bars = ax.bar(["No Discount", "Discount Applied"], discount_purchase.values,
                  color=["#DD8452", "#55A868"], edgecolor="white", width=0.5)
    for bar, val in zip(bars, discount_purchase.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.1%}", ha="center", fontsize=12, fontweight="bold")
    ax.set_ylabel("Purchase Rate", fontsize=12)
    ax.set_title("Purchase Rate by Discount Usage", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "purchase_by_discount.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: purchase_by_discount.png")

    # --- 9. Correlation Heatmap ---
    fig, ax = plt.subplots(figsize=(12, 9))
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, square=True, linewidths=0.5, ax=ax,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: correlation_heatmap.png")

    # --- 10. Age Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Age"], bins=25, color="#64B5CD", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Age", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Age Distribution of Customers", fontsize=14, fontweight="bold")
    ax.axvline(df["Age"].mean(), color="#C44E52", linestyle="--", linewidth=2,
               label=f'Mean Age: {df["Age"].mean():.1f}')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "age_distribution.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: age_distribution.png")

    # --- 11. Browsing Time Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Browsing_Time"], bins=30, color="#CCB974", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Browsing Time (minutes)", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Distribution of Browsing Time", fontsize=14, fontweight="bold")
    ax.axvline(df["Browsing_Time"].mean(), color="#C44E52", linestyle="--", linewidth=2,
               label=f'Mean: {df["Browsing_Time"].mean():.1f} min')
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "browsing_time_distribution.png"), dpi=150)
    plt.close()
    print("[EDA] Saved: browsing_time_distribution.png")

    print(f"\n[EDA] All {11} plots saved to: {output_dir}/")


if __name__ == "__main__":
    df = pd.read_csv("data/ecommerce_data.csv")
    run_eda(df)
