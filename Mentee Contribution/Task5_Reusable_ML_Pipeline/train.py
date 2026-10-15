from data_loader import load_data
from preprocessing import preprocess

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

import joblib


# Load data

df = load_data()


# Preprocess

X, y = preprocess(df)


# Split data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create model

model = RandomForestClassifier(
    random_state=42
)


# Train

model.fit(
    X_train,
    y_train
)


# Test

prediction = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    prediction
)


print(
    "Accuracy:",
    accuracy
)


# Save model

joblib.dump(
    model,
    "models/random_forest.pkl"
)


print(
    "Model saved!"
)