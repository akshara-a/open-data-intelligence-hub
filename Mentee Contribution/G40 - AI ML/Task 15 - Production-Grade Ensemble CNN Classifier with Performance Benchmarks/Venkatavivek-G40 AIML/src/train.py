"""Model Training Orchestrator and Artifact Saving."""

import os
import matplotlib.pyplot as plt
import tensorflow as tf
from augmentation import build_augmentation_pipeline
from data_loader import load_cifar10_data
from models import build_baseline_cnn, build_deep_cnn, build_regularized_cnn
from preprocessing import preprocess_dataset


def train_single_model(
    model_builder,
    model_name: str,
    x_train,
    y_train_cat,
    x_val,
    y_val_cat,
    use_augmentation: bool = False,
    epochs: int = 30,
    batch_size: int = 32,
    save_dir: str = "models",
    results_dir: str = "results",
) -> tf.keras.Model:
    """Trains a single CNN architecture with early stopping and checkpointing.

    Args:
        model_builder: Builder function returning an uncompiled Keras model.
        model_name: Identifier name string for logging and filesystem.
        x_train: Normalized training set features.
        y_train_cat: One-hot encoded training targets.
        x_val: Normalized validation features.
        y_val_cat: One-hot encoded validation targets.
        use_augmentation: If True, wraps model with augmentation pipeline.
        epochs: Max epochs to train.
        batch_size: Mini-batch gradient step size.
        save_dir: Output path for saved models.
        results_dir: Output path for diagnostic plots.

    Returns:
        tf.keras.Model: Trained optimal model instance loaded from checkpoint.
    """
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    base_model = model_builder(
        input_shape=x_train.shape[1:], num_classes=y_train_cat.shape[1]
    )

    if use_augmentation:
        aug_pipeline = build_augmentation_pipeline(x_train.shape[1:])
        inputs = tf.keras.Input(shape=x_train.shape[1:])
        x = aug_pipeline(inputs)
        outputs = base_model(x)
        model = tf.keras.Model(
            inputs=inputs, outputs=outputs, name=f"{model_name}_Augmented"
        )
    else:
        model = base_model

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    checkpoint_path = os.path.join(save_dir, f"{model_name}.keras")

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=6, restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path, monitor="val_loss", save_best_only=True
        ),
    ]

    history = model.fit(
        x_train,
        y_train_cat,
        validation_data=(x_val, y_val_cat),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1,
    )

    # Plot history curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(history.history["loss"], label="Train Loss")
    ax1.plot(history.history["val_loss"], label="Val Loss")
    ax1.set_title(f"{model_name} Loss Curve")
    ax1.legend()

    ax2.plot(history.history["accuracy"], label="Train Accuracy")
    ax2.plot(history.history["val_accuracy"], label="Val Accuracy")
    ax2.set_title(f"{model_name} Accuracy Curve")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(
        os.path.join(results_dir, f"training_history_{model_name}.png")
    )
    plt.close()

    return tf.keras.models.load_model(checkpoint_path)


def run_training_pipeline():
    """Runs complete end-to-end training execution routine across models."""
    (x_tr, y_tr), (x_va, y_va), _, _ = load_cifar10_data()
    x_tr_norm, y_tr_cat = preprocess_dataset(x_tr, y_tr)
    x_va_norm, y_va_cat = preprocess_dataset(x_va, y_va)

    models_dict = {
        "cnn_baseline": (build_baseline_cnn, False),
        "cnn_regularized": (build_regularized_cnn, True),
        "cnn_deep": (build_deep_cnn, True),
    }

    for name, (builder, aug_flag) in models_dict.items():
        print(f"--- Training Model: {name} ---")
        train_single_model(
            model_builder=builder,
            model_name=name,
            x_train=x_tr_norm,
            y_train_cat=y_tr_cat,
            x_val=x_va_norm,
            y_val_cat=y_va_cat,
            use_augmentation=aug_flag,
        )


if __name__ == "__main__":
    run_training_pipeline()