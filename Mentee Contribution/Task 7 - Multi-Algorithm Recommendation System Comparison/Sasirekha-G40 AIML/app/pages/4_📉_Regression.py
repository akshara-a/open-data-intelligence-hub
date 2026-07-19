import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.title("📉 Product Rating Prediction")

# -------------------------
# Load Model
# -------------------------
try:
    model = joblib.load(r"C:\Users\ELCOT\Desktop\Sasirekha-G40 AIML 7\models\best_ridge_model.pkl")
    st.success("✅ Ridge Regression Model Loaded Successfully")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.write("Enter customer details to predict the Product Rating.")

# -------------------------
# User Inputs
# -------------------------

price = st.number_input(
    "Product Price",
    min_value=1.0,
    value=500.0
)

discount = st.slider(
    "Discount (%)",
    0,
    80,
    10
)

previous_purchases = st.number_input(
    "Previous Purchases",
    0,
    100,
    5
)

recommendation_score = st.slider(
    "Recommendation Score",
    0,
    100,
    70
)

average_order_value = st.number_input(
    "Average Order Value",
    100.0,
    10000.0,
    1200.0
)

time_on_page = st.number_input(
    "Time on Page (seconds)",
    5,
    1000,
    120
)

views = st.number_input(
    "Number of Product Views",
    1,
    500,
    15
)

# -------------------------
# Predict Button
# -------------------------

if st.button("Predict Product Rating"):

    # 1. Create base DataFrame with exact lowercase names matching your original data
    input_df = pd.DataFrame({
        "price": [price],
        "discount": [discount],
        "previous_purchases": [previous_purchases],
        "recommendation_score": [recommendation_score],
        "average_order_value": [average_order_value],
        "time_on_page": [time_on_page],
        "views": [views]
    })

    # 2. Safety Check: Align features with model expectations
    # This automatically adds missing categorical columns (like gender, region) as 0
    # to prevent "ValueError: feature_names mismatch" from your trained model
    try:
        model_features = model.feature_names_in_
        
        # Add missing columns with default value of 0
        for col in model_features:
            if col not in input_df.columns:
                input_df[col] = 0
                
        # Reorder columns to match the exact sequence the model expects
        input_df = input_df[model_features]
        
        # 3. Make Prediction
        prediction = model.predict(input_df)
        
        # Clip values to standard 1.0 - 5.0 star rating boundaries if needed
        final_rating = np.clip(prediction[0], 1.0, 5.0)

        st.success(
            f"⭐ Predicted Product Rating : {final_rating:.2f}"
        )
        
    except AttributeError:
        # Fallback if the saved model doesn't expose feature_names_in_
        try:
            prediction = model.predict(input_df)
            st.success(f"⭐ Predicted Product Rating : {prediction[0]:.2f}")
        except Exception as err:
            st.error(f"❌ Feature Mismatch Error: Your model expects more columns than provided. Details: {err}")