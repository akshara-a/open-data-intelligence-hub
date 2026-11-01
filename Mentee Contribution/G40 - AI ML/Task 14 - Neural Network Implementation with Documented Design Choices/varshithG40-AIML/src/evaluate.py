import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
from src.data_loader import load_datasets

def evaluate_model(model_path="models/cnn_casting_model.keras", save_dir="plots"):
    os.makedirs(save_dir, exist_ok=True)
    _, _, test_dataset = load_datasets()
    
    print(f"Loading trained model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("\nEvaluating on Test Dataset:")
    test_results = model.evaluate(test_dataset)
    metrics_names = model.metrics_names
    for name, val in zip(metrics_names, test_results):
        print(f"  {name.capitalize()}: {val:.4f}")
        
    # Get true labels and predicted probabilities
    actual_labels = []
    probabilities = []
    
    for images, labels in test_dataset:
        preds = model.predict(images, verbose=0)
        actual_labels.extend(labels.numpy().flatten())
        probabilities.extend(preds.flatten())
        
    actual_labels = np.array(actual_labels, dtype=int)
    probabilities = np.array(probabilities)
    predictions = (probabilities >= 0.5).astype(int)
    
    # Compute confusion matrix
    cm = confusion_matrix(actual_labels, predictions)
    print("\nConfusion Matrix:")
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(actual_labels, predictions, target_names=["Non-defective (0)", "Defective (1)"]))
    
    # Plot Confusion Matrix Heatmap
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Non-defective (0)', 'Defective (1)'],
                yticklabels=['Non-defective (0)', 'Defective (1)'],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title("Confusion Matrix - Casting Defect Inspection", fontsize=14, fontweight='bold')
    plt.xlabel("Predicted Class", fontsize=12)
    plt.ylabel("Actual Class", fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/confusion_matrix.png", dpi=300)
    plt.close()
    
    print(f"Confusion matrix plot saved to {save_dir}/confusion_matrix.png")
    return test_results, cm, actual_labels, predictions, probabilities

if __name__ == "__main__":
    evaluate_model()
