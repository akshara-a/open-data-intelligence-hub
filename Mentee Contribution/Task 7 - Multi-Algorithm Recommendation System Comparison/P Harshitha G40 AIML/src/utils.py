import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set plot style for premium visuals
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'figure.figsize': (10, 6)
})

# Curated HSL-derived hex color palette for premium design
PALETTE = ["#4f46e5", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

def plot_regression_results(y_test, y_pred, save_path):
    """
    Generate actual vs. predicted plot for Ridge Regression.
    """
    directory = os.path.dirname(save_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    plt.figure(figsize=(8, 6))
    
    # Scatter plot with hexbin or alpha for density
    plt.scatter(
        y_test,
        y_pred,
        alpha=0.4,
        color=PALETTE[0],
        edgecolor="black",
        linewidth=0.5,
        s=50
    )
    # Perfect prediction line
    min_val = np.min([np.min(y_test), np.min(y_pred)])
    max_val = np.max([np.max(y_test), np.max(y_pred)])
    plt.plot([min_val, max_val], [min_val, max_val], '--', color=PALETTE[4], linewidth=2, label='Perfect Prediction')
    
    plt.title('Ridge Regression: Actual vs. Predicted Ratings')
    plt.xlabel('Actual Ratings')
    plt.ylabel('Predicted Ratings')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Regression plot saved to '{save_path}'")

def plot_classification_results(cm, save_path):
    """
    Generate Confusion Matrix Heatmap for Logistic Regression.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(7, 6))
    
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues', 
        cbar=False, 
        xticklabels=['Not Purchased', 'Purchased'], 
        yticklabels=['Not Purchased', 'Purchased'],
        annot_kws={"size": 14, "weight": "bold"}
    )
    
    plt.title('Logistic Regression: Confusion Matrix')
    plt.xlabel('Predicted Purchase Status')
    plt.ylabel('Actual Purchase Status')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Classification plot saved to '{save_path}'")

def plot_elbow_curve(k_range, inertias, save_path):
    """
    Generate K-Means Elbow Curve.
    """
    if not k_range or not inertias:
        print("No data available for elbow curve.")
        return
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(8, 5))
    
    plt.plot(k_range, inertias, 'o-', color=PALETTE[0], linewidth=2.5, markersize=8)
    
    plt.title('K-Means Clustering: Elbow Method (Inertia)')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
    plt.xticks(k_range)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Elbow curve plot saved to '{save_path}'")

def plot_silhouette_scores(k_range, scores, save_path):
    """
    Generate Silhouette Scores Curve.
    """
    if not k_range or not scores:
        print("No data available for silhouette plot.")
        return
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(8, 5))
    
    plt.plot(k_range, scores, 's-', color=PALETTE[2], linewidth=2.5, markersize=8)
    
    # Highlight highest score
    best_idx = np.argmax(scores)
    best_k = k_range[best_idx]
    best_score = scores[best_idx]
    plt.scatter(best_k, best_score, color=PALETTE[4], s=150, zorder=5, label=f'Best K={best_k} ({best_score:.4f})')
    
    plt.title('K-Means Clustering: Silhouette Scores')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.xticks(k_range)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Silhouette scores plot saved to '{save_path}'")

def plot_cluster_characteristics(profiles, save_path):
    """
    Generate bar plot comparing key metrics across clusters.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Standardize values for visual comparison on the same scale
    df_plot = profiles.copy()
    features = [
        'Number_of_Products_Viewed',
        'Number_of_Purchases',
        'Average_Rating_Given',
        'Average_Time_Spent',
        'Total_Amount_Spent',
        'Number_of_Products_Added_to_Cart'
    ]
    
    # Melt dataframe for easy seaborn plotting
    df_melted = df_plot.melt(
        id_vars=['Cluster', 'Segment_Name'], 
        value_vars=features,
        var_name='Behavior Feature', 
        value_name='Average Value'
    )
    
    # Clean up feature names for plot readability
    df_melted['Behavior Feature'] = (
        df_melted['Behavior Feature']
        .str.replace('_', ' ', regex=False)
    )
    
    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=df_melted,
        x='Behavior Feature',
        y='Average Value',
        hue='Segment_Name',
        palette=sns.color_palette(
            PALETTE,
            n_colors=len(df_melted["Segment_Name"].unique())
        )
    )
    
    plt.title('Customer Segment Profiles Comparison (Mean Behavior Metrics)')
    plt.xlabel('Customer Behavior Features')
    plt.ylabel('Average Feature Value')
    plt.xticks(rotation=15)
    plt.legend(title='Customer Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()
    print(f"Cluster profile comparison plot saved to '{save_path}'")
