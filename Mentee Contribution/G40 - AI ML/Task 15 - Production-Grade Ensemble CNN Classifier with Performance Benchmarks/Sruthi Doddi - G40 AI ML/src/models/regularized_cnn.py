"""
Part 4 — CNN Model 2: Regularized CNN (Section 17).
Adds Batch Normalization + Dropout to reduce overfitting (Sections 18-19).
"""

from tensorflow.keras import layers, models


def build_regularized_cnn(input_shape=(32, 32, 3), num_classes=10, dropout_rate=0.3):
    model = models.Sequential(name="cnn_regularized")
    model.add(layers.Input(shape=input_shape))

    model.add(layers.Conv2D(32, (3, 3), padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(dropout_rate))

    model.add(layers.Conv2D(64, (3, 3), padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(dropout_rate))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(dropout_rate))
    model.add(layers.Dense(num_classes, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    build_regularized_cnn().summary()
