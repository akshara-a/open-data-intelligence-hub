import joblib
import pandas as pd

model = joblib.load("../models/churn_model.pkl")

new_customer = pd.DataFrame({
    "gender": [1],
    "SeniorCitizen": [0],
    "Partner": [1],
    "Dependents": [0],
    "tenure": [12],
    "PhoneService": [1],
    "MultipleLines": [0],
    "InternetService": [1],
    "OnlineSecurity": [0],
    "OnlineBackup": [1],
    "DeviceProtection": [1],
    "TechSupport": [0],
    "StreamingTV": [1],
    "StreamingMovies": [1],
    "Contract": [0],
    "PaperlessBilling": [1],
    "PaymentMethod": [2],
    "MonthlyCharges": [80],
    "TotalCharges": [960]
})

prediction = model.predict(new_customer)

if prediction[0] == 1:
    print("Customer will churn")
else:
    print("Customer will stay")