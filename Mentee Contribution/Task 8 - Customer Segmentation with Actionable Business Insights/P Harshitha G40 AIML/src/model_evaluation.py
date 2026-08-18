"""
Model Evaluation Module
========================
Provides reusable evaluation functions for regression and classification models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)


def evaluate_regression(y_true, y_pred, model_name="Regression Model"):
    """
    Evaluate a regression model and return metrics as a dictionary.
    Metrics: MAE, MSE, RMSE, R² Score
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    metrics = {
        'Model': model_name,
        'MAE': round(mae, 4),
        'MSE': round(mse, 4),
        'RMSE': round(rmse, 4),
        'R2_Score': round(r2, 4)
    }

    print(f"\n--- {model_name} - Regression Metrics ---")
    print(f"  Mean Absolute Error (MAE)  : {mae:,.4f}")
    print(f"  Mean Squared Error (MSE)   : {mse:,.4f}")
    print(f"  Root Mean Squared Error    : {rmse:,.4f}")
    print(f"  R² Score                   : {r2:.4f}")

    return metrics


def evaluate_classification(y_true, y_pred, y_prob=None, model_name="Classification Model"):
    """
    Evaluate a classification model and return metrics as a dictionary.
    Metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    metrics = {
        'Model': model_name,
        'Accuracy': round(acc, 4),
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1_Score': round(f1, 4),
    }

    print(f"\n--- {model_name} - Classification Metrics ---")
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-Score  : {f1:.4f}")

    if y_prob is not None:
        try:
            roc_auc = roc_auc_score(y_true, y_prob)
            metrics['ROC_AUC'] = round(roc_auc, 4)
            print(f"  ROC-AUC   : {roc_auc:.4f}")
        except ValueError:
            print("  ROC-AUC   : Could not compute (single class in y_true)")

    print(f"\n  Classification Report:\n")
    print(classification_report(y_true, y_pred, zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    print(f"  Confusion Matrix:\n{cm}")

    return metrics


def compare_models(metrics_list):
    """
    Compare multiple models side by side.
    Takes a list of metric dictionaries and returns a DataFrame.
    """
    df_comparison = pd.DataFrame(metrics_list)
    print("\n--- Model Comparison ---")
    print(df_comparison.to_string(index=False))
    return df_comparison


if __name__ == "__main__":
    # Quick test with dummy data
    np.random.seed(42)
    y_true_reg = np.random.rand(100) * 100
    y_pred_reg = y_true_reg + np.random.randn(100) * 10
    evaluate_regression(y_true_reg, y_pred_reg, "Test Regression")

    y_true_cls = np.random.randint(0, 2, 100)
    y_pred_cls = np.random.randint(0, 2, 100)
    evaluate_classification(y_true_cls, y_pred_cls, model_name="Test Classification")
