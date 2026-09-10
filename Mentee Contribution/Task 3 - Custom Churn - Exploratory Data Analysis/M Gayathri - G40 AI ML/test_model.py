import joblib

model = joblib.load("models/logistic_regression_model.pkl")

print("✅ Model loaded successfully!")
print(model)