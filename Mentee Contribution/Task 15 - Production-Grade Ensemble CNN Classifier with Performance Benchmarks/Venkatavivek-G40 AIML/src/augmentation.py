"""GPU-Accelerated In-Graph Data Augmentation Sequential Pipeline."""

import tensorflow as tf
from tensorflow.keras import layers, models


def build_augmentation_pipeline(
    input_shape: tuple[int, int, int] = (32, 32, 3)
) -> models.Sequential:
    """Constructs a Keras Sequential model for real-time training augmentation.

    Args:
        input_shape: Dimensions of training image tensors.

    Returns:
        tf.keras.models.Sequential: Augmentation pipeline layer stack.
    """
    return models.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.08, 0.08),
        ],
        name="Data_Augmentation_Pipeline",
    )