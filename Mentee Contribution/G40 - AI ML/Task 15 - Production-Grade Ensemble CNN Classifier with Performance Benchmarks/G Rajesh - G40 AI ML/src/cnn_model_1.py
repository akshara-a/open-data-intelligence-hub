import os
import sys

import matplotlib.pyplot as plt
import tensorflow as tf


# Allow importing data_loader.py from the same src directory.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import (
    prepare_datasets,
    create_tf_datasets,
    NUM_CLASSES,
)


SEED = 42
EPOCHS = 20
LEARNING_RATE = 0.001

MODEL_PATH = "models/cnn_model_1.keras"
REPORTS_DIR = "reports"


tf.keras.utils.set_random_seed(SEED)


def build_model():
    """Build CNN Model 1."""

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(
                shape=(32, 32, 3)
            ),

            tf.keras.layers.Conv2D(
                32,
                (3, 3),
                padding="same",
                activation="relu",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(
                32,
                (3, 3),
                padding="same",
                activation="relu",
            ),
            tf.keras.layers.MaxPooling2D(
                (2, 2)
            ),
            tf.keras.layers.Dropout(0.25),

            tf.keras.layers.Conv2D(
                64,
                (3, 3),
                padding="same",
                activation="relu",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(
                64,
                (3, 3),
                padding="same",
                activation="relu",
            ),
            tf.keras.layers.MaxPooling2D(
                (2, 2)
            ),
            tf.keras.layers.Dropout(0.25),

            tf.keras.layers.Conv2D(
                128,
                (3, 3),
                padding="same",
                activation="relu",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(
                (2, 2)
            ),
            tf.keras.layers.Dropout(0.30),

            tf.keras.layers.Flatten(),

            tf.keras.layers.Dense(
                128,
                activation="relu",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.40),

            tf.keras.layers.Dense(
                NUM_CLASSES,
                activation="softmax",
            ),
        ],
        name="CNN_Model_1",
    )

    return model


def plot_history(history):
    """Save training accuracy and loss graphs."""

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Accuracy
    plt.figure(figsize=(10, 6))

    plt.plot(
        history.history["accuracy"],
        label="Training Accuracy",
    )

    plt.plot(
        history.history["val_accuracy"],
        label="Validation Accuracy",
    )

    plt.title("CNN Model 1 - Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            REPORTS_DIR,
            "cnn_model_1_accuracy.png",
        ),
        dpi=150,
    )

    plt.close()

    # Loss
    plt.figure(figsize=(10, 6))

    plt.plot(
        history.history["loss"],
        label="Training Loss",
    )

    plt.plot(
        history.history["val_loss"],
        label="Validation Loss",
    )

    plt.title("CNN Model 1 - Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            REPORTS_DIR,
            "cnn_model_1_loss.png",
        ),
        dpi=150,
    )

    plt.close()

    print(
        "Training graphs saved successfully."
    )


def main():

    print("=" * 60)
    print("TASK 15 - CNN MODEL 1")
    print("=" * 60)

    print("\nPreparing CIFAR-10 datasets...")

    (
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    ) = prepare_datasets()

    train_ds, val_ds, test_ds = create_tf_datasets(
        x_train,
        y_train,
        x_val,
        y_val,
        x_test,
        y_test,
    )

    print("\nBuilding CNN Model 1...")

    model = build_model()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),
        loss="sparse_categorical_crossentropy",
        metrics=[
            "accuracy",
        ],
    )

    model.summary()

    os.makedirs("models", exist_ok=True)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
    ]

    print("\nStarting CNN Model 1 training...")
    print(f"Epochs: {EPOCHS}")
    print(f"Learning rate: {LEARNING_RATE}")

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    print("\nLoading best saved model...")

    best_model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("\nEvaluating CNN Model 1 on test data...")

    test_loss, test_accuracy = (
        best_model.evaluate(
            test_ds,
            verbose=1,
        )
    )

    print("\n" + "=" * 60)
    print("CNN MODEL 1 TEST RESULTS")
    print("=" * 60)

    print(
        f"Test Loss:     {test_loss:.4f}"
    )

    print(
        f"Test Accuracy: {test_accuracy:.4f}"
    )

    print(
        f"Test Accuracy: {test_accuracy * 100:.2f}%"
    )

    plot_history(history)

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nTASK 15 CNN MODEL 1 COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()