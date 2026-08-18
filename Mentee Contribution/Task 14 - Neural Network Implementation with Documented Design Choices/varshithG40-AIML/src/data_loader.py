import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tensorflow as tf
from tensorflow.keras import layers

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

def get_data_augmentation():
    """
    Returns data augmentation sequence for training data.
    Augmentation handles real-world variations: product orientation, slight rotation,
    zoom changes, and lighting/contrast shifts.
    """
    return tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.05),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10)
    ], name="data_augmentation")

def load_datasets(data_dir: str = "data"):
    """
    Loads train, validation, and test datasets from directory.
    Resizes images to (224, 224) with batch size 32 and binary labels.
    """
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{data_dir}/train",
        class_names=["ok_front", "def_front"],
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=True,
        seed=42
    )

    val_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{data_dir}/val",
        class_names=["ok_front", "def_front"],
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )

    test_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{data_dir}/test",
        class_names=["ok_front", "def_front"],
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )

    # Cache and Prefetch for high performance training
    train_dataset = train_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_dataset = val_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    test_dataset = test_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_dataset, val_dataset, test_dataset
