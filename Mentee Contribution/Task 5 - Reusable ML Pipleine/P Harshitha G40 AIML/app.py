import os

import joblib
import pandas as pd
import streamlit as st


# =========================================================
# Configuration
# =========================================================

MODEL_PATH = "models/churn_model.pkl"
DATA_PATH = "data/customer_churn.csv"


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)


# =========================================================
# Load Model
# =========================================================

if not os.path.exists(MODEL_PATH):
    st.error(
        "Trained model not found.\n\n"
        "Please train the model first using:\n\n"
        "`py src\\train.py`"
    )
    st.stop()

try:
    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error("Unable to load the trained model.")
    st.exception(e)
    st.stop()


# =========================================================
# Load Dataset
# =========================================================

if not os.path.exists(DATA_PATH):
    st.error(
        "Dataset not found at:\n\n"
        f"`{DATA_PATH}`"
    )
    st.stop()

try:
    reference_df = pd.read_csv(DATA_PATH)

except Exception as e:
    st.error("Unable to load the customer churn dataset.")
    st.exception(e)
    st.stop()


# =========================================================
# Application Header
# =========================================================

st.title("📊 Customer Churn Prediction")

st.write(
    "Enter customer details below to predict whether "
    "the customer is likely to churn."
)


# =========================================================
# Customer Information
# =========================================================

st.subheader("Customer Information")

col1, col2 = st.columns(2)


# =========================================================
# Column 1
# =========================================================

with col1:

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12,
        step=1
    )

    phone_service = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        [
            "No",
            "No phone service",
            "Yes"
        ]
    )

    internet_service = st.selectbox(
        "Internet Service",
        [
            "DSL",
            "Fiber optic",
            "No"
        ]
    )

    online_security = st.selectbox(
        "Online Security",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )

    online_backup = st.selectbox(
        "Online Backup",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )


# =========================================================
# Column 2
# =========================================================

with col2:

    device_protection = st.selectbox(
        "Device Protection",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )

    tech_support = st.selectbox(
        "Tech Support",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        [
            "No",
            "No internet service",
            "Yes"
        ]
    )

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Electronic check",
            "Mailed check"
        ]
    )

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=0.01
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=840.0,
        step=0.01
    )


# =========================================================
# Prediction
# =========================================================

st.divider()

if st.button(
    "🔮 Predict Churn",
    use_container_width=True
):

    try:

        # =================================================
        # Encode Input Features
        # These mappings MUST match feature_engineering.py
        # =================================================

        gender_encoded = {
            "Female": 0,
            "Male": 1
        }[gender]

        senior_citizen_encoded = {
            "No": 0,
            "Yes": 1
        }[senior_citizen]

        partner_encoded = {
            "No": 0,
            "Yes": 1
        }[partner]

        dependents_encoded = {
            "No": 0,
            "Yes": 1
        }[dependents]

        phone_service_encoded = {
            "No": 0,
            "Yes": 1
        }[phone_service]

        multiple_lines_encoded = {
            "No": 0,
            "No phone service": 1,
            "Yes": 2
        }[multiple_lines]

        internet_service_encoded = {
            "DSL": 0,
            "Fiber optic": 1,
            "No": 2
        }[internet_service]

        online_security_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[online_security]

        online_backup_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[online_backup]

        device_protection_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[device_protection]

        tech_support_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[tech_support]

        streaming_tv_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[streaming_tv]

        streaming_movies_encoded = {
            "No": 0,
            "No internet service": 1,
            "Yes": 2
        }[streaming_movies]

        contract_encoded = {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2
        }[contract]

        paperless_billing_encoded = {
            "No": 0,
            "Yes": 1
        }[paperless_billing]

        payment_method_encoded = {
            "Bank transfer (automatic)": 0,
            "Credit card (automatic)": 1,
            "Electronic check": 2,
            "Mailed check": 3
        }[payment_method]


        # =================================================
        # Create Input DataFrame
        # =================================================

        input_data = pd.DataFrame({
            "gender": [gender_encoded],
            "SeniorCitizen": [senior_citizen_encoded],
            "Partner": [partner_encoded],
            "Dependents": [dependents_encoded],
            "tenure": [tenure],
            "PhoneService": [phone_service_encoded],
            "MultipleLines": [multiple_lines_encoded],
            "InternetService": [internet_service_encoded],
            "OnlineSecurity": [online_security_encoded],
            "OnlineBackup": [online_backup_encoded],
            "DeviceProtection": [device_protection_encoded],
            "TechSupport": [tech_support_encoded],
            "StreamingTV": [streaming_tv_encoded],
            "StreamingMovies": [streaming_movies_encoded],
            "Contract": [contract_encoded],
            "PaperlessBilling": [paperless_billing_encoded],
            "PaymentMethod": [payment_method_encoded],
            "MonthlyCharges": [monthly_charges],
            "TotalCharges": [total_charges]
        })


        # =================================================
        # Make Prediction
        # =================================================

        prediction = model.predict(input_data)

        # Model target is "Yes" / "No"
        prediction_value = str(prediction[0])


        # =================================================
        # Display Prediction
        # =================================================

        st.subheader("Prediction Result")

        if prediction_value == "Yes":

            st.error(
                "⚠️ Customer is likely to churn."
            )

        else:

            st.success(
                "✅ Customer is likely to stay."
            )


        # =================================================
        # Prediction Probability
        # =================================================

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_data)[0]

            classes = model.classes_

            probability_dict = dict(
                zip(classes, probabilities)
            )

            churn_probability = (
                probability_dict.get("Yes", 0) * 100
            )

            stay_probability = (
                probability_dict.get("No", 0) * 100
            )


            st.subheader("Prediction Probability")

            probability_col1, probability_col2 = st.columns(2)

            with probability_col1:

                st.metric(
                    "Stay Probability",
                    f"{stay_probability:.2f}%"
                )

            with probability_col2:

                st.metric(
                    "Churn Probability",
                    f"{churn_probability:.2f}%"
                )


        # =================================================
        # Show Processed Input
        # =================================================

        with st.expander("View Processed Input"):

            st.dataframe(
                input_data,
                use_container_width=True
            )


    except Exception as e:

        st.error("Prediction failed.")

        st.exception(e)
        