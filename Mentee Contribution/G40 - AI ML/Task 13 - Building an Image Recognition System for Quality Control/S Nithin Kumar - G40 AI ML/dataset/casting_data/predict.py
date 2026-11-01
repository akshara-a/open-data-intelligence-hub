import os
import tensorflow as tf
import numpy as np

# -----------------------------
# Model location
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "casting_defect_model.keras"
)

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")

# -----------------------------
# Use a known test image
# -----------------------------
IMAGE_PATH = os.path.join(
    BASE_DIR,
    "test",
    "def_front",
    os.listdir(os.path.join(BASE_DIR, "test", "def_front"))[0]
)

print("Testing image:")
print(IMAGE_PATH)

# -----------------------------
# Load image
# -----------------------------
image = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=(128, 128)
)

image_array = tf.keras.utils.img_to_array(image)
image_array = np.expand_dims(image_array, axis=0)

# -----------------------------
# Prediction
# -----------------------------
prediction = model.predict(image_array, verbose=0)[0][0]

print("\nPrediction score:", prediction)

if prediction < 0.5:
    print("Result: DEFECT ❌")
else:
    print("Result: OK ✅")