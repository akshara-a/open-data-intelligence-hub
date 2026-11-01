"""
Part 5 — CNN Model 3: Deeper CNN (Section 20).
Extra conv layers + Global Average Pooling for more complex features.
"""

from tensorflow.keras import layers, models


def build_deep_cnn(input_shape=(32, 32, 3), num_classes=10):
    model = models.Sequential(name="cnn_deep")
    model.add(layers.Input(shape=input_shape))

    model.add(layers.Conv2D(32, (3, 3), padding="same", activation="relu"))
    model.add(layers.Conv2D(32, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(layers.Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3), padding="same", activation="relu"))
    model.add(layers.BatchNormalization())

    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(num_classes, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    build_deep_cnn().summary()
