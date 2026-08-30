import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers

from src.augmentation import get_augmentation


IMG_SIZE = (224, 224, 3)


def build_deep_cnn():
    """
    Build the deeper CNN architecture.

    Uses:
    - Data augmentation
    - Multiple convolutional blocks
    - Batch Normalization
    - Dropout
    - L2 regularization
    - Global Average Pooling

    Binary classification:
        0 = defective
        1 = non-defective
    """

    model = keras.Sequential(
        [
            keras.Input(shape=IMG_SIZE),

            get_augmentation(),

            layers.Rescaling(1.0 / 255.0),

            # Block 1
            layers.Conv2D(
                32,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.Conv2D(
                32,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.15),

            # Block 2
            layers.Conv2D(
                64,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.Conv2D(
                64,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.20),

            # Block 3
            layers.Conv2D(
                128,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.Conv2D(
                128,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Block 4
            layers.Conv2D(
                256,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.Conv2D(
                256,
                (3, 3),
                padding="same",
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.30),

            layers.GlobalAveragePooling2D(),

            layers.Dense(
                128,
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),
            layers.BatchNormalization(),
            layers.Dropout(0.40),

            layers.Dense(1, activation="sigmoid"),
        ],
        name="deep_cnn",
    )

    return model


if __name__ == "__main__":
    model = build_deep_cnn()

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall"),
        ],
    )

    model.summary()