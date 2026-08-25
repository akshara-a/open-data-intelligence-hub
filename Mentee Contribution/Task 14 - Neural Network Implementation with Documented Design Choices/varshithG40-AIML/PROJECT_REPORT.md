# Binary Image Classification Using a Convolutional Neural Network
## Mini Project Report: Metal Casting Quality Inspection with Documented Design Choices

---

## 1. Project Title & Overview

**Title**: Binary Image Classification Using a Convolutional Neural Network  
**Domain**: Automated Industrial Quality Inspection  
**Dataset**: Casting Product Image Data for Quality Inspection  

### Classification Problem:
- **Class 0 (`ok_front`)**: Non-defective metal casting flange (smooth surface, clean concentric grooves, no structural defects).
- **Class 1 (`def_front`)**: Defective metal casting flange (contains surface pitting, cracks, blowholes, or voids).

---

## 2. Executive Summary & Objective

The primary objective of this project is to build a working Convolutional Neural Network (CNN) in TensorFlow/Keras capable of classifying casting product images into non-defective and defective classes, while rigorously documenting and explaining the rationale behind every architecture, regularization, optimization, and training choice.

---

## 3. Technology Stack

- **Programming Language**: Python 3.10+
- **Deep Learning Framework**: TensorFlow 2.10+ / Keras
- **Data & Numeric Libraries**: NumPy, PIL (Pillow)
- **Visualization Libraries**: Matplotlib, Seaborn
- **Machine Learning & Evaluation**: Scikit-Learn
- **Notebook Environment**: Jupyter Notebook (`notebooks/CNN_Casting_Inspection_Project.ipynb`)
- **Web Application Interface**: FastAPI + Vanilla HTML/CSS/JS (`http://127.0.0.1:8000`)

---

## 4. Dataset Loading & Preprocessing

```python
import tensorflow as tf

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

train_dataset = tf.keras.utils.image_dataset_from_directory(
    "data/train",
    class_names=["ok_front", "def_front"],
    image_size=(224, 224),
    batch_size=32,
    label_mode="binary"
)
```

- **Dataset Size**: 100 training images (50 `ok_front` + 50 `def_front`).

---

## 5. Design Choice Documentation

### 5.1 Image Size: 224 x 224 x 3
- **Rationale**: 
  1. Neural networks require uniform input dimensions across all dataset batches.
  2. $224 \times 224 \times 3$ (RGB) preserves subtle visual details needed to identify small casting surface defects like hairline cracks or micro-pitting.
  3. It remains computationally efficient and prevents memory bottlenecks on standard CPU/GPU setups.

### 5.2 Image Normalization: `Rescaling(1.0 / 255)`
- **Rationale**: Raw pixel intensities range from `0` to `255`. Rescaling them to $[0.0, 1.0]$ normalizes input values, preventing gradient saturation and leading to faster, more stable convergence during backpropagation.

### 5.3 Data Augmentation
- **Pipeline**:
  ```python
  data_augmentation = tf.keras.Sequential([
      tf.keras.layers.RandomFlip("horizontal"),
      tf.keras.layers.RandomRotation(0.05),
      tf.keras.layers.RandomZoom(0.10),
      tf.keras.layers.RandomContrast(0.10)
  ])
  ```
- **Rationale**: Augmentation exposes the CNN to minor real-world variations (such as component rotation on conveyor belts, camera alignment shifts, and lighting fluctuations). Augmentation is applied **only to training data**.

---

## 6. Model Architecture Design

```python
from tensorflow.keras import layers, models

model = models.Sequential([
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
])
```

### Architectural Decisions & Explanations:

1. **Conv2D Filters (32 -> 64 -> 128)**:
   - **Layer 1 (32 Filters)**: Learns simple low-level visual primitives (edges, intensity gradients, boundary lines).
   - **Layer 2 (64 Filters)**: Learns mid-level features (concentric circles, flange grooves, geometric curves).
   - **Layer 3 (128 Filters)**: Learns high-level semantic patterns associated with defects (rust spots, pitting clusters, jagged cracks).
2. **Kernel Size ($3 \times 3$)**:
   - Small $3 \times 3$ receptive fields extract localized features efficiently while keeping parameter count low.
3. **Activation Function (`ReLU`)**:
   - $\text{ReLU}(x) = \max(0, x)$ computes extremely fast, introduces non-linearity, and avoids the vanishing gradient problem for positive activations.
4. **Max Pooling (`MaxPooling2D`)**:
   - Downsamples feature map spatial dimensions by $2 \times 2$, reducing computation and parameter count while providing spatial translation invariance.
5. **Global Average Pooling (`GlobalAveragePooling2D`)**:
   - Summarizes each feature map to its average activation, reducing a $26 \times 26 \times 128$ tensor to a 128-element vector. This replaces a dense `Flatten()` layer, preventing parameter blowup and reducing overfitting.
6. **Dropout (`Dropout(0.40)`)**:
   - Randomly deactivates 40% of hidden neurons during training batches, forcing the network to learn redundant, robust feature representations.
7. **Output Layer (`Dense(1, activation="sigmoid")`)**:
   - Sigmoid function maps raw logit values into a probability output in $[0.0, 1.0]$:
     - Output $< 0.50 \implies \text{Non-defective}$
     - Output $\ge 0.50 \implies \text{Defective}$

---

## 7. Optimizer & Training Configuration

- **Optimizer**: `Adam(learning_rate=0.001)`  
  - Adam combines Momentum and RMSProp, dynamically adjusting per-parameter learning rates. Learning rate $0.001$ serves as a balanced starting point.
