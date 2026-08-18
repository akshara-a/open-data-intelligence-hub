import os
# pyrefly: ignore [missing-import]
import joblib
import warnings
# pyrefly: ignore [missing-import]
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

warnings.filterwarnings("ignore")


def train_logistic_regression(X_train, y_train, X_test, y_test):
    """
    Train a Logistic Regression model, perform GridSearchCV,
    evaluate performance, and save the best model.
    """

    print("=" * 60)
    print("Training Logistic Regression Model")
    print("=" * 60)

    # -----------------------------
    # Base Model
    # -----------------------------
    base_model = LogisticRegression(
        random_state=42,
        max_iter=500
    )

    base_model.fit(X_train, y_train)

    y_pred_base = base_model.predict(X_test)

    acc_base = accuracy_score(y_test, y_pred_base)
    prec_base = precision_score(y_test, y_pred_base, zero_division=0)
    rec_base = recall_score(y_test, y_pred_base, zero_division=0)
    f1_base = f1_score(y_test, y_pred_base, zero_division=0)
    cm_base = confusion_matrix(y_test, y_pred_base)

    print("\nBase Logistic Regression Performance")
    print("------------------------------------")
    print(f"Accuracy : {acc_base:.4f}")
    print(f"Precision: {prec_base:.4f}")
    print(f"Recall   : {rec_base:.4f}")
    print(f"F1 Score : {f1_base:.4f}")
    print("\nConfusion Matrix:")
    print(cm_base)

    # -----------------------------
    # Hyperparameter Grid
    # -----------------------------
    param_grid = {
        "C": [0.01, 0.1, 1, 10],
        "solver": ["liblinear", "lbfgs"],
        "max_iter": [100, 200, 500]
    }

    # -----------------------------
    # Grid Search
    # -----------------------------
    grid_search = GridSearchCV(
        estimator=LogisticRegression(random_state=42),
        param_grid=param_grid,
        scoring="f1",
        cv=5,
        n_jobs=-1,
        verbose=1,
        refit=True
    )

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    print("\nBest Hyperparameters")
    print("--------------------")
    print(best_params)

    # -----------------------------
    # Evaluate Tuned Model
    # -----------------------------
    y_pred_best = best_model.predict(X_test)

    acc_best = accuracy_score(y_test, y_pred_best)
    prec_best = precision_score(y_test, y_pred_best, zero_division=0)
    rec_best = recall_score(y_test, y_pred_best, zero_division=0)
    f1_best = f1_score(y_test, y_pred_best, zero_division=0)
    cm_best = confusion_matrix(y_test, y_pred_best)

    print("\nTuned Logistic Regression Performance")
    print("-------------------------------------")
    print(f"Accuracy : {acc_best:.4f}")
    print(f"Precision: {prec_best:.4f}")
    print(f"Recall   : {rec_best:.4f}")
    print(f"F1 Score : {f1_best:.4f}")
    print("\nConfusion Matrix:")
    print(cm_best)

    # -----------------------------
    # Save Model
    # -----------------------------
    os.makedirs("outputs", exist_ok=True)

    model_path = os.path.join("outputs", "logistic_model.pkl")
    joblib.dump(best_model, model_path)

    print(f"\nModel saved successfully to: {model_path}")

    # -----------------------------
    # Results Dictionary
    # -----------------------------
    results = {
        "base": {
            "accuracy": acc_base,
            "precision": prec_base,
            "recall": rec_base,
            "f1": f1_base,
            "confusion_matrix": cm_base
        },
        "tuned": {
            "accuracy": acc_best,
            "precision": prec_best,
            "recall": rec_best,
            "f1": f1_best,
            "confusion_matrix": cm_best
        },
        "best_params": best_params,
        "predictions": y_pred_best
    }

    return best_model, results