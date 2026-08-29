import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers

from src.augmentation import get_augmentation


IMG_SIZE = (224, 224, 3)


def build_regularized_cnn():
    """
    Build the regularized CNN architecture.

    Uses:
    - Data augmentation
    - Batch Normalization
    - L2 regularization
    - Dropout

    Binary classification:
        0 = defective
        1 = non-defective
    """

    model = keras.Sequential(
        [
            keras.Input(shape=IMG_SIZE),

            get_augmentation(),

            layers.Rescaling(1.0 / 255.0),

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

            layers.GlobalAveragePooling2D(),

            layers.Dense(
                64,
                activation="relu",
                kernel_regularizer=regularizers.l2(1e-4),
            ),

            layers.Dropout(0.40),

            layers.Dense(1, activation="sigmoid"),
        ],
        name="regularized_cnn",
    )

    return model


if __name__ == "__main__":
    model = build_regularized_cnn()

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