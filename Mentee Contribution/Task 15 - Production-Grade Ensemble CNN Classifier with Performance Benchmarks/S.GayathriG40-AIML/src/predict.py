import numpy as np
from pathlib import Path

from tensorflow import keras

from src.data_loader import CLASS_NAMES


def load_model(model_name):

    root = Path(__file__).resolve().parents[1]

    model_path = (
        root /
        "models" /
        (model_name + ".keras")
    )

    return keras.models.load_model(
        model_path
    )


def get_predictions(
    model,
    images
):

    probabilities = model.predict(
        images,
        verbose=0
    )

    predictions = np.argmax(
        probabilities,
        axis=1
    )

    return (
        probabilities,
        predictions
    )


def predict_image(
    model,
    image
):

    image = np.asarray(
        image,
        dtype="float32"
    )

    if image.max() > 1:

        image = image / 255.0

    image = np.expand_dims(
        image,
        axis=0
    )

    probabilities, predictions = (
        get_predictions(
            model,
            image
        )
    )

    class_id = int(
        predictions[0]
    )

    return {
        "class_id": class_id,
        "class_name": CLASS_NAMES[class_id],
        "confidence": float(
            probabilities[0][class_id]
        )
    }