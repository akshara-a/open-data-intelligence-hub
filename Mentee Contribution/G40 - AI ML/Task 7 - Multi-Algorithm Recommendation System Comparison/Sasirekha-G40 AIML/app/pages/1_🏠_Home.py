import streamlit as st
from utils.data_loader import load_data

st.title("🏠 SmartShop Recommendation Dashboard")

df = load_data()

st.header("Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        len(df)
    )

with col2:
    st.metric(
        "Categories",
        df["Category"].nunique()
    )

with col3:
    st.metric(
        "Regions",
        df["Region"].nunique()
    )

with col4:
    st.metric(
        "Membership Types",
        df["Membership"].nunique()
    )

st.divider()

st.markdown("""
### Machine Learning Algorithms

- 📉 Ridge Regression
- 🎯 Logistic Regression
- 👥 K-Means Clustering

---

### Business Goals

✔ Predict Product Ratings

✔ Predict Purchases

✔ Segment Customers

✔ Generate Business Insights
""")