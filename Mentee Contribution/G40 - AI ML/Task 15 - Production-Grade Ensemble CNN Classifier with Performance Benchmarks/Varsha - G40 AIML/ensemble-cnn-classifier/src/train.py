import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from data_loader import load_small_cifar10
from models.baseline_cnn import build_baseline_cnn
from models.regularized_cnn import build_regularized_cnn
from models.deep_cnn import build_deep_cnn


# Create folders if they don't exist
os.makedirs("models", exist_ok=True)
os.makedirs("results", exist_ok=True)


# Load dataset
(
    X_train,
    y_train,
    X_val,
    y_val,
    X_test,
    y_test
) = load_small_cifar10()


# Normalize images
X_train = X_train.astype("float32") / 255.0
X_val = X_val.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0


# CNN models
model_builders = {
    "cnn_baseline": build_baseline_cnn,
    "cnn_regularized": build_regularized_cnn,
    "cnn_deep": build_deep_cnn
}


for model_name, build_model in model_builders.items():

    print("\n" + "=" * 60)
    print(f"TRAINING: {model_name}")
    print("=" * 60)

    model = build_model()

    # Stop if validation accuracy does not improve
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=2,
        restore_best_weights=True
    )

    # Save best model
    model_path = f"models/{model_name}.keras"

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        model_path,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max"
    )

    # Train
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=5,
        batch_size=64,
        callbacks=[early_stopping, checkpoint],
        verbose=1
    )

    # Save training graph
    plt.figure(figsize=(8, 5))

    plt.plot(history.history["accuracy"], label="Training Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

    plt.title(f"{model_name} Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()

    graph_path = f"results/{model_name}_accuracy.png"
    plt.savefig(graph_path)
    plt.close()

    print(f"\nSaved model: {model_path}")
    print(f"Saved graph: {graph_path}")


print("\n" + "=" * 60)
print("ALL 3 CNN MODELS TRAINED SUCCESSFULLY")
print("=" * 60)