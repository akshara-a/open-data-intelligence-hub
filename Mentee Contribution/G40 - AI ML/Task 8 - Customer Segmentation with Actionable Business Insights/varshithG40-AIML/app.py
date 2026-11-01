import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.generate_data import generate_synthetic_data
from src.data_preprocessing import build_rfm_features, prepare_feature_frame, scale_features
from src.clustering import evaluate_kmeans, fit_kmeans, profile_clusters, assign_segment_names


def load_data():
    data_dir = ROOT / "data"
    customer_df, transactions_df = generate_synthetic_data(data_dir)
    rfm_df = build_rfm_features(transactions_df)
    feature_frame = prepare_feature_frame(customer_df, rfm_df)
    return customer_df, transactions_df, feature_frame


def plot_cluster_summary(summary):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.barplot(data=summary.reset_index(), x="Cluster", y="CustomerCount", ax=axes[0])
    axes[0].set_title("Cluster Sizes")
    sns.barplot(data=summary.reset_index(), x="Cluster", y="AvgSpending", ax=axes[1])
    axes[1].set_title("Average Spending")
    plt.tight_layout()
    return fig


def main():
    st.set_page_config(page_title="Customer Segmentation UI", layout="wide")
    st.title("Customer Segmentation Dashboard")
    st.markdown("Use this interface to explore customer clusters, spending, and model insights.")

    customer_df, transactions_df, feature_frame = load_data()

    st.sidebar.header("Clustering Settings")
    n_clusters = st.sidebar.slider("Number of clusters", 2, 6, 4)
    st.sidebar.markdown("\n---\nUse the chart and summary to decide the best cluster count.")

    clustering_features = feature_frame[["Recency", "Frequency", "Monetary", "AverageOrderValue", "DiscountUsage", "CustomerRating"]].dropna()
    scaled_features, _ = scale_features(clustering_features)
    eval_results = evaluate_kmeans(scaled_features, range(2, 8))
    model, cluster_labels = fit_kmeans(scaled_features, n_clusters)

    cluster_df = feature_frame.loc[clustering_features.index].copy()
    cluster_df["Cluster"] = cluster_labels.astype(int).values
    cluster_summary = profile_clusters(cluster_df, cluster_labels)
    cluster_summary = assign_segment_names(cluster_summary)

    st.subheader("Cluster Overview")
    st.dataframe(cluster_summary.reset_index()[["Cluster", "Segment", "CustomerCount", "AvgSpending", "AvgFrequency", "AvgRecency"]])

    st.subheader("Cluster Metrics")
    fig = plot_cluster_summary(cluster_summary)
    st.pyplot(fig)

    st.subheader("Elbow and Silhouette")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(range(2, 8), eval_results["inertia"], marker="o")
    axes[0].set_title("Elbow Method")
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("Inertia")
    axes[1].plot(range(2, 8), eval_results["silhouette"], marker="o", color="green")
    axes[1].set_title("Silhouette Score")
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("Score")
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Sample Customer Data")
    st.dataframe(customer_df.head(10))

    st.sidebar.header("Business Recommendation")
    st.sidebar.write("- Reward high-value loyal customers.")
    st.sidebar.write("- Re-engage inactive customers.")
    st.sidebar.write("- Use discounts carefully.")


if __name__ == "__main__":
    main()
