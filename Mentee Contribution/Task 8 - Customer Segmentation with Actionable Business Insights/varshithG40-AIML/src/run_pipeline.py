from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.generate_data import generate_synthetic_data
from src.data_preprocessing import build_rfm_features, prepare_feature_frame, scale_features
from src.clustering import evaluate_kmeans, fit_kmeans, profile_clusters, assign_segment_names
from src.regression import prepare_regression_data, fit_regression_models
from src.classification import prepare_classification_data, fit_classification_model


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    customer_df, transactions_df = generate_synthetic_data(DATA_DIR)
    rfm_df = build_rfm_features(transactions_df)
    feature_frame = prepare_feature_frame(customer_df, rfm_df)

    clustering_features = feature_frame[["Recency", "Frequency", "Monetary", "AverageOrderValue", "DiscountUsage", "CustomerRating"]].copy()
    clustering_features = clustering_features.dropna()
    scaled_features, scaler = scale_features(clustering_features)

    eval_results = evaluate_kmeans(scaled_features, range(2, 8))
    best_k = 4
    model, cluster_labels = fit_kmeans(scaled_features, best_k)

    cluster_df = feature_frame.loc[clustering_features.index].copy()
    cluster_df["Cluster"] = cluster_labels.astype(int).values
    cluster_summary = profile_clusters(cluster_df, cluster_labels)
    cluster_summary = assign_segment_names(cluster_summary)

    cluster_map = cluster_df.set_index("CustomerID")["Cluster"]
    customer_df["Cluster"] = customer_df["CustomerID"].map(cluster_map).astype("Int64")
    customer_df["Segment"] = customer_df["Cluster"].map(cluster_summary["Segment"].to_dict())
    customer_df.to_csv(REPORTS_DIR / "customer_segments.csv", index=False)

    regression_features, regression_target = prepare_regression_data(customer_df)
    regression_results = fit_regression_models(regression_features, regression_target)

    classification_features, classification_target = prepare_classification_data(customer_df, pd.Series(customer_df["Cluster"], index=customer_df.index))
    classification_results = fit_classification_model(classification_features, classification_target)

    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].plot(range(2, 8), eval_results["inertia"], marker="o")
    axes[0, 0].set_title("Elbow Method")
    axes[0, 0].set_xlabel("Number of clusters")
    axes[0, 0].set_ylabel("Inertia")

    axes[0, 1].plot(range(2, 8), eval_results["silhouette"], marker="o", color="green")
    axes[0, 1].set_title("Silhouette Scores")
    axes[0, 1].set_xlabel("Number of clusters")
    axes[0, 1].set_ylabel("Silhouette Score")

    sns.barplot(data=cluster_summary.reset_index(), x="Cluster", y="CustomerCount", ax=axes[1, 0])
    axes[1, 0].set_title("Cluster Sizes")

    sns.barplot(data=cluster_summary.reset_index(), x="Cluster", y="AvgSpending", ax=axes[1, 1])
    axes[1, 1].set_title("Average Spending by Cluster")

    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "model_overview.png", dpi=300)
    plt.close(fig)

    business_insights = []
    business_insights.append("# Business Insights\n")
    business_insights.append("## Segment Summary\n")
    for _, row in cluster_summary.reset_index().iterrows():
        business_insights.append(f"- Cluster {int(row['Cluster'])} ({row['Segment']}): {int(row['CustomerCount'])} customers, average spending {row['AvgSpending']:.2f}, average recency {row['AvgRecency']:.2f}.\n")
    business_insights.append("\n## Recommended Actions\n")
    business_insights.append("- Reward high-value loyal customers with exclusive offers and premium memberships.\n")
    business_insights.append("- Re-engage inactive customers with personalized comeback campaigns.\n")
    business_insights.append("- Use discount-led offers selectively for discount-driven customers to protect margin.\n")

    (REPORTS_DIR / "business_insights.md").write_text("".join(business_insights), encoding="utf-8")

    print("Customer segmentation pipeline completed successfully.")
    print("- Saved customer segments report to reports/customer_segments.csv")
    print("- Saved business insights to reports/business_insights.md")
    print("- Saved visualization to reports/model_overview.png")
    print("Regression metrics:")
    print(regression_results["metrics"])
    print("Classification metrics:")
    print(classification_results["metrics"])


if __name__ == "__main__":
    main()
