import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from src.predict import (
    load_model,
    get_predictions
)

from src.data_loader import CLASS_NAMES


def evaluate_model(
    model,
    X_test,
    y_test
):

    probabilities, predictions = (
        get_predictions(
            model,
            X_test
        )
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("Accuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1 Score :", f1)

    print(
        classification_report(
            y_test,
            predictions,
            target_names=CLASS_NAMES,
            zero_division=0
        )
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "confusion_matrix": cm,
        "probabilities": probabilities,
        "predictions": predictions
    }