"""
============================================================

Interview Question 15

What is Regularization, and why is it used?

Interview Answer

Regularization is a technique used to reduce overfitting
by adding a penalty term to the model's cost function.

It prevents the model from learning excessively large
coefficients.

Advantages

1. Reduces overfitting
2. Improves generalization
3. Handles multicollinearity
4. Produces more stable models

Common Types

1. Ridge Regression (L2)
2. Lasso Regression (L1)
3. Elastic Net (L1 + L2)

============================================================
"""

import pandas as pd
import numpy as np

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

# -------------------------------------------------------
# Generate Dataset
# -------------------------------------------------------

X, y = make_regression(
    n_samples=300,
    n_features=5,
    noise=25,
    random_state=42
)

feature_names = [
    "Feature_1",
    "Feature_2",
    "Feature_3",
    "Feature_4",
    "Feature_5"
]

df = pd.DataFrame(X, columns=feature_names)

df["Target"] = y

print("Dataset\n")
print(df.head())

# -------------------------------------------------------
# Split Dataset
# -------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# -------------------------------------------------------
# Linear Regression
# -------------------------------------------------------

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_prediction = linear_model.predict(X_test)

linear_r2 = r2_score(
    y_test,
    linear_prediction
)

linear_mse = mean_squared_error(
    y_test,
    linear_prediction
)

# -------------------------------------------------------
# Ridge Regression
# -------------------------------------------------------

ridge_model = Ridge(alpha=10)

ridge_model.fit(X_train, y_train)

ridge_prediction = ridge_model.predict(X_test)

ridge_r2 = r2_score(
    y_test,
    ridge_prediction
)

ridge_mse = mean_squared_error(
    y_test,
    ridge_prediction
)

# -------------------------------------------------------
# Coefficient Comparison
# -------------------------------------------------------

coefficient_table = pd.DataFrame({

    "Feature": feature_names,

    "Linear Regression":

        linear_model.coef_,

    "Ridge Regression":

        ridge_model.coef_

})

print("\nCoefficient Comparison\n")

print(coefficient_table)

# -------------------------------------------------------
# Performance Comparison
# -------------------------------------------------------

performance = pd.DataFrame({

    "Model": [

        "Linear Regression",

        "Ridge Regression"

    ],

    "R² Score": [

        linear_r2,

        ridge_r2

    ],

    "MSE": [

        linear_mse,

        ridge_mse

    ]

})

print("\nPerformance Comparison\n")

print(performance)

# -------------------------------------------------------
# Best Model
# -------------------------------------------------------

print("\n------------------------------------")

print("Interview Interpretation")

print("------------------------------------")

print(f"Linear Regression R² : {linear_r2:.4f}")

print(f"Ridge Regression R²  : {ridge_r2:.4f}")

print()

print(f"Linear Regression MSE : {linear_mse:.2f}")

print(f"Ridge Regression MSE  : {ridge_mse:.2f}")

print()

print("Notice that Ridge Regression")

print("- Shrinks coefficient values")

print("- Reduces overfitting")

print("- Produces a more stable model")

print("- Helps with multicollinearity")

# -------------------------------------------------------
# Formula
# -------------------------------------------------------

print("\nFormula")

print("------------------------------------")

print("Linear Regression Cost")

print("MSE")

print()

print("Ridge Regression Cost")

print("MSE + αΣβ²")

print()

print("α (alpha) controls")

print("the amount of regularization.")

# -------------------------------------------------------
# Alpha Demonstration
# -------------------------------------------------------

print("\nEffect of Alpha")

print("------------------------------------")

alphas = [0.1, 1, 10, 100]

for alpha in alphas:

    model = Ridge(alpha=alpha)

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    score = r2_score(y_test, prediction)

    print(f"Alpha = {alpha:<5}  R² = {score:.4f}")

# -------------------------------------------------------
# Interview Summary
# -------------------------------------------------------

print("\n------------------------------------")

print("Interview Summary")

print("------------------------------------")

print("""

Regularization helps reduce overfitting.

It adds a penalty to the cost function.

Large coefficients become smaller.

Benefits

• Better Generalization

• Stable Coefficients

• Handles Multicollinearity

• Better Prediction on Unseen Data

Common Regularization Methods

1. Ridge (L2)

2. Lasso (L1)

3. Elastic Net (L1 + L2)

""")