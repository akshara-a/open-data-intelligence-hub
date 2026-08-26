"""
augmentation.py

Shared data augmentation pipeline, used as the first learned layer inside
each of the three CNN architectures (see src/models/).
"""

import tensorflow as tf
from tensorflow.keras import layers


def build_augmentation():
    return tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomTranslation(0.08, 0.08),
        layers.RandomContrast(0.10),
        layers.RandomBrightness(0.10),
    ], name="data_augmentation")
