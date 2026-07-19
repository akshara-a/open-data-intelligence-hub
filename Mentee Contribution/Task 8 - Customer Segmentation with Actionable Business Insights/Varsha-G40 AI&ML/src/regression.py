# ==========================================
# Regression Model
# Predict Monetary Value (M)
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("reports/customer_segments.csv")

print("=" * 60)
print("REGRESSION MODEL")
print("=" * 60)

# ------------------------------------------
# Select Features
# ------------------------------------------

X = df[
    [
        "Income",
        "R",
        "F",
        "Age",
        "Children",
        "CampaignsAccepted",
        "WebActivity"
    ]
]

# Target Variable

y = df["M"]

# ------------------------------------------
# Train-Test Split
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==========================================
# Linear Regression
# ==========================================

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

# Evaluation

linear_mae = mean_absolute_error(y_test, linear_predictions)
linear_rmse = mean_squared_error(
    y_test,
    linear_predictions
) ** 0.5

linear_r2 = r2_score(
    y_test,
    linear_predictions
)

print("\nLinear Regression Results")

print("MAE :", round(linear_mae,3))
print("RMSE:", round(linear_rmse,3))
print("R2  :", round(linear_r2,3))

# ==========================================
# Ridge Regression
# ==========================================

ridge_model = Ridge(alpha=1.0)

ridge_model.fit(X_train, y_train)

ridge_predictions = ridge_model.predict(X_test)

ridge_mae = mean_absolute_error(
    y_test,
    ridge_predictions
)

ridge_rmse = mean_squared_error(
    y_test,
    ridge_predictions
) ** 0.5

ridge_r2 = r2_score(
    y_test,
    ridge_predictions
)

print("\nRidge Regression Results")

print("MAE :", round(ridge_mae,3))
print("RMSE:", round(ridge_rmse,3))
print("R2  :", round(ridge_r2,3))

# ==========================================
# Comparison Table
# ==========================================

comparison = pd.DataFrame({

    "Model":[
        "Linear Regression",
        "Ridge Regression"
    ],

    "MAE":[
        linear_mae,
        ridge_mae
    ],

    "RMSE":[
        linear_rmse,
        ridge_rmse
    ],

    "R2":[
        linear_r2,
        ridge_r2
    ]

})

print("\nModel Comparison")
print(comparison)

comparison.to_csv(
    "reports/regression_results.csv",
    index=False
)

# ==========================================
# Visualization
# ==========================================

plt.figure(figsize=(8,6))

plt.scatter(
    y_test,
    linear_predictions
)

plt.xlabel("Actual Monetary")

plt.ylabel("Predicted Monetary")

plt.title("Linear Regression: Actual vs Predicted")

plt.grid(True)

plt.show()

plt.figure(figsize=(8,6))

plt.scatter(
    y_test,
    ridge_predictions
)

plt.xlabel("Actual Monetary")

plt.ylabel("Predicted Monetary")

plt.title("Ridge Regression: Actual vs Predicted")

plt.grid(True)

plt.show()

print("\nRegression Completed Successfully!")