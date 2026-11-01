"""
Exploratory Data Analysis Module
=================================
Generates comprehensive visualizations to understand customer behaviour patterns.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os


def set_plot_style():
    """Set a consistent, professional plot style."""
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
    })


def plot_spending_distribution(df, save_path):
    """Plot the distribution of Total Spending."""
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['TotalSpending'], bins=30, kde=True, color='#2196F3', ax=ax)
    ax.set_title('Customer Total Spending Distribution', fontweight='bold')
    ax.set_xlabel('Total Spending')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {save_path}")


def plot_correlation_heatmap(df, save_path):
    """Plot a correlation heatmap of numerical features."""
    set_plot_style()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Exclude CustomerID from correlation
    numeric_cols = [c for c in numeric_cols if c != 'CustomerID']
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5, ax=ax,
                cbar_kws={'shrink': 0.8})
    ax.set_title('Feature Correlation Heatmap', fontweight='bold')
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {save_path}")


def plot_boxplot_outliers(df, save_path):
    """Plot boxplots for key numerical features to identify outliers."""
    set_plot_style()
    features = ['AnnualIncome', 'TotalSpending', 'PurchaseFrequency',
                'AverageOrderValue', 'DaysSinceLastPurchase', 'WebsiteVisits']
    features = [f for f in features if f in df.columns]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4']

    for i, col in enumerate(features):
        sns.boxplot(y=df[col], ax=axes[i], color=colors[i % len(colors)])
        axes[i].set_title(col, fontweight='bold')
        axes[i].set_ylabel('')

    # Hide extra subplots
    for j in range(len(features), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle('Outlier Detection - Boxplots of Key Features', fontweight='bold', fontsize=14)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {save_path}")


def plot_purchase_frequency(df, save_path):
    """Plot the distribution of purchase frequency."""
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['PurchaseFrequency'], bins=25, kde=True, color='#4CAF50', ax=ax)
    ax.set_title('Purchase Frequency Distribution', fontweight='bold')
    ax.set_xlabel('Purchase Frequency')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {save_path}")


def plot_average_spending_by_category(df, save_path):
    """Plot average spending by product category."""
    set_plot_style()
    if 'ProductCategory' not in df.columns:
        print("ProductCategory column not found, skipping.")
        return

    avg_spending = df.groupby('ProductCategory')['TotalSpending'].mean().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0']
    bars = ax.barh(avg_spending.index, avg_spending.values, color=colors[:len(avg_spending)])

    # Add value labels
    for bar, val in zip(bars, avg_spending.values):
        ax.text(val + 50, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontweight='bold')

    ax.set_title('Average Spending by Product Category', fontweight='bold')
    ax.set_xlabel('Average Total Spending ($)')
    ax.set_ylabel('Product Category')
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {save_path}")


def run_eda(df, images_dir):
    """Run all EDA visualizations and save to the images directory."""
    os.makedirs(images_dir, exist_ok=True)
    print("\n" + "=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # Print key statistics
    print(f"\nDataset Shape: {df.shape}")
    print(f"Total Customers: {df['CustomerID'].nunique()}")
    print(f"\nGender Distribution:\n{df['Gender'].value_counts()}")
    print(f"\nProduct Category Distribution:\n{df['ProductCategory'].value_counts()}")
    print(f"\nPurchase Likelihood Distribution:\n{df['PurchaseLikelihood'].value_counts()}")
    print(f"\nAge Statistics: Mean={df['Age'].mean():.1f}, "
          f"Min={df['Age'].min()}, Max={df['Age'].max()}")
    print(f"Annual Income: Mean=${df['AnnualIncome'].mean():,.0f}, "
          f"Median=${df['AnnualIncome'].median():,.0f}")
    print(f"Total Spending: Mean=${df['TotalSpending'].mean():,.0f}, "
          f"Median=${df['TotalSpending'].median():,.0f}")

    # Generate all plots
    plot_spending_distribution(df, os.path.join(images_dir, 'spending_distribution.png'))
    plot_correlation_heatmap(df, os.path.join(images_dir, 'correlation_heatmap.png'))
    plot_boxplot_outliers(df, os.path.join(images_dir, 'boxplot_outliers.png'))
    plot_purchase_frequency(df, os.path.join(images_dir, 'purchase_frequency.png'))
    plot_average_spending_by_category(df, os.path.join(images_dir, 'average_spending.png'))

    print("\nAll EDA visualizations generated successfully!")
    return True


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "customer_data.csv")
    images_dir = os.path.join(base_dir, "images")
    df = pd.read_csv(data_path)
    run_eda(df, images_dir)
