"""
Regression utilities: predicting CustomerRating from behavioural
features using Linear and Ridge Regression, with GridSearchCV tuning
for Ridge's alpha.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def get_regression_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }


def run_regression_pipeline(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Baseline Linear Regression
    lin = LinearRegression()
    lin.fit(X_train, y_train)
    lin_pred = lin.predict(X_test)
    lin_metrics = get_regression_metrics(y_test, lin_pred)

    # Baseline Ridge (default alpha)
    ridge_base = Ridge(alpha=1.0, random_state=random_state)
    ridge_base.fit(X_train, y_train)
    ridge_base_pred = ridge_base.predict(X_test)
    ridge_base_metrics = get_regression_metrics(y_test, ridge_base_pred)

    # Tuned Ridge via GridSearchCV
    param_grid = {"alpha": [0.01, 0.1, 1.0, 5.0, 10.0, 50.0, 100.0]}
    grid = GridSearchCV(Ridge(random_state=random_state), param_grid,
                         cv=5, scoring="neg_root_mean_squared_error")
    grid.fit(X_train, y_train)
    ridge_tuned = grid.best_estimator_
    ridge_tuned_pred = ridge_tuned.predict(X_test)
    ridge_tuned_metrics = get_regression_metrics(y_test, ridge_tuned_pred)

    results = {
        "Linear Regression": {"model": lin, "metrics": lin_metrics, "y_pred": lin_pred},
        "Ridge (baseline)": {"model": ridge_base, "metrics": ridge_base_metrics, "y_pred": ridge_base_pred},
        "Ridge (tuned)": {"model": ridge_tuned, "metrics": ridge_tuned_metrics,
                           "y_pred": ridge_tuned_pred, "best_params": grid.best_params_},
    }
    return results, (X_train, X_test, y_train, y_test)
