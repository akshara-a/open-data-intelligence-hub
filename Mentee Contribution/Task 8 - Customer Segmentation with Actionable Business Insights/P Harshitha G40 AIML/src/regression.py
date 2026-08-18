"""
Regression Module
==================
Predicts TotalSpending using Linear Regression and Ridge Regression.
Compares both models and saves predictions and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

from . import model_evaluation


def prepare_regression_data(df):
    """
    Prepare features and target for regression.
    Target: TotalSpending (continuous)
    Features: all numeric columns except TotalSpending and CustomerID
    """
    df_prep = df.copy()

    # Encode Gender if needed
    if 'Gender' in df_prep.columns and 'Gender_Encoded' not in df_prep.columns:
        le = LabelEncoder()
        df_prep['Gender_Encoded'] = le.fit_transform(df_prep['Gender'])

    # One-hot encode ProductCategory if needed
    if 'ProductCategory' in df_prep.columns:
        cat_cols = [c for c in df_prep.columns if c.startswith('Category_')]
        if not cat_cols:
            dummies = pd.get_dummies(df_prep['ProductCategory'], prefix='Category', dtype=int)
            df_prep = pd.concat([df_prep, dummies], axis=1)

    # Define target
    target_col = 'TotalSpending'

    # Exclude non-feature columns
    exclude_cols = ['CustomerID', 'TotalSpending', 'Gender', 'ProductCategory']
    if 'Cluster' in df_prep.columns:
        exclude_cols.append('Cluster')

    feature_cols = [c for c in df_prep.columns
                    if c not in exclude_cols
                    and df_prep[c].dtype in [np.float64, np.int64,
                                              np.float32, np.int32, np.uint8]]

    X = df_prep[feature_cols]
    y = df_prep[target_col]

    print(f"Regression target: {target_col}")
    print(f"Regression features ({len(feature_cols)}): {feature_cols}")
    print(f"Target stats: Mean={y.mean():,.2f}, Std={y.std():,.2f}, "
          f"Min={y.min()}, Max={y.max()}")

    return X, y, feature_cols


def train_regression(X, y, test_size=0.2, random_state=42):
    """
    Train Linear Regression and Ridge Regression models.
    Returns both fitted models and test split.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set : {X_test.shape[0]} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # --- Linear Regression ---
    print("\n--- Linear Regression ---")
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr = lr_model.predict(X_test_scaled)

    # --- Ridge Regression ---
    print("\n--- Ridge Regression (alpha=1.0) ---")
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train_scaled, y_train)
    y_pred_ridge = ridge_model.predict(X_test_scaled)

    return (lr_model, ridge_model, scaler,
            X_train, X_test, y_train, y_test,
            y_pred_lr, y_pred_ridge)


def plot_regression_results(y_test, y_pred_lr, y_pred_ridge, save_path=None):
    """Plot Actual vs Predicted scatter plots for both regression models."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    for ax, y_pred, title, color in zip(
        axes,
        [y_pred_lr, y_pred_ridge],
        ['Linear Regression', 'Ridge Regression'],
        ['#2196F3', '#E91E63']
    ):
        ax.scatter(y_test, y_pred, alpha=0.5, color=color, s=40, edgecolors='w', linewidth=0.3)

        # Perfect prediction line
        all_vals = np.concatenate([y_test, y_pred])
        min_val, max_val = all_vals.min(), all_vals.max()
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, label='Perfect Fit')

        ax.set_title(f'{title} - Actual vs Predicted', fontweight='bold')
        ax.set_xlabel('Actual Total Spending')
        ax.set_ylabel('Predicted Total Spending')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.suptitle('Regression Results: Actual vs Predicted Spending', fontweight='bold', fontsize=14)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.close(fig)


def run_regression(df, images_dir, outputs_dir):
    """
    Run the full regression pipeline.
    Returns models, metrics comparison, and predictions.
    """
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("REGRESSION - TOTAL SPENDING PREDICTION")
    print("=" * 60)

    # Prepare data
    X, y, feature_cols = prepare_regression_data(df)

    # Train models
    (lr_model, ridge_model, scaler,
     X_train, X_test, y_train, y_test,
     y_pred_lr, y_pred_ridge) = train_regression(X, y)

    # Evaluate both models
    metrics_lr = model_evaluation.evaluate_regression(
        y_test, y_pred_lr, model_name="Linear Regression"
    )
    metrics_ridge = model_evaluation.evaluate_regression(
        y_test, y_pred_ridge, model_name="Ridge Regression"
    )

    # Compare
    comparison = model_evaluation.compare_models([metrics_lr, metrics_ridge])

    # Determine best model
    best_name = (
        "Linear Regression"
        if metrics_lr['R2_Score'] >= metrics_ridge['R2_Score']
        else "Ridge Regression"
    )
    best_pred = y_pred_lr if best_name == "Linear Regression" else y_pred_ridge
    print(f"\n  Selected Model: {best_name}")

    # Plot results
    plot_regression_results(
        y_test, y_pred_lr, y_pred_ridge,
        save_path=os.path.join(images_dir, 'regression_results.png')
    )

    # Save predictions
    pred_df = pd.DataFrame({
        'Actual_TotalSpending': y_test.values,
        'LinearRegression_Predicted': y_pred_lr.round(2),
        'Ridge_Predicted': y_pred_ridge.round(2)
    })
    pred_df.to_csv(os.path.join(outputs_dir, 'regression_predictions.csv'), index=False)
    print(f"Saved: {os.path.join(outputs_dir, 'regression_predictions.csv')}")

    print("\nRegression complete!")
    return lr_model, ridge_model, comparison, pred_df


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "customer_data.csv")
    images_dir = os.path.join(base_dir, "images")
    outputs_dir = os.path.join(base_dir, "outputs")
    df = pd.read_csv(data_path)
    run_regression(df, images_dir, outputs_dir)
