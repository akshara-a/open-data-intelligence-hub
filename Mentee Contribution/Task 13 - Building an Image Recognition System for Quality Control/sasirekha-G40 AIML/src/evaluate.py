"""
Evaluation pipeline for the trained casting defect model.

Loads the best saved model and evaluates it ONLY on the held-out test
dataset (never used during training or validation).

Run from the project root with:

    python -m src.evaluate
"""

import csv

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from src import config
from src.data_loader import load_train_validation_test_datasets
from src.utils import get_logger, save_json

logger = get_logger(__name__)


def load_best_model() -> tf.keras.Model:
    if not config.BEST_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model found at {config.BEST_MODEL_PATH}.\n"
            f"Run `python -m src.train` first to train and save a model."
        )
    logger.info("Loading model from: %s", config.BEST_MODEL_PATH)
    return tf.keras.models.load_model(config.BEST_MODEL_PATH)


def get_predictions_and_labels(model: tf.keras.Model, test_dataset):
    """
    Run the model over the (unshuffled) test dataset and return the raw
    defect probabilities alongside the true binary labels, in matching
    order.
    """
    logger.info("Generating predictions on the test dataset")
    prediction_probabilities = model.predict(test_dataset, verbose=0).flatten()

    actual_labels = np.concatenate(
        [labels.numpy().flatten() for _, labels in test_dataset]
    ).astype(int)

    return prediction_probabilities, actual_labels


def evaluate_at_default_threshold(model, test_dataset, prediction_probabilities, actual_labels):
    """
    Report model.evaluate() metrics, classification report, and confusion
    matrix at the default (0.50) threshold, then save all of them to
    reports/metrics/.
    """
    logger.info("Evaluating test dataset")
    test_results = model.evaluate(test_dataset, verbose=0)
    metric_names = model.metrics_names
    test_metrics = dict(zip(metric_names, [float(v) for v in test_results]))
    logger.info("Test results: %s", test_metrics)

    predicted_labels = (prediction_probabilities >= config.DEFAULT_THRESHOLD).astype(int)

    report_dict = classification_report(
        actual_labels,
        predicted_labels,
        target_names=config.CLASS_DISPLAY_NAMES,
        output_dict=True,
    )
    print(
        classification_report(
            actual_labels,
            predicted_labels,
            target_names=config.CLASS_DISPLAY_NAMES,
        )
    )

    matrix = confusion_matrix(actual_labels, predicted_labels)
    tn, fp, fn, tp = matrix.ravel()

    logger.info("True Negatives: %d", tn)
    logger.info("False Positives: %d", fp)
    logger.info("False Negatives: %d", fn)
    logger.info("True Positives: %d", tp)

    # False negatives are especially dangerous in quality control: a
    # defective product is classified as non-defective and may reach
    # the customer.
    false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    logger.info("False Negative Rate: %.4f", false_negative_rate)
    logger.info("False Positive Rate: %.4f", false_positive_rate)

    # Save classification report
    save_json(report_dict, config.CLASSIFICATION_REPORT_PATH)

    # Save test metrics (from model.evaluate + FN/FP rates)
    test_metrics.update(
        {
            "false_negative_rate": float(false_negative_rate),
            "false_positive_rate": float(false_positive_rate),
            "threshold": config.DEFAULT_THRESHOLD,
        }
    )
    save_json(test_metrics, config.TEST_METRICS_PATH)

    # Save confusion matrix as JSON
    confusion_matrix_dict = {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "labels": config.CLASS_DISPLAY_NAMES,
    }
    save_json(confusion_matrix_dict, config.CONFUSION_MATRIX_JSON_PATH)

    # Save confusion matrix figure
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=config.CLASS_DISPLAY_NAMES,
        yticklabels=config.CLASS_DISPLAY_NAMES,
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix (threshold = 0.50)")
    plt.tight_layout()
    plt.savefig(config.CONFUSION_MATRIX_PLOT, dpi=200)
    plt.close()
    logger.info("Saved: %s", config.CONFUSION_MATRIX_PLOT)

    return test_metrics, confusion_matrix_dict


def threshold_analysis(prediction_probabilities, actual_labels, thresholds=None):
    """
    Evaluate accuracy, precision, recall, false positives, and false
    negatives across a range of decision thresholds, save the results
    as a CSV, and plot recall vs. threshold.

    A lower threshold generally increases recall (catches more true
    defects) at the cost of precision (more good products flagged for
    review). The right threshold depends on the relative business cost
    of a missed defect vs. an unnecessary manual inspection -- there is
    no universally "best" threshold.
    """
    if thresholds is None:
        thresholds = config.THRESHOLDS_TO_EVALUATE

    rows = []

    for threshold in thresholds:
        predicted_labels = (prediction_probabilities >= threshold).astype(int)
        matrix = confusion_matrix(actual_labels, predicted_labels)
        tn, fp, fn, tp = matrix.ravel()

        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        rows.append(
            {
                "threshold": threshold,
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "false_positives": int(fp),
                "false_negatives": int(fn),
            }
        )

        logger.info(
            "Threshold %.2f -> accuracy=%.4f precision=%.4f recall=%.4f FP=%d FN=%d",
            threshold, accuracy, precision, recall, fp, fn,
        )

    config.THRESHOLD_ANALYSIS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(config.THRESHOLD_ANALYSIS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Saved: %s", config.THRESHOLD_ANALYSIS_PATH)

    # Plot recall vs threshold
    plt.figure(figsize=(7, 5))
    plt.plot(
        [r["threshold"] for r in rows],
        [r["recall"] for r in rows],
        marker="o",
        label="Recall",
    )
    plt.plot(
        [r["threshold"] for r in rows],
        [r["precision"] for r in rows],
        marker="o",
        label="Precision",
    )
    plt.xlabel("Decision Threshold")
    plt.ylabel("Score")
    plt.title("Precision and Recall vs. Decision Threshold")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(config.THRESHOLD_RECALL_PLOT, dpi=200)
    plt.close()
    logger.info("Saved: %s", config.THRESHOLD_RECALL_PLOT)

    return rows


def main():
    model = load_best_model()

    logger.info("Loading dataset")
    _, _, test_dataset = load_train_validation_test_datasets()

    prediction_probabilities, actual_labels = get_predictions_and_labels(model, test_dataset)

    evaluate_at_default_threshold(model, test_dataset, prediction_probabilities, actual_labels)
    threshold_analysis(prediction_probabilities, actual_labels)

    logger.info("Evaluation complete. See reports/metrics/ and reports/figures/.")


if __name__ == "__main__":
    main()
