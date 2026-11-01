"""
ensemble.py
===========
Implements the core Ensemble combination algorithms:
  1. Majority Voting (Hard Voting)
  2. Soft Voting (Arithmetic Mean of Probabilities)
  3. Weighted Soft Voting (Validation-tuned weights)
Also provides model disagreement analysis and ensemble confusion matrix generation.
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from tensorflow import keras

try:
    from .preprocessing import load_full_dataset, CLASSES
    from .evaluate import plot_confusion_matrix
except (ImportError, ValueError):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.preprocessing import load_full_dataset, CLASSES
    from src.evaluate import plot_confusion_matrix

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")


class EnsembleClassifier:
    """
    Ensemble classifier encapsulating multiple CNN models.
    Supports Hard (Majority) Voting, Soft Voting, and Weighted Soft Voting.
    """
    def __init__(self, models: list = None, model_weights: list = None):
        self.models = models or []
        self.model_weights = model_weights

    def load_models_from_disk(self):
        """Loads default checkpointed CNNs from models/ directory."""
        self.models = [
            keras.models.load_model(os.path.join(MODELS_DIR, "cnn_baseline.keras")),
            keras.models.load_model(os.path.join(MODELS_DIR, "cnn_regularized.keras")),
            keras.models.load_model(os.path.join(MODELS_DIR, "cnn_deep.keras"))
        ]
        return self

    def compute_validation_weights(self, X_val: np.ndarray, y_val: np.ndarray) -> np.ndarray:
        """
        Derives ensemble weights from validation dataset performance to prevent test leakage (Section 43).
        Weights are normalized proportional to validation accuracies.
        """
        y_val_indices = np.argmax(y_val, axis=1)
        val_accuracies = []
        
        for model in self.models:
            probs = model.predict(X_val, verbose=0)
            preds = np.argmax(probs, axis=1)
            acc = accuracy_score(y_val_indices, preds)
            val_accuracies.append(max(acc, 0.10))  # lower-bound to avoid zero weight
            
        val_accuracies = np.array(val_accuracies, dtype=np.float32)
        # Normalize weights so they sum to 1.0
        self.model_weights = val_accuracies / np.sum(val_accuracies)
        print(f"[ENSEMBLE] Computed validation weights: {self.model_weights.round(3).tolist()}")
        return self.model_weights

    def get_individual_probabilities(self, X: np.ndarray) -> np.ndarray:
        """
        Runs all models and returns an array of shape (num_models, N, num_classes).
        """
        all_probs = [model.predict(X, verbose=0) for model in self.models]
        return np.array(all_probs)  # (3, N, 2)

    def predict_majority_voting(self, X: np.ndarray) -> np.ndarray:
        """
        Ensemble Method 1 — Majority Voting (Hard Voting).
        Takes the mode of the discrete class predictions from each CNN.
        """
        all_probs = self.get_individual_probabilities(X)  # (3, N, 2)
        all_preds = np.argmax(all_probs, axis=2)          # (3, N)
        majority_preds, _ = stats.mode(all_preds, axis=0, keepdims=False)
        return majority_preds

    def predict_soft_voting(self, X: np.ndarray) -> tuple:
        """
        Ensemble Method 2 — Soft Voting.
        Averages class probability distributions across all models.
        Returns (mean_probabilities, predicted_classes).
        """
        all_probs = self.get_individual_probabilities(X)  # (3, N, 2)
        mean_probs = np.mean(all_probs, axis=0)           # (N, 2)
        preds = np.argmax(mean_probs, axis=1)
        return mean_probs, preds

    def predict_weighted_soft_voting(self, X: np.ndarray, weights: np.ndarray = None) -> tuple:
        """
        Ensemble Method 3 — Weighted Soft Voting.
        Combines model predictions using validation-calibrated weights.
        Returns (weighted_probabilities, predicted_classes).
        """
        if weights is None:
            if self.model_weights is None:
                weights = np.ones(len(self.models)) / len(self.models)
            else:
                weights = self.model_weights
                
        all_probs = self.get_individual_probabilities(X)  # (3, N, 2)
        weighted_probs = np.tensordot(weights, all_probs, axes=(0, 0))  # (N, 2)
        preds = np.argmax(weighted_probs, axis=1)
        return weighted_probs, preds

    def analyze_disagreements(self, X: np.ndarray, y_true_one_hot: np.ndarray) -> dict:
        """
        Analyzes when models agree and disagree (Sections 59-60).
        """
        y_true = np.argmax(y_true_one_hot, axis=1)
        all_probs = self.get_individual_probabilities(X)  # (3, N, 2)
        all_preds = np.argmax(all_probs, axis=2)          # (3, N)
        N = len(y_true)
        
        unanimous_agree = 0
        two_agree = 0
        all_disagree = 0
        ensemble_fixed_errors = 0
        
        soft_probs, soft_preds = self.predict_soft_voting(X)
        
        for i in range(N):
            sample_preds = all_preds[:, i]
            unique_preds, counts = np.unique(sample_preds, return_counts=True)
            max_count = np.max(counts)
            
            if max_count == 3:
                unanimous_agree += 1
            elif max_count == 2:
                two_agree += 1
                wrong_models = np.sum(sample_preds != y_true[i])
                if wrong_models == 1 and soft_preds[i] == y_true[i]:
                    ensemble_fixed_errors += 1
            else:
                all_disagree += 1
                
        disagreement_metrics = {
            "Total Samples": N,
            "Unanimous Agreement": unanimous_agree,
            "Unanimous Agreement Rate (%)": round(unanimous_agree / N * 100, 2),
            "Partial Agreement (2 vs 1)": two_agree,
            "Partial Agreement Rate (%)": round(two_agree / N * 100, 2),
            "Complete Disagreement": all_disagree,
            "Errors Fixed by Ensemble": ensemble_fixed_errors
        }
        return disagreement_metrics


def evaluate_all_ensembles(ensemble: EnsembleClassifier = None) -> tuple:
    """
    Evaluates Majority Voting, Soft Voting, and Weighted Soft Voting on the test set.
    """
    (X_train, y_train), (X_val, y_val), (X_test, y_test), _ = load_full_dataset()
    y_test_indices = np.argmax(y_test, axis=1)
    
    if ensemble is None:
        ensemble = EnsembleClassifier()
        ensemble.load_models_from_disk()
        
    ensemble.compute_validation_weights(X_val, y_val)
    
    print("\n=======================================================")
    print(" Evaluating Ensemble Strategies on Test Dataset")
    print("=======================================================")
    
    # 1. Majority Voting
    maj_preds = ensemble.predict_majority_voting(X_test)
    maj_acc = accuracy_score(y_test_indices, maj_preds)
    maj_prec = precision_score(y_test_indices, maj_preds, average="macro", zero_division=0)
    maj_rec = recall_score(y_test_indices, maj_preds, average="macro", zero_division=0)
    maj_f1 = f1_score(y_test_indices, maj_preds, average="macro", zero_division=0)
    
    # 2. Soft Voting
    soft_probs, soft_preds = ensemble.predict_soft_voting(X_test)
    soft_acc = accuracy_score(y_test_indices, soft_preds)
    soft_prec = precision_score(y_test_indices, soft_preds, average="macro", zero_division=0)
    soft_rec = recall_score(y_test_indices, soft_preds, average="macro", zero_division=0)
    soft_f1 = f1_score(y_test_indices, soft_preds, average="macro", zero_division=0)
    soft_loss = log_loss(y_test, soft_probs)
    
    # Plot Ensemble Confusion Matrix
    cm_path = os.path.join(RESULTS_DIR, "confusion_matrix_ensemble.png")
    plot_confusion_matrix(y_test_indices, soft_preds, "Ensemble (Soft Voting)", cm_path)
    
    # 3. Weighted Soft Voting
    w_probs, w_preds = ensemble.predict_weighted_soft_voting(X_test)
    w_acc = accuracy_score(y_test_indices, w_preds)
    w_prec = precision_score(y_test_indices, w_preds, average="macro", zero_division=0)
    w_rec = recall_score(y_test_indices, w_preds, average="macro", zero_division=0)
    w_f1 = f1_score(y_test_indices, w_preds, average="macro", zero_division=0)
    w_loss = log_loss(y_test, w_probs)
    
    results = [
        {"Ensemble Method": "Majority Voting (Hard)", "Accuracy (%)": round(maj_acc * 100, 2), "Precision (%)": round(maj_prec * 100, 2), "Recall (%)": round(maj_rec * 100, 2), "F1-score (%)": round(maj_f1 * 100, 2), "Loss": "N/A"},
        {"Ensemble Method": "Soft Voting (Average)", "Accuracy (%)": round(soft_acc * 100, 2), "Precision (%)": round(soft_prec * 100, 2), "Recall (%)": round(soft_rec * 100, 2), "F1-score (%)": round(soft_f1 * 100, 2), "Loss": round(soft_loss, 4)},
        {"Ensemble Method": "Weighted Soft Voting", "Accuracy (%)": round(w_acc * 100, 2), "Precision (%)": round(w_prec * 100, 2), "Recall (%)": round(w_rec * 100, 2), "F1-score (%)": round(w_f1 * 100, 2), "Loss": round(w_loss, 4)}
    ]
    
    disagreements = ensemble.analyze_disagreements(X_test, y_test)
    print("\n--- Model Disagreement Analysis ---")
    for k, v in disagreements.items():
        print(f"  {k}: {v}")
        
    df = pd.DataFrame(results)
    return df, disagreements


if __name__ == "__main__":
    df, _ = evaluate_all_ensembles()
    print("\n", df.to_string(index=False))
