"""
Regression Model Module — Part A
==================================
Implements Linear Regression and Ridge Regression to predict
product ratings based on customer and product features.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import warnings
warnings.filterwarnings("ignore")


def train_linear_regression(X_train, y_train, X_test, y_test):
    """Train a Linear Regression model and return predictions + metrics."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2_Score": r2_score(y_test, y_pred),
    }

    return model, y_pred, metrics


def train_ridge_regression(X_train, y_train, X_test, y_test, alpha=1.0):
    """Train a Ridge Regression model and return predictions + metrics."""
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2_Score": r2_score(y_test, y_pred),
    }

    return model, y_pred, metrics


def plot_regression_results(y_test, y_pred_linear, y_pred_ridge,
                             metrics_linear, metrics_ridge,
                             feature_names, model_linear, model_ridge,
                             output_dir="outputs/plots"):
    """Generate and save regression evaluation plots."""
    os.makedirs(output_dir, exist_ok=True)

    # --- 1. Actual vs Predicted (both models) ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].scatter(y_test, y_pred_linear, alpha=0.4, color="#4C72B0", s=20)
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                 "r--", linewidth=2)
    axes[0].set_xlabel("Actual Rating", fontsize=12)
    axes[0].set_ylabel("Predicted Rating", fontsize=12)
    axes[0].set_title(f"Linear Regression\nR² = {metrics_linear['R2_Score']:.4f}",
                       fontsize=13, fontweight="bold")

    axes[1].scatter(y_test, y_pred_ridge, alpha=0.4, color="#55A868", s=20)
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                 "r--", linewidth=2)
    axes[1].set_xlabel("Actual Rating", fontsize=12)
    axes[1].set_ylabel("Predicted Rating", fontsize=12)
    axes[1].set_title(f"Ridge Regression\nR² = {metrics_ridge['R2_Score']:.4f}",
                       fontsize=13, fontweight="bold")

    plt.suptitle("Actual vs Predicted Ratings", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regression_actual_vs_predicted.png"),
                dpi=150, bbox_inches="tight")
    plt.close()

    # --- 2. Residual Distribution ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    residuals_linear = y_test - y_pred_linear
    residuals_ridge = y_test - y_pred_ridge

    axes[0].hist(residuals_linear, bins=30, color="#4C72B0", edgecolor="white", alpha=0.85)
    axes[0].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[0].set_xlabel("Residual", fontsize=12)
    axes[0].set_ylabel("Frequency", fontsize=12)
    axes[0].set_title("Linear Regression Residuals", fontsize=13, fontweight="bold")

    axes[1].hist(residuals_ridge, bins=30, color="#55A868", edgecolor="white", alpha=0.85)
    axes[1].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[1].set_xlabel("Residual", fontsize=12)
    axes[1].set_ylabel("Frequency", fontsize=12)
    axes[1].set_title("Ridge Regression Residuals", fontsize=13, fontweight="bold")

    plt.suptitle("Residual Distribution", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regression_residuals.png"),
                dpi=150, bbox_inches="tight")
    plt.close()

    # --- 3. Feature Importance (Coefficients) ---
    fig, ax = plt.subplots(figsize=(10, 6))
    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Linear": model_linear.coef_,
        "Ridge": model_ridge.coef_,
    })
    x = np.arange(len(feature_names))
    width = 0.35
    ax.bar(x - width / 2, coef_df["Linear"], width, label="Linear Regression",
           color="#4C72B0", edgecolor="white")
    ax.bar(x + width / 2, coef_df["Ridge"], width, label="Ridge Regression",
           color="#55A868", edgecolor="white")
    ax.set_xlabel("Feature", fontsize=12)
    ax.set_ylabel("Coefficient Value", fontsize=12)
    ax.set_title("Feature Coefficients Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(feature_names, rotation=45, ha="right")
    ax.legend(fontsize=11)
    ax.axhline(0, color="gray", linestyle="-", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regression_coefficients.png"), dpi=150)
    plt.close()

    print("[Regression] Saved: regression_actual_vs_predicted.png")
    print("[Regression] Saved: regression_residuals.png")
    print("[Regression] Saved: regression_coefficients.png")


def run_regression(reg_data, output_dir="outputs/plots"):
    """
    Run the complete regression pipeline.

    Parameters
    ----------
    reg_data : dict
        Preprocessed regression data from data_preprocessing.
    output_dir : str
        Directory to save plots.

    Returns
    -------
    dict
        Dictionary containing models, predictions, and metrics.
    """
    print("\n" + "=" * 60)
    print("PART A: REGRESSION — RATING PREDICTION")
    print("=" * 60)

    X_train_scaled = reg_data["X_train_scaled"]
    X_test_scaled = reg_data["X_test_scaled"]
    y_train = reg_data["y_train"]
    y_test = reg_data["y_test"]
    feature_names = reg_data["feature_names"]

    # Train models
    model_lr, y_pred_lr, metrics_lr = train_linear_regression(
        X_train_scaled, y_train, X_test_scaled, y_test
    )
    model_ridge, y_pred_ridge, metrics_ridge = train_ridge_regression(
        X_train_scaled, y_train, X_test_scaled, y_test, alpha=1.0
    )

    # Print metrics
    print("\n--- Linear Regression Metrics ---")
    for k, v in metrics_lr.items():
        print(f"  {k}: {v:.4f}")

    print("\n--- Ridge Regression Metrics ---")
    for k, v in metrics_ridge.items():
        print(f"  {k}: {v:.4f}")

    # Comparison
    print("\n--- Model Comparison ---")
    comparison = pd.DataFrame({
        "Metric": list(metrics_lr.keys()),
        "Linear Regression": list(metrics_lr.values()),
        "Ridge Regression": list(metrics_ridge.values()),
    })
    print(comparison.to_string(index=False))

    # Example prediction
    sample_pred = y_pred_ridge[:5]
    sample_actual = y_test.values[:5]
    print("\n--- Sample Predictions (Ridge) ---")
    for i in range(5):
        print(f"  Actual: {sample_actual[i]:.1f} -> Predicted: {sample_pred[i]:.2f}")

    # Plot results
    plot_regression_results(
        y_test, y_pred_lr, y_pred_ridge,
        metrics_lr, metrics_ridge,
        feature_names, model_lr, model_ridge,
        output_dir
    )

    return {
        "linear": {"model": model_lr, "predictions": y_pred_lr, "metrics": metrics_lr},
        "ridge": {"model": model_ridge, "predictions": y_pred_ridge, "metrics": metrics_ridge},
        "comparison": comparison,
    }


if __name__ == "__main__":
    from data_preprocessing import preprocess_all
    data = preprocess_all("data/ecommerce_data.csv")
    run_regression(data["regression"])
