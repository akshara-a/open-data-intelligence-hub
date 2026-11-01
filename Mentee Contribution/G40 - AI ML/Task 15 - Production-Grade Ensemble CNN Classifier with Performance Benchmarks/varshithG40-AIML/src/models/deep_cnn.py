"""
deep_cnn.py
===========
CNN Model 3 — Deeper CNN
Architecture:
  Input (128, 128, 3)
   ↓ Conv2D(32, 3x3, ReLU)
   ↓ Conv2D(32, 3x3, ReLU)
   ↓ BatchNormalization
   ↓ MaxPooling2D(2, 2)
   ↓ Conv2D(64, 3x3, ReLU)
   ↓ Conv2D(64, 3x3, ReLU)
   ↓ BatchNormalization
   ↓ MaxPooling2D(2, 2)
   ↓ GlobalAveragePooling2D
   ↓ Dense(64, ReLU)
   ↓ Dense(2, Softmax)
"""

from tensorflow import keras
from keras import layers


def build_deep_cnn(input_shape=(128, 128, 3), num_classes=2) -> keras.Model:
    """
    Constructs CNN 3 (Deeper CNN).
    Uses stacked consecutive convolutional layers to capture hierarchical and non-linear patterns,
    combined with Global Average Pooling to reduce parameter counts while preserving spatial feature maps.
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape, name="input_deep"),
        
        # Deep Block 1: Conv -> Conv -> BN -> Pool
        layers.Conv2D(32, (3, 3), padding="same", activation="relu", name="conv1a_deep"),
        layers.Conv2D(32, (3, 3), padding="same", activation="relu", name="conv1b_deep"),
        layers.BatchNormalization(name="bn1_deep"),
        layers.MaxPooling2D((2, 2), name="pool1_deep"),
        
        # Deep Block 2: Conv -> Conv -> BN -> Pool
        layers.Conv2D(64, (3, 3), padding="same", activation="relu", name="conv2a_deep"),
        layers.Conv2D(64, (3, 3), padding="same", activation="relu", name="conv2b_deep"),
        layers.BatchNormalization(name="bn2_deep"),
        layers.MaxPooling2D((2, 2), name="pool2_deep"),
        
        # Spatial Aggregation & Classifier Head
        layers.GlobalAveragePooling2D(name="gap_deep"),
        layers.Dense(64, activation="relu", name="dense_deep"),
        layers.Dropout(0.20, name="drop_deep"),
        layers.Dense(num_classes, activation="softmax", name="output_deep")
    ], name="CNN_3_Deeper")
    
    return model


if __name__ == "__main__":
    m = build_deep_cnn()
    m.summary()
