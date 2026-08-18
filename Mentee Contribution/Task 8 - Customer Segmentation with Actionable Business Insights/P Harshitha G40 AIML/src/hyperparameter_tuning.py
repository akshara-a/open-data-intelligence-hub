"""
Hyperparameter Tuning Module
=============================
Optimizes Logistic Regression (classifier) and Ridge Regression (regressor)
using GridSearchCV. Compares baseline vs tuned model performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (f1_score, roc_auc_score,
                              mean_squared_error, r2_score)
import os


def _prepare_data(df, target_col, exclude_cols):
    """Helper to encode and extract features/target from the dataframe."""
    df_prep = df.copy()

    if 'Gender' in df_prep.columns and 'Gender_Encoded' not in df_prep.columns:
        le = LabelEncoder()
        df_prep['Gender_Encoded'] = le.fit_transform(df_prep['Gender'])

    if 'ProductCategory' in df_prep.columns:
        cat_cols = [c for c in df_prep.columns if c.startswith('Category_')]
        if not cat_cols:
            dummies = pd.get_dummies(df_prep['ProductCategory'], prefix='Category', dtype=int)
            df_prep = pd.concat([df_prep, dummies], axis=1)

    feature_cols = [c for c in df_prep.columns
                    if c not in exclude_cols
                    and df_prep[c].dtype in [np.float64, np.int64,
                                              np.float32, np.int32, np.uint8]]
    X = df_prep[feature_cols]
    y = df_prep[target_col]
    return X, y


def tune_logistic_regression(df, random_state=42):
    """
    Tune LogisticRegression hyperparameters using GridSearchCV.
    Compares baseline (default C=1) vs best tuned model.
    """
    print("\n" + "=" * 60)
    print("HYPERPARAMETER TUNING - Logistic Regression")
    print("=" * 60)

    exclude_cols = ['CustomerID', 'PurchaseLikelihood', 'Gender', 'ProductCategory']
    if 'Cluster' in df.columns:
        exclude_cols.append('Cluster')

    X, y = _prepare_data(df, 'PurchaseLikelihood', exclude_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # --- Baseline ---
    baseline = LogisticRegression(max_iter=1000, random_state=random_state)
    baseline.fit(X_train_s, y_train)
    y_pred_base = baseline.predict(X_test_s)
    y_prob_base = baseline.predict_proba(X_test_s)[:, 1]

    base_f1  = f1_score(y_test, y_pred_base, zero_division=0)
    base_auc = roc_auc_score(y_test, y_prob_base)
    print(f"\nBaseline Logistic Regression:")
    print(f"  F1-Score : {base_f1:.4f}")
    print(f"  ROC-AUC  : {base_auc:.4f}")

    # --- GridSearchCV ---
    # Note: 'penalty' param is deprecated in sklearn 1.8+; use C and solver only
    param_grid = {
        'C':        [0.01, 0.1, 1.0, 10.0, 100.0],
        'solver':   ['liblinear', 'lbfgs', 'saga'],
        'max_iter': [500, 1000]
    }

    n_combos = len(param_grid['C']) * len(param_grid['solver']) * len(param_grid['max_iter'])
    print(f"\nRunning GridSearchCV ({n_combos} combos)...")

    grid = GridSearchCV(
        LogisticRegression(random_state=random_state),
        param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=0
    )
    grid.fit(X_train_s, y_train)

    best_params = grid.best_params_
    best_model  = grid.best_estimator_
    y_pred_best = best_model.predict(X_test_s)
    y_prob_best = best_model.predict_proba(X_test_s)[:, 1]

    tuned_f1  = f1_score(y_test, y_pred_best, zero_division=0)
    tuned_auc = roc_auc_score(y_test, y_prob_best)

    print(f"\nBest Parameters: {best_params}")
    print(f"Tuned Logistic Regression:")
    print(f"  F1-Score : {tuned_f1:.4f}  (Baseline: {base_f1:.4f})")
    print(f"  ROC-AUC  : {tuned_auc:.4f}  (Baseline: {base_auc:.4f})")
    improvement_f1  = ((tuned_f1 - base_f1) / (base_f1 + 1e-9)) * 100
    improvement_auc = ((tuned_auc - base_auc) / (base_auc + 1e-9)) * 100
    print(f"  F1 Improvement  : {improvement_f1:+.2f}%")
    print(f"  AUC Improvement : {improvement_auc:+.2f}%")

    comparison = {
        'Model': ['Logistic Regression (Baseline)', 'Logistic Regression (Tuned)'],
        'F1_Score': [round(base_f1, 4),  round(tuned_f1, 4)],
        'ROC_AUC':  [round(base_auc, 4), round(tuned_auc, 4)],
        'Best_Params': [{'C': 1.0, 'penalty': 'l2', 'solver': 'lbfgs'}, best_params]
    }
    return pd.DataFrame(comparison), best_model, scaler


def tune_ridge_regression(df, random_state=42):
    """
    Tune Ridge Regression hyperparameter (alpha) using GridSearchCV.
    Compares baseline (alpha=1.0) vs best tuned model.
    """
    print("\n" + "=" * 60)
    print("HYPERPARAMETER TUNING - Ridge Regression")
    print("=" * 60)

    exclude_cols = ['CustomerID', 'TotalSpending', 'Gender', 'ProductCategory']
    if 'Cluster' in df.columns:
        exclude_cols.append('Cluster')

    X, y = _prepare_data(df, 'TotalSpending', exclude_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # --- Baseline ---
    baseline = Ridge(alpha=1.0)
    baseline.fit(X_train_s, y_train)
    y_pred_base = baseline.predict(X_test_s)
    base_rmse = np.sqrt(mean_squared_error(y_test, y_pred_base))
    base_r2   = r2_score(y_test, y_pred_base)

    print(f"\nBaseline Ridge Regression (alpha=1.0):")
    print(f"  RMSE : {base_rmse:,.4f}")
    print(f"  R²   : {base_r2:.4f}")

    # --- GridSearchCV ---
    alphas = [0.001, 0.01, 0.1, 1.0, 10.0, 50.0, 100.0, 500.0, 1000.0]
    param_grid = {'alpha': alphas}

    print(f"\nRunning GridSearchCV over {len(alphas)} alpha values...")
    grid = GridSearchCV(Ridge(), param_grid, cv=5,
                        scoring='neg_root_mean_squared_error', n_jobs=-1)
    grid.fit(X_train_s, y_train)

    best_alpha = grid.best_params_['alpha']
    best_model = grid.best_estimator_
    y_pred_best = best_model.predict(X_test_s)
    tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred_best))
    tuned_r2   = r2_score(y_test, y_pred_best)

    print(f"\nBest alpha: {best_alpha}")
    print(f"Tuned Ridge Regression:")
    print(f"  RMSE : {tuned_rmse:,.4f}  (Baseline: {base_rmse:,.4f})")
    print(f"  R²   : {tuned_r2:.4f}  (Baseline: {base_r2:.4f})")
    rmse_change = ((tuned_rmse - base_rmse) / (base_rmse + 1e-9)) * 100
    print(f"  RMSE Change : {rmse_change:+.2f}%")

    comparison = {
        'Model': ['Ridge Regression (Baseline)', 'Ridge Regression (Tuned)'],
        'RMSE':  [round(base_rmse, 4),  round(tuned_rmse, 4)],
        'R2_Score': [round(base_r2, 4), round(tuned_r2, 4)],
        'Alpha': [1.0, best_alpha]
    }
    return pd.DataFrame(comparison), best_model, scaler


def run_hyperparameter_tuning(df):
    """
    Run both hyperparameter tuning experiments and return comparison tables.
    """
    print("\n" + "=" * 60)
    print("HYPERPARAMETER TUNING")
    print("=" * 60)

    cls_comparison, best_cls, cls_scaler = tune_logistic_regression(df)
    reg_comparison, best_reg, reg_scaler = tune_ridge_regression(df)

    print("\n--- Full Comparison Table ---")
    print("\nClassification:")
    print(cls_comparison.to_string(index=False))
    print("\nRegression:")
    print(reg_comparison.to_string(index=False))

    return cls_comparison, reg_comparison, best_cls, best_reg


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "customer_data.csv")
    df = pd.read_csv(data_path)
    run_hyperparameter_tuning(df)
