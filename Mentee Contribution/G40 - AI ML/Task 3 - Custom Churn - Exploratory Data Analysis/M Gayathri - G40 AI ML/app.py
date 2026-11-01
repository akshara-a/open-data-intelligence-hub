import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/customer_churn_model.pkl")

# Load feature names
feature_names = joblib.load("models/feature_names.pkl")

# Title
st.title("Customer Churn Prediction System")

st.write("Enter customer details below:")

# --------------------------
# Customer Details
# --------------------------

gender = st.selectbox("Gender", ["Male", "Female"])

senior = st.selectbox("Senior Citizen", [0, 1])

partner = st.selectbox("Partner", ["Yes", "No"])

dependents = st.selectbox("Dependents", ["Yes", "No"])

phone = st.selectbox("Phone Service", ["Yes", "No"])

multiple = st.selectbox(
    "Multiple Lines",
    ["No", "Yes", "No phone service"]
)

internet = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)

paperless = st.selectbox(
    "Paperless Billing",
    ["Yes", "No"]
)

payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

tenure = st.number_input(
    "Tenure (months)",
    min_value=0,
    max_value=72
)

monthly = st.number_input(
    "Monthly Charges",
    min_value=0.0
)

total = st.number_input(
    "Total Charges",
    min_value=0.0
)

if st.button("Predict"):

    # Create a dictionary with all features initialized to 0
    input_data = {feature: 0 for feature in feature_names}

    # Numeric features
    input_data["SeniorCitizen"] = senior
    input_data["tenure"] = tenure
    input_data["MonthlyCharges"] = monthly
    input_data["TotalCharges"] = total

    # Categorical features
    if gender == "Male":
        input_data["gender_Male"] = 1

    if partner == "Yes":
        input_data["Partner_Yes"] = 1

    if dependents == "Yes":
        input_data["Dependents_Yes"] = 1

    if phone == "Yes":
        input_data["PhoneService_Yes"] = 1

    if multiple == "Yes":
        input_data["MultipleLines_Yes"] = 1
    elif multiple == "No phone service":
        input_data["MultipleLines_No phone service"] = 1

    if internet == "Fiber optic":
        input_data["InternetService_Fiber optic"] = 1
    elif internet == "No":
        input_data["InternetService_No"] = 1

    if contract == "One year":
        input_data["Contract_One year"] = 1
    elif contract == "Two year":
        input_data["Contract_Two year"] = 1

    if paperless == "Yes":
        input_data["PaperlessBilling_Yes"] = 1

    if payment == "Credit card (automatic)":
        input_data["PaymentMethod_Credit card (automatic)"] = 1
    elif payment == "Electronic check":
        input_data["PaymentMethod_Electronic check"] = 1
    elif payment == "Mailed check":
        input_data["PaymentMethod_Mailed check"] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Reorder columns to match training
    input_df = input_df[feature_names]

    # Predict
    prediction = model.predict(input_df)

    # Display result
    if prediction[0] == 1:
        st.error("⚠️ Customer is Likely to Churn")
    else:
        st.success("✅ Customer is Not Likely to Churn")