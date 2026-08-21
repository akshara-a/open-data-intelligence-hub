"""Reusable model evaluation and visualization functions."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_elbow_and_silhouette(results, output_dir="reports/visualizations"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scores = pd.DataFrame(results)

    plt.figure(figsize=(8, 5))
    plt.plot(scores["k"], scores["inertia"], marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.tight_layout()
    plt.savefig(output_dir / "elbow_method.png", dpi=150)
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(scores["k"], scores["silhouette_score"], marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score by Number of Clusters")
    plt.tight_layout()
    plt.savefig(output_dir / "silhouette_scores.png", dpi=150)
    plt.show()


def plot_actual_vs_predicted(y_true, y_pred, output_path):
    plt.figure(figsize=(7, 5))
    plt.scatter(y_true, y_pred)
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.show()
