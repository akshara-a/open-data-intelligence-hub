"""
Part 1 — Dataset
Loads CIFAR-10, creates a fixed train/val/test split shared by all CNNs.
"""

import os
import numpy as np
from tensorflow.keras.datasets import cifar10

CLASS_NAMES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

SEED = 42  # fixed seed so every model trains/tests on the same split


def load_cifar10(val_fraction=0.15):
    """
    Returns (x_train, y_train), (x_val, y_val), (x_test, y_test).
    Uses Keras's built-in downloader (chunked + retry-safe).
    Test set is untouched — only the original training set is split
    into train/val, per the guide's fair-comparison rule (Section 13).
    """
    (x_train_full, y_train_full), (x_test, y_test) = cifar10.load_data()

    rng = np.random.default_rng(seed=SEED)
    n = len(x_train_full)
    idx = rng.permutation(n)

    val_size = int(val_fraction * n)
    val_idx = idx[:val_size]
    train_idx = idx[val_size:]

    x_train, y_train = x_train_full[train_idx], y_train_full[train_idx]
    x_val, y_val = x_train_full[val_idx], y_train_full[val_idx]

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)


def visualize_samples(x, y, class_names=CLASS_NAMES, n=10, save_path=None):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    for i, ax in enumerate(axes.flat):
        ax.imshow(x[i])
        ax.set_title(class_names[int(y[i])])
        ax.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


if __name__ == "__main__":
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()

    print("Train:", x_train.shape, y_train.shape)
    print("Val:  ", x_val.shape, y_val.shape)
    print("Test: ", x_test.shape, y_test.shape)
    print("Classes:", CLASS_NAMES)

    os.makedirs("results", exist_ok=True)
    visualize_samples(x_train, y_train, save_path="results/sample_images.png")
