import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_plot_style():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

def generate_eda_reports(df, output_dir="../reports/figures"):
    """
    Performs comprehensive Exploratory Data Analysis (EDA) and saves visualization plots.
    """
    set_plot_style()
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Target Distribution Plot
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df['Purchase'].value_counts()
    percentages = df['Purchase'].value_counts(normalize=True) * 100
    bars = ax.bar(['No Purchase (0)', 'Purchase (1)'], counts, color=['#e74c3c', '#2ecc71'])
    for bar, pct in zip(bars, percentages):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 10, f"{yval} ({pct:.1f}%)", ha='center', va='bottom', fontweight='bold')
    ax.set_title("Target Distribution (Purchase vs. Non-Purchase)", fontsize=12, pad=15)
    ax.set_ylabel("Customer Count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "target_distribution.png"), dpi=300)
    plt.close('all')

    # 2. Conversion Rates by Categorical Variables (Device, TrafficSource, DiscountUsed)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Device Type Conversion
    device_conv = df.groupby('DeviceType')['Purchase'].mean().reset_index()
    sns.barplot(data=device_conv, x='DeviceType', y='Purchase', hue='DeviceType', ax=axes[0], palette='Blues_d', legend=False)
    axes[0].set_title("Purchase Rate by Device Type")
    axes[0].set_ylabel("Conversion Rate")
    axes[0].set_ylim(0, 1)
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():.2%}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

    # Traffic Source Conversion
    traffic_conv = df.groupby('TrafficSource')['Purchase'].mean().reset_index()
    sns.barplot(data=traffic_conv, x='TrafficSource', y='Purchase', hue='TrafficSource', ax=axes[1], palette='Purples_d', legend=False)
    axes[1].set_title("Purchase Rate by Traffic Source")
    axes[1].set_ylabel("")
    axes[1].tick_params(axis='x', rotation=30)
    axes[1].set_ylim(0, 1)
    for p in axes[1].patches:
        axes[1].annotate(f"{p.get_height():.2%}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

    # Discount Used Conversion
    discount_conv = df.groupby('DiscountUsed')['Purchase'].mean().reset_index()
    discount_conv['DiscountLabel'] = discount_conv['DiscountUsed'].map({0: 'No Discount', 1: 'Discount Used'})
    sns.barplot(data=discount_conv, x='DiscountLabel', y='Purchase', hue='DiscountLabel', ax=axes[2], palette='Greens_d', legend=False)
    axes[2].set_title("Purchase Rate by Discount Usage")
    axes[2].set_ylabel("")
    axes[2].set_ylim(0, 1)
    for p in axes[2].patches:
        axes[2].annotate(f"{p.get_height():.2%}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "categorical_conversion_rates.png"), dpi=300)
    plt.close('all')

    # 3. Numerical Features Boxplots by Target
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    sns.boxplot(data=df, x='Purchase', y='CartItems', hue='Purchase', ax=axes[0, 0], palette=['#e74c3c', '#2ecc71'], legend=False)
    axes[0, 0].set_title("Cart Items by Purchase Decision")
    
    sns.boxplot(data=df, x='Purchase', y='TimeOnSite', hue='Purchase', ax=axes[0, 1], palette=['#e74c3c', '#2ecc71'], legend=False)
    axes[0, 1].set_title("Time on Site (min) by Purchase Decision")

    sns.boxplot(data=df, x='Purchase', y='PagesViewed', hue='Purchase', ax=axes[1, 0], palette=['#e74c3c', '#2ecc71'], legend=False)
    axes[1, 0].set_title("Pages Viewed by Purchase Decision")

    sns.boxplot(data=df, x='Purchase', y='PreviousPurchases', hue='Purchase', ax=axes[1, 1], palette=['#e74c3c', '#2ecc71'], legend=False)
    axes[1, 1].set_title("Previous Purchases by Purchase Decision")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "key_behavioral_boxplots.png"), dpi=300)
    plt.close('all')

    # 4. Correlation Heatmap
    plt.figure(figsize=(12, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, square=True)
    plt.title("Correlation Heatmap of Numerical Features", fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
    plt.close('all')

    print(f"[Exploratory Analysis] Generated and saved all EDA charts to '{output_dir}'.")
