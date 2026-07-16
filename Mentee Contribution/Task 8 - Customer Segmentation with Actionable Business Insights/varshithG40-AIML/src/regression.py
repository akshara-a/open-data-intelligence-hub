import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def prepare_regression_data(customer_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    features_df = customer_df[[
        "Age",
        "AnnualIncome",
        "PurchaseFrequency",
        "AverageOrderValue",
        "DaysSinceLastPurchase",
        "WebsiteVisits",
        "DiscountUsage",
        "CustomerRating",
        "Gender",
        "ProductCategory",
    ]].copy()
    target = customer_df["TotalSpending"]
    return features_df, target


def fit_regression_models(features: pd.DataFrame, target: pd.Series) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)

    numeric_features = ["Age", "AnnualIncome", "PurchaseFrequency", "AverageOrderValue", "DaysSinceLastPurchase", "WebsiteVisits", "DiscountUsage", "CustomerRating"]
    categorical_features = ["Gender", "ProductCategory"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
        ]
    )

    baseline_model = Pipeline([("preprocessor", preprocessor), ("regressor", LinearRegression())])
    baseline_model.fit(X_train, y_train)
    baseline_pred = baseline_model.predict(X_test)

    param_grid = {"regressor__alpha": [0.1, 0.5, 1.0, 2.0, 5.0]}
    ridge_model = Pipeline([("preprocessor", preprocessor), ("regressor", Ridge())])
    grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring="neg_root_mean_squared_error")
    grid_search.fit(X_train, y_train)
    tuned_pred = grid_search.best_estimator_.predict(X_test)

    metrics = {
        "LinearRegression": evaluate_model(baseline_model, baseline_pred, y_test),
        "Ridge": evaluate_model(grid_search.best_estimator_, tuned_pred, y_test),
    }
    metrics["best_alpha"] = grid_search.best_params_["regressor__alpha"]
    return {"baseline": baseline_model, "tuned": grid_search.best_estimator_, "metrics": metrics}


def evaluate_model(model, predictions, target) -> dict:
    return {
        "MAE": round(mean_absolute_error(target, predictions), 2),
        "MSE": round(mean_squared_error(target, predictions), 2),
        "RMSE": round(np.sqrt(mean_squared_error(target, predictions)), 2),
        "R2": round(r2_score(target, predictions), 3),
    }
