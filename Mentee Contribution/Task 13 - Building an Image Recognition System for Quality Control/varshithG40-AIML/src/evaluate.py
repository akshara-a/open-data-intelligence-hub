"""
Evaluation Module for Automated Casting Defect Detection System
Evaluates model on test dataset, computes metrics, confusion matrix, threshold tuning, and false negative analysis.
"""

import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from src.data_loader import load_casting_datasets
from src.utils import plot_confusion_matrix_heatmap, save_classification_report

def evaluate_model(
    model_path="models/best_casting_defect_model.keras",
    test_dir="data/test",
    reports_dir="reports"
):
    """
    Evaluates trained model on unseen test dataset.
    
    Args:
        model_path: Filepath to saved Keras model.
        test_dir: Path to test image directory.
        reports_dir: Directory to save evaluation reports and plots.
        
    Returns:
        dict: Evaluation metrics dictionary.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Saved model file not found at '{model_path}'. Run train.py first.")

    print(f"Loading trained model from '{model_path}'...")
    model = tf.keras.models.load_model(model_path)

    print("\nLoading test dataset...")
    _, _, test_dataset = load_casting_datasets(test_dir=test_dir)

    # 1. Test Dataset Loss & Metrics Evaluation
    print("\nEvaluating model on test dataset...")
    test_results = model.evaluate(test_dataset, verbose=1)
    
    metrics_names = model.metrics_names
    test_summary = {name: val for name, val in zip(metrics_names, test_results)}
    
    print("\n=== Test Set Evaluation Results ===")
    for metric_name, score in test_summary.items():
        print(f"  {metric_name.capitalize()}: {score:.4f}")

    # 2. Generate Prediction Probabilities & Labels
    print("\nGenerating predictions for test dataset...")
    prediction_probabilities = model.predict(test_dataset, verbose=1).flatten()

    # Extract true ground-truth labels from test dataset
    actual_labels = np.concatenate([
        labels.numpy().flatten()
        for images, labels in test_dataset
    ]).astype(int)

    # Default threshold (0.50)
    predicted_labels = (prediction_probabilities >= 0.50).astype(int)

    # 3. Classification Report
    print("\n=== Classification Report (Threshold = 0.50) ===")
    report_text = classification_report(
        actual_labels,
        predicted_labels,
        target_names=["Non-defective (0)", "Defective (1)"],
        digits=4
    )
    print(report_text)
    save_classification_report(report_text, os.path.join(reports_dir, "classification_report.txt"))

    # 4. Confusion Matrix Analysis
    cm = confusion_matrix(actual_labels, predicted_labels)
    tn, fp, fn, tp = cm.ravel()

    print("\n=== Confusion Matrix ===")
    print(f"  True Negatives (TN - Good product approved): {tn}")
    print(f"  False Positives (FP - Good product rejected): {fp}")
    print(f"  False Negatives (FN - DEFECTIVE PRODUCT PASSED!): {fn}")
    print(f"  True Positives (TP - Defective product rejected): {tp}")

    plot_confusion_matrix_heatmap(
        cm,
        class_names=["Non-defective", "Defective"],
        save_path=os.path.join(reports_dir, "confusion_matrix.png")
    )

    # 5. Threshold Analysis for Factory Decision Tuning
    print("\n=== Threshold Sensitivity Sweep Analysis ===")
    print(f"{'Threshold':<12} | {'Precision':<10} | {'Recall':<10} | {'False Positives':<16} | {'False Negatives':<16}")
    print("-" * 75)
    
    thresholds = [0.30, 0.40, 0.50, 0.60, 0.70]
    for th in thresholds:
        th_preds = (prediction_probabilities >= th).astype(int)
        th_cm = confusion_matrix(actual_labels, th_preds)
        th_tn, th_fp, th_fn, th_tp = th_cm.ravel()
        prec = th_tp / (th_tp + th_fp) if (th_tp + th_fp) > 0 else 0
        rec = th_tp / (th_tp + th_fn) if (th_tp + th_fn) > 0 else 0
        print(f"{th:<12.2f} | {prec:<10.4f} | {rec:<10.4f} | {th_fp:<16} | {th_fn:<16}")

    print("\nEvaluation complete! Reports and visualizations saved.")
    return test_summary

if __name__ == "__main__":
    evaluate_model()
