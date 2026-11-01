import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix


def prepare_classification_data(customer_df: pd.DataFrame, cluster_labels: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
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
    features_df["Cluster"] = cluster_labels.astype(int).values
    target = customer_df["PurchaseLikelihood"]
    return features_df, target


def fit_classification_model(features: pd.DataFrame, target: pd.Series) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)

    numeric_features = ["Age", "AnnualIncome", "PurchaseFrequency", "AverageOrderValue", "DaysSinceLastPurchase", "WebsiteVisits", "DiscountUsage", "CustomerRating", "Cluster"]
    categorical_features = ["Gender", "ProductCategory"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=500))
    ])

    param_grid = {
        "classifier__C": [0.1, 0.5, 1.0, 2.0],
        "classifier__solver": ["liblinear", "lbfgs"],
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1")
    grid_search.fit(X_train, y_train)
    predictions = grid_search.best_estimator_.predict(X_test)

    metrics = {
        "Accuracy": round(accuracy_score(y_test, predictions), 3),
        "Precision": round(precision_score(y_test, predictions), 3),
        "Recall": round(recall_score(y_test, predictions), 3),
        "F1": round(f1_score(y_test, predictions), 3),
        "ROC_AUC": round(roc_auc_score(y_test, grid_search.best_estimator_.predict_proba(X_test)[:, 1]), 3),
        "ConfusionMatrix": confusion_matrix(y_test, predictions),
    }

    return {"model": grid_search.best_estimator_, "metrics": metrics, "best_params": grid_search.best_params_}
