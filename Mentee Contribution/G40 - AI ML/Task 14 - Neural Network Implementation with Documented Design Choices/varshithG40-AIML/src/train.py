import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
import tensorflow as tf
from src.data_loader import load_datasets
from src.model import build_cnn_model, build_bonus_model, compile_model

def get_callbacks():
    return [
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

def plot_history(history, save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Accuracy Plot
    plt.figure(figsize=(8, 6))
    plt.plot(history.history["accuracy"], label="Training Accuracy", linewidth=2, marker='o')
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy", linewidth=2, marker='s')
    plt.title("Model Training vs Validation Accuracy", fontsize=14, fontweight='bold')
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Accuracy", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/accuracy_plot.png", dpi=300)
    plt.close()

    # 2. Loss Plot
    plt.figure(figsize=(8, 6))
    plt.plot(history.history["loss"], label="Training Loss", linewidth=2, marker='o')
    plt.plot(history.history["val_loss"], label="Validation Loss", linewidth=2, marker='s')
    plt.title("Model Training vs Validation Loss", fontsize=14, fontweight='bold')
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Loss (Binary Crossentropy)", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/loss_plot.png", dpi=300)
    plt.close()

def plot_bonus_comparison(history_base, history_bonus, save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(history_base.history["val_accuracy"], label="Baseline (Dropout 0.40)", linewidth=2, marker='o')
    plt.plot(history_bonus.history["val_accuracy"], label="Bonus Variant (Dropout 0.20)", linewidth=2, marker='^')
    plt.title("Validation Accuracy Comparison: Baseline vs Bonus Variant", fontsize=14, fontweight='bold')
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Validation Accuracy", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/bonus_comparison.png", dpi=300)
    plt.close()

def train():
    os.makedirs("models", exist_ok=True)
    print("Loading datasets...")
    train_dataset, val_dataset, test_dataset = load_datasets()

    print("\n--- Training Baseline Model ---")
    model = build_cnn_model()
    compile_model(model)
    model.summary()

    callbacks = get_callbacks()
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=15,
        callbacks=callbacks
    )

    model.save("models/cnn_casting_model.keras")
    print("Baseline Model saved to models/cnn_casting_model.keras")

    plot_history(history)
    print("Baseline training graphs saved to plots/")

    print("\n--- Training Bonus Experiment Model (Dropout 0.20) ---")
    bonus_model = build_bonus_model()
    compile_model(bonus_model)
    history_bonus = bonus_model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=15,
        callbacks=callbacks
    )

    bonus_model.save("models/cnn_bonus_model.keras")
    print("Bonus Model saved to models/cnn_bonus_model.keras")

    plot_bonus_comparison(history, history_bonus)
    print("Bonus comparison plot saved to plots/bonus_comparison.png")

    return history, history_bonus

if __name__ == "__main__":
    train()
