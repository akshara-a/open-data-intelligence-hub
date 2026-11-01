"""
Data Augmentation Pipeline Module for Casting Quality Inspection
Defines data augmentation transformations applied strictly during model training.
"""

import tensorflow as tf
from tensorflow.keras import layers

def get_data_augmentation_pipeline():
    """
    Creates a Keras Sequential data augmentation pipeline.
    
    Includes mild transformations appropriate for industrial casting inspection:
    - Horizontal Flip: Simulates opposite orientation
    - Small Rotation (±5%): Simulates slight rotational misalignment
    - Small Zoom (±10%): Simulates slight camera distance variation
    - Small Translation (±5%): Simulates off-center product placement
    - Contrast Adjustment (±10%): Simulates lighting variations
    
    Returns:
        tf.keras.Sequential: Augmentation pipeline layer block.
    """
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.05),
        layers.RandomZoom(0.10),
        layers.RandomTranslation(height_factor=0.05, width_factor=0.05),
        layers.RandomContrast(0.10)
    ], name="data_augmentation")
    
    return data_augmentation
