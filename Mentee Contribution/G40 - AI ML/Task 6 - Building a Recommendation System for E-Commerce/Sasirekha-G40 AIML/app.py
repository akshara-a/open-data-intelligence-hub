import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Recommendation System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/ecommerce_clustered.csv")

df = load_data()

st.sidebar.title("🛒 Navigation")

st.sidebar.success("Select a page from the sidebar.")

st.title("🛒 E-Commerce Recommendation System")

st.markdown(
"""
An End-to-End Machine Learning Project using

- Regression
- Classification
- Clustering
- Streamlit
- Scikit-Learn
"""
)

st.markdown("---")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
"Customers",
len(df)
)

c2.metric(
"Products",
df["Product_ID"].nunique()
)

c3.metric(
"Purchases",
int(df["Purchase_Status"].sum())
)

c4.metric(
"Average Rating",
round(df["Rating"].mean(),2)
)

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.info("Use the sidebar to explore different pages.")

st.markdown("---")

st.caption("Developed using Streamlit + Scikit-Learn")
