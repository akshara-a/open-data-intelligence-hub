import numpy as np

from src.data_loader import load_mnist_data
from src.cnn_models import create_cnn_model_1, create_cnn_model_2


def train_models():
    print("Loading dataset...")

    x_train, y_train, x_test, y_test = load_mnist_data()

    # Normalize pixel values
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    print("\nCreating CNN models...")

    model_1 = create_cnn_model_1()
    model_2 = create_cnn_model_2()

    print("\nTraining CNN Model 1...")

    model_1.fit(
        x_train,
        y_train,
        epochs=3,
        batch_size=64,
        validation_split=0.1
    )

    print("\nTraining CNN Model 2...")

    model_2.fit(
        x_train,
        y_train,
        epochs=3,
        batch_size=64,
        validation_split=0.1
    )

    print("\nEvaluating CNN Model 1...")

    loss_1, accuracy_1 = model_1.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    print("CNN Model 1 accuracy:", accuracy_1)

    print("\nEvaluating CNN Model 2...")

    loss_2, accuracy_2 = model_2.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    print("CNN Model 2 accuracy:", accuracy_2)

    print("\nGenerating ensemble predictions...")

    predictions_1 = model_1.predict(x_test, verbose=0)
    predictions_2 = model_2.predict(x_test, verbose=0)

    ensemble_predictions = (
        predictions_1 + predictions_2
    ) / 2

    ensemble_labels = np.argmax(
        ensemble_predictions,
        axis=1
    )

    ensemble_accuracy = np.mean(
        ensemble_labels == y_test
    )

    print("Ensemble CNN accuracy:", ensemble_accuracy)

    # Save trained models
    model_1.save("models/cnn_model_1.keras")
    model_2.save("models/cnn_model_2.keras")

    print("\nModels saved successfully.")


if __name__ == "__main__":
    train_models()