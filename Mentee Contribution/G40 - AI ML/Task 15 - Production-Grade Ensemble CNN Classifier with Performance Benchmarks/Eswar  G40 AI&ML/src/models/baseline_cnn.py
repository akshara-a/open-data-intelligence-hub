"""baseline_cnn.py — simple two-conv-block CNN, no regularization."""

from tensorflow.keras import layers, models
from src.augmentation import build_augmentation


def build_cnn_baseline():
    return models.Sequential([
        layers.Input(shape=(32, 32, 3)),
        build_augmentation(),
        layers.Rescaling(1.0 / 255),
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ], name="cnn_baseline")


if __name__ == "__main__":
    build_cnn_baseline().summary()
