import numpy as np
import pandas as pd
import tensorflow as tf
from .config import MODELS_DIR, RESULTS_DIR
from .data_loader import create_or_load_splits
from .dataset import build_dataset
from .ensemble import soft_vote

MODEL_NAMES = ["cnn_baseline", "cnn_regularized", "cnn_deep"]

def transform_batch(images, variant):
    if variant == "original":
        return images
    if variant == "rotated":
        return tf.image.rot90(images, k=1)
    if variant == "blurred":
        return tf.nn.avg_pool2d(images, ksize=3, strides=1, padding="SAME")
    if variant == "noisy":
        return tf.clip_by_value(images + tf.random.normal(tf.shape(images), stddev=0.08), 0.0, 1.0)
    if variant == "darkened":
        return tf.clip_by_value(images * 0.55, 0.0, 1.0)
    if variant == "brightened":
        return tf.clip_by_value(images * 1.35, 0.0, 1.0)
    if variant == "cropped":
        cropped = tf.image.central_crop(images, 0.75)
        return tf.image.resize(cropped, tf.shape(images)[1:3])
    raise ValueError(variant)

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    _, _, test_df = create_or_load_splits()
    test_ds = build_dataset(test_df)
    y_true = test_df["label"].to_numpy()
    images = np.concatenate([x.numpy() for x, _ in test_ds], axis=0)

    models = [tf.keras.models.load_model(MODELS_DIR / f"{name}.keras") for name in MODEL_NAMES]
    variants = ["original", "rotated", "blurred", "noisy", "darkened", "brightened", "cropped"]
    rows = []

    for variant in variants:
        x = transform_batch(tf.convert_to_tensor(images), variant)
        probabilities = [model.predict(x, verbose=0) for model in models]
        predictions = [p.argmax(axis=1) for p in probabilities]
        ensemble_pred, _ = soft_vote(probabilities)
        rows.append({
            "variant": variant,
            "cnn_baseline_accuracy": float(np.mean(predictions[0] == y_true)),
            "cnn_regularized_accuracy": float(np.mean(predictions[1] == y_true)),
            "cnn_deep_accuracy": float(np.mean(predictions[2] == y_true)),
            "ensemble_soft_accuracy": float(np.mean(ensemble_pred == y_true)),
        })

    pd.DataFrame(rows).to_csv(RESULTS_DIR / "robustness_results.csv", index=False)
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
