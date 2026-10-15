import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


# Load dataset
data = pd.read_csv(
    "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)


# Remove customer ID
data.drop("customerID", axis=1, inplace=True)


# Convert TotalCharges
data["TotalCharges"] = pd.to_numeric(
    data["TotalCharges"],
    errors="coerce"
)

data.dropna(inplace=True)


# Encode categorical columns
encoder = LabelEncoder()

for column in data.select_dtypes(include="object"):
    data[column] = encoder.fit_transform(data[column])


# Split data

X = data.drop("Churn", axis=1)
y = data["Churn"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train model

model = RandomForestClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# Save model

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    "models/churn_model.pkl"
)


print("Training completed!")
print("Model saved at models/churn_model.pkl")