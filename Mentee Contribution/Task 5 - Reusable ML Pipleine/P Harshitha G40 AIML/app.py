import streamlit as st
import pandas as pd
import joblib

model = joblib.load("models/churn_model.pkl")

st.title("Customer Churn Prediction")

tenure = st.number_input("Tenure", 0, 100)
monthly = st.number_input("Monthly Charges", 0.0)

if st.button("Predict"):

    data = pd.DataFrame({
        "gender":[0],
        "SeniorCitizen":[0],
        "Partner":[1],
        "Dependents":[0],
        "tenure":[tenure],
        "PhoneService":[1],
        "MultipleLines":[0],
        "InternetService":[1],
        "OnlineSecurity":[0],
        "OnlineBackup":[1],
        "DeviceProtection":[1],
        "TechSupport":[0],
        "StreamingTV":[1],
        "StreamingMovies":[1],
        "Contract":[0],
        "PaperlessBilling":[1],
        "PaymentMethod":[2],
        "MonthlyCharges":[monthly],
        "TotalCharges":[tenure * monthly]
    })

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("Customer is likely to churn.")
    else:
        st.success("Customer is likely to stay.")