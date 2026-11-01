import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = "results"
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")

os.makedirs(PLOTS_DIR, exist_ok=True)

# Load final comparison
file_path = os.path.join(
    RESULTS_DIR,
    "final_comparison.csv"
)

df = pd.read_csv(file_path)

# ------------------------------------------------------------
# Function to create comparison graph
# ------------------------------------------------------------

def create_plot(column, title, ylabel, filename):

    plot_df = df.dropna(subset=[column])

    plt.figure(figsize=(10, 6))

    plt.bar(
        plot_df["Model"],
        plot_df[column]
    )

    plt.title(title)
    plt.xlabel("Model")
    plt.ylabel(ylabel)

    plt.xticks(
        rotation=20,
        ha="right"
    )

    plt.tight_layout()

    output_path = os.path.join(
        PLOTS_DIR,
        filename
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Created:", output_path)


# ------------------------------------------------------------
# Performance graphs
# ------------------------------------------------------------

create_plot(
    "Accuracy",
    "Accuracy Comparison",
    "Accuracy",
    "accuracy_comparison.png"
)

create_plot(
    "Precision",
    "Precision Comparison",
    "Precision",
    "precision_comparison.png"
)

create_plot(
    "Recall",
    "Recall Comparison",
    "Recall",
    "recall_comparison.png"
)

create_plot(
    "F1_Score",
    "F1 Score Comparison",
    "F1 Score",
    "f1_comparison.png"
)

# ------------------------------------------------------------
# Model benchmark graphs
# ------------------------------------------------------------

create_plot(
    "Parameters",
    "Model Parameter Comparison",
    "Number of Parameters",
    "parameter_comparison.png"
)

create_plot(
    "Model_Size_MB",
    "Model Size Comparison",
    "Model Size (MB)",
    "model_size_comparison.png"
)

create_plot(
    "Latency_ms",
    "Inference Latency Comparison",
    "Latency (ms/image)",
    "latency_comparison.png"
)

create_plot(
    "Throughput_images_sec",
    "Inference Throughput Comparison",
    "Images per Second",
    "throughput_comparison.png"
)

create_plot(
    "Memory_MB",
    "Memory Usage Comparison",
    "Memory Usage (MB)",
    "memory_comparison.png"
)

print("\n" + "=" * 60)
print("ALL GRAPHS GENERATED SUCCESSFULLY")
print("=" * 60)

print("\nGraphs saved in:")
print(os.path.abspath(PLOTS_DIR))