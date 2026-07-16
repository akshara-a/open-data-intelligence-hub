"""
Classification Model Module — Part B
======================================
Implements Logistic Regression to predict whether a customer
will purchase a product based on browsing and product features.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
import os
import warnings
warnings.filterwarnings("ignore")


def train_logistic_regression(X_train, y_train, X_test, y_test,
                                C=1.0, penalty="l2", solver="lbfgs", max_iter=1000):
    """Train a Logistic Regression model and return predictions + metrics."""
    model = LogisticRegression(C=C, penalty=penalty, solver=solver,
                                max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1_Score": f1_score(y_test, y_pred),
        "ROC_AUC": roc_auc_score(y_test, y_prob),
    }

    return model, y_pred, y_prob, metrics


def plot_classification_results(y_test, y_pred, y_prob, metrics,
                                 feature_names, model,
                                 output_dir="outputs/plots"):
    """Generate and save classification evaluation plots."""
    os.makedirs(output_dir, exist_ok=True)

    # --- 1. Confusion Matrix ---
    fig, ax = plt.subplots(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Not Purchased", "Purchased"],
                yticklabels=["Not Purchased", "Purchased"],
                linewidths=1, linecolor="white")
    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("Actual", fontsize=12)
    ax.set_title("Confusion Matrix — Purchase Prediction", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classification_confusion_matrix.png"), dpi=150)
    plt.close()

    # --- 2. ROC Curve ---
    fig, ax = plt.subplots(figsize=(8, 6))
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    ax.plot(fpr, tpr, color="#4C72B0", linewidth=2.5,
            label=f'Logistic Regression (AUC = {metrics["ROC_AUC"]:.4f})')
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.7, label="Random Classifier")
    ax.fill_between(fpr, tpr, alpha=0.15, color="#4C72B0")
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curve — Purchase Prediction", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11, loc="lower right")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classification_roc_curve.png"), dpi=150)
    plt.close()

    # --- 3. Feature Importance (Coefficients) ---
    fig, ax = plt.subplots(figsize=(10, 6))
    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": model.coef_[0],
    }).sort_values("Coefficient", ascending=True)

    colors = ["#C44E52" if c < 0 else "#55A868" for c in coef_df["Coefficient"]]
    ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="white")
    ax.set_xlabel("Coefficient Value", fontsize=12)
    ax.set_title("Feature Importance — Logistic Regression", fontsize=14, fontweight="bold")
    ax.axvline(0, color="gray", linestyle="-", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classification_feature_importance.png"), dpi=150)
    plt.close()

    # --- 4. Prediction Probability Distribution ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(y_prob[y_test == 0], bins=30, alpha=0.7, color="#DD8452",
            label="Not Purchased", edgecolor="white")
    ax.hist(y_prob[y_test == 1], bins=30, alpha=0.7, color="#55A868",
            label="Purchased", edgecolor="white")
    ax.axvline(0.5, color="red", linestyle="--", linewidth=2, label="Threshold (0.5)")
    ax.set_xlabel("Predicted Probability", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Prediction Probability Distribution", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classification_probability_dist.png"), dpi=150)
    plt.close()

    print("[Classification] Saved: classification_confusion_matrix.png")
    print("[Classification] Saved: classification_roc_curve.png")
    print("[Classification] Saved: classification_feature_importance.png")
    print("[Classification] Saved: classification_probability_dist.png")


def run_classification(clf_data, output_dir="outputs/plots"):
    """
    Run the complete classification pipeline.

    Parameters
    ----------
    clf_data : dict
        Preprocessed classification data from data_preprocessing.
    output_dir : str
        Directory to save plots.

    Returns
    -------
    dict
        Dictionary containing model, predictions, probabilities, and metrics.
    """
    print("\n" + "=" * 60)
    print("PART B: CLASSIFICATION — PURCHASE PREDICTION")
    print("=" * 60)

    X_train_scaled = clf_data["X_train_scaled"]
    X_test_scaled = clf_data["X_test_scaled"]
    y_train = clf_data["y_train"]
    y_test = clf_data["y_test"]
    feature_names = clf_data["feature_names"]

    # Train model
    model, y_pred, y_prob, metrics = train_logistic_regression(
        X_train_scaled, y_train, X_test_scaled, y_test
    )

    # Print metrics
    print("\n--- Logistic Regression Metrics ---")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")

    # Classification report
    print("\n--- Detailed Classification Report ---")
    print(classification_report(y_test, y_pred,
                                 target_names=["Not Purchased", "Purchased"]))

    # Sample predictions
    print("--- Sample Predictions ---")
    for i in range(5):
        status = "Yes" if y_pred[i] == 1 else "No"
        print(f"  Purchase Likelihood: {status} | Probability: {y_prob[i]:.0%}")

    # Plot results
    plot_classification_results(
        y_test, y_pred, y_prob, metrics,
        feature_names, model, output_dir
    )

    return {
        "model": model,
        "predictions": y_pred,
        "probabilities": y_prob,
        "metrics": metrics,
    }


if __name__ == "__main__":
    from data_preprocessing import preprocess_all
    data = preprocess_all("data/ecommerce_data.csv")
    run_classification(data["classification"])
