import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import glob
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def predict_unseen(model_path="models/cnn_casting_model.keras", unseen_dir="data/unseen", save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    model = tf.keras.models.load_model(model_path)
    
    unseen_files = sorted(glob.glob(f"{unseen_dir}/*.png"))
    if not unseen_files:
        print(f"No unseen images found in {unseen_dir}")
        return
    
    print(f"\n--- Testing Unseen Images from {unseen_dir} ---")
    results = []
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()
    
    for i, file_path in enumerate(unseen_files[:6]):
        img_raw = load_img(file_path, target_size=(224, 224))
        img_array = img_to_array(img_raw)
        img_batch = np.expand_dims(img_array, axis=0) # shape (1, 224, 224, 3)
        
        prob = model.predict(img_batch, verbose=0)[0][0]
        
        if prob >= 0.5:
            pred_label = "Defective"
            prob_percent = prob * 100
            action = "Send for manual inspection"
            color = "red"
        else:
            pred_label = "Non-defective"
            prob_percent = (1 - prob) * 100
            action = "Pass quality check"
            color = "green"
            
        filename = os.path.basename(file_path)
        print(f"Image: {filename}")
        print(f"  Prediction: {pred_label}")
        print(f"  Probability: {prob_percent:.1f}%")
        print(f"  Action: {action}\n")
        
        results.append({
            "filename": filename,
            "prediction": pred_label,
            "probability": prob_percent,
            "action": action
        })
        
        ax = axes[i]
        ax.imshow(img_raw)
        ax.axis("off")
        ax.set_title(f"{filename}\nPred: {pred_label} ({prob_percent:.1f}%)\n{action}",
                     fontsize=10, color=color, fontweight="bold")

    for j in range(len(unseen_files), len(axes)):
        axes[j].axis("off")
        
    plt.suptitle("Unseen Metal Casting Image Inspection Results", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/unseen_predictions.png", dpi=300)
    plt.close()
    
    print(f"Unseen predictions visualization saved to {save_dir}/unseen_predictions.png")
    return results

if __name__ == "__main__":
    predict_unseen()
