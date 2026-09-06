import tensorflow as tf
from tensorflow.keras import layers


def get_augmentation():
    """
    Data augmentation used during training.

    These transformations are intentionally moderate so that
    manufacturing defect features are not destroyed.
    """

    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.05),
            layers.RandomZoom(0.10),
            layers.RandomTranslation(0.05, 0.05),
            layers.RandomContrast(0.10),
        ],
        name="data_augmentation",
    )