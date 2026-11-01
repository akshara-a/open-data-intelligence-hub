"""
Model Evaluation Module — Part E
==================================
Compares all models, maps performance to business goals,
and generates a comprehensive summary report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")


def create_model_comparison_table(reg_results, clf_results, clust_results):
    """
    Create a comprehensive model comparison table.

    Returns
    -------
    pd.DataFrame
        Comparison table with model, task, metrics, and business value.
    """
    comparison = pd.DataFrame([
        {
            "Model": "Linear Regression",
            "ML Task": "Rating Prediction",
            "MAE": reg_results["linear"]["metrics"]["MAE"],
            "RMSE": reg_results["linear"]["metrics"]["RMSE"],
            "R² Score": reg_results["linear"]["metrics"]["R2_Score"],
            "Accuracy": "-",
            "F1 Score": "-",
            "ROC-AUC": "-",
            "Silhouette": "-",
            "Business Value": "Recommend products users may rate highly",
        },
        {
            "Model": "Ridge Regression",
            "ML Task": "Rating Prediction",
            "MAE": reg_results["ridge"]["metrics"]["MAE"],
            "RMSE": reg_results["ridge"]["metrics"]["RMSE"],
            "R² Score": reg_results["ridge"]["metrics"]["R2_Score"],
            "Accuracy": "-",
            "F1 Score": "-",
            "ROC-AUC": "-",
            "Silhouette": "-",
            "Business Value": "Recommend products with regularized prediction",
        },
        {
            "Model": "Logistic Regression",
            "ML Task": "Purchase Prediction",
            "MAE": "-",
            "RMSE": "-",
            "R² Score": "-",
            "Accuracy": clf_results["metrics"]["Accuracy"],
            "F1 Score": clf_results["metrics"]["F1_Score"],
            "ROC-AUC": clf_results["metrics"]["ROC_AUC"],
            "Silhouette": "-",
            "Business Value": "Identify users likely to purchase",
        },
        {
            "Model": "K-Means Clustering",
            "ML Task": "Customer Segmentation",
            "MAE": "-",
            "RMSE": "-",
            "R² Score": "-",
            "Accuracy": "-",
            "F1 Score": "-",
            "ROC-AUC": "-",
            "Silhouette": clust_results["metrics"]["Silhouette_Score"],
            "Business Value": "Create targeted marketing strategies",
        },
    ])

    return comparison


def create_business_alignment_table():
    """Create a business goal → ML approach mapping table."""
    alignment = pd.DataFrame([
        {"Business Goal": "Recommend products users may like", "ML Approach": "Regression (Rating Prediction)"},
        {"Business Goal": "Predict whether a user will purchase", "ML Approach": "Classification (Logistic Regression)"},
        {"Business Goal": "Group similar customers", "ML Approach": "Clustering (K-Means)"},
        {"Business Goal": "Improve campaign targeting", "ML Approach": "Classification + Clustering"},
        {"Business Goal": "Increase sales conversion", "ML Approach": "Recommendation + Purchase Prediction"},
        {"Business Goal": "Improve customer experience", "ML Approach": "Personalized recommendations"},
    ])
    return alignment


def plot_model_comparison(reg_results, clf_results, clust_results,
                           output_dir="outputs/plots"):
    """Generate comprehensive model comparison visualizations."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # --- 1. Regression Metrics ---
    metrics = ["MAE", "RMSE", "R2_Score"]
    linear_vals = [reg_results["linear"]["metrics"][m] for m in metrics]
    ridge_vals = [reg_results["ridge"]["metrics"][m] for m in metrics]

    x = np.arange(len(metrics))
    width = 0.35
    axes[0].bar(x - width / 2, linear_vals, width, label="Linear", color="#4C72B0", edgecolor="white")
    axes[0].bar(x + width / 2, ridge_vals, width, label="Ridge", color="#55A868", edgecolor="white")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(["MAE", "RMSE", "R² Score"])
    axes[0].set_title("Regression Metrics", fontsize=13, fontweight="bold")
    axes[0].legend(fontsize=10)
    axes[0].set_ylabel("Score", fontsize=11)

    # --- 2. Classification Metrics ---
    clf_metrics = ["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"]
    clf_vals = [clf_results["metrics"][m] for m in clf_metrics]
    colors = ["#4C72B0", "#55A868", "#DD8452", "#C44E52", "#8172B2"]
    bars = axes[1].bar([m.replace("_", "\n") for m in clf_metrics], clf_vals,
                        color=colors, edgecolor="white")
    for bar, val in zip(bars, clf_vals):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f"{val:.3f}", ha="center", fontsize=9, fontweight="bold")
    axes[1].set_title("Classification Metrics", fontsize=13, fontweight="bold")
    axes[1].set_ylabel("Score", fontsize=11)
    axes[1].set_ylim(0, 1.1)

    # --- 3. Clustering Metrics ---
    clust_metrics_names = ["Inertia\n(×0.001)", "Silhouette\nScore"]
    clust_vals = [
        clust_results["metrics"]["Inertia"] / 1000,
        clust_results["metrics"]["Silhouette_Score"],
    ]
    bars = axes[2].bar(clust_metrics_names, clust_vals,
                        color=["#CCB974", "#64B5CD"], edgecolor="white", width=0.5)
    for bar, val, raw in zip(bars, clust_vals,
                              [clust_results["metrics"]["Inertia"],
                               clust_results["metrics"]["Silhouette_Score"]]):
        axes[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                     f"{raw:.2f}", ha="center", fontsize=10, fontweight="bold")
    axes[2].set_title("Clustering Metrics", fontsize=13, fontweight="bold")
    axes[2].set_ylabel("Score", fontsize=11)

    plt.suptitle("Model Performance Comparison", fontsize=16, fontweight="bold", y=1.03)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "model_comparison.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("[Evaluation] Saved: model_comparison.png")


