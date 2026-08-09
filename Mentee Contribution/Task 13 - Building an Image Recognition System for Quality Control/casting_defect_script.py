import tensorflow as tf
import numpy as np

def predict_product(image_path, model_path="models/best_casting_defect_model.keras", threshold=0.50):
    model = tf.keras.models.load_model(model_path)
    image = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    image_array = tf.keras.utils.img_to_array(image)
    image_array = tf.expand_dims(image_array, axis=0)

    defect_probability = float(model.predict(image_array, verbose=0)[0][0])

    if defect_probability >= threshold:
        predicted_class = "Defective (1)"
        recommended_action = "Reject or send for manual inspection"
    else:
        predicted_class = "Non-defective (0)"
        recommended_action = "Product may proceed on production line"

    print(f"Prediction: {predicted_class}")
    print(f"Defect probability: {defect_probability:.2%}")
    print(f"Recommended action: {recommended_action}")

if __name__ == "__main__":
    import sys
    img_path = sys.argv[1] if len(sys.argv) > 1 else "data/test/def_front/img_0000.jpeg"
    predict_product(img_path)
