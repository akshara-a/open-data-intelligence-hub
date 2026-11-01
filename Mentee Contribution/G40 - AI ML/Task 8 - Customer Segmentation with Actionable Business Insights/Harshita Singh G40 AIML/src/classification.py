"""
Classification utilities: predicting PurchaseLikelihood using
Logistic Regression, with GridSearchCV tuning.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)


def get_classification_metrics(y_true, y_pred, y_proba):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1": f1_score(y_true, y_pred),
        "ROC_AUC": roc_auc_score(y_true, y_proba),
    }


def run_classification_pipeline(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Baseline Logistic Regression
    base = LogisticRegression(max_iter=1000, random_state=random_state)
    base.fit(X_train, y_train)
    base_pred = base.predict(X_test)
    base_proba = base.predict_proba(X_test)[:, 1]
    base_metrics = get_classification_metrics(y_test, base_pred, base_proba)

    # Tuned via GridSearchCV
    param_grid = {
        "C": [0.01, 0.1, 1, 10, 100],
        "penalty": ["l2"],
        "solver": ["lbfgs"],
    }
    grid = GridSearchCV(
        LogisticRegression(max_iter=1000, random_state=random_state),
        param_grid, cv=5, scoring="f1"
    )
    grid.fit(X_train, y_train)
    tuned = grid.best_estimator_
    tuned_pred = tuned.predict(X_test)
    tuned_proba = tuned.predict_proba(X_test)[:, 1]
    tuned_metrics = get_classification_metrics(y_test, tuned_pred, tuned_proba)

    results = {
        "Logistic Regression (baseline)": {
            "model": base, "metrics": base_metrics,
            "y_pred": base_pred, "y_proba": base_proba,
            "confusion_matrix": confusion_matrix(y_test, base_pred),
        },
        "Logistic Regression (tuned)": {
            "model": tuned, "metrics": tuned_metrics,
            "y_pred": tuned_pred, "y_proba": tuned_proba,
            "confusion_matrix": confusion_matrix(y_test, tuned_pred),
            "best_params": grid.best_params_,
        },
    }
    return results, (X_train, X_test, y_train, y_test)
