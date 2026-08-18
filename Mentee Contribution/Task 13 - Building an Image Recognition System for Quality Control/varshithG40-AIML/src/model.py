"""
CNN Model Architecture for Casting Defect Detection
Defines the binary image classification neural network matching specified specs.
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from src.augmentation import get_data_augmentation_pipeline

def build_casting_cnn_model(input_shape=(224, 224, 3)):
    """
    Builds and returns the Convolutional Neural Network (CNN) architecture.
    
    Architecture Design:
    - Input: 224x224x3 RGB image
    - Data Augmentation Layer (Active only during training)
    - Rescaling Layer: Normalizes pixel values from [0, 255] to [0.0, 1.0]
    - Block 1: Conv2D(32, kernel_size=3) + ReLU + MaxPooling2D
    - Block 2: Conv2D(64, kernel_size=3) + ReLU + MaxPooling2D
    - Block 3: Conv2D(128, kernel_size=3) + ReLU + MaxPooling2D
    - Feature Aggregation: GlobalAveragePooling2D
    - Regularization: Dropout(0.40)
    - Fully Connected: Dense(64) + ReLU
    - Regularization: Dropout(0.30)
    - Output Neuron: Dense(1) + Sigmoid (produces probability between 0 and 1)
    
    Args:
        input_shape: Image input shape tuple.
        
    Returns:
        tf.keras.Model: Uncompiled Keras Sequential model.
    """
    data_augmentation = get_data_augmentation_pipeline()

    model = models.Sequential([
        layers.Input(shape=input_shape),

        data_augmentation,
        layers.Rescaling(1.0 / 255.0),

        layers.Conv2D(32, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(),

        layers.Conv2D(64, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(),

        layers.Conv2D(128, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),

        layers.Dropout(0.40),

        layers.Dense(64, activation="relu"),
        layers.Dropout(0.30),

        layers.Dense(1, activation="sigmoid")
    ], name="casting_defect_cnn")

    return model

if __name__ == "__main__":
    model = build_casting_cnn_model()
    model.summary()
