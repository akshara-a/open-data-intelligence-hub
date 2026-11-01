"""
Helpers for turning technical model results into a business-facing
model comparison table and cluster naming.
"""

import pandas as pd


def build_model_comparison_table(kmeans_silhouette, reg_results, clf_results):
    rows = [
        {
            "Model": "K-Means",
            "Objective": "Customer segmentation",
            "Baseline Performance": "-",
            "Tuned Performance": f"Silhouette = {kmeans_silhouette:.3f}",
            "Selected Model": "Yes",
        },
        {
            "Model": "Linear Regression",
            "Objective": "Predict CustomerRating",
            "Baseline Performance": f"RMSE={reg_results['Linear Regression']['metrics']['RMSE']:.3f}, "
                                     f"R2={reg_results['Linear Regression']['metrics']['R2']:.3f}",
            "Tuned Performance": "-",
            "Selected Model": "No",
        },
        {
            "Model": "Ridge Regression",
            "Objective": "Predict CustomerRating",
            "Baseline Performance": f"RMSE={reg_results['Ridge (baseline)']['metrics']['RMSE']:.3f}, "
                                     f"R2={reg_results['Ridge (baseline)']['metrics']['R2']:.3f}",
            "Tuned Performance": f"RMSE={reg_results['Ridge (tuned)']['metrics']['RMSE']:.3f}, "
                                  f"R2={reg_results['Ridge (tuned)']['metrics']['R2']:.3f}",
            "Selected Model": "Yes",
        },
        {
            "Model": "Logistic Regression",
            "Objective": "Predict PurchaseLikelihood",
            "Baseline Performance": f"F1={clf_results['Logistic Regression (baseline)']['metrics']['F1']:.3f}, "
                                     f"ROC-AUC={clf_results['Logistic Regression (baseline)']['metrics']['ROC_AUC']:.3f}",
            "Tuned Performance": f"F1={clf_results['Logistic Regression (tuned)']['metrics']['F1']:.3f}, "
                                  f"ROC-AUC={clf_results['Logistic Regression (tuned)']['metrics']['ROC_AUC']:.3f}",
            "Selected Model": "Yes",
        },
    ]
    return pd.DataFrame(rows)
