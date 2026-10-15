from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "outputs" / "clustered_customers.csv"

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Dataset",
        "EDA",
        "Customer Segments",
        "Business Insights"
    ]
)

# -----------------------------
# Home
# -----------------------------

if page == "Home":

    st.title("🛍 Customer Segmentation Dashboard")

    st.markdown("""
This dashboard performs **Customer Segmentation using K-Means Clustering**
and provides actionable business insights.
""")

    c1, c2, c3 = st.columns(3)

    c1.metric("Customers", len(df))
    c2.metric("Clusters", df["Cluster"].nunique())
    c3.metric("Average Spending", round(df["Spending_Score"].mean(),2))

# -----------------------------
# Dataset
# -----------------------------

elif page == "Dataset":

    st.title("📊 Dataset")

    st.dataframe(df)

# -----------------------------
# EDA
# -----------------------------

elif page == "EDA":

    st.title("📈 Exploratory Data Analysis")

    fig = px.histogram(
        df,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        df,
        x="Annual_Income",
        nbins=20,
        title="Annual Income Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        df,
        x="Spending_Score",
        nbins=20,
        title="Spending Score Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Customer Segments
# -----------------------------

elif page == "Customer Segments":

    st.title("🤖 Customer Segments")

    fig = px.scatter(
        df,
        x="Annual_Income",
        y="Spending_Score",
        color=df["Cluster"].astype(str),
        hover_data=["Age","Gender"],
        title="Customer Clusters"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Business Insights
# -----------------------------

elif page == "Business Insights":

    st.title("💡 Business Insights")

    summary = df.groupby("Cluster").agg({
        "Age":"mean",
        "Annual_Income":"mean",
        "Spending_Score":"mean",
        "CustomerID":"count"
    })

    summary.rename(columns={
        "CustomerID":"Customers"
    }, inplace=True)

    st.dataframe(summary)

    cluster = st.selectbox(
        "Select Cluster",
        sorted(df["Cluster"].unique())
    )

    income = summary.loc[cluster,"Annual_Income"]
    spending = summary.loc[cluster,"Spending_Score"]

    if income > 70 and spending > 60:

        st.success("⭐ VIP Customers")

        st.write("""
- Premium Membership
- Loyalty Rewards
- Exclusive Events
- Personalized Services
""")

    elif income > 70:

        st.info("💰 High Income, Low Spending")

        st.write("""
- Upselling Campaigns
- Personalized Discounts
- Luxury Product Promotions
""")

    elif spending > 60:

        st.warning("🛍 High Spending, Moderate Income")

        st.write("""
- Bundle Offers
- Cashback
- Referral Programs
""")

    else:

        st.error("📦 Budget Customers")

        st.write("""
- Seasonal Discounts
- Coupons
- Flash Sales
""")

# -----------------------------
# Download Dataset
# -----------------------------

st.sidebar.download_button(
    label="📥 Download Clustered Dataset",
    data=df.to_csv(index=False),
    file_name="clustered_customers.csv",
    mime="text/csv"
)