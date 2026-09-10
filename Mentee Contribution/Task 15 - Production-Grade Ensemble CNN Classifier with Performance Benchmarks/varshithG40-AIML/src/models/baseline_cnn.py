"""
baseline_cnn.py
===============
CNN Model 1 — Baseline CNN
Architecture:
  Input (128, 128, 3)
   ↓ Conv2D(32, 3x3)
   ↓ ReLU
   ↓ MaxPooling2D(2, 2)
   ↓ Conv2D(64, 3x3)
   ↓ ReLU
   ↓ MaxPooling2D(2, 2)
   ↓ Flatten
   ↓ Dense(64, ReLU)
   ↓ Dense(2, Softmax)
"""

from tensorflow import keras
from keras import layers


def build_baseline_cnn(input_shape=(128, 128, 3), num_classes=2) -> keras.Model:
    """
    Constructs CNN 1 (Baseline CNN).
    A lightweight, straightforward sequential feature extractor serving as the reference baseline.
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape, name="input_baseline"),
        
        # Conv Block 1
        layers.Conv2D(32, (3, 3), padding="same", activation="relu", name="conv1_baseline"),
        layers.MaxPooling2D((2, 2), name="pool1_baseline"),
        
        # Conv Block 2
        layers.Conv2D(64, (3, 3), padding="same", activation="relu", name="conv2_baseline"),
        layers.MaxPooling2D((2, 2), name="pool2_baseline"),
        
        # Classifier Head
        layers.Flatten(name="flatten_baseline"),
        layers.Dense(64, activation="relu", name="dense_baseline"),
        layers.Dense(num_classes, activation="softmax", name="output_baseline")
    ], name="CNN_1_Baseline")
    
    return model


if __name__ == "__main__":
    m = build_baseline_cnn()
    m.summary()
