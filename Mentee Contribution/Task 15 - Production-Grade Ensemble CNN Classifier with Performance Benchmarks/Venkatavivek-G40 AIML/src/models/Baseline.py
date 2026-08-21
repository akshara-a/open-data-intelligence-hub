"""Baseline CNN Model Architecture."""

import tensorflow as tf
from tensorflow.keras import layers, models


def build_baseline_cnn(
    input_shape: tuple[int, int, int] = (32, 32, 3), num_classes: int = 10
) -> models.Sequential:
    """Builds a simple reference CNN model without advanced regularization.

    Args:
        input_shape: Dimensions of the input images (H, W, C).
        num_classes: Number of target output classes.

    Returns:
        tf.keras.models.Sequential: Uncompiled Keras sequential model.
    """
    model = models.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.Flatten(),
            layers.Dense(64, activation="relu"),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="CNN_Baseline",
    )
    return model