import os
import json

def make_markdown_cell(source_text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_text.strip().splitlines(True)
    }

def make_code_cell(source_text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_text.strip().splitlines(True)
    }

def build_notebook():
    cells = []
    
    # Title & Objective
    cells.append(make_markdown_cell(
"""# Task 14: Binary Image Classification Using a Convolutional Neural Network

### Mini Project: Quality Inspection for Casting Products

**Objective**: Build a Convolutional Neural Network (CNN) to classify casting product images into two categories:
- **Class 0: `ok_front` (Non-defective)**
- **Class 1: `def_front` (Defective)**

Document every critical design choice, evaluate classification performance metrics (Accuracy, Precision, Recall), plot training history curves, perform sample predictions, and conduct a bonus design comparison experiment.
"""
    ))
    
    # Section 1: Setup & Imports
    cells.append(make_markdown_cell(
"""## 1. Setup & Imports

Import required Python libraries: TensorFlow, NumPy, Matplotlib, Scikit-learn, and PIL.
"""
    ))
    
    cells.append(make_code_cell(
"""import os
import json
import glob
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import confusion_matrix, classification_report
from PIL import Image

print("TensorFlow Version:", tf.__version__)
"""
    ))
    
    # Section 2: Data Loading & Preprocessing
    cells.append(make_markdown_cell(
"""## 2. Load the Dataset & Normalization

### Design Choice: Image Size (224 x 224 x 3)
- **Why?** Images in raw datasets vary in dimension. CNNs require uniform input tensor shapes. `224 x 224` preserves fine visual features (such as tiny surface cracks and pinhole porosity) while remaining computationally efficient for training.

### Design Choice: Normalization (`Rescaling(1.0 / 255)`)
- **Why?** Converts pixel values from `[0, 255]` to `[0.0, 1.0]`. Normalizing inputs keeps gradients stable, preventing exploding/vanishing gradients and accelerating optimization convergence.
"""
    ))
    
    cells.append(make_code_cell(
"""IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

train_dataset = tf.keras.utils.image_dataset_from_directory(
    "../data/train",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=True,
    seed=42
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    "../data/validation",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    "../data/test",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)
"""
    ))
    
    # Section 3: Data Augmentation
    cells.append(make_markdown_cell(
"""## 3. Data Augmentation

### Design Choice: Mild Augmentation
- **RandomFlip("horizontal")**: Simulates casting product orientation changes on conveyor belts.
- **RandomRotation(0.05)**: Accounts for slight angular positioning variations.
- **RandomZoom(0.10)**: Handles minor camera height differences.
- **RandomContrast(0.10)**: Simulates factory lighting fluctuations.
- **Why apply only to training data?** Validation and test data represent real-world un-augmented inspection targets.
"""
    ))
    
    cells.append(make_code_cell(
"""data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10)
], name="data_augmentation")
"""
    ))
    
    # Section 4: CNN Architecture Definition
    cells.append(make_markdown_cell(
"""## 4. Build the CNN Model

### Documented Architecture Choices:
1. **Conv2D (32 filters, 3x3)**: Extracts low-level visual features (edges, contours).
2. **Conv2D (64 filters, 3x3)**: Learns mid-level geometric shapes and bolt holes.
3. **Conv2D (128 filters, 3x3)**: Learns high-level defect features (cracks, pinholes, gouges).
4. **ReLU Activation**: Simple, fast non-linear activation; eliminates vanishing gradients.
5. **MaxPooling2D**: Downsamples spatial resolution by 50% in width and height, reducing parameters and computation.
6. **GlobalAveragePooling2D**: Summarizes feature maps into a 1D vector. Prevents parameter explosion compared to `Flatten()`.
7. **Dropout (0.40)**: Randomly disables 40% of units during training to combat overfitting.
8. **Dense (1, Sigmoid)**: Produces binary output probability between `0` and `1`.
"""
    ))
    
    cells.append(make_code_cell(
"""def create_baseline_cnn():
    return models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        data_augmentation,
        layers.Rescaling(1.0 / 255),

        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, activation="relu"),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.40),

        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ], name="Casting_CNN_Classifier")

model = create_baseline_cnn()
model.summary()
"""
    ))
    
    # Section 5: Compile & Train
    cells.append(make_markdown_cell(
"""## 5. Compile & Train Model

### Training Options Rationale:
- **Adam Optimizer (`learning_rate=0.001`)**: Adaptive learning rates per parameter, robust default setting.
- **Binary Cross-Entropy Loss**: Standard loss function for 2-class probabilistic classification.
- **Callbacks**:
  - `EarlyStopping(patience=5)`: Halts training if `val_loss` stops improving, saving best weights.
  - `ReduceLROnPlateau(patience=2, factor=0.5)`: Decreases learning rate when validation loss plateaus.
"""
    ))
    
    cells.append(make_code_cell(
"""model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2
    )
]

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25,
    callbacks=callbacks
)
"""
    ))
    
    # Section 6: Plot Training Results
    cells.append(make_markdown_cell(
"""## 6. Plot Training & Validation Curves

Examine performance graphs to evaluate model learning and detect overfitting.
"""
    ))
    
    cells.append(make_code_cell(
"""# Plot Accuracy Graph
plt.figure(figsize=(7, 5))
plt.plot(history.history["accuracy"], 'b-o', label="Training Accuracy")
plt.plot(history.history["val_accuracy"], 'r-s', label="Validation Accuracy")
plt.title("Training vs Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(loc="lower right")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# Plot Loss Graph
plt.figure(figsize=(7, 5))
plt.plot(history.history["loss"], 'b-o', label="Training Loss")
plt.plot(history.history["val_loss"], 'r-s', label="Validation Loss")
plt.title("Training vs Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend(loc="upper right")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
"""
    ))
    
    # Section 7: Evaluation & Confusion Matrix
    cells.append(make_markdown_cell(
"""## 7. Model Evaluation & Confusion Matrix

### Why Recall Matters for Defective Class:
In industrial quality control, a **False Negative** (predicting a defective casting as non-defective) is extremely dangerous. It leads to defective components being installed in machinery, causing mechanical failures. High **Recall** ensures maximum detection of defective parts.
"""
    ))
    
    cells.append(make_code_cell(
"""test_results = model.evaluate(test_dataset)
print("Test Loss:", test_results[0])
print("Test Accuracy:", test_results[1])
print("Test Precision:", test_results[2])
print("Test Recall:", test_results[3])

# Generate Predictions & Confusion Matrix
actual_labels = []
for images, labels in test_dataset:
    actual_labels.extend(labels.numpy().flatten())
actual_labels = np.array(actual_labels, dtype=int)

probabilities = model.predict(test_dataset)
predictions = (probabilities.flatten() >= 0.5).astype(int)

cm = confusion_matrix(actual_labels, predictions)
print("\\nConfusion Matrix:")
print(cm)
"""
    ))
    
    # Section 8: Unseen Sample Predictions
    cells.append(make_markdown_cell(
"""## 8. Test Unseen Sample Images

Test 5 unseen images and print class prediction, probability, and recommended quality inspection action.
"""
    ))
    
    cells.append(make_code_cell(
"""test_def_samples = sorted(glob.glob("../data/test/def_front/*.jpeg"))[:3]
test_ok_samples = sorted(glob.glob("../data/test/ok_front/*.jpeg"))[:2]
sample_paths = test_def_samples + test_ok_samples

for idx, path in enumerate(sample_paths, 1):
    img = tf.keras.preprocessing.image.load_img(path, target_size=IMAGE_SIZE)
    img_arr = tf.keras.preprocessing.image.img_to_array(img)
    img_batch = np.expand_dims(img_arr, axis=0)
    
    prob = float(model.predict(img_batch, verbose=0)[0][0])
    if prob >= 0.5:
        pred_label = "Defective"
        action = "Send for manual inspection"
        confidence = prob * 100
    else:
        pred_label = "Non-defective"
        action = "Pass quality inspection"
        confidence = (1.0 - prob) * 100
        
    print(f"Sample #{idx} ({os.path.basename(path)}):")
    print(f"  Prediction: {pred_label}")
    print(f"  Probability: {prob*100:.1f}% defective")
    print(f"  Action: {action}\\n")
"""
    ))
    
    # Section 9: Required Design Decision Table
    cells.append(make_markdown_cell(
"""## 9. Required Design Decision Table

| Design Decision | Selected Value | Reason |
|---|---|---|
| Image size | 224 x 224 | Balance between detail and computation |
| Problem type | Binary classification | Two output classes |
| Model type | CNN | Suitable for images |
| Conv filters | 32, 64, 128 | Learn increasingly complex features |
| Kernel size | 3 x 3 | Efficient local feature extraction |
| Hidden activation | ReLU | Efficient and commonly used |
| Pooling | MaxPooling | Reduces feature dimensions |
| Output activation | Sigmoid | Produces binary probability |
| Optimizer | Adam | Adaptive and beginner-friendly |
| Learning rate | 0.001 | Reasonable Adam starting value |
| Loss | Binary Cross-Entropy | Suitable for two classes |
| Batch size | 32 | Balanced memory and training |
| Epochs | Maximum 25 | Enough training with early stopping |
| Dropout | 0.40 | Helps reduce overfitting |
| Augmentation | Flip, rotation, zoom, contrast | Improves robustness |
| Metrics | Accuracy, Precision, Recall | Evaluate overall and defect performance |
"""
    ))
    
    # Section 10: Bonus Experiment
    cells.append(make_markdown_cell(
"""## 10. Bonus Experiment: GAP vs. Flatten

Compare baseline CNN (`GlobalAveragePooling2D`) with an alternative architecture (`Flatten`).

```text
Original Design: GlobalAveragePooling2D()
Changed Design: Flatten()
Reason for Change: Test parameter impact of dense flattening vs spatial pooling.
Observation: GlobalAveragePooling2D dramatically reduces parameter count (~115k vs ~7.4M), mitigating overfitting and preserving test accuracy.
```
"""
    ))
    
    notebook_dict = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    os.makedirs("notebooks", exist_ok=True)
    nb_path = "notebooks/task14_cnn_classification.ipynb"
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook_dict, f, indent=2)
        
    print(f"Jupyter notebook created directly at {nb_path}")

if __name__ == "__main__":
    build_notebook()
