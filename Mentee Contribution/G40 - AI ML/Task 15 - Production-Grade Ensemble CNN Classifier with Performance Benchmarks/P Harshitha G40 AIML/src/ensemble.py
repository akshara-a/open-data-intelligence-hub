import os

# pyrefly: ignore [missing-import]
import torch

# pyrefly: ignore [missing-import]
import numpy as np

# pyrefly: ignore [missing-import]
from scipy.stats import mode
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)

from data_loader import get_data_loaders
from preprocessing import get_base_transform
from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN
from evaluate import plot_confusion_matrix


def load_all_models():
    """
    Loads all trained CNN models and sets them to evaluation mode.
    """

    models = {
        "cnn1": BaselineCNN(),
        "cnn2": RegularizedCNN(),
        "cnn3": DeepCNN(),
    }

    paths = {
        "cnn1": "./models/cnn_baseline.keras",
        "cnn2": "./models/cnn_regularized.keras",
        "cnn3": "./models/cnn_deep.keras",
    }

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    loaded_models = {}

    for key, model in models.items():

        if os.path.exists(paths[key]):

            model.load_state_dict(
                torch.load(
                    paths[key],
                    map_location=device,
                )
            )

            model.to(device)
            model.eval()

            loaded_models[key] = model

            print(f"Loaded {key} from {paths[key]}")

        else:
            raise FileNotFoundError(
                f"Model checkpoint for {key} missing at {paths[key]}"
            )

    return loaded_models, device


def collect_predictions_and_probs(models, test_loader, device):
    """
    Collects prediction probabilities and predicted class labels
    from each model.
    """

    model_probs = {
        key: []
        for key in models.keys()
    }

    targets = []

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)

            targets.extend(
                labels.cpu().numpy()
            )

            for key, model in models.items():

                outputs = model(images)

                probs = torch.softmax(
                    outputs,
                    dim=1
                ).cpu().numpy()

                model_probs[key].extend(probs)

    for key in model_probs:

        model_probs[key] = np.array(
            model_probs[key]
        )

    targets = np.array(targets)

    return model_probs, targets


def majority_voting(model_probs):
    """
    Majority (Hard) Voting:
    Selects the class receiving the highest number of votes.
    """

    preds_list = [
        np.argmax(
            model_probs[key],
            axis=1
        )
        for key in model_probs.keys()
    ]

    preds_matrix = np.column_stack(
        preds_list
    )

    majority_preds, _ = mode(
        preds_matrix,
        axis=1,
        keepdims=False
    )

    return np.asarray(
        majority_preds
    ).ravel()


def soft_voting(model_probs):
    """
    Soft Voting:
    Averages prediction probabilities across all models
    and selects the class with the highest average probability.
    """

    avg_probs = np.mean(
        list(model_probs.values()),
        axis=0
    )

    final_preds = np.argmax(
        avg_probs,
        axis=1
    )

    return final_preds, avg_probs


def weighted_soft_voting(model_probs, weights):
    """
    Weighted Soft Voting:
    Calculates a weighted average of prediction probabilities.
    """

    first_probs = list(
        model_probs.values()
    )[0]

    weighted_probs = np.zeros_like(
        first_probs
    )

    for key, weight in weights.items():

        weighted_probs += (
            weight * model_probs[key]
        )

    final_preds = np.argmax(
        weighted_probs,
        axis=1
    )

    return final_preds, weighted_probs


def calculate_metrics(targets, predictions):
    """
    Calculates accuracy, precision, recall and F1-score.
    """

    accuracy = accuracy_score(
        targets,
        predictions
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            targets,
            predictions,
            average="macro",
            zero_division=0,
        )
    )

    return accuracy, precision, recall, f1


