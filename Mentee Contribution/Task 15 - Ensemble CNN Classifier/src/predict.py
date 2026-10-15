import os
import sys
import numpy as np
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data


MODEL_DIR = "models"

CLASS_NAMES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]


def load_best_model():

    model_path = os.path.join(
        MODEL_DIR,
        "deep_cnn.keras"
    )

    print("Loading Deep CNN model...")

    model = tf.keras.models.load_model(
        model_path
    )

    print("Model loaded successfully!")

    return model


def predict_sample_image(model, X_test, y_test):

    # Select a sample image
    image_index = 0

    image = X_test[image_index]

    # Add batch dimension
    input_image = np.expand_dims(
        image,
        axis=0
    )

    # Make prediction
    prediction = model.predict(
        input_image,
        verbose=0
    )

    predicted_class = np.argmax(
        prediction[0]
    )

    confidence = np.max(
        prediction[0]
    )

    actual_class = y_test[image_index]

    print("\n" + "=" * 60)
    print("IMAGE PREDICTION")
    print("=" * 60)

    print(
        f"Actual Class    : "
        f"{CLASS_NAMES[actual_class]}"
    )

    print(
        f"Predicted Class : "
        f"{CLASS_NAMES[predicted_class]}"
    )

    print(
        f"Confidence      : "
        f"{confidence * 100:.2f}%"
    )

    if actual_class == predicted_class:

        print("\nPrediction: CORRECT ✅")

    else:

        print("\nPrediction: INCORRECT ❌")


def main():

    # Load dataset
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    # Load best model
    model = load_best_model()

    # Predict one image
    predict_sample_image(
        model,
        X_test,
        y_test
    )


if __name__ == "__main__":
    main()