def generate_final_report(reg_results, clf_results, clust_results,
                            tuning_results, output_dir="outputs/results"):
    """Generate a comprehensive text report."""
    os.makedirs(output_dir, exist_ok=True)

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("E-COMMERCE RECOMMENDATION SYSTEM — FINAL REPORT")
    report_lines.append("=" * 70)

    # --- Regression Summary ---
    report_lines.append("\n\n1. REGRESSION — RATING PREDICTION")
    report_lines.append("-" * 40)
    report_lines.append("\nLinear Regression:")
    for k, v in reg_results["linear"]["metrics"].items():
        report_lines.append(f"  {k}: {v:.4f}")
    report_lines.append("\nRidge Regression:")
    for k, v in reg_results["ridge"]["metrics"].items():
        report_lines.append(f"  {k}: {v:.4f}")

    # Determine better model
    if reg_results["ridge"]["metrics"]["R2_Score"] >= reg_results["linear"]["metrics"]["R2_Score"]:
        report_lines.append("\n  -> Ridge Regression performs equally or better due to regularization.")
    else:
        report_lines.append("\n  -> Linear Regression performs slightly better on this dataset.")

    report_lines.append("\n  Business Impact: Rating prediction helps recommend products")
    report_lines.append("  that users are likely to rate highly, improving user satisfaction.")

    # --- Classification Summary ---
    report_lines.append("\n\n2. CLASSIFICATION — PURCHASE PREDICTION")
    report_lines.append("-" * 40)
    for k, v in clf_results["metrics"].items():
        report_lines.append(f"  {k}: {v:.4f}")
    report_lines.append("\n  Business Impact: Purchase prediction enables personalized")
    report_lines.append("  recommendations, targeted discounts, and cart recovery campaigns.")

    # --- Clustering Summary ---
    report_lines.append("\n\n3. CLUSTERING — CUSTOMER SEGMENTATION")
    report_lines.append("-" * 40)
    report_lines.append(f"  Number of Clusters: {clust_results['metrics']['n_clusters']}")
    report_lines.append(f"  Inertia: {clust_results['metrics']['Inertia']:.2f}")
    report_lines.append(f"  Silhouette Score: {clust_results['metrics']['Silhouette_Score']:.4f}")
    report_lines.append("\n  Cluster Profiles:")
    report_lines.append(clust_results["profiles"].to_string())
    report_lines.append("\n  Business Impact: Customer segmentation enables targeted")
    report_lines.append("  marketing, loyalty programs, and personalized experiences.")

    # --- Hyperparameter Tuning Summary ---
    report_lines.append("\n\n4. HYPERPARAMETER TUNING RESULTS")
    report_lines.append("-" * 40)
    report_lines.append(f"\n  Ridge Regression Best Alpha: {tuning_results['ridge']['best_params']}")
    report_lines.append(f"  Logistic Regression Best Params: {tuning_results['logistic']['best_params']}")
    report_lines.append(f"  K-Means Best Config: n_clusters={int(tuning_results['kmeans']['best_config']['n_clusters'])}, "
                        f"init={tuning_results['kmeans']['best_config']['init']}")

    # --- Business Goal Mapping ---
    report_lines.append("\n\n5. BUSINESS GOAL ALIGNMENT")
    report_lines.append("-" * 40)
    alignment = create_business_alignment_table()
    report_lines.append(alignment.to_string(index=False))

    # --- Conclusion ---
    report_lines.append("\n\n6. CONCLUSION")
    report_lines.append("-" * 40)
    report_lines.append("""
The e-commerce recommendation system combines regression, classification,
and clustering to solve different business problems:

• Regression models predict user ratings, enabling the platform to
  recommend products that users are likely to enjoy.

• Logistic regression predicts purchase likelihood, helping identify
  users who are ready to buy and enabling targeted marketing.

• K-Means clustering segments customers into distinct groups, allowing
  the business to tailor strategies for each segment.

By tuning hyperparameters, model performance was optimized for each task.
The combination of these models provides a comprehensive recommendation
system that can improve customer experience, increase conversion rates,
and drive revenue growth.
""")

    report_lines.append("=" * 70)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 70)

    # Save report
    report_text = "\n".join(report_lines)
    filepath = os.path.join(output_dir, "final_report.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n[Evaluation] Report saved to: {filepath}")
    return report_text


