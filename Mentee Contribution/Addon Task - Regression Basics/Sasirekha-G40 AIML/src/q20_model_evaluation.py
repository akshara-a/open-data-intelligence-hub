"""
============================================================

Interview Question 20

How would you evaluate the performance
of a Regression Model?

Interview Answer

Regression models are evaluated using several metrics:

1. MAE  (Mean Absolute Error)
2. MSE  (Mean Squared Error)
3. RMSE (Root Mean Squared Error)
4. R² Score
5. Adjusted R² Score

Each metric measures model performance differently.

============================================================
"""

import pandas as pd
import numpy as np

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------------------------------
# Generate Dataset
# --------------------------------------------------------

X, y = make_regression(
    n_samples=300,
    n_features=4,
    noise=20,
    random_state=42
)

feature_names = [
    "Feature_1",
    "Feature_2",
    "Feature_3",
    "Feature_4"
]

df = pd.DataFrame(
    X,
    columns=feature_names
)

df["Target"] = y

print("Dataset Preview\n")
print(df.head())

# --------------------------------------------------------
# Split Dataset
# --------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# --------------------------------------------------------
# Train Model
# --------------------------------------------------------

model = LinearRegression()

model.fit(X_train, y_train)

# --------------------------------------------------------
# Prediction
# --------------------------------------------------------

prediction = model.predict(X_test)

# --------------------------------------------------------
# Evaluation Metrics
# --------------------------------------------------------

mae = mean_absolute_error(
    y_test,
    prediction
)

mse = mean_squared_error(
    y_test,
    prediction
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    prediction
)

# --------------------------------------------------------
# Adjusted R²
# --------------------------------------------------------

n = len(y_test)

p = X_test.shape[1]

adjusted_r2 = 1 - (
    ((1 - r2) * (n - 1))
    /
    (n - p - 1)
)

# --------------------------------------------------------
# Display Metrics
# --------------------------------------------------------

results = pd.DataFrame({

    "Metric":[

        "MAE",

        "MSE",

        "RMSE",

        "R² Score",

        "Adjusted R²"

    ],

    "Value":[

        mae,

        mse,

        rmse,

        r2,

        adjusted_r2

    ]

})

print("\nModel Evaluation\n")

print(results)

# --------------------------------------------------------
# Actual vs Predicted
# --------------------------------------------------------

comparison = pd.DataFrame({

    "Actual": y_test,

    "Predicted": prediction

})

print("\nActual vs Predicted\n")

print(comparison.head(15))

# --------------------------------------------------------
# Metric Explanation
# --------------------------------------------------------

print("\n------------------------------------")

print("Metric Explanation")

print("------------------------------------")

print(f"MAE  : {mae:.2f}")

print("Average absolute prediction error.")

print()

print(f"MSE  : {mse:.2f}")

print("Squares large errors.")

print()

print(f"RMSE : {rmse:.2f}")

print("Same unit as target variable.")

print()

print(f"R²   : {r2:.4f}")

print("Explains variance in target.")

print()

print(f"Adjusted R² : {adjusted_r2:.4f}")

print("Penalizes unnecessary features.")

# --------------------------------------------------------
# Overall Interpretation
# --------------------------------------------------------

print("\n------------------------------------")

print("Overall Interpretation")

print("------------------------------------")

if r2 >= 0.90:

    print("Excellent Regression Model")

elif r2 >= 0.80:

    print("Very Good Regression Model")

elif r2 >= 0.70:

    print("Good Regression Model")

else:

    print("Model Needs Improvement")

# --------------------------------------------------------
# Interview Summary
# --------------------------------------------------------

print("\n------------------------------------")

print("Interview Summary")

print("------------------------------------")

print("""

MAE

↓

Easy to Understand

↓

Less sensitive to outliers

------------------------------------

MSE

↓

Squares errors

↓

Highly sensitive to outliers

------------------------------------

RMSE

↓

Square root of MSE

↓

Same unit as target

------------------------------------

R² Score

↓

Measures goodness of fit

↓

Higher is better

------------------------------------

Adjusted R²

↓

Used in Multiple Regression

↓

Penalizes unnecessary features

""")

print("====================================================")
print("Regression Model Evaluation Completed Successfully")
print("====================================================")