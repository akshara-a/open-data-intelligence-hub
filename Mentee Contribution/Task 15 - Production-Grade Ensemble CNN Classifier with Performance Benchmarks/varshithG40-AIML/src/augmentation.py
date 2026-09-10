"""
augmentation.py
===============
Data augmentation pipeline applied strictly to the training dataset.
Includes Random Flip, Rotation, Zoom, Translation/Crop, and Brightness/Contrast adjustments.
"""

import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np


def get_data_augmentation_layer(image_size=(128, 128)) -> keras.Sequential:
    """
    Returns a Keras Sequential layer sequence for training-time data augmentation.
    Helps prevent overfitting on small sample sizes and improves model generalization.
    """
    return keras.Sequential([
        layers.Input(shape=(*image_size, 3)),
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.12),          # +/- ~15 degrees
        layers.RandomZoom(0.10),              # +/- 10% zoom
        layers.RandomTranslation(0.08, 0.08), # +/- 8% spatial translation
        layers.RandomContrast(0.15),          # +/- 15% contrast jitter
    ], name="data_augmentation")


def augment_batch(images: np.ndarray, labels: np.ndarray, multiplier: int = 2) -> tuple:
    """
    Generates augmented training copies to expand the training footprint.
    Applied strictly to training partitions.
    """
    aug_layer = get_data_augmentation_layer(image_size=(images.shape[1], images.shape[2]))
    
    all_imgs = [images]
    all_lbls = [labels]
    
    for _ in range(multiplier):
        aug_imgs = aug_layer(images, training=True).numpy()
        all_imgs.append(aug_imgs)
        all_lbls.append(labels)
        
    X_aug = np.concatenate(all_imgs, axis=0)
    y_aug = np.concatenate(all_lbls, axis=0)
    return X_aug, y_aug


if __name__ == "__main__":
    dummy_x = np.random.rand(8, 128, 128, 3).astype(np.float32)
    dummy_y = np.array([[1, 0]] * 4 + [[0, 1]] * 4, dtype=np.float32)
    aug_x, aug_y = augment_batch(dummy_x, dummy_y, multiplier=1)
    print(f"Original batch: {dummy_x.shape} -> Augmented batch: {aug_x.shape}")
