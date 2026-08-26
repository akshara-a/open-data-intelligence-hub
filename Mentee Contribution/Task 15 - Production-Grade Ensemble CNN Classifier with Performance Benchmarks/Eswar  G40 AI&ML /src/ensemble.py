"""
ensemble.py

Combines predictions from the three trained CNNs via majority voting,
soft voting, and weighted soft voting (weighted by each model's
validation accuracy).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def get_all_predictions(trained_models, test_images):
    model_names = list(trained_models.keys())
    all_probs = {name: trained_models[name].predict(test_images, batch_size=64, verbose=0)
                 for name in model_names}
    all_preds = {name: np.argmax(all_probs[name], axis=1) for name in model_names}
    return model_names, all_probs, all_preds


def majority_vote(all_preds, model_names, num_classes=10):
    stacked = np.stack([all_preds[name] for name in model_names], axis=1)
    return np.array([np.bincount(row, minlength=num_classes).argmax() for row in stacked]), stacked


def soft_vote(all_probs, model_names):
    soft_probs = np.mean([all_probs[name] for name in model_names], axis=0)
    return np.argmax(soft_probs, axis=1), soft_probs


def weighted_soft_vote(all_probs, model_names, val_accuracies):
    weights = np.array([val_accuracies[name] for name in model_names])
    weights = weights / weights.sum()
    weighted_probs = np.zeros_like(next(iter(all_probs.values())))
    for i, name in enumerate(model_names):
        weighted_probs += weights[i] * all_probs[name]
    return np.argmax(weighted_probs, axis=1), weighted_probs, dict(zip(model_names, weights.tolist()))


def eval_ensemble(preds, test_labels, label, class_names, results_dir="results"):
    acc = accuracy_score(test_labels, preds)
    prec = precision_score(test_labels, preds, average="macro", zero_division=0)
    rec = recall_score(test_labels, preds, average="macro", zero_division=0)
    f1 = f1_score(test_labels, preds, average="macro", zero_division=0)
    cm = confusion_matrix(test_labels, preds)

    plt.figure(figsize=(6, 5))
    plt.imshow(cm, cmap="Greens")
    plt.xticks(range(10), class_names, rotation=90); plt.yticks(range(10), class_names)
    plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.title(f"Ensemble ({label}) Confusion Matrix")
    plt.colorbar(); plt.tight_layout()
    fname = label.lower().replace(" ", "_")
    plt.savefig(os.path.join(results_dir, f"ensemble_{fname}_confusion_matrix.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print(f"{label}: acc={acc:.4f} prec={prec:.4f} rec={rec:.4f} f1={f1:.4f}")
    return {"accuracy": float(acc), "precision_macro": float(prec), "recall_macro": float(rec),
            "f1_macro": float(f1), "confusion_matrix": cm.tolist()}


def disagreement_analysis(stacked_preds, all_preds, soft_preds, test_labels, results, model_names):
    all_agree = np.all(stacked_preds == stacked_preds[:, [0]], axis=1)
    best_individual = max(model_names, key=lambda n: results[n]["test_accuracy"])
    best_individual_wrong = (all_preds[best_individual] != test_labels)

    rescued = int(np.sum(best_individual_wrong & (soft_preds == test_labels)))
    hurt = int(np.sum((~best_individual_wrong) & (soft_preds != test_labels)))

    return {
        "full_agreement_rate": float(all_agree.mean()),
        "disagreement_rate": float(1 - all_agree.mean()),
        "best_individual_model": best_individual,
        "cases_ensemble_fixed_best_individual_mistake": rescued,
        "cases_ensemble_introduced_new_mistake": hurt,
    }
