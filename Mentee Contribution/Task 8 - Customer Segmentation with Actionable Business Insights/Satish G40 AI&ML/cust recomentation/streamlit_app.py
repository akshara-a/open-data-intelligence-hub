"""Streamlit app for Customer Segmentation project.

Run: streamlit run streamlit_app.py
"""
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from src.data_processing import load_and_preprocess
from src.clustering import run_kmeans
from src.regression import run_regressions
from src.classification import run_classification


st.set_page_config(page_title="Customer Segmentation", layout="wide")


@st.cache_data
def load_data(path="data/customer_data.csv"):
    return pd.read_csv(path)


def show_summary(df):
    st.subheader("Dataset preview")
    st.dataframe(df.head(50))
    st.subheader("Summary statistics")
    st.write(df.describe(include='all'))


def plot_distributions(df):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df["AnnualIncome"], kde=True, ax=ax[0])
    ax[0].set_title("Annual Income")
    sns.histplot(df["TotalSpending"], kde=True, ax=ax[1])
    ax[1].set_title("Total Spending")
    st.pyplot(fig)


def cluster_and_plot(X, raw_df, k):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    raw_df = raw_df.copy()
    raw_df["Cluster"] = labels

    # PCA for 2D visualization
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X)
    raw_df["x"] = coords[:, 0]
    raw_df["y"] = coords[:, 1]

    st.subheader(f"Clusters (K={k})")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=raw_df, x="x", y="y", hue="Cluster", palette="tab10", ax=ax, s=40)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    st.pyplot(fig)

    st.write("Cluster sizes:")
    st.write(raw_df["Cluster"].value_counts().sort_index())

    st.write("Cluster centers (numeric feature means):")
    st.write(raw_df.groupby("Cluster")[ ["Age","AnnualIncome","TotalSpending","PurchaseFrequency","AverageOrderValue","DaysSinceLastPurchase","WebsiteVisits","DiscountUsage","CustomerRating"] ].mean().round(2))


def main():
    st.title("Customer Segmentation with Actionable Insights")

    if not os.path.exists("data/customer_data.csv"):
        st.error("Dataset not found. Run scripts/generate_data.py to create data/customer_data.csv")
        return

    df = load_data()
    st.sidebar.header("Options")
    show_data = st.sidebar.checkbox("Show data & summary", value=True)

    if show_data:
        show_summary(df)
        plot_distributions(df)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Clustering")
    k = st.sidebar.slider("Select K for K-Means", min_value=2, max_value=10, value=3)

    # Use numeric features for clustering
    numeric_cols = ["Age","AnnualIncome","TotalSpending","PurchaseFrequency","AverageOrderValue","DaysSinceLastPurchase","WebsiteVisits","DiscountUsage","CustomerRating"]
    X = df[numeric_cols].fillna(0).values

    if st.sidebar.button("Run clustering"):
        cluster_and_plot(X, df, k)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Models")
    if st.sidebar.button("Train regression & classification"):
        with st.spinner("Training models..."):
            X_df, y_dict, preprocessor = load_and_preprocess("data/customer_data.csv")
            reg_results, lr_model, ridge_model = run_regressions(X_df, y_dict["regression"], preprocessor)
            clf_metrics, clf_model = run_classification(X_df, y_dict["classification"], preprocessor)

        st.subheader("Regression Results")
        st.json(reg_results)
        st.subheader("Classification Results")
        st.json(clf_metrics)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Business Recommendations")
    if st.sidebar.button("Show recommendations"):
        st.subheader("Actionable Recommendations")
        st.write("- Target high-value clusters with premium offers and loyalty programs.")
        st.write("- Re-engage customers with high 'DaysSinceLastPurchase' via email campaigns and discounts.")
        st.write("- Offer personalized discounts to customers with high website visits but low purchase frequency.")
        st.write("- Improve product bundles and cross-sell based on popular ProductCategory segments.")


if __name__ == "__main__":
    main()
