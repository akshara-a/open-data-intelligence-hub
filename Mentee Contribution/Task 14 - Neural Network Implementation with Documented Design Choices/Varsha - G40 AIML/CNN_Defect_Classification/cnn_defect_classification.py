import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

print("TensorFlow version:", tf.__version__)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 123

print("Setup completed successfully!")
# Dataset paths
TRAIN_DIR = "data/casting_data/train"
TEST_DIR = "data/casting_data/test"

# Class order
# 0 = Non-defective
# 1 = Defective
CLASS_NAMES = ["ok_front", "def_front"]

# Load training data (80%)
train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

# Load validation data (20%)
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary"
)

# Load test data
test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)

print("Class names:", train_dataset.class_names)
print("Dataset loaded successfully!")
# -----------------------------------
# STEP 9: Data Augmentation
# -----------------------------------

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomContrast(0.10)
])

# -----------------------------------
# CNN Model
# -----------------------------------

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),

    # Data augmentation
    data_augmentation,

    # Normalize pixel values
    tf.keras.layers.Rescaling(1.0 / 255),

    # Convolution Block 1
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    # Convolution Block 2
    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    # Convolution Block 3
    tf.keras.layers.Conv2D(128, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),

    # Reduce feature maps
    tf.keras.layers.GlobalAveragePooling2D(),

    # Prevent overfitting
    tf.keras.layers.Dropout(0.40),

    # Fully connected layer
    tf.keras.layers.Dense(64, activation="relu"),

    # Binary classification
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Display model architecture
model.summary()
# -----------------------------------
# STEP 10: Compile the Model
# -----------------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]
)

print("Model compiled successfully!")
# -----------------------------------
# STEP 11: Training Callbacks
# -----------------------------------

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2
    )
]

print("Callbacks configured successfully!")
# -----------------------------------
# STEP 12: Train the Model
# -----------------------------------

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25,
    callbacks=callbacks
)

print("Training completed!")
# STEP 13: Plot Training and Validation Accuracy/Loss

plt.figure(figsize=(12, 5))

# Accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("Training and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

# Loss
plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()
print("Training completed!")
model.save("models/casting_defect_cnn.keras")
print("Trained model saved successfully!")