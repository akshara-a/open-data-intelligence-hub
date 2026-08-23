"""Deep CNN Model Architecture."""

import tensorflow as tf
from tensorflow.keras import layers, models


def build_deep_cnn(
    input_shape: tuple[int, int, int] = (32, 32, 3), num_classes: int = 10
) -> models.Sequential:
    """Builds a deeper CNN utilizing Global Average Pooling.

    Args:
        input_shape: Dimensions of the input images (H, W, C).
        num_classes: Number of target output classes.

    Returns:
        tf.keras.models.Sequential: Uncompiled Keras sequential model.
    """
    model = models.Sequential(
        [
            layers.Input(shape=input_shape),
            # Block 1
            layers.Conv2D(32, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Conv2D(32, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            # Block 2
            layers.Conv2D(64, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Conv2D(64, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            # Block 3
            layers.Conv2D(128, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.Conv2D(128, (3, 3), padding="same"),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.4),
            # Dense Classifier with GAP
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation="relu"),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ],
        name="CNN_Deep",
    )
    return model