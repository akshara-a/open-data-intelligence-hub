import streamlit as st
import pandas as pd
import pickle

# Load models
with open("ridge_model.pkl", "rb") as f:
    ridge_model = pickle.load(f)

with open("logistic_model.pkl", "rb") as f:
    logistic_model = pickle.load(f)

with open("kmeans_model.pkl", "rb") as f:
    kmeans_model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# App title
st.title("E-Commerce Customer Analytics System")
st.write("Predict Rating, Purchase Status, and Customer Segment")

# Input fields
unit_price = st.number_input("Unit Price", min_value=0.0)
quantity = st.number_input("Quantity", min_value=1)
discount_percent = st.number_input("Discount Percent", min_value=0.0)
pages_viewed = st.number_input("Pages Viewed", min_value=1)
time_on_site = st.number_input("Time on Site (seconds)", min_value=1)
revenue = st.number_input("Revenue", min_value=0.0)
rating = st.number_input("Customer Rating", min_value=1.0, max_value=5.0)

# -------------------------
# Rating Prediction
# -------------------------
st.header("⭐ Predict Product Rating")

if st.button("Predict Rating"):

    features = pd.DataFrame({
        "unit_price": [unit_price],
        "quantity": [quantity],
        "discount_percent": [discount_percent],
        "pages_viewed": [pages_viewed],
        "time_on_site_sec": [time_on_site],
        "revenue": [revenue]
    })

    prediction = ridge_model.predict(features)

    st.success(f"Predicted Rating: {prediction[0]:.2f}")

# -------------------------
# Purchase Prediction
# -------------------------
st.header("🛒 Predict Purchase Status")

if st.button("Predict Purchase"):

    features = pd.DataFrame({
        "unit_price": [unit_price],
        "quantity": [quantity],
        "discount_percent": [discount_percent],
        "pages_viewed": [pages_viewed],
        "time_on_site_sec": [time_on_site],
        "rating": [rating],
        "revenue": [revenue]
    })

    prediction = logistic_model.predict(features)

    if prediction[0] == 1:
        st.success("Customer is likely to purchase.")
    else:
        st.error("Customer is unlikely to purchase.")

# -------------------------
# Customer Segmentation
# -------------------------
st.header("👥 Customer Segment")

if st.button("Find Customer Segment"):

    cluster_features = pd.DataFrame({
        "pages_viewed": [pages_viewed],
        "time_on_site_sec": [time_on_site],
        "quantity": [quantity],
        "revenue": [revenue]
    })

    scaled = scaler.transform(cluster_features)
    cluster = kmeans_model.predict(scaled)

    st.success(f"Customer belongs to Cluster {cluster[0]}")
