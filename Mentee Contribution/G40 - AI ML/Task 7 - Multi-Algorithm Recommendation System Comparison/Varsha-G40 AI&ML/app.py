# ==========================================================
# E-COMMERCE RECOMMENDATION SYSTEM
# STREAMLIT APPLICATION
# PART 1
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Recommendation System",
    page_icon="🛒",
    layout="wide"
)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/ecommerce.csv")

# ----------------------------------------------------------
# Load Models
# ----------------------------------------------------------

ridge_model = joblib.load("models/ridge_model.pkl")
logistic_model = joblib.load("models/logistic_model.pkl")
kmeans_model = joblib.load("models/kmeans_model.pkl")

scaler = joblib.load("models/scaler.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# ----------------------------------------------------------
# Title
# ----------------------------------------------------------

st.title("🛒 E-Commerce Recommendation System")

st.write("### Machine Learning Modules")

st.success("✔ Product Rating Prediction (Ridge Regression)")
st.success("✔ Purchase Prediction (Logistic Regression)")
st.success("✔ Customer Segmentation (K-Means Clustering)")

# ----------------------------------------------------------
# Customer Information
# ----------------------------------------------------------

st.header("Customer Information")

col1, col2 = st.columns(2)

with col1:

    device_type = st.selectbox(
        "Device Type",
        sorted(df["device_type"].astype(str).unique())
    )

    user_type = st.selectbox(
        "User Type",
        sorted(df["user_type"].astype(str).unique())
    )

    marketing_channel = st.selectbox(
        "Marketing Channel",
        sorted(df["marketing_channel"].astype(str).unique())
    )

    product_category = st.selectbox(
        "Product Category",
        sorted(df["product_category"].astype(str).unique())
    )

    payment_method = st.selectbox(
        "Payment Method",
        sorted(df["payment_method"].astype(str).unique())
    )

    location = st.selectbox(
        "Location",
        sorted(df["location"].astype(str).unique())
    )

with col2:

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        value=1000.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1
    )

    discount_percent = st.slider(
        "Discount Percent",
        0,
        100,
        10
    )

    discount_amount = st.number_input(
        "Discount Amount",
        min_value=0.0,
        value=100.0
    )

    revenue = st.number_input(
        "Revenue",
        min_value=0.0,
        value=1000.0
    )

    pages_viewed = st.slider(
        "Pages Viewed",
        1,
        100,
        10
    )

    time_on_site_sec = st.slider(
        "Time On Site (Seconds)",
        10,
        3000,
        500
    )

# ----------------------------------------------------------
# Shopping Behaviour
# ----------------------------------------------------------

st.header("Shopping Behaviour")

col3, col4 = st.columns(2)

with col3:

    added_to_cart = st.selectbox(
        "Added To Cart",
        [0, 1]
    )

    visit_day = st.selectbox(
        "Visit Day",
        sorted(df["visit_day"].astype(str).unique())
    )

    visit_month = st.selectbox(
        "Visit Month",
        sorted(df["visit_month"].astype(str).unique())
    )

with col4:

    visit_weekday = st.selectbox(
        "Visit Weekday",
        sorted(df["visit_weekday"].astype(str).unique())
    )

    visit_season = st.selectbox(
        "Visit Season",
        sorted(df["visit_season"].astype(str).unique())
    )

    session_duration_bucket = st.selectbox(
        "Session Duration Bucket",
        sorted(df["session_duration_bucket"].astype(str).unique())
    )

# ----------------------------------------------------------
# Predict Button
# ----------------------------------------------------------

predict = st.button(
    "Predict",
    use_container_width=True
)
# ==========================================================
# PART 2 : PREPROCESS USER INPUT
# ==========================================================

