"""
Trains all three CNNs with the shared config from Section 23,
using Early Stopping (Section 28) and Model Checkpointing (Section 29).
Saves models to models/ as required by Section 30.
"""

import os
import json
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from data_loader import load_cifar10
from preprocessing import prepare_dataset
from models.baseline_cnn import build_baseline_cnn
from models.regularized_cnn import build_regularized_cnn
from models.deep_cnn import build_deep_cnn

MODELS_DIR = "models"
RESULTS_DIR = "results"
BATCH_SIZE = 32
MAX_EPOCHS = 30


def get_callbacks(model_name):
    os.makedirs(MODELS_DIR, exist_ok=True)
    return [
        EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True
        ),
        ModelCheckpoint(
            filepath=os.path.join(MODELS_DIR, f"{model_name}.keras"),
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]


def plot_history(history, model_name):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    plt.figure()
    plt.plot(history.history["accuracy"], label="train_acc")
    plt.plot(history.history["val_accuracy"], label="val_acc")
    plt.title(f"{model_name} — Accuracy")
    plt.xlabel("Epoch"); plt.ylabel("Accuracy"); plt.legend()
    plt.savefig(os.path.join(RESULTS_DIR, f"training_history_{model_name}_acc.png"))
    plt.close()

    plt.figure()
    plt.plot(history.history["loss"], label="train_loss")
    plt.plot(history.history["val_loss"], label="val_loss")
    plt.title(f"{model_name} — Loss")
    plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend()
    plt.savefig(os.path.join(RESULTS_DIR, f"training_history_{model_name}_loss.png"))
    plt.close()


def train_model(build_fn, model_name, x_train, y_train, x_val, y_val):
    print(f"\n=== Training {model_name} ===")
    model = build_fn()
    history = model.fit(
        x_train, y_train,
        validation_data=(x_val, y_val),
        batch_size=BATCH_SIZE,
        epochs=MAX_EPOCHS,
        callbacks=get_callbacks(model_name),
        verbose=2,
    )
    plot_history(history, model_name)

    with open(os.path.join(RESULTS_DIR, f"history_{model_name}.json"), "w") as f:
        json.dump(history.history, f)

    return model, history


def main():
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_cifar10()
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = prepare_dataset(
        x_train, y_train, x_val, y_val, x_test, y_test
    )

    train_model(build_baseline_cnn, "cnn_baseline", x_train, y_train, x_val, y_val)
    train_model(build_regularized_cnn, "cnn_regularized", x_train, y_train, x_val, y_val)
    train_model(build_deep_cnn, "cnn_deep", x_train, y_train, x_val, y_val)

    print("\nAll three models trained and saved to models/")


if __name__ == "__main__":
    main()
