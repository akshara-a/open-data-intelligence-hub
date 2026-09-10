"""
predict.py

Loads the three saved models and runs ensemble (soft-voting) inference on
new images.

Usage:
    python -m src.predict path/to/image1.png path/to/image2.png
"""

import sys
import numpy as np
import tensorflow as tf

from src.data_loader import CLASS_NAMES, IMAGE_SIZE

MODEL_NAMES = ["cnn_baseline", "cnn_regularized", "cnn_deep"]
MODELS_DIR = "models"


def load_models(models_dir=MODELS_DIR):
    return {name: tf.keras.models.load_model(f"{models_dir}/{name}.keras") for name in MODEL_NAMES}


def load_image(path):
    img = tf.keras.utils.load_img(path, target_size=IMAGE_SIZE)
    return tf.keras.utils.img_to_array(img).astype(np.uint8)


def predict_batch(models, images):
    """images: (N, 32, 32, 3) uint8 array. Returns soft-voted class names + probabilities."""
    all_probs = [model.predict(images, batch_size=64, verbose=0) for model in models.values()]
    soft_probs = np.mean(all_probs, axis=0)
    preds = np.argmax(soft_probs, axis=1)
    return [CLASS_NAMES[p] for p in preds], soft_probs


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.predict <image_path> [image_path ...]")
        sys.exit(1)

    models = load_models()
    images = np.stack([load_image(p) for p in sys.argv[1:]])
    labels, probs = predict_batch(models, images)

    for path, label, prob in zip(sys.argv[1:], labels, probs):
        confidence = prob[CLASS_NAMES.index(label)]
        print(f"{path}: {label} (confidence={confidence:.3f})")


if __name__ == "__main__":
    main()
