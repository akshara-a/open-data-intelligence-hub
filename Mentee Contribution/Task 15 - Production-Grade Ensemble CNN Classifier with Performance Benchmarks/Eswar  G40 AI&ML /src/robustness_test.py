"""
robustness_test.py

Generates corrupted variants of the test set (rotation, blur, noise,
darkening, brightening) and measures how much each model's — and the
ensemble's — accuracy degrades under each corruption.
"""

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


def make_rotated(images):
    return tf.keras.layers.RandomRotation((25 / 360, 25 / 360))(images, training=True).numpy()


def make_blurred(images):
    imgs = tf.convert_to_tensor(images, dtype=tf.float32)
    kernel = tf.ones((5, 5, 3, 1), dtype=tf.float32) / 25.0
    blurred = tf.nn.depthwise_conv2d(imgs, kernel, strides=[1, 1, 1, 1], padding="SAME")
    return np.clip(blurred.numpy(), 0, 255).astype(np.uint8)


def make_noisy(images, sigma=20):
    noise = np.random.normal(0, sigma, images.shape)
    return np.clip(images.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def make_darker(images, factor=0.4):
    return np.clip(images.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def make_brighter(images, factor=1.8):
    return np.clip(images.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def build_corruptions(test_images):
    return {
        "rotated": make_rotated(test_images.astype(np.float32)),
        "blurred": make_blurred(test_images),
        "noisy": make_noisy(test_images),
        "darker": make_darker(test_images),
        "brighter": make_brighter(test_images),
    }


def save_sample_grid(test_images, corruptions, results_dir="results"):
    fig, axes = plt.subplots(1, 6, figsize=(18, 3))
    axes[0].imshow(test_images[0].astype(np.uint8)); axes[0].set_title("Original"); axes[0].axis("off")
    for i, (name, imgs) in enumerate(corruptions.items(), start=1):
        axes[i].imshow(imgs[0].astype(np.uint8)); axes[i].set_title(name); axes[i].axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "robustness_sample_images.png"), dpi=150, bbox_inches="tight")
    plt.close()


def run_robustness_tests(trained_models, model_names, test_images, test_labels, corruptions):
    robustness_results = {}
    for corruption_name, corrupted_images in corruptions.items():
        row = {}
        corrupted_probs = {}
        for name in model_names:
            probs = trained_models[name].predict(corrupted_images, batch_size=64, verbose=0)
            preds = np.argmax(probs, axis=1)
            row[name] = float(accuracy_score(test_labels, preds))
            corrupted_probs[name] = probs
        soft_corrupt_probs = np.mean([corrupted_probs[n] for n in model_names], axis=0)
        soft_corrupt_preds = np.argmax(soft_corrupt_probs, axis=1)
        row["ensemble_soft_voting"] = float(accuracy_score(test_labels, soft_corrupt_preds))
        robustness_results[corruption_name] = row
        print(f"{corruption_name}: {row}")
    return robustness_results
