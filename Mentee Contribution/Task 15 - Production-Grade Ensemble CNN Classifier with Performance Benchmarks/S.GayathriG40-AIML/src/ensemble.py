import numpy as np


def majority_voting(
    prediction_arrays,
    num_classes=10
):

    predictions = np.stack(
        prediction_arrays,
        axis=1
    )

    final_predictions = []

    for row in predictions:

        counts = np.bincount(
            row,
            minlength=num_classes
        )

        final_predictions.append(
            np.argmax(counts)
        )

    return np.array(final_predictions)


def soft_voting(probability_arrays):

    probabilities = np.stack(
        probability_arrays,
        axis=0
    )

    average_probabilities = np.mean(
        probabilities,
        axis=0
    )

    predictions = np.argmax(
        average_probabilities,
        axis=1
    )

    return (
        average_probabilities,
        predictions
    )


def weighted_soft_voting(
    probability_arrays,
    weights
):

    weights = np.array(weights)

    weights = weights / weights.sum()

    result = 0

    for weight, probability in zip(
        weights,
        probability_arrays
    ):

        result = result + (
            weight * probability
        )

    predictions = np.argmax(
        result,
        axis=1
    )

    return result, predictions