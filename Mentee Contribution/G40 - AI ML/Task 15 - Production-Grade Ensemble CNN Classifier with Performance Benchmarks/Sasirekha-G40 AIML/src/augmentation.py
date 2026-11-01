import tensorflow as tf

def build_augmentation():
    # Mild augmentation only. The original project used stronger augmentation
    # while the models were not yet learning reliably on this small dataset.
    return tf.keras.Sequential([
        tf.keras.layers.RandomRotation(0.03),
        tf.keras.layers.RandomContrast(0.05),
    ], name="mild_industrial_augmentation")
