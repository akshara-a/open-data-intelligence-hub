"""
evaluate.py
===========
Calculates classification performance metrics (Accuracy, Precision, Recall, F1-Score, Loss)
and generates formatted confusion matrices for each individual CNN model.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, log_loss
from tensorflow import keras

from .preprocessing import load_full_dataset, CLASSES

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")


def plot_confusion_matrix(y_true, y_pred, model_name: str, save_path: str):
    """
    Renders and saves a sleek annotated confusion matrix heatmap.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5), dpi=300)
    
    # Elegant color palette
    cmap = sns.light_palette("#1e40af", as_cmap=True)
    
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=cmap,
        xticklabels=[c.capitalize() for c in CLASSES],
        yticklabels=[c.capitalize() for c in CLASSES],
        cbar=True,
        linewidths=1.5,
        linecolor="#f8fafc",
        annot_kws={"size": 14, "weight": "bold"}
    )
    
    plt.title(f"Confusion Matrix — {model_name}", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Predicted Class", fontsize=11, fontweight="bold", labelpad=8)
    plt.ylabel("Actual True Class", fontsize=11, fontweight="bold", labelpad=8)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[PLOT] Saved confusion matrix: {save_path}")


def evaluate_single_model(model: keras.Model, model_name: str, X_test: np.ndarray, y_test: np.ndarray, cm_filename: str) -> dict:
    """
    Evaluates one model on the test partition and computes standard classification metrics.
    """
    # y_test is one-hot (N, 2)
    y_true_indices = np.argmax(y_test, axis=1)
    
    # Predict probabilities
    probs = model.predict(X_test, verbose=0)
    preds = np.argmax(probs, axis=1)
    
    acc = accuracy_score(y_true_indices, preds)
    prec = precision_score(y_true_indices, preds, average="macro", zero_division=0)
    rec = recall_score(y_true_indices, preds, average="macro", zero_division=0)
    f1 = f1_score(y_true_indices, preds, average="macro", zero_division=0)
    loss = log_loss(y_test, probs)
    
    cm_path = os.path.join(RESULTS_DIR, cm_filename)
    plot_confusion_matrix(y_true_indices, preds, model_name, cm_path)
    
    metrics = {
        "Model": model_name,
        "Accuracy": float(acc),
        "Precision": float(prec),
        "Recall": float(rec),
        "F1-score": float(f1),
        "Loss": float(loss),
        "Probabilities": probs,
        "Predictions": preds
    }
    
    return metrics


def evaluate_all_individual_models(models_dict: dict = None) -> pd.DataFrame:
    """
    Evaluates CNN 1, CNN 2, and CNN 3 on the shared test dataset.
    """
    _, _, (X_test, y_test), _ = load_full_dataset()
    
    if models_dict is None:
        models_dict = {
            "CNN 1 (Baseline)": keras.models.load_model(os.path.join(MODELS_DIR, "cnn_baseline.keras")),
            "CNN 2 (Regularized)": keras.models.load_model(os.path.join(MODELS_DIR, "cnn_regularized.keras")),
            "CNN 3 (Deeper)": keras.models.load_model(os.path.join(MODELS_DIR, "cnn_deep.keras"))
        }
        
    cm_files = {
        "CNN 1 (Baseline)": "confusion_matrix_cnn1.png",
        "CNN 2 (Regularized)": "confusion_matrix_cnn2.png",
        "CNN 3 (Deeper)": "confusion_matrix_cnn3.png"
    }
    
    results = []
    print("\n=======================================================")
    print(" Evaluating Individual CNNs on Test Dataset (N=15)")
    print("=======================================================")
    
    for name, model in models_dict.items():
        cm_file = cm_files.get(name, f"confusion_matrix_{name.lower().replace(' ', '_')}.png")
        m = evaluate_single_model(model, name, X_test, y_test, cm_file)
        results.append({
            "Model": m["Model"],
            "Accuracy (%)": round(m["Accuracy"] * 100, 2),
            "Precision (%)": round(m["Precision"] * 100, 2),
            "Recall (%)": round(m["Recall"] * 100, 2),
            "F1-score (%)": round(m["F1-score"] * 100, 2),
            "Loss": round(m["Loss"], 4)
        })
        print(f"[{name}] Acc: {m['Accuracy']*100:.1f}% | Prec: {m['Precision']*100:.1f}% | Rec: {m['Recall']*100:.1f}% | F1: {m['F1-score']*100:.1f}%")
        
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    df = evaluate_all_individual_models()
    print("\n", df.to_string(index=False))
