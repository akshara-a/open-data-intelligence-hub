"""Regression experiments: Linear Regression and Ridge Regression with CV."""
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


def run_regressions(X, y, preprocessor, out_dir="outputs/models"):
    # Transform features
    X_trans = preprocessor.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_trans, y, test_size=0.2, random_state=42)

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    preds_lr = lr.predict(X_test)
    lr_mse = mean_squared_error(y_test, preds_lr)
    lr_r2 = r2_score(y_test, preds_lr)

    # Ridge with GridSearch
    ridge = Ridge()
    param_grid = {"alpha": [0.1, 1.0, 10.0, 50.0]}
    grid = GridSearchCV(ridge, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid.fit(X_train, y_train)
    best_ridge = grid.best_estimator_
    preds_ridge = best_ridge.predict(X_test)
    ridge_mse = mean_squared_error(y_test, preds_ridge)
    ridge_r2 = r2_score(y_test, preds_ridge)

    results = {
        "linear": {"mse": lr_mse, "r2": lr_r2},
        "ridge": {"mse": ridge_mse, "r2": ridge_r2, "best_params": grid.best_params_},
    }
    return results, lr, best_ridge