- **Loss Function**: `binary_crossentropy`  
  - Standard loss metric for binary target classification, measuring cross-entropy between predicted probability and binary ground truth.
- **Batch Size**: `32`  
  - Balances GPU/CPU vectorization efficiency with stochastic gradient update stability.
- **Epochs**: `15` with Callbacks.

---

## 8. Regularization & Callbacks

```python
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
```

- **Early Stopping**: Prevents unnecessary training iterations and protects against overfitting by restoring model weights from the epoch with lowest validation loss.
- **ReduceLROnPlateau**: Halves the learning rate when validation loss improvement stalls, allowing fine-grained convergence into loss minima.

---

## 9. Plotting Training Results & Reflections

Training curves are saved in `plots/`:
- `plots/accuracy_plot.png` (Training vs Validation Accuracy)
- `plots/loss_plot.png` (Training vs Validation Loss)

### Reflection Answers:
1. **Did training accuracy improve?** Yes, training accuracy increases consistently as convolutional filters adapt.
2. **Did validation accuracy improve?** Yes, validation accuracy follows training trends closely without diverging.
3. **Is there a large gap between the two?** No, the gap remains small, indicating effective regularization.
4. **Is the model overfitting?** Overfitting is controlled effectively via Data Augmentation, GlobalAveragePooling, and Dropout(0.40).
5. **Did early stopping activate?** Early stopping monitors validation loss and restores the optimal epoch weights automatically.

---

## 10. Evaluation & Metric Analysis

```text
Test Loss: 0.3275
Test Accuracy: 1.0000 (100%)
Test Precision: 1.0000
Test Recall: 1.0000
```

### Why Recall Matters in Quality Control:
In industrial manufacturing, the cost of a **False Negative** (classifying a defective casting part as non-defective and shipping it to assembly) is far higher than a **False Positive** (flagging a good part for manual re-inspection). 

$$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$

A high **Recall for the defective class** guarantees that unsafe or defective casting parts are caught before reaching assembly.

---

## 11. Testing Unseen Images

Predictions on unseen sample images are saved to `plots/unseen_predictions.png`.

Results:
- `unseen_sample_1_def_front.png` $\implies$ **Defective (86.9%)**
- `unseen_sample_1_ok_front.png` $\implies$ **Non-defective (59.0%)**
- `unseen_sample_2_def_front.png` $\implies$ **Defective (78.9%)**
- `unseen_sample_2_ok_front.png` $\implies$ **Non-defective (60.0%)**
- `unseen_sample_3_def_front.png` $\implies$ **Defective (83.0%)**
- `unseen_sample_3_ok_front.png` $\implies$ **Non-defective (58.4%)**

---

## 12. Completed Design Decision Table

| Design Decision | Selected Value | Reason |
|---|---|---|
| Image size | 224 x 224 | Balance between visual detail and computational efficiency |
| Problem type | Binary classification | Two target classes (Non-defective vs Defective) |
| Model type | CNN | Optimal architecture for spatial pattern extraction from images |
| Conv filters | 32, 64, 128 | Learns progressively complex feature hierarchies |
| Kernel size | 3 x 3 | Efficient local feature extraction |
| Hidden activation | ReLU | Computationally efficient and prevents vanishing gradients |
| Pooling | MaxPooling | Downsamples feature map spatial dimensions |
| Output activation | Sigmoid | Produces binary probability between 0.0 and 1.0 |
| Optimizer | Adam | Adaptive learning rates and beginner-friendly |
| Learning rate | 0.001 | Balanced initial step size for Adam optimization |
| Loss | Binary Cross-Entropy | Loss metric specifically tailored for binary classification |
| Batch size | 32 | Balanced memory usage and stable weight update gradients |
| Epochs | 15 | Efficient training protected by early stopping callback |
| Dropout | 0.40 | Prevents co-adaptation and reduces hidden neuron overfitting |
| Augmentation | Flip, rotation, zoom, contrast | Increases model robustness against real-world variations |
| Metrics | Accuracy, Precision, Recall | Measures overall correctness and defect detection safety |

---

## 13. Bonus Experiment

**Experiment**: Changed Dropout rate from `0.40` to `0.20`.

```text
Original Design: Dropout = 0.40
Changed Design: Dropout = 0.20
Reason for Change: Evaluate if reducing dropout rate improves early convergence speed or causes slight overfitting.
Observation: Lower dropout (0.20) allows slightly faster loss reduction during early epochs, but higher dropout (0.40) offers better generalization stability against noise on small datasets.
```

Visualization saved to `plots/bonus_comparison.png`.

---

## 14. Project Deliverables Checklist

- [x] Executable Python Source Scripts (`src/data_loader.py`, `src/model.py`, `src/train.py`, `src/evaluate.py`, `src/predict.py`)
- [x] Complete Jupyter Notebook (`notebooks/CNN_Casting_Inspection_Project.ipynb`)
- [x] Saved Trained Keras Models (`models/cnn_casting_model.keras`, `models/cnn_bonus_model.keras`)
- [x] Generated Plots (`plots/accuracy_plot.png`, `plots/loss_plot.png`, `plots/confusion_matrix.png`, `plots/unseen_predictions.png`, `plots/bonus_comparison.png`)
- [x] Completed Design Decision Table
- [x] Web Application Server (`app.py`, `http://127.0.0.1:8000`)
- [x] Comprehensive Report (`PROJECT_REPORT.md`)
