import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


IMG_SIZE = (224, 224, 3)


def build_baseline_cnn():
    """
    Build the baseline CNN architecture.

    Binary classification:
        0 = defective
        1 = non-defective
    """

    model = keras.Sequential(
        [
            keras.Input(shape=IMG_SIZE),

            layers.Conv2D(
                32,
                (3, 3),
                activation="relu",
                padding="same"
            ),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(
                64,
                (3, 3),
                activation="relu",
                padding="same"
            ),
            layers.MaxPooling2D((2, 2)),

            layers.Conv2D(
                128,
                (3, 3),
                activation="relu",
                padding="same"
            ),
            layers.MaxPooling2D((2, 2)),

            layers.GlobalAveragePooling2D(),

            layers.Dense(64, activation="relu"),

            layers.Dense(1, activation="sigmoid"),
        ],
        name="baseline_cnn",
    )

    return model


if __name__ == "__main__":
    model = build_baseline_cnn()

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