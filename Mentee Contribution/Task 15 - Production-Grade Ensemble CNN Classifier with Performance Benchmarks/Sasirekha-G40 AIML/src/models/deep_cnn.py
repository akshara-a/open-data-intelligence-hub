import tensorflow as tf
from ..config import IMAGE_SIZE

def conv_bn_relu(x, filters):
    x = tf.keras.layers.Conv2D(
        filters, 3, padding="same", use_bias=False,
        kernel_initializer="he_normal"
    )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    return tf.keras.layers.Activation("relu")(x)

def build_model(num_classes=6):
    inputs = tf.keras.Input(shape=(*IMAGE_SIZE, 3))

    x = conv_bn_relu(inputs, 32)
    x = conv_bn_relu(x, 32)
    x = tf.keras.layers.MaxPooling2D()(x)

    x = conv_bn_relu(x, 64)
    x = conv_bn_relu(x, 64)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Dropout(0.15)(x)

    x = conv_bn_relu(x, 128)
    x = conv_bn_relu(x, 128)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Dropout(0.20)(x)

    x = conv_bn_relu(x, 256)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.30)(x)

    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs, name="cnn_deep")
