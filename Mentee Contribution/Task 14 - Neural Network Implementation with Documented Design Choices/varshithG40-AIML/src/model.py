import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tensorflow as tf
from tensorflow.keras import layers, models
from src.data_loader import get_data_augmentation

def build_cnn_model(input_shape=(224, 224, 3), dropout_rate=0.40):
    """
    Builds the baseline Convolutional Neural Network (CNN) architecture.
    
    Architecture Design:
    - Input shape: (224, 224, 3)
    - Data Augmentation: RandomFlip, RandomRotation, RandomZoom, RandomContrast
    - Rescaling: Normalizes pixel values from [0, 255] to [0.0, 1.0]
    - Conv2D(32, 3): Extract low-level edge/contour features
    - MaxPooling2D(): Spatial downsampling
    - Conv2D(64, 3): Extract mid-level geometric texture features
    - MaxPooling2D(): Spatial downsampling
    - Conv2D(128, 3): Extract high-level defect pattern features
    - MaxPooling2D(): Spatial downsampling
    - GlobalAveragePooling2D(): Summarizes feature maps to avoid high parameter count of Flatten
    - Dropout(dropout_rate): Regularization to reduce overfitting
    - Dense(64, activation='relu'): Fully connected representation
    - Dense(1, activation='sigmoid'): Binary classification output (0 = Non-defective, 1 = Defective)
    """
    data_aug = get_data_augmentation()
    
    model = models.Sequential([
        layers.Input(shape=input_shape),
        data_aug,
        layers.Rescaling(1.0 / 255.0),
        
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.Conv2D(128, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.GlobalAveragePooling2D(),
        layers.Dropout(dropout_rate),
        
        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ], name="Casting_CNN_Baseline")
    
    return model

def build_bonus_model(input_shape=(224, 224, 3), dropout_rate=0.20):
    """
    Builds the bonus experiment model variant (Dropout changed from 0.40 to 0.20).
    """
    data_aug = get_data_augmentation()
    
    model = models.Sequential([
        layers.Input(shape=input_shape),
        data_aug,
        layers.Rescaling(1.0 / 255.0),
        
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.Conv2D(128, 3, activation="relu"),
        layers.MaxPooling2D(),
        
        layers.GlobalAveragePooling2D(),
        layers.Dropout(dropout_rate),
        
        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ], name="Casting_CNN_Bonus_Dropout020")
    
    return model

def compile_model(model, learning_rate=0.001):
    """
    Compiles the Keras model with Adam optimizer, binary cross-entropy loss, and metrics.
    """
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")
        ]
    )
    return model

if __name__ == "__main__":
    model = build_cnn_model()
    model.summary()
