import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve, classification_report
)

def evaluate_single_model(model, X_test, y_test, model_name="Model"):
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else preds
    
    metrics = {
        "Model": model_name,
        "Accuracy": round(accuracy_score(y_test, preds), 4),
        "Precision": round(precision_score(y_test, preds, zero_division=0), 4),
        "Recall": round(recall_score(y_test, preds, zero_division=0), 4),
        "F1-Score": round(f1_score(y_test, preds, zero_division=0), 4),
        "ROC-AUC": round(roc_auc_score(y_test, probs), 4)
    }
    return metrics, preds, probs

def evaluate_all_models(models_dict, X_test, y_test):
    results = []
    for name, model in models_dict.items():
        metrics, _, _ = evaluate_single_model(model, X_test, y_test, model_name=name)
        results.append(metrics)
    return pd.DataFrame(results)

def plot_confusion_matrix(y_test, preds, model_name="Model", output_path=None):
    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Did Not Purchase", "Purchased"],
                yticklabels=["Did Not Purchase", "Purchased"])
    plt.title(f"Confusion Matrix - {model_name}", fontsize=12, pad=15)
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")
    plt.tight_layout()
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close('all')

def plot_roc_curves(models_dict, X_test, y_test, output_path=None):
    plt.figure(figsize=(8, 6))
    for name, model in models_dict.items():
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, probs)
            auc = roc_auc_score(y_test, probs)
            plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})")
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Chance')
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity / Recall)")
    plt.title("Receiver Operating Characteristic (ROC) Curve Comparison", fontsize=12, pad=15)
    plt.legend(loc="lower right")
    plt.tight_layout()
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
    plt.close('all')

def threshold_analysis(model, X_test, y_test, thresholds=None):
    if thresholds is None:
        thresholds = np.arange(0.1, 1.0, 0.05)
    
    probs = model.predict_proba(X_test)[:, 1]
    rows = []
    for th in thresholds:
        custom_preds = (probs >= th).astype(int)
        prec = precision_score(y_test, custom_preds, zero_division=0)
        rec = recall_score(y_test, custom_preds, zero_division=0)
        f1 = f1_score(y_test, custom_preds, zero_division=0)
        acc = accuracy_score(y_test, custom_preds)
        rows.append({"Threshold": round(th, 2), "Accuracy": round(acc, 4), "Precision": round(prec, 4), "Recall": round(rec, 4), "F1-Score": round(f1, 4)})
    
    return pd.DataFrame(rows)

def categorize_purchase_risk(X_test, y_test, model):
    probs = model.predict_proba(X_test)[:, 1]
    df_res = X_test.copy()
    df_res["ActualPurchase"] = y_test.values
    df_res["PurchaseProbability"] = np.round(probs, 4)
    df_res["PurchaseLikelihoodTier"] = pd.cut(
        df_res["PurchaseProbability"],
        bins=[0.0, 0.30, 0.60, 1.0],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )
    return df_res
