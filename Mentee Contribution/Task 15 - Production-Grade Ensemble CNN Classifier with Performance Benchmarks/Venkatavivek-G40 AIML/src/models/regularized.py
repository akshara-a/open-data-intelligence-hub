"""Regularized CNN Model Architecture."""

import tensorflow as tf
from tensorflow.keras import layers, models


def build_regularized_cnn(
    input_shape: tuple[int, int, int] = (32, 32, 3), num_classes: int = 10
) -> models.Sequential:
    """Builds a CNN with Batch Normalization and Dropout layers.

    Args:
        input_shape: Dimensions of the input images (H, W, C).
        num_classes: Number of target output classes.

    Returns:
        tf.keras.models.Sequential: Uncompiled Keras sequential model.
    """
    model = models.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(32, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Conv2D(32, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            layers.Conv2D(64, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Conv2D(64, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.35),
            layers.Flatten(),
            layers.Dense(128),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="CNN_Regularized",
    )
    return model