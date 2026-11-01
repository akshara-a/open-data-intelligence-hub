import json
import shutil
import matplotlib.pyplot as plt
import tensorflow as tf

from .config import (
    MODELS_DIR, RESULTS_DIR, MAX_EPOCHS, LEARNING_RATE,
    CLASS_NAMES, SEED
)
from .data_loader import create_or_load_splits
from .dataset import build_dataset, sanity_check_dataset
from .augmentation import build_augmentation
from .models.baseline_cnn import build_model as build_baseline
from .models.regularized_cnn import build_model as build_regularized
from .models.deep_cnn import build_model as build_deep

def plot_history(history, model_name):
    for metric, title in [("accuracy", "Accuracy"), ("loss", "Loss")]:
        plt.figure(figsize=(7, 5))
        plt.plot(history.history[metric], label="Training")
        plt.plot(history.history["val_" + metric], label="Validation")
        plt.xlabel("Epoch")
        plt.ylabel(title)
        plt.title(f"{model_name} {title}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f"{model_name}_{metric}.png", dpi=150)
        plt.close()

def make_training_model(base_model):
    inputs = tf.keras.Input(shape=base_model.input_shape[1:])
    x = build_augmentation()(inputs)
    outputs = base_model(x)
    return tf.keras.Model(inputs, outputs, name=base_model.name)

def main():
    tf.keras.utils.set_random_seed(SEED)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Always recreate splits for this corrected project.
    train_df, val_df, _ = create_or_load_splits(force_recreate=True)

    train_ds = build_dataset(train_df, training=True)
    val_ds = build_dataset(val_df, training=False)
    sanity_check_dataset(train_ds, expected_classes=len(CLASS_NAMES))

    model_builders = {
        "cnn_baseline": build_baseline,
        "cnn_regularized": build_regularized,
        "cnn_deep": build_deep,
    }

    summary = {}

    for name, builder in model_builders.items():
        print("\n" + "=" * 70)
        print(f"TRAINING: {name}")
        print("=" * 70)

        tf.keras.backend.clear_session()
        tf.keras.utils.set_random_seed(SEED)

        base_model = builder(num_classes=len(CLASS_NAMES))
        model = make_training_model(base_model)

        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=LEARNING_RATE,
                clipnorm=1.0,
            ),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=["accuracy"],
        )

        model_path = MODELS_DIR / f"{name}.keras"
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                model_path,
                monitor="val_accuracy",
                mode="max",
                save_best_only=True,
                verbose=1,
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor="val_accuracy",
                mode="max",
                patience=8,
                min_delta=0.002,
                restore_best_weights=True,
                verbose=1,
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.5,
                patience=3,
                min_lr=1e-5,
                verbose=1,
            ),
        ]

        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=MAX_EPOCHS,
            callbacks=callbacks,
            verbose=2,
        )

        plot_history(history, name)
        summary[name] = {
            "best_validation_accuracy": float(max(history.history["val_accuracy"])),
            "best_validation_loss": float(min(history.history["val_loss"])),
            "epochs_completed": len(history.history["loss"]),
            "parameters": int(model.count_params()),
        }

        # Important diagnostic: if a model remains at random chance, stop immediately.
        best_acc = summary[name]["best_validation_accuracy"]
        if best_acc < 0.30:
            print(
                f"\nWARNING: {name} did not learn adequately "
                f"(best validation accuracy {best_acc:.3f}). "
                "Training is stopping so you do not waste time."
            )
            break

    with open(RESULTS_DIR / "training_summary.json", "w", encoding="utf-8") as f:
        json.dump({"classes": CLASS_NAMES, "models": summary}, f, indent=2)

    print("\nTraining finished. Next run:")
    print("  python -m src.evaluate")
    print("  python -m src.benchmark")
    print("  python -m src.robustness_test")

if __name__ == "__main__":
    main()
