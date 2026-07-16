# ==========================================================
# STEP 5 : RIDGE REGRESSION
# Product Rating Prediction
# ==========================================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("=" * 60)
print("RIDGE REGRESSION")
print("=" * 60)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv("data/processed_ecommerce.csv")

print("\nDataset Loaded Successfully")
print("Shape :", df.shape)

# ----------------------------------------------------------
# Feature Selection
# ----------------------------------------------------------

features = [

    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "revenue",
    "pages_viewed",
    "time_on_site_sec",
    "added_to_cart",
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "payment_method",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "session_duration_bucket",
    "location"

]

X = df[features]

y = df["rating"]

print("\nFeatures Selected Successfully")
print("Number of Features :", len(features))

# ----------------------------------------------------------
# Train Test Split
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# ----------------------------------------------------------
# Grid Search
# ----------------------------------------------------------

parameters = {
    "alpha": [0.01, 0.1, 1, 10, 100]
}

ridge = Ridge()

grid = GridSearchCV(

    ridge,

    parameters,

    cv=5,

    scoring="r2"

)

print("\nRunning Grid Search...")

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Alpha :", grid.best_params_["alpha"])

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------

predictions = best_model.predict(X_test)

# ----------------------------------------------------------
# Evaluation
# ----------------------------------------------------------

mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)

rmse = mse ** 0.5

r2 = r2_score(y_test, predictions)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print("MAE :", round(mae,4))

print("RMSE :", round(rmse,4))

print("R2 Score :", round(r2,4))

# ----------------------------------------------------------
# Save Model
# ----------------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/ridge_model.pkl")

print("\nModel Saved Successfully")

print("Location : models/ridge_model.pkl")

print("\nRIDGE REGRESSION COMPLETED SUCCESSFULLY")