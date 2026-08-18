"""
Utility Functions for Casting Defect Detection System
Handles directory setup, plot generation, and metric reporting.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def ensure_directories(dir_paths):
    """Ensure required output directories exist."""
    for path in dir_paths:
        os.makedirs(path, exist_ok=True)

def plot_training_history(history, save_dir="reports"):
    """
    Plot and save training & validation accuracy and loss graphs.
    
    Args:
        history: Keras History object or history dictionary.
        save_dir: Directory path to save output graphs.
    """
    ensure_directories([save_dir])
    
    hist_dict = history.history if hasattr(history, 'history') else history
    
    training_accuracy = hist_dict.get("accuracy", [])
    validation_accuracy = hist_dict.get("val_accuracy", [])
    training_loss = hist_dict.get("loss", [])
    validation_loss = hist_dict.get("val_loss", [])
    
    epochs = range(1, len(training_accuracy) + 1)
    
    # 1. Plot Accuracy Graph
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, training_accuracy, 'b-o', label="Training Accuracy", linewidth=2)
    plt.plot(epochs, validation_accuracy, 'g-s', label="Validation Accuracy", linewidth=2)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Accuracy", fontsize=12)
    plt.title("Training and Validation Accuracy", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    acc_path = os.path.join(save_dir, "accuracy_graph.png")
    plt.savefig(acc_path, dpi=300)
    plt.close()
    print(f"Saved accuracy graph to {acc_path}")
    
    # 2. Plot Loss Graph
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, training_loss, 'r-o', label="Training Loss", linewidth=2)
    plt.plot(epochs, validation_loss, 'm-s', label="Validation Loss", linewidth=2)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Loss (Binary Crossentropy)", fontsize=12)
    plt.title("Training and Validation Loss", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    loss_path = os.path.join(save_dir, "loss_graph.png")
    plt.savefig(loss_path, dpi=300)
    plt.close()
    print(f"Saved loss graph to {loss_path}")

def plot_confusion_matrix_heatmap(matrix, class_names=["Non-defective", "Defective"], save_path="reports/confusion_matrix.png"):
    """
    Plot and save confusion matrix with raw counts and cell labels (TN, FP, FN, TP).
    
    Args:
        matrix: 2x2 confusion matrix array.
        class_names: List of class labels.
        save_path: Filepath to save generated image.
    """
    ensure_directories([os.path.dirname(save_path)])
    
    plt.figure(figsize=(7, 6))
    
    # Format cell text with count + label
    tn, fp, fn, tp = matrix.ravel()
    labels = np.array([
        [f"TN\n{tn}", f"FP\n{fp}"],
        [f"FN\n{fn}", f"TP\n{tp}"]
    ])
    
    sns.heatmap(matrix, annot=labels, fmt='', cmap="Blues", cbar=True,
                xticklabels=class_names, yticklabels=class_names,
                annot_kws={"size": 14, "weight": "bold"})
    
    plt.xlabel("Predicted Class", fontsize=12, fontweight='bold')
    plt.ylabel("Actual Class", fontsize=12, fontweight='bold')
    plt.title("Casting Defect Inspection Confusion Matrix", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrix plot to {save_path}")

def save_classification_report(report_text, save_path="reports/classification_report.txt"):
    """Save textual classification report to file."""
    ensure_directories([os.path.dirname(save_path)])
    with open(save_path, "w") as f:
        f.write(report_text)
    print(f"Saved classification report to {save_path}")
