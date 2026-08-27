# ============================================================
# MINI PROJECT 2
# Reusable Customer Churn Prediction Pipeline
# ============================================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# ============================================================
# Create Missing Columns (Project Requirement)
# ============================================================

np.random.seed(42)

df["Age"] = np.random.randint(18, 70, len(df))
df["SupportTickets"] = np.random.randint(0, 8, len(df))

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Rename Contract column
df.rename(columns={"Contract": "ContractType"}, inplace=True)

# ============================================================
# Remove Customer ID
# ============================================================

df.drop("customerID", axis=1, inplace=True)

# ============================================================
# Separate Features and Target
# ============================================================

X = df.drop("Churn", axis=1)
y = df["Churn"]

# ============================================================
# Train Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ============================================================
# Feature Lists
# ============================================================

numeric_features = [
    "Age",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "SupportTickets"
]

categorical_features = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "ContractType",
    "PaperlessBilling",
    "PaymentMethod"
]

# ============================================================
# Numerical Pipeline
# ============================================================

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# ============================================================
# Categorical Pipeline
# ============================================================

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# ============================================================
# Column Transformer
# ============================================================

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])

# ============================================================
# Complete Pipeline
# ============================================================

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ))
])

# ============================================================
# Train Model
# ============================================================

pipeline.fit(X_train, y_train)

# ============================================================
# Prediction
# ============================================================

y_pred = pipeline.predict(X_test)

# ============================================================
# Evaluation
# ============================================================

print("="*50)
print("Accuracy")
print("="*50)

print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))

# ============================================================
# Save Pipeline
# ============================================================

joblib.dump(pipeline, "customer_churn_pipeline.pkl")

print("\nPipeline Saved Successfully!")

# ============================================================
# Load Pipeline
# ============================================================

loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")

# ============================================================
# Predict New Customer
# ============================================================

new_customer = pd.DataFrame({

    "gender": ["Female"],
    "Partner": ["Yes"],
    "Dependents": ["No"],
    "PhoneService": ["Yes"],
    "MultipleLines": ["No"],
    "InternetService": ["Fiber optic"],
    "OnlineSecurity": ["No"],
    "OnlineBackup": ["Yes"],
    "DeviceProtection": ["Yes"],
    "TechSupport": ["No"],
    "StreamingTV": ["Yes"],
    "StreamingMovies": ["Yes"],
    "ContractType": ["Month-to-month"],
    "PaperlessBilling": ["Yes"],
    "PaymentMethod": ["Electronic check"],

    "Age": [30],
    "tenure": [5],
    "MonthlyCharges": [89.5],
    "TotalCharges": [447.5],
    "SupportTickets": [4]

})

prediction = loaded_pipeline.predict(new_customer)

print("\nPrediction for New Customer:")
print(prediction)