if predict:

    try:

        # -----------------------------
        # Encode categorical values
        # -----------------------------

        device_type = label_encoders["device_type"].transform([str(device_type)])[0]
        user_type = label_encoders["user_type"].transform([str(user_type)])[0]
        marketing_channel = label_encoders["marketing_channel"].transform([str(marketing_channel)])[0]
        product_category = label_encoders["product_category"].transform([str(product_category)])[0]
        payment_method = label_encoders["payment_method"].transform([str(payment_method)])[0]
        visit_day = label_encoders["visit_day"].transform([str(visit_day)])[0]
        visit_month = label_encoders["visit_month"].transform([str(visit_month)])[0]
        visit_weekday = label_encoders["visit_weekday"].transform([str(visit_weekday)])[0]
        visit_season = label_encoders["visit_season"].transform([str(visit_season)])[0]
        session_duration_bucket = label_encoders["session_duration_bucket"].transform(
            [str(session_duration_bucket)]
        )[0]
        location = label_encoders["location"].transform([str(location)])[0]

        # -----------------------------
        # Scale numerical features
        # -----------------------------

        numerical_df = pd.DataFrame(
            [[
                unit_price,
                quantity,
                discount_percent,
                discount_amount,
                revenue,
                pages_viewed,
                time_on_site_sec
            ]],
            columns=[
                "unit_price",
                "quantity",
                "discount_percent",
                "discount_amount",
                "revenue",
                "pages_viewed",
                "time_on_site_sec"
            ]
        )

        scaled = scaler.transform(numerical_df)

        unit_price = float(scaled[0][0])
        quantity = float(scaled[0][1])
        discount_percent = float(scaled[0][2])
        discount_amount = float(scaled[0][3])
        revenue = float(scaled[0][4])
        pages_viewed = float(scaled[0][5])
        time_on_site_sec = float(scaled[0][6])

        # -----------------------------
        # Ridge Regression Features
        # -----------------------------

        ridge_features = pd.DataFrame([{

            "unit_price": unit_price,
            "quantity": quantity,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "revenue": revenue,
            "pages_viewed": pages_viewed,
            "time_on_site_sec": time_on_site_sec,
            "added_to_cart": added_to_cart,
            "device_type": device_type,
            "user_type": user_type,
            "marketing_channel": marketing_channel,
            "product_category": product_category,
            "payment_method": payment_method,
            "visit_day": visit_day,
            "visit_month": visit_month,
            "visit_weekday": visit_weekday,
            "visit_season": visit_season,
            "session_duration_bucket": session_duration_bucket,
            "location": location

        }])

        predicted_rating = ridge_model.predict(ridge_features)[0]

        # -----------------------------
        # Logistic Regression Features
        # -----------------------------

        logistic_features = pd.DataFrame([{

            "device_type": device_type,
            "user_type": user_type,
            "marketing_channel": marketing_channel,
            "product_category": product_category,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "revenue": revenue,
            "pages_viewed": pages_viewed,
            "time_on_site_sec": time_on_site_sec,
            "added_to_cart": added_to_cart,
            "rating": predicted_rating,
            "payment_method": payment_method,
            "visit_day": visit_day,
            "visit_month": visit_month,
            "visit_weekday": visit_weekday,
            "visit_season": visit_season,
            "session_duration_bucket": session_duration_bucket,
            "location": location

        }])

        purchase_prediction = logistic_model.predict(logistic_features)[0]

        # -----------------------------
        # KMeans Features
        # -----------------------------

        cluster_features = pd.DataFrame([{

            "pages_viewed": pages_viewed,
            "time_on_site_sec": time_on_site_sec,
            "quantity": quantity,
            "revenue": revenue,
            "rating": predicted_rating,
            "added_to_cart": added_to_cart

        }])

        cluster = kmeans_model.predict(cluster_features)[0]

    except Exception as e:

        st.error(e)
# ==========================================================
# PART 3 : DISPLAY RESULTS
# ==========================================================

if predict:

    st.markdown("---")
    st.header("Prediction Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "⭐ Predicted Rating",
            round(float(predicted_rating),2)
        )

    with col2:

        if purchase_prediction == 1:

            st.success("🛒 Customer Will Purchase")

        else:

            st.error("❌ Customer Will Not Purchase")

    with col3:

        cluster_names = {

            0:"Premium Customer",

            1:"Frequent Buyer",

            2:"Occasional Buyer",

            3:"Discount Seeker"

        }

        st.info(cluster_names.get(cluster,"Unknown"))

# ----------------------------------------------------------
# Prediction Summary
# ----------------------------------------------------------

    st.markdown("---")

    st.subheader("Prediction Summary")

    summary = pd.DataFrame({

        "Predicted Rating":[round(float(predicted_rating),2)],

        "Purchase Prediction":[
            "Yes" if purchase_prediction==1 else "No"
        ],

        "Customer Segment":[
            cluster_names.get(cluster)
        ]

    })

    st.dataframe(summary,use_container_width=True)

# ----------------------------------------------------------
# Customer Behaviour Chart
# ----------------------------------------------------------

    st.subheader("Customer Behaviour")

    chart = pd.DataFrame({

        "Feature":[

            "Revenue",

            "Pages Viewed",

            "Quantity",

            "Discount %"

        ],

        "Value":[

            revenue,

            pages_viewed,

            quantity,

            discount_percent

        ]

    })

    st.bar_chart(

        chart.set_index("Feature")

    )

# ----------------------------------------------------------
# Rating Progress
# ----------------------------------------------------------

    st.subheader("Predicted Rating Score")

    progress = min(max(predicted_rating/5,0),1)

    st.progress(progress)

    st.write(

        f"Predicted Rating : {round(float(predicted_rating),2)} / 5"

    )

# ----------------------------------------------------------
# Download Result
# ----------------------------------------------------------

    csv = summary.to_csv(index=False).encode()

    st.download_button(

        label="⬇ Download Prediction",

        data=csv,

        file_name="prediction.csv",

        mime="text/csv"

    )

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

    st.markdown("---")

    st.success("Prediction Completed Successfully ✅")