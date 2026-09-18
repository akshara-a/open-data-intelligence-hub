import numpy as np


def average_predictions(predictions_1, predictions_2):
    """
    Combine predictions from two CNN models
    by averaging their probabilities.
    """

    ensemble_predictions = (
        predictions_1 + predictions_2
    ) / 2

    return ensemble_predictions


def get_ensemble_labels(ensemble_predictions):
    """
    Select the class with the highest probability.
    """

    ensemble_labels = np.argmax(
        ensemble_predictions,
        axis=1
    )

    return ensemble_labels


def calculate_ensemble_accuracy(
    ensemble_predictions,
    y_test
):
    """
    Calculate ensemble classification accuracy.
    """

    ensemble_labels = get_ensemble_labels(
        ensemble_predictions
    )

    accuracy = np.mean(
        ensemble_labels == y_test
    )

    return accuracy