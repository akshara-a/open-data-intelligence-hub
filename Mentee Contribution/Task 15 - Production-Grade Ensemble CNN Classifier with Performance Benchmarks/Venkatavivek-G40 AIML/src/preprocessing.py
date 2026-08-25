"""Image Scaling and Vector Formatting Modules."""

import numpy as np
import tensorflow as tf


def normalize_images(images: np.ndarray) -> np.ndarray:
    """Normalizes image pixel dynamic range from [0, 255] to [0.0, 1.0].

    Args:
        images: Array of raw image tensors.

    Returns:
        Float32 numpy array normalized to [0.0, 1.0].
    """
    return images.astype("float32") / 255.0


def preprocess_dataset(
    images: np.ndarray, labels: np.ndarray, num_classes: int = 10
) -> tuple[np.ndarray, np.ndarray]:
    """Applies end-to-end preprocessing pipeline to data arrays.

    Args:
        images: Raw input image array.
        labels: Integer label vector.
        num_classes: Total target categories.

    Returns:
        Tuple of (normalized_images, one_hot_encoded_labels).
    """
    x_norm = normalize_images(images)
    y_cat = tf.keras.utils.to_categorical(labels, num_classes)
    return x_norm, y_cat