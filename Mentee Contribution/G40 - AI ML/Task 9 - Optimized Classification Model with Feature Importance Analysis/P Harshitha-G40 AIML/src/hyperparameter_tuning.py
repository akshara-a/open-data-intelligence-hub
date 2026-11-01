import os
# pyrefly: ignore [missing-import]
import matplotlib
matplotlib.use('Agg')
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from sklearn.model_selection import GridSearchCV

def optimize_random_forest(pipeline, X_train, y_train, scoring="f1", cv=5):
    param_grid = {
        "classifier__n_estimators": [100, 200, 300],
        "classifier__max_depth": [None, 5, 10, 15],
        "classifier__min_samples_split": [2, 5, 10],
        "classifier__min_samples_leaf": [1, 2, 4],
        "classifier__class_weight": [None, "balanced"]
    }
    
    print("[Hyperparameter Tuning] Initiating GridSearchCV for Random Forest...")
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        n_jobs=-1,
        verbose=0
    )
    grid_search.fit(X_train, y_train)
    print(f"[Hyperparameter Tuning] Best Parameters: {grid_search.best_params_}")
    print(f"[Hyperparameter Tuning] Best CV Score ({scoring}): {grid_search.best_score_:.4f}")
    return grid_search

def optimize_decision_tree(pipeline, X_train, y_train, scoring="f1", cv=5):
    param_grid = {
        "classifier__max_depth": [3, 5, 8, 12, None],
        "classifier__min_samples_split": [2, 5, 10],
        "classifier__min_samples_leaf": [1, 2, 4],
        "classifier__criterion": ["gini", "entropy"],
        "classifier__class_weight": [None, "balanced"]
    }
    
    print("[Hyperparameter Tuning] Initiating GridSearchCV for Decision Tree...")
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        n_jobs=-1,
        verbose=0
    )
    grid_search.fit(X_train, y_train)
    print(f"[Hyperparameter Tuning] Best Parameters: {grid_search.best_params_}")
    print(f"[Hyperparameter Tuning] Best CV Score ({scoring}): {grid_search.best_score_:.4f}")
    return grid_search

def analyze_sensitivity(grid_search, param_name="classifier__max_depth", output_path=None):
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    plt.figure(figsize=(8, 5))
    if param_name in results_df.columns:
        sns.boxplot(data=results_df, x=param_name, y="mean_test_score", palette="Blues")
        plt.title(f"Hyperparameter Sensitivity Analysis ({param_name})", fontsize=12, pad=15)
        plt.xlabel(param_name.replace("classifier__", ""))
        plt.ylabel("Mean CV Score (F1)")
        plt.tight_layout()
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, dpi=300)
        plt.close('all')
    return results_df
