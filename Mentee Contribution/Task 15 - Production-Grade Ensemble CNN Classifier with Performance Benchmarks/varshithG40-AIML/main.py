"""
main.py
=======
Main end-to-end execution script for the Production-Grade Ensemble CNN Classifier.
Orchestrates:
  1. Dataset loading & deterministic 70/15/15 splitting (100 images total, 50 cats/50 dogs)
  2. Training CNN 1 (Baseline), CNN 2 (Regularized), and CNN 3 (Deeper) for 15 epochs
  3. Individual CNN evaluation (Accuracy, Precision, Recall, F1, Loss, Confusion Matrices)
  4. Ensemble evaluation (Hard Majority Voting, Soft Voting, Weighted Soft Voting)
  5. Comprehensive production benchmarking (Latency, Throughput, RAM Memory, Model Sizes, Parameter Counts)
  6. Robustness stress-testing under image transformations (Noise, Blur, Rotation, Illumination, Cropping)
  7. Final comparative report & summary artifact generation
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data_loader import prepare_dataset
from src.train import train_all_models
from src.evaluate import evaluate_all_individual_models
from src.ensemble import evaluate_all_ensembles, EnsembleClassifier
from src.benchmark import run_full_benchmark_suite
from src.robustness_test import evaluate_robustness_suite

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "results"))


def run_pipeline():
    print("=" * 70)
    print(" PRODUCTION-GRADE ENSEMBLE CNN CLASSIFIER WITH PERFORMANCE BENCHMARKS ")
    print("=" * 70)
    
    # 1. Dataset Preparation
    print("\n>>> STEP 1: PREPARING DATASET (100 IMAGES: 50 CATS, 50 DOGS)")
    prepare_dataset(force=False)
    
    # 2. Training Models
    print("\n>>> STEP 2: TRAINING CNN MODELS (15 EPOCHS MAX)")
    train_all_models(apply_augmentation=True)
    
    # 3. Evaluating Individual CNNs
    print("\n>>> STEP 3: EVALUATING INDIVIDUAL MODELS")
    df_indiv = evaluate_all_individual_models()
    
    # 4. Evaluating Ensemble Methods
    print("\n>>> STEP 4: EVALUATING ENSEMBLE CLASSIFIERS")
    df_ens, disagreements = evaluate_all_ensembles()
    
    # 5. Production Benchmarking
    print("\n>>> STEP 5: RUNNING PRODUCTION BENCHMARKS")
    df_bench = run_full_benchmark_suite()
    
    # 6. Robustness Stress-Testing
    print("\n>>> STEP 6: EXECUTING ROBUSTNESS STRESS-TESTING SUITE")
    df_robust = evaluate_robustness_suite()
    
    # 7. Compile Final Unified Comparison Table (Section 66)
    print("\n>>> STEP 7: COMPILING FINAL BENCHMARK SUMMARY TABLE")
    
    # Merge classification metrics with benchmark metrics
    final_rows = []
    
    # CNN 1
    m1_acc = df_indiv.loc[df_indiv["Model"] == "CNN 1 (Baseline)", "Accuracy (%)"].values[0]
    m1_f1 = df_indiv.loc[df_indiv["Model"] == "CNN 1 (Baseline)", "F1-score (%)"].values[0]
    m1_prec = df_indiv.loc[df_indiv["Model"] == "CNN 1 (Baseline)", "Precision (%)"].values[0]
    m1_rec = df_indiv.loc[df_indiv["Model"] == "CNN 1 (Baseline)", "Recall (%)"].values[0]
    m1_bench = df_bench[df_bench["Architecture"] == "CNN 1 (Baseline)"].iloc[0]
    
    final_rows.append({
        "Model / Method": "CNN 1 (Baseline)",
        "Accuracy (%)": m1_acc,
        "Precision (%)": m1_prec,
        "Recall (%)": m1_rec,
        "F1-Score (%)": m1_f1,
        "Trainable Params": m1_bench["Parameters (Trainable)"],
        "Model Size (MB)": m1_bench["Model Size (MB)"],
        "Avg Latency (ms)": m1_bench["Avg Latency (ms)"],
        "Throughput (img/s)": m1_bench["Throughput (img/s)"],
        "RAM Usage (MB)": m1_bench["RAM Memory (MB)"]
    })
    
    # CNN 2
    m2_acc = df_indiv.loc[df_indiv["Model"] == "CNN 2 (Regularized)", "Accuracy (%)"].values[0]
    m2_f1 = df_indiv.loc[df_indiv["Model"] == "CNN 2 (Regularized)", "F1-score (%)"].values[0]
    m2_prec = df_indiv.loc[df_indiv["Model"] == "CNN 2 (Regularized)", "Precision (%)"].values[0]
    m2_rec = df_indiv.loc[df_indiv["Model"] == "CNN 2 (Regularized)", "Recall (%)"].values[0]
    m2_bench = df_bench[df_bench["Architecture"] == "CNN 2 (Regularized)"].iloc[0]
    
    final_rows.append({
        "Model / Method": "CNN 2 (Regularized)",
        "Accuracy (%)": m2_acc,
        "Precision (%)": m2_prec,
        "Recall (%)": m2_rec,
        "F1-Score (%)": m2_f1,
        "Trainable Params": m2_bench["Parameters (Trainable)"],
        "Model Size (MB)": m2_bench["Model Size (MB)"],
        "Avg Latency (ms)": m2_bench["Avg Latency (ms)"],
        "Throughput (img/s)": m2_bench["Throughput (img/s)"],
        "RAM Usage (MB)": m2_bench["RAM Memory (MB)"]
    })
    
    # CNN 3
    m3_acc = df_indiv.loc[df_indiv["Model"] == "CNN 3 (Deeper)", "Accuracy (%)"].values[0]
    m3_f1 = df_indiv.loc[df_indiv["Model"] == "CNN 3 (Deeper)", "F1-score (%)"].values[0]
    m3_prec = df_indiv.loc[df_indiv["Model"] == "CNN 3 (Deeper)", "Precision (%)"].values[0]
    m3_rec = df_indiv.loc[df_indiv["Model"] == "CNN 3 (Deeper)", "Recall (%)"].values[0]
    m3_bench = df_bench[df_bench["Architecture"] == "CNN 3 (Deeper)"].iloc[0]
    
    final_rows.append({
        "Model / Method": "CNN 3 (Deeper)",
        "Accuracy (%)": m3_acc,
        "Precision (%)": m3_prec,
        "Recall (%)": m3_rec,
        "F1-Score (%)": m3_f1,
        "Trainable Params": m3_bench["Parameters (Trainable)"],
        "Model Size (MB)": m3_bench["Model Size (MB)"],
        "Avg Latency (ms)": m3_bench["Avg Latency (ms)"],
        "Throughput (img/s)": m3_bench["Throughput (img/s)"],
        "RAM Usage (MB)": m3_bench["RAM Memory (MB)"]
    })
    
    # Majority Voting
    maj_row = df_ens[df_ens["Ensemble Method"] == "Majority Voting (Hard)"].iloc[0]
    ens_bench_seq = df_bench[df_bench["Architecture"] == "Ensemble (Sequential Soft Voting)"].iloc[0]
    final_rows.append({
        "Model / Method": "Majority Voting (Hard)",
        "Accuracy (%)": maj_row["Accuracy (%)"],
        "Precision (%)": maj_row["Precision (%)"],
        "Recall (%)": maj_row["Recall (%)"],
        "F1-Score (%)": maj_row["F1-score (%)"],
        "Trainable Params": ens_bench_seq["Parameters (Trainable)"],
        "Model Size (MB)": ens_bench_seq["Model Size (MB)"],
        "Avg Latency (ms)": ens_bench_seq["Avg Latency (ms)"],
        "Throughput (img/s)": ens_bench_seq["Throughput (img/s)"],
        "RAM Usage (MB)": ens_bench_seq["RAM Memory (MB)"]
    })
    
    # Soft Voting
    soft_row = df_ens[df_ens["Ensemble Method"] == "Soft Voting (Average)"].iloc[0]
    final_rows.append({
        "Model / Method": "Soft Voting (Ensemble)",
        "Accuracy (%)": soft_row["Accuracy (%)"],
        "Precision (%)": soft_row["Precision (%)"],
        "Recall (%)": soft_row["Recall (%)"],
        "F1-Score (%)": soft_row["F1-score (%)"],
        "Trainable Params": ens_bench_seq["Parameters (Trainable)"],
        "Model Size (MB)": ens_bench_seq["Model Size (MB)"],
        "Avg Latency (ms)": ens_bench_seq["Avg Latency (ms)"],
        "Throughput (img/s)": ens_bench_seq["Throughput (img/s)"],
        "RAM Usage (MB)": ens_bench_seq["RAM Memory (MB)"]
    })
    
    # Weighted Soft Voting
    w_row = df_ens[df_ens["Ensemble Method"] == "Weighted Soft Voting"].iloc[0]
    final_rows.append({
        "Model / Method": "Weighted Soft Voting",
        "Accuracy (%)": w_row["Accuracy (%)"],
        "Precision (%)": w_row["Precision (%)"],
        "Recall (%)": w_row["Recall (%)"],
        "F1-Score (%)": w_row["F1-score (%)"],
        "Trainable Params": ens_bench_seq["Parameters (Trainable)"],
        "Model Size (MB)": ens_bench_seq["Model Size (MB)"],
        "Avg Latency (ms)": ens_bench_seq["Avg Latency (ms)"],
        "Throughput (img/s)": ens_bench_seq["Throughput (img/s)"],
        "RAM Usage (MB)": ens_bench_seq["RAM Memory (MB)"]
    })
    
    df_final = pd.DataFrame(final_rows)
    final_csv_path = os.path.join(RESULTS_DIR, "final_comparison.csv")
    df_final.to_csv(final_csv_path, index=False)
    
    print("\n" + "=" * 80)
    print("                       FINAL BENCHMARK COMPARISON TABLE")
    print("=" * 80)
    print(df_final.to_string(index=False))
    print(f"\n[SUCCESS] Final comparison saved to: {final_csv_path}")
    print("=" * 80)
    return df_final


if __name__ == "__main__":
    run_pipeline()
