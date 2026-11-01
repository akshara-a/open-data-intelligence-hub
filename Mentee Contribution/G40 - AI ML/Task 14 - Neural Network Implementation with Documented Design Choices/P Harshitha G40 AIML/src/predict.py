import os
import glob
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import tensorflow as tf
# pyrefly: ignore [missing-import]
from tensorflow.keras.preprocessing.image import load_img, img_to_array

IMAGE_SIZE = (224, 224)

def predict_sample_images(model_path: str = "models/best_cnn_model.keras", num_samples: int = 5):
    os.makedirs("predictions", exist_ok=True)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Run train.py first.")
        
    model = tf.keras.models.load_model(model_path)
    
    # Pick sample unseen test images (mix of ok_front and def_front)
    def_images = sorted(glob.glob("data/test/def_front/*.jpeg")) + sorted(glob.glob("data/test/def_front/*.png"))
    ok_images = sorted(glob.glob("data/test/ok_front/*.jpeg")) + sorted(glob.glob("data/test/ok_front/*.png"))
    
    # Select 3 defective, 2 non-defective to make 5 unseen images
    selected_paths = []
    if len(def_images) >= 3:
        selected_paths.extend(def_images[:3])
    else:
        selected_paths.extend(def_images)
        
    if len(ok_images) >= 2:
        selected_paths.extend(ok_images[:2])
    else:
        selected_paths.extend(ok_images)
        
    selected_paths = selected_paths[:num_samples]
    
    print(f"\n--- Testing {len(selected_paths)} Unseen Images ---")
    
    for idx, img_path in enumerate(selected_paths, start=1):
        # Load image for model input
        raw_img = load_img(img_path, target_size=IMAGE_SIZE)
        img_array = img_to_array(raw_img)
        img_batch = np.expand_dims(img_array, axis=0) # shape (1, 224, 224, 3)
        
        # Prediction probability
        prob = float(model.predict(img_batch, verbose=0)[0][0])
        
        # Decision based on 0.5 threshold
        if prob >= 0.5:
            pred_class = "Defective (Class 1)"
            confidence = prob * 100.0
            action = "Send for manual inspection"
            color = "red"
        else:
            pred_class = "Non-defective (Class 0)"
            confidence = (1.0 - prob) * 100.0
            action = "Pass quality inspection"
            color = "green"
            
        print(f"\nSample #{idx}: {os.path.basename(img_path)}")
        print(f"Prediction: {pred_class}")
        print(f"Probability: {prob*100:.1f}% defective (Confidence: {confidence:.1f}%)")
        print(f"Action: {action}")
        
        # Plot and save image with overlay
        display_img = load_img(img_path)
        plt.figure(figsize=(6, 6))
        plt.imshow(display_img)
        plt.title(f"Sample #{idx}: {os.path.basename(img_path)}\nPrediction: {pred_class} ({confidence:.1f}%)\nAction: {action}",
                  color=color, fontsize=11, fontweight='bold')
        plt.axis("off")
        plt.tight_layout()
        out_fig_path = f"predictions/prediction_{idx}.png"
        plt.savefig(out_fig_path, dpi=300)
        plt.close()
        
    print(f"\nAll sample predictions saved into predictions/ folder.")

if __name__ == "__main__":
    predict_sample_images()
