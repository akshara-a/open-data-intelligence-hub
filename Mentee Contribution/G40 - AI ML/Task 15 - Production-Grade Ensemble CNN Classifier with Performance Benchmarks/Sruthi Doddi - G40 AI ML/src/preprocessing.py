"""
Part 1 — Dataset preparation: normalization (Section 14).
"""

import numpy as np
from tensorflow.keras.utils import to_categorical

NUM_CLASSES = 10


def normalize_images(x):
    """Scale pixel values from [0, 255] to [0, 1]."""
    return x.astype("float32") / 255.0


def encode_labels(y, num_classes=NUM_CLASSES):
    """One-hot encode integer class labels."""
    return to_categorical(y, num_classes=num_classes)


def prepare_dataset(x_train, y_train, x_val, y_val, x_test, y_test):
    x_train = normalize_images(x_train)
    x_val = normalize_images(x_val)
    x_test = normalize_images(x_test)

    y_train = encode_labels(y_train)
    y_val = encode_labels(y_val)
    y_test = encode_labels(y_test)

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)


if __name__ == "__main__":
    from data_loader import load_cifar10

    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )
    print("Pixel range:", x_train.min(), "-", x_train.max())
    print("Label shape:", y_train.shape)
