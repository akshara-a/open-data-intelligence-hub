import os
import pandas as pd

RESULTS_DIR = "results"

individual_file = os.path.join(
    RESULTS_DIR, "individual_model_results.csv"
)
ensemble_file = os.path.join(
    RESULTS_DIR, "ensemble_results.csv"
)
benchmark_file = os.path.join(
    RESULTS_DIR, "benchmark_results.csv"
)

output_file = os.path.join(
    RESULTS_DIR, "final_comparison.csv"
)

print("=" * 70)
print("FINAL PERFORMANCE COMPARISON")
print("=" * 70)

# ============================================================
# 1. INDIVIDUAL CNN RESULTS
# ============================================================

individual = pd.read_csv(individual_file)

individual = individual.rename(
    columns={
        "F1": "F1_Score",
        "F1_Score": "F1_Score"
    }
)

individual["Category"] = "Individual CNN"

individual = individual[
    [
        "Model",
        "Category",
        "Accuracy",
        "Precision",
        "Recall",
        "F1_Score"
    ]
]

# ============================================================
# 2. ENSEMBLE RESULTS
# ============================================================

ensemble = pd.read_csv(ensemble_file)

ensemble = ensemble.rename(
    columns={
        "F1": "F1_Score",
        "F1_Score": "F1_Score"
    }
)

# IMPORTANT:
# Keep ONLY actual ensemble methods.
# Do not include CNN1/CNN2/CNN3 again.
ensemble = ensemble[
    ensemble["Model"].isin(
        ["Majority Voting", "Soft Voting"]
    )
].copy()

ensemble["Category"] = "Ensemble Method"

ensemble = ensemble[
    [
        "Model",
        "Category",
        "Accuracy",
        "Precision",
        "Recall",
        "F1_Score"
    ]
]

# ============================================================
# 3. COMBINE PERFORMANCE RESULTS
# ============================================================

performance = pd.concat(
    [individual, ensemble],
    ignore_index=True
)

# ============================================================
# 4. BENCHMARK RESULTS
# ============================================================

benchmark = pd.read_csv(benchmark_file)

print("\nBenchmark Results:")
print("-" * 70)
print(benchmark.to_string(index=False))

# Rename benchmark columns to clean names
benchmark = benchmark.rename(
    columns={
        "Model Size (MB)": "Model_Size_MB",
        "Latency (ms/image)": "Latency_ms",
        "Throughput (images/sec)": "Throughput_images_sec",
        "Memory Usage (MB)": "Memory_MB"
    }
)

benchmark = benchmark[
    [
        "Model",
        "Parameters",
        "Model_Size_MB",
        "Latency_ms",
        "Throughput_images_sec",
        "Memory_MB"
    ]
]

# ============================================================
# 5. MERGE BENCHMARK DATA
# ============================================================

final_df = performance.merge(
    benchmark,
    on="Model",
    how="left"
)

# ============================================================
# 6. ADD EMPTY BENCHMARK VALUES FOR ENSEMBLES
# ============================================================

# Ensemble methods do not have separate model benchmark
# measurements in the current benchmark CSV.

# ============================================================
# 7. ORDER COLUMNS
# ============================================================

final_df = final_df[
    [
        "Model",
        "Category",
        "Accuracy",
        "Precision",
        "Recall",
        "F1_Score",
        "Parameters",
        "Model_Size_MB",
        "Latency_ms",
        "Throughput_images_sec",
        "Memory_MB"
    ]
]

# ============================================================
# 8. ROUND VALUES
# ============================================================

final_df["Accuracy"] = final_df["Accuracy"].round(4)
final_df["Precision"] = final_df["Precision"].round(4)
final_df["Recall"] = final_df["Recall"].round(4)
final_df["F1_Score"] = final_df["F1_Score"].round(4)

final_df["Model_Size_MB"] = final_df["Model_Size_MB"].round(3)
final_df["Latency_ms"] = final_df["Latency_ms"].round(3)
final_df["Throughput_images_sec"] = (
    final_df["Throughput_images_sec"].round(3)
)
final_df["Memory_MB"] = final_df["Memory_MB"].round(2)

# ============================================================
# 9. SAVE FINAL CSV
# ============================================================

final_df.to_csv(
    output_file,
    index=False
)

# ============================================================
# 10. DISPLAY FINAL TABLE
# ============================================================

print("\n")
print("=" * 70)
print("FINAL COMPARISON TABLE")
print("=" * 70)

print(
    final_df.to_string(index=False)
)

# ============================================================
# 11. BEST INDIVIDUAL CNN
# ============================================================

individual_only = final_df[
    final_df["Category"] == "Individual CNN"
]

best_individual = individual_only.loc[
    individual_only["Accuracy"].idxmax()
]

print("\n")
print("=" * 70)
print("BEST INDIVIDUAL CNN")
print("=" * 70)

print("Model     :", best_individual["Model"])
print("Accuracy  :", best_individual["Accuracy"])
print("Precision :", best_individual["Precision"])
print("Recall    :", best_individual["Recall"])
print("F1 Score  :", best_individual["F1_Score"])

# ============================================================
# 12. BEST ENSEMBLE
# ============================================================

ensemble_only = final_df[
    final_df["Category"] == "Ensemble Method"
]

best_ensemble = ensemble_only.loc[
    ensemble_only["Accuracy"].idxmax()
]

print("\n")
print("=" * 70)
print("BEST ENSEMBLE METHOD")
print("=" * 70)

print("Method    :", best_ensemble["Model"])
print("Accuracy  :", best_ensemble["Accuracy"])
print("Precision :", best_ensemble["Precision"])
print("Recall    :", best_ensemble["Recall"])
print("F1 Score  :", best_ensemble["F1_Score"])

# ============================================================
# 13. ENSEMBLE IMPROVEMENT
# ============================================================

accuracy_difference = (
    best_ensemble["Accuracy"]
    - best_individual["Accuracy"]
)

percentage_difference = accuracy_difference * 100

print("\n")
print("=" * 70)
print("ENSEMBLE IMPROVEMENT")
print("=" * 70)

print(
    f"Best Individual Accuracy : "
    f"{best_individual['Accuracy']:.4f}"
)

print(
    f"Best Ensemble Accuracy   : "
    f"{best_ensemble['Accuracy']:.4f}"
)

print(
    f"Accuracy Difference      : "
    f"{percentage_difference:+.2f}%"
)

# ============================================================
# 14. FINAL FILE INFORMATION
# ============================================================

print("\n")
print("=" * 70)
print("FINAL COMPARISON COMPLETED")
print("=" * 70)

print("Saved file:")
print(os.path.abspath(output_file))

print("\nTotal rows   :", len(final_df))
print("Total columns:", len(final_df.columns))

print("\nFinal models:")
for model in final_df["Model"]:
    print("-", model)

print("\n" + "=" * 70)