def run_evaluation(reg_results, clf_results, clust_results, tuning_results,
                    output_dir="outputs"):
    """
    Run the complete evaluation pipeline.

    Parameters
    ----------
    reg_results : dict
        Results from regression model.
    clf_results : dict
        Results from classification model.
    clust_results : dict
        Results from clustering model.
    tuning_results : dict
        Results from hyperparameter tuning.
    output_dir : str
        Base output directory.

    Returns
    -------
    dict
        Evaluation results including comparison table and report.
    """
    print("\n" + "=" * 60)
    print("PART E: MODEL EVALUATION & BUSINESS ALIGNMENT")
    print("=" * 60)

    plots_dir = os.path.join(output_dir, "plots")
    results_dir = os.path.join(output_dir, "results")

    # Model comparison table
    comparison = create_model_comparison_table(reg_results, clf_results, clust_results)
    print("\n--- Model Comparison Table ---")

    # Format numeric columns for display
    display_comparison = comparison.copy()
    for col in ["MAE", "RMSE", "R² Score", "Accuracy", "F1 Score", "ROC-AUC", "Silhouette"]:
        display_comparison[col] = display_comparison[col].apply(
            lambda x: f"{x:.4f}" if isinstance(x, float) else x
        )
    print(display_comparison[["Model", "ML Task", "MAE", "RMSE", "R² Score",
                              "Accuracy", "F1 Score", "ROC-AUC", "Silhouette"]].to_string(index=False))

    # Save comparison table
    os.makedirs(results_dir, exist_ok=True)
    comparison.to_csv(os.path.join(results_dir, "model_comparison.csv"), index=False, encoding="utf-8")
    print(f"\n[Evaluation] Comparison table saved to: {results_dir}/model_comparison.csv")

    # Business alignment
    alignment = create_business_alignment_table()
    print("\n--- Business Goal Alignment ---")
    print(alignment.to_string(index=False))

    # Plot comparison
    plot_model_comparison(reg_results, clf_results, clust_results, plots_dir)

    # Generate final report
    report = generate_final_report(reg_results, clf_results, clust_results,
                                    tuning_results, results_dir)
    print("\n" + report)

    return {
        "comparison_table": comparison,
        "alignment_table": alignment,
        "report": report,
    }
