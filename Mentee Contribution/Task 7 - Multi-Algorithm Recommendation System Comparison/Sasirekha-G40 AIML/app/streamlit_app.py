import streamlit as st

st.set_page_config(
    page_title="SmartShop Recommendation System",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 SmartShop Recommendation System")

st.success("Use the left sidebar to navigate through the application.")

st.markdown("""
### Welcome

This application demonstrates:

- Ridge Regression
- Logistic Regression
- K-Means Clustering

Please select a page from the sidebar.
""")