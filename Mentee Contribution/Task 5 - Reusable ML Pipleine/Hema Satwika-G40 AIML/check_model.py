import joblib

# Load the saved model
model = joblib.load("customer_churn_pipeline.pkl")

# Print the model
print(model)