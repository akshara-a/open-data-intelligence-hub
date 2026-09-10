"""
train.py

Trains all three CNN architectures (baseline, regularized, deep) on CIFAR-10
and saves the best checkpoint of each to models/.

Usage:
    python -m src.train
"""

import os
import time
import numpy as np
import tensorflow as tf

from src.data_loader import load_from_csv, CLASS_NAMES
from src.models.baseline_cnn import build_cnn_baseline
from src.models.regularized_cnn import build_cnn_regularized
from src.models.deep_cnn import build_cnn_deep
from src.evaluate import evaluate_and_record, plot_history

tf.random.set_seed(42)
np.random.seed(42)

MODELS_DIR = "models"
RESULTS_DIR = "results"


def make_callbacks(model_name, patience=5):
    return [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=patience, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(MODELS_DIR, f"{model_name}.keras"),
            monitor="val_loss", save_best_only=True),
    ]


def train_one(name, build_fn, data, epochs, patience, results, process, mem_before):
    model = build_fn()
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    t0 = time.time()
    history = model.fit(data["train_dataset"], validation_data=data["validation_dataset"],
                         epochs=epochs, callbacks=make_callbacks(name, patience), verbose=2)
    train_time = time.time() - t0
    plot_history(history, name, RESULTS_DIR)
    evaluate_and_record(name, model, data, mem_before, train_time,
                         len(history.history["accuracy"]), results, process,
                         MODELS_DIR, RESULTS_DIR, CLASS_NAMES)
    return model


def main():
    import psutil
    import json

    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    process = psutil.Process(os.getpid())

    data = load_from_csv()
    results = {}

    for name, build_fn, epochs, patience in [
        ("cnn_baseline", build_cnn_baseline, 30, 5),
        ("cnn_regularized", build_cnn_regularized, 30, 5),
        ("cnn_deep", build_cnn_deep, 20, 4),
    ]:
        mem_before = process.memory_info().rss / (1024 * 1024)
        train_one(name, build_fn, data, epochs, patience, results, process, mem_before)

    with open(os.path.join(RESULTS_DIR, "individual_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("Training complete. Results saved to results/individual_results.json")


if __name__ == "__main__":
    main()
