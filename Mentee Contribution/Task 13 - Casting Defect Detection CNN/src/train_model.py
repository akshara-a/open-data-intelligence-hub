from pathlib import Path
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    Dropout
)
from tensorflow.keras.optimizers import Adam

from data_preparation import load_dataset, IMAGE_SIZE


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_DIR / "models"
REPORT_DIR = PROJECT_DIR / "reports"

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def build_cnn_model():
    """
    Creates the CNN model.
    """

    model = Sequential(
        [
            Conv2D(
                32,
                (3, 3),
                activation="relu",
                input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
            ),

            MaxPooling2D(pool_size=(2, 2)),

            Conv2D(
                64,
                (3, 3),
                activation="relu"
            ),

            MaxPooling2D(pool_size=(2, 2)),

            Conv2D(
                128,
                (3, 3),
                activation="relu"
            ),

            MaxPooling2D(pool_size=(2, 2)),

            Flatten(),

            Dense(128, activation="relu"),

            Dropout(0.5),

            Dense(1, activation="sigmoid")
        ]
    )

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model


def plot_training_history(history):
    """
    Saves training accuracy and loss graphs.
    """

    # Accuracy graph
    plt.figure(figsize=(8, 5))

    plt.plot(history.history["accuracy"], label="Training Accuracy")
    plt.plot(
        history.history["val_accuracy"],
        label="Validation Accuracy"
    )

    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    accuracy_path = REPORT_DIR / "training_accuracy.png"
    plt.savefig(accuracy_path)
    plt.close()

    # Loss graph
    plt.figure(figsize=(8, 5))

    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(
        history.history["val_loss"],
        label="Validation Loss"
    )

    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    loss_path = REPORT_DIR / "training_loss.png"
    plt.savefig(loss_path)
    plt.close()

    print("Training graphs saved inside the reports folder.")


def train_model():
    """
    Loads data, trains the CNN, and saves the model.
    """

    train_generator, validation_generator, test_generator = load_dataset()

    model = build_cnn_model()

    model.summary()

    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=10
    )

    model_path = MODEL_DIR / "casting_defect_cnn.keras"
    model.save(model_path)

    print(f"Model saved at: {model_path}")

    plot_training_history(history)

    test_loss, test_accuracy = model.evaluate(test_generator)

    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")


if __name__ == "__main__":
    train_model()