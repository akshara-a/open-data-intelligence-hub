import os
import json
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

def main():
    os.makedirs("reports", exist_ok=True)
    
    model_path = "models/best_cnn_model.keras"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Run train.py first.")
        
    model = tf.keras.models.load_model(model_path)
    
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        "data/test",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )
    
    print("\n--- Evaluating Model on Test Dataset ---")
    test_results = model.evaluate(test_dataset)
    metrics_names = model.metrics_names
    for name, val in zip(metrics_names, test_results):
        print(f"Test {name.capitalize()}: {val:.4f}")
        
    # Get actual labels and predictions
    actual_labels = []
    for images, labels in test_dataset:
        actual_labels.extend(labels.numpy().flatten())
    actual_labels = np.array(actual_labels, dtype=int)
    
    probabilities = model.predict(test_dataset)
    predictions = (probabilities.flatten() >= 0.5).astype(int)
    
    # Compute Confusion Matrix
    cm = confusion_matrix(actual_labels, predictions)
    print("\n--- Confusion Matrix ---")
    print(cm)
    print("\n--- Classification Report ---")
    print(classification_report(actual_labels, predictions, target_names=["ok_front (0)", "def_front (1)"]))
    
    # Plot Confusion Matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=["ok_front (0)", "def_front (1)"],
           yticklabels=["ok_front (0)", "def_front (1)"],
           title="Confusion Matrix - Casting Quality Inspection",
           ylabel="Actual Label",
           xlabel="Predicted Label")
    
    # Annotate matrix cells
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.savefig("reports/confusion_matrix.png", dpi=300)
    plt.close()
    
    # Plot Training & Validation History Graphs if available
    history_path = "reports/history.json"
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history = json.load(f)
            
        epochs = range(1, len(history["accuracy"]) + 1)
        
        # Accuracy Graph
        plt.figure(figsize=(7, 5))
        plt.plot(epochs, history["accuracy"], 'b-o', label="Training Accuracy")
        plt.plot(epochs, history["val_accuracy"], 'r-s', label="Validation Accuracy")
        plt.title("Training and Validation Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend(loc="lower right")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig("reports/accuracy_graph.png", dpi=300)
        plt.close()
        
        # Loss Graph
        plt.figure(figsize=(7, 5))
        plt.plot(epochs, history["loss"], 'b-o', label="Training Loss")
        plt.plot(epochs, history["val_loss"], 'r-s', label="Validation Loss")
        plt.title("Training and Validation Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend(loc="upper right")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig("reports/loss_graph.png", dpi=300)
        plt.close()
        
        print("\nEvaluation graphs saved to reports/ directory.")

if __name__ == "__main__":
    main()
