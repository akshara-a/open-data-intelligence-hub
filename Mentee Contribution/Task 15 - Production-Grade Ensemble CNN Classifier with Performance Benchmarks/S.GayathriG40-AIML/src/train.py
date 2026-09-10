import time
from pathlib import Path

from tensorflow import keras

from src.data_loader import (
    load_cifar10,
    train_val_split
)

from src.preprocessing import preprocess_dataset

from models.cnn_models import (
    build_baseline_cnn,
    build_regularized_cnn,
    build_deep_cnn
)


BATCH_SIZE = 32
EPOCHS = 30
VALIDATION_SIZE = 5000


ROOT = Path(__file__).resolve().parents[1]

MODELS_DIR = ROOT / "models"

MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def train_model(
    model,
    model_name,
    X_train,
    y_train,
    X_val,
    y_val
):

    model_path = MODELS_DIR / (
        model_name + ".keras"
    )

    callbacks = [

        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        keras.callbacks.ModelCheckpoint(
            str(model_path),
            monitor="val_accuracy",
            save_best_only=True
        ),

        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2
        )
    ]

    start = time.perf_counter()

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )

    elapsed = time.perf_counter() - start

    print(
        "Training time:",
        round(elapsed, 2),
        "seconds"
    )

    return model, history


def main():

    X_train, y_train, X_test, y_test = load_cifar10()

    (
        X_train,
        y_train,
        X_val,
        y_val
    ) = train_val_split(
        X_train,
        y_train,
        VALIDATION_SIZE
    )

    (
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    ) = preprocess_dataset(
        X_train,
        y_train,
        X_val,
        y_val,
        X_test,
        y_test
    )

    models = [

        (
            build_baseline_cnn(),
            "cnn_baseline"
        ),

        (
            build_regularized_cnn(),
            "cnn_regularized"
        ),

        (
            build_deep_cnn(),
            "cnn_deep"
        )
    ]

    for model, name in models:

        print("\nTraining:", name)

        train_model(
            model,
            name,
            X_train,
            y_train,
            X_val,
            y_val
        )

    print("\nTraining completed.")


if __name__ == "__main__":
    main()