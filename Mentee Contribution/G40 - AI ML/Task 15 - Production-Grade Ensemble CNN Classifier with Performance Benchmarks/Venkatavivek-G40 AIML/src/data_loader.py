"""Data Ingestion and Standardized Split Management."""

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_cifar10_data(
    val_split: float = 0.15, seed: int = 42
) -> tuple[
    tuple[np.ndarray, np.ndarray],
    tuple[np.ndarray, np.ndarray],
    tuple[np.ndarray, np.ndarray],
    list[str],
]:
    """Loads CIFAR-10 data and establishes strict deterministic splits across all models.

    Args:
        val_split: Fraction of training data allocated for validation.
        seed: Random seed for partition reproducibility.

    Returns:
        Tuple containing (X_train, y_train), (X_val, y_val), (X_test, y_test), and class_names.
    """
    class_names = [
        "airplane",
        "automobile",
        "bird",
        "cat",
        "deer",
        "dog",
        "frog",
        "horse",
        "ship",
        "truck",
    ]

    (x_train_full, y_train_full), (x_test, y_test) = (
        tf.keras.datasets.cifar10.load_data()
    )

    x_train, x_val, y_train, y_val = train_test_split(
        x_train_full,
        y_train_full,
        test_size=val_split,
        random_state=seed,
        stratify=y_train_full,
    )

    return (x_train, y_train), (x_val, y_val), (x_test, y_test), class_names