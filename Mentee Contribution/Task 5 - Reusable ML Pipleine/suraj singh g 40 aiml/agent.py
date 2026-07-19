
import pandas as pd
import joblib
import os

print("model saved")



# 2. Model load 
model = joblib.load('churn_pipeline_final.pkl')
print("Model Loaded Successfully!")

# 3. new customer
new_customer = pd.DataFrame([{
    'gender': 'Male',
    'SeniorCitizen': 0,
    'Partner': 'No',
    'Dependents': 'No',
    'tenure': 2,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No',
    'OnlineBackup': 'No',
    'DeviceProtection': 'No',
    'TechSupport': 'No',
    'StreamingTV': 'Yes',
    'StreamingMovies': 'No',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 85.5,
    'TotalCharges': 171.0
}])

# 4. Prediction
prediction = model.predict(new_customer)[0]
probability = model.predict_proba(new_customer)[0][1]

print("\n" + "="*50)
print("PREDICTION RESULT")
print("="*50)

if prediction == 1:
    print("Result: CHURN (Customer will leave)")
    print(f"Risk Percentage: {probability*100:.2f}%")
else:
    print("Result: STAY (Customer will stay)")
    print(f"Risk Percentage: {probability*100:.2f}%")