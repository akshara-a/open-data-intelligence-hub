import os
import pandas as pd

RESULTS_DIR = "results"

robustness_file = os.path.join(
    RESULTS_DIR,
    "robustness_results.csv"
)

disagreement_file = os.path.join(
    RESULTS_DIR,
    "disagreement_results.csv"
)

disagreement_summary_file = os.path.join(
    RESULTS_DIR,
    "disagreement_summary.csv"
)

# ============================================================
# ROBUSTNESS ANALYSIS
# ============================================================

print("=" * 70)
print("ROBUSTNESS ANALYSIS")
print("=" * 70)

robustness = pd.read_csv(robustness_file)

print("\nRobustness Results:")
print("-" * 70)
print(robustness.to_string(index=False))

# ------------------------------------------------------------
# Calculate robustness summary correctly
# ------------------------------------------------------------

robustness_summary = (
    robustness
    .groupby("Model")["Accuracy"]
    .agg(
        Average_Robustness_Accuracy="mean",
        Worst_Case_Accuracy="min",
        Best_Case_Accuracy="max"
    )
    .reset_index()
)

robustness_summary[
    "Average_Robustness_Accuracy"
] = robustness_summary[
    "Average_Robustness_Accuracy"
].round(4)

robustness_summary[
    "Worst_Case_Accuracy"
] = robustness_summary[
    "Worst_Case_Accuracy"
].round(4)

robustness_summary[
    "Best_Case_Accuracy"
] = robustness_summary[
    "Best_Case_Accuracy"
].round(4)

robustness_output = os.path.join(
    RESULTS_DIR,
    "final_robustness_summary.csv"
)

robustness_summary.to_csv(
    robustness_output,
    index=False
)

print("\nRobustness Summary:")
print("-" * 70)
print(
    robustness_summary.to_string(index=False)
)

# ============================================================
# DISAGREEMENT ANALYSIS
# ============================================================

print("\n")
print("=" * 70)
print("DISAGREEMENT ANALYSIS")
print("=" * 70)

disagreement = pd.read_csv(
    disagreement_file
)

print("\nDisagreement Results:")
print("-" * 70)

# Show only the important summary columns
display_columns = [
    "True_Label",
    "CNN1_Prediction",
    "CNN2_Prediction",
    "CNN3_Prediction",
    "Ensemble_Prediction",
    "All_Models_Agree"
]

available_columns = [
    column
    for column in display_columns
    if column in disagreement.columns
]

print(
    disagreement[available_columns]
    .to_string(index=False)
)

# ============================================================
# DISAGREEMENT SUMMARY
# ============================================================

if os.path.exists(disagreement_summary_file):

    summary = pd.read_csv(
        disagreement_summary_file
    )

    print("\nDisagreement Summary:")
    print("-" * 70)

    print(
        summary.to_string(index=False)
    )

# ============================================================
# SAVE CLEAN DISAGREEMENT RESULTS
# ============================================================

clean_disagreement_file = os.path.join(
    RESULTS_DIR,
    "final_disagreement_analysis.csv"
)

disagreement.to_csv(
    clean_disagreement_file,
    index=False
)

# ============================================================
# FINAL STATUS
# ============================================================

print("\n")
print("=" * 70)
print("FINAL ANALYSIS COMPLETED")
print("=" * 70)

print("\nCreated files:")

print(
    os.path.abspath(robustness_output)
)

print(
    os.path.abspath(clean_disagreement_file)
)

print("\n✓ Individual CNN evaluation")
print("✓ Ensemble evaluation")
print("✓ Model benchmarks")
print("✓ Performance graphs")
print("✓ Robustness analysis")
print("✓ Disagreement analysis")

print("\n" + "=" * 70)