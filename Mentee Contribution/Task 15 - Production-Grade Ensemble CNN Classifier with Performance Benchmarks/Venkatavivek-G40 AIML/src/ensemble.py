"""Inference Combination Engine and Voting Mechanisms."""

import numpy as np


def majority_voting_predict(predictions_list: list[np.ndarray]) -> np.ndarray:
    """Computes hard majority vote across output prediction matrices.

    Args:
        predictions_list: List of class-probability arrays (N, NumClasses) per model.

    Returns:
        1D numpy array containing ensemble discrete class decisions.
    """
    class_preds = [np.argmax(p, axis=1) for p in predictions_list]
    stacked = np.vstack(class_preds)
    majority_vote, _ = np.apply_along_axis(
        lambda x: np.bincount(x, minlength=predictions_list[0].shape[1]),
        axis=0,
        arr=stacked,
    ), None

    # Alternative row-wise argmax over bincounts
    votes = np.array(
        [
            np.argmax(
                np.bincount(
                    stacked[:, i], minlength=predictions_list[0].shape[1]
                )
            )
            for i in range(stacked.shape[1])
        ]
    )
    return votes


def soft_voting_predict(predictions_list: list[np.ndarray]) -> np.ndarray:
    """Computes unweighted average probability matrix across models.

    Args:
        predictions_list: List of probability arrays (N, NumClasses).

    Returns:
        Averaged class-probability array (N, NumClasses).
    """
    return np.mean(predictions_list, axis=0)


def weighted_soft_voting_predict(
    predictions_list: list[np.ndarray], weights: list[float]
) -> np.ndarray:
    """Computes weighted linear combination of output probability distributions.

    Args:
        predictions_list: List of probability arrays (N, NumClasses).
        weights: List of floating-point weights matching models count.

    Returns:
        Weighted probability array (N, NumClasses).
    """
    normalized_weights = np.array(weights) / np.sum(weights)
    weighted_preds = [
        pred * w for pred, w in zip(predictions_list, normalized_weights)
    ]
    return np.sum(weighted_preds, axis=0)