def evaluate_ensemble():

    print("\n=== Loading Dataset ===")

    eval_transform = get_base_transform()

    _, val_loader, test_loader, classes = get_data_loaders(
        batch_size=64,
        eval_transform=eval_transform,
    )

    print("\n=== Loading Trained Models ===")

    models, device = load_all_models()

    print(
        f"\nEnsemble evaluation running on device: {device}"
    )

    print("\n=== Collecting Test Predictions ===")

    model_probs, targets = (
        collect_predictions_and_probs(
            models,
            test_loader,
            device,
        )
    )

    # ---------------------------------------------------------
    # 1. MAJORITY / HARD VOTING
    # ---------------------------------------------------------

    print("\n=== Majority Voting ===")

    maj_preds = majority_voting(
        model_probs
    )

    maj_acc, maj_p, maj_r, maj_f1 = (
        calculate_metrics(
            targets,
            maj_preds,
        )
    )

    # ---------------------------------------------------------
    # 2. SOFT VOTING
    # ---------------------------------------------------------

    print("\n=== Soft Voting ===")

    soft_preds, soft_probs = soft_voting(
        model_probs
    )

    soft_acc, soft_p, soft_r, soft_f1 = (
        calculate_metrics(
            targets,
            soft_preds,
        )
    )

    # ---------------------------------------------------------
    # 3. VALIDATION ACCURACY WEIGHTS
    # ---------------------------------------------------------

    print("\n=== Calculating Validation Weights ===")

    val_probs, val_targets = (
        collect_predictions_and_probs(
            models,
            val_loader,
            device,
        )
    )

    val_accs = {}

    for key in models.keys():

        val_predictions = np.argmax(
            val_probs[key],
            axis=1,
        )

        val_accs[key] = accuracy_score(
            val_targets,
            val_predictions,
        )

    total_val_acc = sum(
        val_accs.values()
    )

    weights = {
        key: val_accs[key] / total_val_acc
        for key in val_accs.keys()
    }

    print("\nValidation Accuracies:")

    for key, value in val_accs.items():

        print(
            f"{key}: {value * 100:.2f}%"
        )

    print("\nModel Weights:")

    for key, value in weights.items():

        print(
            f"{key}: {value:.4f}"
        )

    # ---------------------------------------------------------
    # 4. WEIGHTED SOFT VOTING
    # ---------------------------------------------------------

    print("\n=== Weighted Soft Voting ===")

    weighted_preds, weighted_probs = (
        weighted_soft_voting(
            model_probs,
            weights,
        )
    )

    w_acc, w_p, w_r, w_f1 = (
        calculate_metrics(
            targets,
            weighted_preds,
        )
    )

    # ---------------------------------------------------------
    # 5. CONFUSION MATRIX FOR SOFT VOTING
    # ---------------------------------------------------------

    cm_ensemble = confusion_matrix(
        targets,
        soft_preds,
    )

    plot_confusion_matrix(
        cm_ensemble,
        classes,
        "Soft Voting Ensemble",
        "./results/confusion_matrix_ensemble.png",
    )

    # ---------------------------------------------------------
    # 6. PRINT FINAL RESULTS
    # ---------------------------------------------------------

    print(
        "\n=============================================="
    )

    print(
        "        ENSEMBLE PERFORMANCE RESULTS"
    )

    print(
        "=============================================="
    )

    print(
        f"\n1. Majority (Hard) Voting"
    )
    print(
        f"   Accuracy : {maj_acc * 100:.2f}%"
    )
    print(
        f"   Precision: {maj_p * 100:.2f}%"
    )
    print(
        f"   Recall   : {maj_r * 100:.2f}%"
    )
    print(
        f"   F1-Score : {maj_f1 * 100:.2f}%"
    )

    print(
        f"\n2. Soft Voting"
    )
    print(
        f"   Accuracy : {soft_acc * 100:.2f}%"
    )
    print(
        f"   Precision: {soft_p * 100:.2f}%"
    )
    print(
        f"   Recall   : {soft_r * 100:.2f}%"
    )
    print(
        f"   F1-Score : {soft_f1 * 100:.2f}%"
    )

    print(
        f"\n3. Weighted Soft Voting"
    )
    print(
        f"   Accuracy : {w_acc * 100:.2f}%"
    )
    print(
        f"   Precision: {w_p * 100:.2f}%"
    )
    print(
        f"   Recall   : {w_r * 100:.2f}%"
    )
    print(
        f"   F1-Score : {w_f1 * 100:.2f}%"
    )

    print(
        "\n=============================================="
    )

    return {
        "majority": {
            "accuracy": maj_acc,
            "precision": maj_p,
            "recall": maj_r,
            "f1_score": maj_f1,
            "preds": maj_preds,
        },

        "soft": {
            "accuracy": soft_acc,
            "precision": soft_p,
            "recall": soft_r,
            "f1_score": soft_f1,
            "preds": soft_preds,
            "probs": soft_probs,
        },

        "weighted": {
            "accuracy": w_acc,
            "precision": w_p,
            "recall": w_r,
            "f1_score": w_f1,
            "preds": weighted_preds,
            "probs": weighted_probs,
        },

        "targets": targets,

        "model_probs": model_probs,

        "validation_accuracies": val_accs,

        "weights": weights,
    }


if __name__ == "__main__":
    evaluate_ensemble()