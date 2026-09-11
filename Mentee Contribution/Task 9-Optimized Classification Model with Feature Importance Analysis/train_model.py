import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
df = pd.read_csv("data/heart.csv")


# Features and target
X = df.drop("target", axis=1)
y = df["target"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create scaler
scaler = StandardScaler()


# Scale training data
X_train_scaled = scaler.fit_transform(X_train)

# Scale test data
X_test_scaled = scaler.transform(X_test)


# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train_scaled,
    y_train
)


# Evaluate
y_pred = model.predict(
    X_test_scaled
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred
    )
)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# Create models folder
os.makedirs(
    "models",
    exist_ok=True
)


# Save model and scaler
joblib.dump(
    model,
    "models/heart_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)


print("✅ Model and scaler saved successfully!")