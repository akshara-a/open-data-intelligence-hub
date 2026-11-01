import os
import tensorflow as tf
from tensorflow.keras import layers, models

# ==========================================
# 1. DATASET PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(BASE_DIR, "train")
TEST_DIR = os.path.join(BASE_DIR, "test")

print("Training folder:", TRAIN_DIR)
print("Testing folder:", TEST_DIR)


# ==========================================
# 2. LOAD TRAINING DATA
# ==========================================

train_data = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=(128, 128),
    batch_size=32,
    label_mode="binary",
    shuffle=True
)


# ==========================================
# 3. LOAD TESTING DATA
# ==========================================

test_data = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=(128, 128),
    batch_size=32,
    label_mode="binary",
    shuffle=False
)


# ==========================================
# 4. SHOW CLASS NAMES
# ==========================================

print("Classes:", train_data.class_names)


# ==========================================
# 5. IMPROVE DATA LOADING SPEED
# ==========================================

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(buffer_size=AUTOTUNE)
test_data = test_data.prefetch(buffer_size=AUTOTUNE)


# ==========================================
# 6. CREATE CNN MODEL
# ==========================================

model = models.Sequential([

    # Normalize pixel values
    layers.Rescaling(1.0 / 255, input_shape=(128, 128, 3)),

    # First convolution block
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Second convolution block
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Third convolution block
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    # Convert image features into one dimension
    layers.Flatten(),

    # Fully connected layer
    layers.Dense(128, activation="relu"),

    # Reduce overfitting
    layers.Dropout(0.5),

    # Binary classification
    layers.Dense(1, activation="sigmoid")
])


# ==========================================
# 7. COMPILE MODEL
# ==========================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# ==========================================
# 8. DISPLAY MODEL
# ==========================================

model.summary()


# ==========================================
# 9. TRAIN MODEL
# ==========================================

print("\nStarting model training...\n")

history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=10
)


# ==========================================
# 10. EVALUATE MODEL
# ==========================================

print("\nEvaluating model...\n")

loss, accuracy = model.evaluate(test_data)

print("Test Loss:", loss)
print("Test Accuracy:", accuracy)


# ==========================================
# 11. SAVE MODEL
# ==========================================

MODEL_PATH = os.path.join(BASE_DIR, "casting_defect_model.keras")

model.save(MODEL_PATH)

print("\nModel saved successfully!")
print("Saved at:", MODEL_PATH)