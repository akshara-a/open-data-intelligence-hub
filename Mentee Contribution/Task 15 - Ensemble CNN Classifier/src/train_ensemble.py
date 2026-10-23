import numpy as np
import tensorflow as tf

from src.data_loader import load_mnist_data
from src.cnn_models import create_cnn_model_1, create_cnn_model_2


def train_models():
    print("Loading dataset...")

    x_train, y_train, x_test, y_test = load_mnist_data()

    # Normalize image values from 0-255 to 0-1
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

    # Get prediction probabilities from both models
    predictions_1 = model_1.predict(x_test, verbose=0)
    predictions_2 = model_2.predict(x_test, verbose=0)

    # Average the predictions
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

    print("\nEnsemble CNN accuracy:", ensemble_accuracy)

    # Save models
    model_1.save("models/cnn_model_1.keras")
    model_2.save("models/cnn_model_2.keras")

    print("\nModels saved successfully.")


if __name__ == "__main__":
    train_models()