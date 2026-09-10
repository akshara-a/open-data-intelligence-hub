"""
train.py
========
Training pipeline for CNN 1 (Baseline), CNN 2 (Regularized), and CNN 3 (Deep).
Trains each model for up to 15 epochs using Adam optimizer, categorical cross-entropy,
EarlyStopping, ModelCheckpointing, and training-time data augmentation.
Saves model checkpoints to models/ and training curves to results/.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras

from .preprocessing import load_full_dataset
from .augmentation import augment_batch
from .models import build_baseline_cnn, build_regularized_cnn, build_deep_cnn

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

EPOCHS = 15
BATCH_SIZE = 8
LEARNING_RATE = 0.001
RANDOM_SEED = 42

tf.random.set_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def plot_training_history(history, model_name: str, save_path: str):
    """
    Generates and saves high-resolution Accuracy & Loss curves for training & validation sets.
    """
    acc = history.history.get("accuracy", [])
    val_acc = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs_range = range(1, len(acc) + 1)

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # 1. Accuracy Curve
    ax1.plot(epochs_range, acc, label="Training Accuracy", color="#2563eb", linewidth=2.5, marker="o", markersize=4)
    ax1.plot(epochs_range, val_acc, label="Validation Accuracy", color="#16a34a", linewidth=2.5, linestyle="--", marker="s", markersize=4)
    ax1.set_title(f"{model_name} — Accuracy over Epochs", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Epoch", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Accuracy", fontsize=11, fontweight="bold")
    ax1.set_ylim([0.0, 1.05])
    ax1.legend(loc="lower right", frameon=True, fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # 2. Loss Curve
    ax2.plot(epochs_range, loss, label="Training Loss", color="#dc2626", linewidth=2.5, marker="o", markersize=4)
    ax2.plot(epochs_range, val_loss, label="Validation Loss", color="#ea580c", linewidth=2.5, linestyle="--", marker="s", markersize=4)
    ax2.set_title(f"{model_name} — Categorical Loss over Epochs", fontsize=13, fontweight="bold", pad=12)
    ax2.set_xlabel("Epoch", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Loss", fontsize=11, fontweight="bold")
    ax2.legend(loc="upper right", frameon=True, fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.suptitle(f"Training History & Convergence: {model_name} (15 Epochs)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[PLOT] Saved training curve to: {save_path}")


def train_single_model(model_fn, model_name: str, checkpoint_filename: str, plot_filename: str, X_tr, y_tr, X_v, y_v):
    """
    Trains one CNN model with EarlyStopping, ModelCheckpointing, and saves curves.
    """
    print(f"\n=======================================================")
    print(f" Training {model_name} (Max {EPOCHS} Epochs)")
    print(f"=======================================================")
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    model = model_fn(input_shape=(128, 128, 3), num_classes=2)
    optimizer = keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    ckpt_path = os.path.join(MODELS_DIR, checkpoint_filename)
    plot_path = os.path.join(RESULTS_DIR, plot_filename)
    
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=ckpt_path,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train with batch size 8 on training set
    history = model.fit(
        X_tr, y_tr,
        validation_data=(X_v, y_v),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final best model instance
    model.save(ckpt_path)
    print(f"[SAVE] Checkpointed best weights saved to: {ckpt_path}")
    
    # Generate and save plot
    plot_training_history(history, model_name, plot_path)
    
    return model, history


def train_all_models(apply_augmentation: bool = True):
    """
    Main training orchestrator for all three CNNs.
    """
    (X_train, y_train), (X_val, y_val), (X_test, y_test), _ = load_full_dataset()
    print(f"Dataset Loaded: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")
    
    if apply_augmentation:
        print("[AUGMENT] Applying data augmentation to training partition (2x expansion)...")
        X_train_aug, y_train_aug = augment_batch(X_train, y_train, multiplier=1)
        print(f"[AUGMENT] Expanded training set: {X_train.shape} -> {X_train_aug.shape}")
    else:
        X_train_aug, y_train_aug = X_train, y_train
        
    models_config = [
        (build_baseline_cnn, "CNN 1 (Baseline CNN)", "cnn_baseline.keras", "training_history_cnn1.png"),
        (build_regularized_cnn, "CNN 2 (Regularized CNN)", "cnn_regularized.keras", "training_history_cnn2.png"),
        (build_deep_cnn, "CNN 3 (Deeper CNN)", "cnn_deep.keras", "training_history_cnn3.png")
    ]
    
    trained_models = {}
    histories = {}
    
    for fn, name, ckpt, plot in models_config:
        model, hist = train_single_model(fn, name, ckpt, plot, X_train_aug, y_train_aug, X_val, y_val)
        trained_models[name] = model
        histories[name] = hist
        
    print("\n[ALL MODELS TRAINED SUCCESSFULLY]")
    return trained_models, histories


if __name__ == "__main__":
    train_all_models()
