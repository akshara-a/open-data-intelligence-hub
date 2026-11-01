"""Evaluation Metrics Engine and Performance Reporting."""

import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def compute_metrics(
    y_true: np.ndarray, y_pred_probs_or_classes: np.ndarray
) -> dict[str, float]:
    """Calculates Classification Performance Metrics.

    Args:
        y_true: Ground truth integer class indices (N,).
        y_pred_probs_or_classes: Either probabilities (N, C) or discrete labels (N,).

    Returns:
        Dictionary mapping metric names to calculated float metrics.
    """
    if y_pred_probs_or_classes.ndim > 1:
        y_pred = np.argmax(y_pred_probs_or_classes, axis=1)
    else:
        y_pred = y_pred_probs_or_classes

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(y_true, y_pred, average="weighted")
        ),
        "recall": float(recall_score(y_true, y_pred, average="weighted")),
        "f1_score": float(f1_score(y_true, y_pred, average="weighted")),
    }


def plot_and_save_confusion_matrix(
    y_true: np.ndarray,
    y_pred_classes: np.ndarray,
    class_names: list[str],
    output_path: str,
    title: str = "Confusion Matrix",
) -> None:
    """Generates and saves a confusion matrix visualization map.

    Args:
        y_true: True integer targets.
        y_pred_classes: Predicted integer labels.
        class_names: Category string names.
        output_path: Target filesystem path for PNG output.
        title: Title of plot.
    """
    cm = confusion_matrix(y_true, y_pred_classes)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
    )
    plt.title(title)
    plt.ylabel("Actual Target")
    plt.xlabel("Predicted Output")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()