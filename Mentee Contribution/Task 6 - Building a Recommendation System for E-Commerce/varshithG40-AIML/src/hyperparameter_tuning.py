"""
Hyperparameter Tuning Module — Part D
=======================================
Tunes model parameters using GridSearchCV and RandomizedSearchCV
to improve model performance across all three model types.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, silhouette_score, make_scorer
)
import os
import warnings
warnings.filterwarnings("ignore")


def tune_ridge_regression(X_train, y_train, X_test, y_test):
    """
    Tune Ridge Regression alpha using GridSearchCV.

    Returns
    -------
    dict
        Best parameters, best model, and before/after metrics.
    """
    print("\n--- Tuning Ridge Regression ---")

    param_grid = {
        "alpha": [0.001, 0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
    }

    grid_search = GridSearchCV(
        Ridge(), param_grid, cv=5,
        scoring="neg_mean_squared_error",
        n_jobs=-1, return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    # Before tuning (default alpha=1.0)
    default_model = Ridge(alpha=1.0)
    default_model.fit(X_train, y_train)
    y_pred_default = default_model.predict(X_test)

    before_metrics = {
        "MAE": mean_absolute_error(y_test, y_pred_default),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred_default)),
        "R2_Score": r2_score(y_test, y_pred_default),
    }

    after_metrics = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2_Score": r2_score(y_test, y_pred),
    }

    print(f"  Best Parameters: {grid_search.best_params_}")
    print(f"  Best CV Score (neg MSE): {grid_search.best_score_:.4f}")
    print(f"  Before Tuning — MAE: {before_metrics['MAE']:.4f}, R²: {before_metrics['R2_Score']:.4f}")
    print(f"  After Tuning  — MAE: {after_metrics['MAE']:.4f}, R²: {after_metrics['R2_Score']:.4f}")

    # CV Results for plotting
    cv_results = pd.DataFrame(grid_search.cv_results_)

    return {
        "best_params": grid_search.best_params_,
        "best_model": best_model,
        "before_metrics": before_metrics,
        "after_metrics": after_metrics,
        "cv_results": cv_results,
    }


def tune_logistic_regression(X_train, y_train, X_test, y_test):
    """
    Tune Logistic Regression using GridSearchCV.

    Returns
    -------
    dict
        Best parameters, best model, and before/after metrics.
    """
    print("\n--- Tuning Logistic Regression ---")

    param_grid = {
        "C": [0.01, 0.1, 1.0, 10.0],
        "penalty": ["l1", "l2"],
        "solver": ["liblinear", "saga"],
        "max_iter": [500, 1000],
    }

    grid_search = GridSearchCV(
        LogisticRegression(random_state=42), param_grid, cv=5,
        scoring="f1", n_jobs=-1, return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    # Before tuning (defaults)
    default_model = LogisticRegression(random_state=42, max_iter=1000)
    default_model.fit(X_train, y_train)
    y_pred_default = default_model.predict(X_test)
    y_prob_default = default_model.predict_proba(X_test)[:, 1]

    before_metrics = {
        "Accuracy": accuracy_score(y_test, y_pred_default),
        "F1_Score": f1_score(y_test, y_pred_default),
        "ROC_AUC": roc_auc_score(y_test, y_prob_default),
    }

    after_metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1_Score": f1_score(y_test, y_pred),
        "ROC_AUC": roc_auc_score(y_test, y_prob),
    }

    print(f"  Best Parameters: {grid_search.best_params_}")
    print(f"  Best CV Score (F1): {grid_search.best_score_:.4f}")
    print(f"  Before Tuning — Accuracy: {before_metrics['Accuracy']:.4f}, F1: {before_metrics['F1_Score']:.4f}")
    print(f"  After Tuning  — Accuracy: {after_metrics['Accuracy']:.4f}, F1: {after_metrics['F1_Score']:.4f}")

    return {
        "best_params": grid_search.best_params_,
        "best_model": best_model,
        "before_metrics": before_metrics,
        "after_metrics": after_metrics,
    }


def tune_kmeans(X_scaled, k_range=range(2, 11)):
    """
    Tune K-Means using Elbow Method and Silhouette Analysis.

    Returns
    -------
    dict
        Best number of clusters and evaluation results.
    """
    print("\n--- Tuning K-Means Clustering ---")

    results = []
    for k in k_range:
        for init_method in ["k-means++", "random"]:
            kmeans = KMeans(n_clusters=k, init=init_method, n_init=10,
                            max_iter=300, random_state=42)
            labels = kmeans.fit_predict(X_scaled)
            sil_score = silhouette_score(X_scaled, labels)
            results.append({
                "n_clusters": k,
                "init": init_method,
                "inertia": kmeans.inertia_,
                "silhouette": sil_score,
            })

    results_df = pd.DataFrame(results)

    # Best configuration
    best_idx = results_df["silhouette"].idxmax()
    best_config = results_df.loc[best_idx]

    print(f"  Best Configuration:")
    print(f"    n_clusters: {int(best_config['n_clusters'])}")
    print(f"    init: {best_config['init']}")
    print(f"    Silhouette Score: {best_config['silhouette']:.4f}")
    print(f"    Inertia: {best_config['inertia']:.2f}")

    return {
        "best_config": best_config.to_dict(),
        "results_df": results_df,
    }


def plot_tuning_results(ridge_results, logreg_results, kmeans_results,
                         output_dir="outputs/plots"):
    """Generate and save hyperparameter tuning comparison plots."""
    os.makedirs(output_dir, exist_ok=True)

    # --- 1. Before/After Comparison ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Ridge
    ridge_metrics = ["MAE", "RMSE", "R2_Score"]
    before_vals = [ridge_results["before_metrics"][m] for m in ridge_metrics]
    after_vals = [ridge_results["after_metrics"][m] for m in ridge_metrics]
    x = np.arange(len(ridge_metrics))
    width = 0.35
    axes[0].bar(x - width / 2, before_vals, width, label="Before", color="#DD8452", edgecolor="white")
    axes[0].bar(x + width / 2, after_vals, width, label="After", color="#55A868", edgecolor="white")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(ridge_metrics)
    axes[0].set_title("Ridge Regression Tuning", fontsize=13, fontweight="bold")
    axes[0].legend(fontsize=11)
    axes[0].set_ylabel("Score", fontsize=12)

    # Logistic Regression
    logreg_metrics = ["Accuracy", "F1_Score", "ROC_AUC"]
    before_vals = [logreg_results["before_metrics"][m] for m in logreg_metrics]
    after_vals = [logreg_results["after_metrics"][m] for m in logreg_metrics]
    x = np.arange(len(logreg_metrics))
    axes[1].bar(x - width / 2, before_vals, width, label="Before", color="#DD8452", edgecolor="white")
    axes[1].bar(x + width / 2, after_vals, width, label="After", color="#55A868", edgecolor="white")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(logreg_metrics)
    axes[1].set_title("Logistic Regression Tuning", fontsize=13, fontweight="bold")
    axes[1].legend(fontsize=11)
    axes[1].set_ylabel("Score", fontsize=12)

    plt.suptitle("Hyperparameter Tuning: Before vs After", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "tuning_before_after.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # --- 2. K-Means Tuning Results ---
    results_df = kmeans_results["results_df"]
    fig, ax = plt.subplots(figsize=(10, 6))

    for init_method in ["k-means++", "random"]:
        subset = results_df[results_df["init"] == init_method]
        ax.plot(subset["n_clusters"], subset["silhouette"], "o-", linewidth=2,
                markersize=8, label=f"init={init_method}")

    ax.set_xlabel("Number of Clusters", fontsize=12)
    ax.set_ylabel("Silhouette Score", fontsize=12)
    ax.set_title("K-Means Tuning — Silhouette Score by Init Method", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "tuning_kmeans.png"), dpi=150)
    plt.close()

    print("[Tuning] Saved: tuning_before_after.png")
    print("[Tuning] Saved: tuning_kmeans.png")


def run_hyperparameter_tuning(preprocessed_data, output_dir="outputs/plots"):
    """
    Run the complete hyperparameter tuning pipeline.

    Parameters
    ----------
    preprocessed_data : dict
        All preprocessed data from data_preprocessing.
    output_dir : str
        Directory to save plots.

    Returns
    -------
    dict
        Tuning results for all models.
    """
    print("\n" + "=" * 60)
    print("PART D: HYPERPARAMETER OPTIMIZATION")
    print("=" * 60)

    reg_data = preprocessed_data["regression"]
    clf_data = preprocessed_data["classification"]
    clust_data = preprocessed_data["clustering"]

    # Tune Ridge Regression
    ridge_results = tune_ridge_regression(
        reg_data["X_train_scaled"], reg_data["y_train"],
        reg_data["X_test_scaled"], reg_data["y_test"]
    )

    # Tune Logistic Regression
    logreg_results = tune_logistic_regression(
        clf_data["X_train_scaled"], clf_data["y_train"],
        clf_data["X_test_scaled"], clf_data["y_test"]
    )

    # Tune K-Means
    kmeans_results = tune_kmeans(clust_data["X_scaled"])

    # Plot results
    plot_tuning_results(ridge_results, logreg_results, kmeans_results, output_dir)

    return {
        "ridge": ridge_results,
        "logistic": logreg_results,
        "kmeans": kmeans_results,
    }


if __name__ == "__main__":
    from data_preprocessing import preprocess_all
    data = preprocess_all("data/ecommerce_data.csv")
    run_hyperparameter_tuning(data)
