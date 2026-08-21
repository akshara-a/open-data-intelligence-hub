"""
Single Image Inference Module for Casting Defect Detection
Accepts product image path and outputs predicted class, defect probability, decision threshold, and factory action.
"""

import os
import argparse
import tensorflow as tf
import numpy as np

def predict_product(image_path, model_or_path="models/best_casting_defect_model.keras", threshold=0.50):
    """
    Predicts defect status for a single product casting image.
    
    Args:
        image_path: Path to target product image file.
        model_or_path: Loaded tf.keras Model instance OR path string to saved .keras file.
        threshold: Decision threshold probability (default: 0.50).
        
    Returns:
        dict: Inference results dictionary containing predicted_class, probability, threshold, and action.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target image not found at '{image_path}'.")

    # Load model if string path is passed
    if isinstance(model_or_path, str):
        if not os.path.exists(model_or_path):
            raise FileNotFoundError(f"Saved model file not found at '{model_or_path}'. Run train.py first.")
        model = tf.keras.models.load_model(model_or_path)
    else:
        model = model_or_path

    # Load and preprocess image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )
    image_array = tf.keras.utils.img_to_array(image)
    image_batch = tf.expand_dims(image_array, axis=0)

    # Perform inference
    defect_probability = float(model.predict(image_batch, verbose=0)[0][0])

    if defect_probability >= threshold:
        predicted_class = "Defective"
        binary_label = 1
        recommended_action = "Send for manual inspection"
    else:
        predicted_class = "Non-defective"
        binary_label = 0
        recommended_action = "Product may proceed"

    results = {
        "image_path": image_path,
        "predicted_class": predicted_class,
        "binary_label": binary_label,
        "defect_probability": defect_probability,
        "threshold": threshold,
        "recommended_action": recommended_action
    }

    # Print output formatted as specified in business scenario
    print("\n" + "=" * 50)
    print("      INDUSTRIAL QUALITY INSPECTION RESULT      ")
    print("=" * 50)
    print(f"Image File          : {os.path.basename(image_path)}")
    print(f"Prediction          : {predicted_class}")
    print(f"Defect Probability  : {defect_probability:.2%}")
    print(f"Decision Threshold  : {threshold:.2%}")
    print(f"Recommended Action  : {recommended_action}")
    print("=" * 50 + "\n")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inference CLI for Casting Product Quality Inspection")
    parser.add_argument("--image", type=str, default="sample_images/sample_def_1.jpg", help="Path to input image")
    parser.add_argument("--model", type=str, default="models/best_casting_defect_model.keras", help="Path to trained model")
    parser.add_argument("--threshold", type=float, default=0.50, help="Classification decision threshold (0.0 - 1.0)")
    
    args = parser.parse_args()
    predict_product(args.image, args.model, args.threshold)
