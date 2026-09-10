"""deep_cnn.py — deeper CNN with three conv blocks and global average pooling."""

from tensorflow.keras import layers, models
from src.augmentation import build_augmentation


def build_cnn_deep():
    return models.Sequential([
        layers.Input(shape=(32, 32, 3)),
        build_augmentation(),
        layers.Rescaling(1.0 / 255),
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, padding="same", activation="relu"),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.30),
        layers.Dense(10, activation="softmax"),
    ], name="cnn_deep")


if __name__ == "__main__":
    build_cnn_deep().summary()
