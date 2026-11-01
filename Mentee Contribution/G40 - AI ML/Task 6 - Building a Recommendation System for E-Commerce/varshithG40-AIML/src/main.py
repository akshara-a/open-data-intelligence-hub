"""
Main Pipeline — E-Commerce Recommendation System
==================================================
Master script that orchestrates the entire ML pipeline:
Data Generation → Preprocessing → EDA → Regression →
Classification → Clustering → Hyperparameter Tuning → Evaluation
"""

import sys
import os
import time

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_generation import generate_ecommerce_data
from data_preprocessing import preprocess_all
from eda import run_eda
from regression_model import run_regression
from classification_model import run_classification
from clustering_model import run_clustering
from hyperparameter_tuning import run_hyperparameter_tuning
from model_evaluation import run_evaluation


def main():
    """Run the complete recommendation system pipeline."""
    start_time = time.time()

    print("+" + "=" * 58 + "+")
    print("|   E-COMMERCE RECOMMENDATION SYSTEM -- ML PIPELINE         |")
    print("+" + "=" * 58 + "+")

    # Determine project root (one level up from src/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    output_dir = os.path.join(project_root, "outputs")
    plots_dir = os.path.join(output_dir, "plots")
    results_dir = os.path.join(output_dir, "results")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # ============================================================
    # STEP 1: DATA GENERATION
    # ============================================================
    print("\n" + "=" * 60)
    print("STEP 1: DATA GENERATION")
    print("=" * 60)
    df = generate_ecommerce_data(n_records=5000, output_dir=data_dir)

    # ============================================================
    # STEP 2: DATA PREPROCESSING
    # ============================================================
    data_path = os.path.join(data_dir, "ecommerce_data.csv")
    preprocessed = preprocess_all(data_path)

    # ============================================================
    # STEP 3: EXPLORATORY DATA ANALYSIS
    # ============================================================
    run_eda(preprocessed["df"], output_dir=plots_dir)

    # ============================================================
    # STEP 4: PART A — REGRESSION (RATING PREDICTION)
    # ============================================================
    reg_results = run_regression(preprocessed["regression"], output_dir=plots_dir)

    # ============================================================
    # STEP 5: PART B — CLASSIFICATION (PURCHASE PREDICTION)
    # ============================================================
    clf_results = run_classification(preprocessed["classification"], output_dir=plots_dir)

    # ============================================================
    # STEP 6: PART C — CLUSTERING (CUSTOMER SEGMENTATION)
    # ============================================================
    clust_results = run_clustering(preprocessed["clustering"], output_dir=plots_dir)

    # ============================================================
    # STEP 7: PART D — HYPERPARAMETER TUNING
    # ============================================================
    tuning_results = run_hyperparameter_tuning(preprocessed, output_dir=plots_dir)

    # ============================================================
    # STEP 8: PART E — MODEL EVALUATION & COMPARISON
    # ============================================================
    eval_results = run_evaluation(
        reg_results, clf_results, clust_results, tuning_results,
        output_dir=output_dir
    )

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    elapsed = time.time() - start_time
    print("\n" + "+" + "=" * 58 + "+")
    print("|   PIPELINE COMPLETE                                      |")
    print("+" + "=" * 58 + "+")
    print(f"\n  Total execution time: {elapsed:.1f} seconds")
    print(f"  Dataset: {data_path}")
    print(f"  Plots saved to: {plots_dir}")
    print(f"  Results saved to: {results_dir}")
    print(f"\n  Files generated:")

    # List output files
    for root, dirs, files in os.walk(output_dir):
        for f in sorted(files):
            rel_path = os.path.relpath(os.path.join(root, f), output_dir)
            print(f"    outputs/{rel_path}")

    print("\n  [OK] All tasks completed successfully!")


if __name__ == "__main__":
    main()
