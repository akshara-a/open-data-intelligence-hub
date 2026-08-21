"""
Part 3 — CNN Model 1: Baseline CNN (Section 16).
Simple reference architecture; no regularization tricks.
"""

from tensorflow.keras import layers, models


def build_baseline_cnn(input_shape=(32, 32, 3), num_classes=10):
    model = models.Sequential(name="cnn_baseline")
    model.add(layers.Input(shape=input_shape))

    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(num_classes, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    build_baseline_cnn().summary()
