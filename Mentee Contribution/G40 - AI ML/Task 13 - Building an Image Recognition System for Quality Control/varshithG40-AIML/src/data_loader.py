"""
Data Loader Module for Casting Quality Inspection
Handles dataset loading from directory, train/validation split, prefetching, and optimization.
"""

import os
import tensorflow as tf

def load_casting_datasets(
    train_dir="data/train",
    test_dir="data/test",
    image_size=(224, 224),
    batch_size=32,
    val_split=0.20,
    seed=42
):
    """
    Loads train, validation, and test datasets from directory.
    
    Args:
        train_dir: Path to training dataset directory containing ok_front/ and def_front/.
        test_dir: Path to test dataset directory containing ok_front/ and def_front/.
        image_size: Target image dimensions tuple (height, width).
        batch_size: Number of images per batch.
        val_split: Fraction of train data reserved for validation.
        seed: Random seed for deterministic train/validation split.
        
    Returns:
        tuple: (train_dataset, validation_dataset, test_dataset)
    """
    class_names = ["ok_front", "def_front"]
    
    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Training directory not found at '{train_dir}'. Run generate_dataset.py first.")
    if not os.path.exists(test_dir):
        raise FileNotFoundError(f"Test directory not found at '{test_dir}'. Run generate_dataset.py first.")

    print(f"Loading training dataset from '{train_dir}'...")
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        class_names=class_names,
        validation_split=val_split,
        subset="training",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary"
    )

    print(f"Loading validation dataset from '{train_dir}'...")
    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        class_names=class_names,
        validation_split=val_split,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary"
    )

    print(f"Loading test dataset from '{test_dir}'...")
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        class_names=class_names,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=False
    )

    # Configure dataset prefetching for optimum GPU/CPU performance
    autotune = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=autotune)
    validation_dataset = validation_dataset.prefetch(buffer_size=autotune)
    test_dataset = test_dataset.prefetch(buffer_size=autotune)

    print("Datasets loaded and prefetched successfully.")
    return train_dataset, validation_dataset, test_dataset
