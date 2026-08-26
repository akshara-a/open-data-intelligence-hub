"""regularized_cnn.py — batch-norm + dropout regularized CNN."""

from tensorflow.keras import layers, models
from src.augmentation import build_augmentation


def build_cnn_regularized():
    return models.Sequential([
        layers.Input(shape=(32, 32, 3)),
        build_augmentation(),
        layers.Rescaling(1.0 / 255),
        layers.Conv2D(32, 3, padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),
        layers.Conv2D(64, 3, padding="same"),
        layers.BatchNormalization(),
        layers.Activation("relu"),
        layers.MaxPooling2D(),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.40),
        layers.Dense(10, activation="softmax"),
    ], name="cnn_regularized")


if __name__ == "__main__":
    build_cnn_regularized().summary()
