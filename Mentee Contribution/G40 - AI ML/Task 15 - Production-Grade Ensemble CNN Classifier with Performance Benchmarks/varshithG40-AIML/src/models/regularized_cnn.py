"""
regularized_cnn.py
==================
CNN Model 2 — Regularized CNN
Architecture:
  Input (128, 128, 3)
   ↓ Conv2D(32, 3x3)
   ↓ BatchNormalization
   ↓ ReLU
   ↓ MaxPooling2D(2, 2)
   ↓ Dropout(0.25)
   ↓ Conv2D(64, 3x3)
   ↓ BatchNormalization
   ↓ ReLU
   ↓ MaxPooling2D(2, 2)
   ↓ Dropout(0.30)
   ↓ Flatten
   ↓ Dense(64, ReLU)
   ↓ Dropout(0.40)
   ↓ Dense(2, Softmax)
"""

from tensorflow import keras
from keras import layers


def build_regularized_cnn(input_shape=(128, 128, 3), num_classes=2) -> keras.Model:
    """
    Constructs CNN 2 (Regularized CNN).
    Incorporates Batch Normalization to stabilize activation distributions and Dropout
    to prevent co-adaptation of neurons and mitigate overfitting.
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape, name="input_regularized"),
        
        # Block 1: Conv -> BN -> ReLU -> Pool -> Dropout
        layers.Conv2D(32, (3, 3), padding="same", use_bias=False, name="conv1_reg"),
        layers.BatchNormalization(name="bn1_reg"),
        layers.Activation("relu", name="relu1_reg"),
        layers.MaxPooling2D((2, 2), name="pool1_reg"),
        layers.Dropout(0.25, name="drop1_reg"),
        
        # Block 2: Conv -> BN -> ReLU -> Pool -> Dropout
        layers.Conv2D(64, (3, 3), padding="same", use_bias=False, name="conv2_reg"),
        layers.BatchNormalization(name="bn2_reg"),
        layers.Activation("relu", name="relu2_reg"),
        layers.MaxPooling2D((2, 2), name="pool2_reg"),
        layers.Dropout(0.30, name="drop2_reg"),
        
        # Classifier Head with Dense Dropout
        layers.Flatten(name="flatten_reg"),
        layers.Dense(64, activation="relu", name="dense_reg"),
        layers.Dropout(0.40, name="drop3_reg"),
        layers.Dense(num_classes, activation="softmax", name="output_regularized")
    ], name="CNN_2_Regularized")
    
    return model


if __name__ == "__main__":
    m = build_regularized_cnn()
    m.summary()
