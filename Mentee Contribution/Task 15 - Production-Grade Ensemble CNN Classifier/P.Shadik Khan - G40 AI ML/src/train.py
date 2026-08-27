from pathlib import Path

from tensorflow import keras

from src.data_loader import load_datasets, optimize_dataset
from src.models.baseline_cnn import build_baseline_cnn
from src.models.deep_cnn import build_deep_cnn
from src.models.regularized_cnn import build_regularized_cnn


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

EPOCHS = 15


def compile_model(model):
    """Compile a CNN model for binary classification."""
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall"),
        ],
    )
    return model


def get_callbacks(model_name):
    """Create callbacks for stable model training."""
    return [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=MODELS_DIR / f"{model_name}.keras",
            monitor="val_loss",
            save_best_only=True,
        ),
    ]


def train_model(model, model_name, train_ds, validation_ds):
    """Compile and train one CNN model."""
    print("\n" + "=" * 70)
    print(f"TRAINING: {model_name}")
    print("=" * 70)

    compile_model(model)

    model.summary()

    history = model.fit(
        train_ds,
        validation_data=validation_ds,
        epochs=EPOCHS,
        callbacks=get_callbacks(model_name),
    )

    print(
        f"\nBest model saved to: "
        f"{MODELS_DIR / f'{model_name}.keras'}"
    )

    return history


def main():
    """Train only CNN models that do not already exist."""
    print("=" * 70)
    print("TASK 15 - CNN MODEL TRAINING")
    print("=" * 70)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nLoading datasets...")

    train_ds, validation_ds, test_ds = load_datasets()

    class_names = train_ds.class_names

    train_ds = optimize_dataset(train_ds)
    validation_ds = optimize_dataset(validation_ds)
    test_ds = optimize_dataset(test_ds)

    print("\nDatasets loaded successfully.")
    print(f"Classes: {class_names}")

    models = [
        (build_baseline_cnn, "baseline_cnn"),
        (build_deep_cnn, "deep_cnn"),
        (build_regularized_cnn, "regularized_cnn"),
    ]

    trained_models = []

    for build_function, model_name in models:

        model_path = MODELS_DIR / f"{model_name}.keras"

        if model_path.exists():
            print("\n" + "=" * 70)
            print(f"SKIPPING: {model_name}")
            print("=" * 70)
            print(f"Existing model found:")
            print(model_path)
            trained_models.append(model_name)
            continue

        model = build_function()

        train_model(
            model,
            model_name,
            train_ds,
            validation_ds,
        )

        trained_models.append(model_name)

    print("\n" + "=" * 70)
    print("MODEL TRAINING CHECK")
    print("=" * 70)

    for model_name in trained_models:
        model_path = MODELS_DIR / f"{model_name}.keras"

        if model_path.exists():
            print(f"[OK] {model_name}: {model_path}")
        else:
            print(f"[MISSING] {model_name}")

    print("\n" + "=" * 70)
    print("TRAINING PIPELINE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()