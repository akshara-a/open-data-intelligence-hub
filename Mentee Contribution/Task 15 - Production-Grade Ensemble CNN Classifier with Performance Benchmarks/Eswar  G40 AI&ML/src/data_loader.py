"""
data_loader.py

Loads the CIFAR-10 dataset for the ensemble CNN classifier project.

Supports two sources:
  1. CSV files (cifar10_train.csv / cifar10_test.csv) with flattened pixel
     columns + a 'label' column — produced by scripts/build_cifar10_csv.py
  2. Image folders (cifar10_data/train/<class>/, cifar10_data/test/<class>/)
     — produced by scripts/build_cifar10_folders.py

Both paths return the same thing: numpy arrays for train/val/test images
and labels, plus a tf.data pipeline for training.
"""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

CLASS_NAMES = ["airplane", "automobile", "bird", "cat", "deer",
               "dog", "frog", "horse", "ship", "truck"]
IMAGE_SIZE = (32, 32)
BATCH_SIZE = 32


def load_from_csv(data_dir="cifar10_data", val_split=0.15, seed=42, batch_size=BATCH_SIZE):
    """Load CIFAR-10 from cifar10_train.csv / cifar10_test.csv."""
    train_df = pd.read_csv(os.path.join(data_dir, "cifar10_train.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "cifar10_test.csv"))

    def df_to_arrays(df):
        labels = df["label"].to_numpy()
        pixel_cols = [c for c in df.columns if c.startswith("pixel_")]
        images = df[pixel_cols].to_numpy().reshape(-1, 32, 32, 3).astype(np.uint8)
        return images, labels

    train_images_all, train_labels_all = df_to_arrays(train_df)
    test_images, test_labels = df_to_arrays(test_df)

    train_images, val_images, train_labels, val_labels = train_test_split(
        train_images_all, train_labels_all, test_size=val_split,
        random_state=seed, stratify=train_labels_all)

    train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels)) \
        .shuffle(1000, seed=seed).batch(batch_size)
    validation_dataset = tf.data.Dataset.from_tensor_slices((val_images, val_labels)) \
        .batch(batch_size)

    autotune = tf.data.AUTOTUNE
    return {
        "train_dataset": train_dataset.prefetch(autotune),
        "validation_dataset": validation_dataset.prefetch(autotune),
        "val_images": val_images, "val_labels": val_labels,
        "test_images": test_images, "test_labels": test_labels,
    }


def load_from_image_folders(data_dir="cifar10_data", val_split=0.15, seed=42, batch_size=BATCH_SIZE):
    """Load CIFAR-10 from cifar10_data/train and cifar10_data/test image folders."""
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "train"), class_names=CLASS_NAMES,
        validation_split=val_split, subset="training", seed=seed,
        image_size=IMAGE_SIZE, batch_size=batch_size, label_mode="int")

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "train"), class_names=CLASS_NAMES,
        validation_split=val_split, subset="validation", seed=seed,
        image_size=IMAGE_SIZE, batch_size=batch_size, label_mode="int")

    test_dataset = tf.keras.utils.image_dataset_from_directory(
        os.path.join(data_dir, "test"), class_names=CLASS_NAMES,
        image_size=IMAGE_SIZE, batch_size=batch_size, label_mode="int", shuffle=False)

    def to_numpy(dataset):
        images_list, labels_list = [], []
        for imgs, labels in dataset:
            images_list.append(imgs.numpy())
            labels_list.append(labels.numpy())
        return np.concatenate(images_list, axis=0), np.concatenate(labels_list, axis=0)

    val_images, val_labels = to_numpy(validation_dataset)
    test_images, test_labels = to_numpy(test_dataset)

    autotune = tf.data.AUTOTUNE
    return {
        "train_dataset": train_dataset.prefetch(autotune),
        "validation_dataset": validation_dataset.prefetch(autotune),
        "val_images": val_images, "val_labels": val_labels,
        "test_images": test_images, "test_labels": test_labels,
    }


if __name__ == "__main__":
    data = load_from_csv()
    print("Validation set:", data["val_images"].shape, " Test set:", data["test_images"].shape)
