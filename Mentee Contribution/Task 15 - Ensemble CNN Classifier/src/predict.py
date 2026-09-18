import numpy as np
import tensorflow as tf

from src.data_loader import load_mnist_data
from src.preprocessing import normalize_images
from src.ensemble import average_predictions
from src.ensemble import get_ensemble_labels


def make_predictions():
    print("Loading test dataset...")

    _, _, x_test, y_test = load_mnist_data()

    # Normalize test images
    _, x_test = normalize_images(
        x_test,
        x_test
    )

    print("Loading trained CNN models...")

    model_1 = tf.keras.models.load_model(
        "models/cnn_model_1.keras"
    )

    model_2 = tf.keras.models.load_model(
        "models/cnn_model_2.keras"
    )

    print("Generating predictions...")

    predictions_1 = model_1.predict(
        x_test,
        verbose=0
    )

    predictions_2 = model_2.predict(
        x_test,
        verbose=0
    )

    ensemble_predictions = average_predictions(
        predictions_1,
        predictions_2
    )

    ensemble_labels = get_ensemble_labels(
        ensemble_predictions
    )

    print("\nSample Predictions:")

    for index in range(10):
        print(
            "Actual:",
            y_test[index],
            "| Predicted:",
            ensemble_labels[index]
        )

    accuracy = np.mean(
        ensemble_labels == y_test
    )

    print("\nPrediction accuracy:", accuracy)


if __name__ == "__main__":
    make_predictions()