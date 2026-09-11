import streamlit as st
import pandas as pd
from pathlib import Path

# Import Recommendation Models
from models.popularity import popularity_recommendations
from models.content_based import recommend as content_recommend
from models.collaborative import recommend_products as collaborative_recommend
from models.svd_model import recommend_products as svd_recommend
from models.knn_model import recommend_products as knn_recommend
from models.hybrid import hybrid_recommend

# ----------------------------
# Load Dataset
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "clean_amazon.csv"

df = pd.read_csv(DATA_PATH)

# ----------------------------
# Streamlit Page Config
# ----------------------------

st.set_page_config(
    page_title="Multi-Algorithm Recommendation System",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Multi-Algorithm Recommendation System")
st.markdown("Compare different recommendation algorithms using Amazon product reviews.")

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("Settings")

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    [
        "Popularity",
        "Content Based",
        "Collaborative",
        "SVD",
        "KNN",
        "Hybrid"
    ]
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    5,
    20,
    10
)

# ----------------------------
# Popularity
# ----------------------------

if algorithm == "Popularity":

    st.header("⭐ Popular Products")

    st.dataframe(
        popularity_recommendations(top_n)
    )

# ----------------------------
# Content-Based
# ----------------------------

elif algorithm == "Content Based":

    product = st.selectbox(
        "Select Product",
        sorted(df["product_name"].unique())
    )

    if st.button("Recommend"):

        result = content_recommend(product, top_n)

        st.subheader("Recommended Products")

        st.dataframe(result)

# ----------------------------
# Collaborative
# ----------------------------

elif algorithm == "Collaborative":

    user = st.selectbox(
        "Select User",
        sorted(df["user"].unique())
    )

    if st.button("Recommend"):

        result = collaborative_recommend(user, top_n)

        result = pd.DataFrame(
            result,
            columns=["Product", "Predicted Rating"]
        )

        st.dataframe(result)

# ----------------------------
# SVD
# ----------------------------

elif algorithm == "SVD":

    user = st.selectbox(
        "Select User",
        sorted(df["user"].unique())
    )

    if st.button("Recommend"):

        result = svd_recommend(user, top_n)

        result = pd.DataFrame(
            result,
            columns=["Product", "Predicted Rating"]
        )

        st.dataframe(result)

# ----------------------------
# KNN
# ----------------------------

elif algorithm == "KNN":

    user = st.selectbox(
        "Select User",
        sorted(df["user"].unique())
    )

    if st.button("Recommend"):

        result = knn_recommend(user, top_n)

        result = pd.DataFrame(
            result,
            columns=["Product", "Predicted Rating"]
        )

        st.dataframe(result)

# ----------------------------
# Hybrid
# ----------------------------

elif algorithm == "Hybrid":

    product = st.selectbox(
        "Select Product",
        sorted(df["product_name"].unique())
    )

    user = st.selectbox(
        "Select User",
        sorted(df["user"].unique())
    )

    if st.button("Recommend"):

        result = hybrid_recommend(product, user)

        st.dataframe(result)

# ----------------------------
# Dataset Overview
# ----------------------------

st.markdown("---")

st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Products", df["product_name"].nunique())
col2.metric("Users", df["user"].nunique())
col3.metric("Reviews", len(df))

st.dataframe(df.head())