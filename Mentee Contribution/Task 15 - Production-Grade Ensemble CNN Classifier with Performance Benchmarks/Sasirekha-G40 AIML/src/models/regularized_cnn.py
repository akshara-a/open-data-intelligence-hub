import tensorflow as tf
from ..config import IMAGE_SIZE

def conv_block(x, filters, dropout_rate):
    x = tf.keras.layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.Conv2D(filters, 3, padding="same", use_bias=False)(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)

    x = tf.keras.layers.MaxPooling2D()(x)
    return tf.keras.layers.Dropout(dropout_rate)(x)

def build_model(num_classes=6):
    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))
    x = conv_block(inputs, 32, 0.10)
    x = conv_block(x, 64, 0.15)
    x = conv_block(x, 128, 0.25)

    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs, name="cnn_regularized")
