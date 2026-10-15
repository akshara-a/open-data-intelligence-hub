# Binary Image Classification Using a Convolutional Neural Network

## 📌 Project Overview

This mini project implements a **Convolutional Neural Network (CNN)** for binary image classification.

The model classifies casting product images into two categories:

* **Class 0 – Non-defective (`ok_front`)**
* **Class 1 – Defective (`def_front`)**

The main objective is not only to build a working CNN, but also to **document and justify the important design choices** used during model development.

---

## 🎯 Objectives

The project aims to:

* Build a CNN for binary image classification.
* Preprocess and normalize image data.
* Apply data augmentation to improve model robustness.
* Understand the role of convolution and pooling layers.
* Document CNN architecture decisions.
* Select suitable activation functions, optimizer, loss function, and learning rate.
* Apply dropout and callbacks to reduce overfitting.
* Evaluate the model using accuracy, precision, recall, and a confusion matrix.
* Test the model on unseen images.
* Perform a **bonus experiment** by changing one design choice and comparing the results.

---

## 📂 Dataset

### Dataset Name

**Casting Product Image Data for Quality Inspection**

The dataset contains two classes:

```text
ok_front  → Non-defective
def_front → Defective
```

This makes the dataset suitable for a beginner-friendly binary image classification problem.

---

## 🛠️ Technologies Used

* Python
* TensorFlow / Keras
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook / Google Colab

### Installation

```bash
pip install tensorflow numpy matplotlib scikit-learn
```

The technology stack and required packages are specified in the project instructions.

---

## 🧠 CNN Architecture

The implemented CNN follows this architecture:

```text
Input Image
224 × 224 × 3
       ↓
Data Augmentation
       ↓
Rescaling / Normalization
       ↓
Conv2D – 32 Filters
       ↓
MaxPooling
       ↓
Conv2D – 64 Filters
       ↓
MaxPooling
       ↓
Conv2D – 128 Filters
       ↓
MaxPooling
       ↓
Global Average Pooling
       ↓
Dropout – 0.40
       ↓
Dense – 64 Neurons
       ↓
Dense – 1 Neuron
Sigmoid Activation
       ↓
Binary Prediction
```

The CNN uses progressively increasing filters:

```text
32 → 64 → 128
```

This allows earlier layers to learn simpler visual features while deeper layers learn more complex patterns.

---

## ⚙️ Model Design Choices

| Design Decision   | Selected Value                 | Reason                                           |
| ----------------- | ------------------------------ | ------------------------------------------------ |
| Image Size        | 224 × 224                      | Balance between image detail and computation     |
| Problem Type      | Binary Classification          | Two output classes                               |
| Model             | CNN                            | Suitable for image data                          |
| Conv Filters      | 32, 64, 128                    | Learn increasingly complex features              |
| Kernel Size       | 3 × 3                          | Efficient local feature extraction               |
| Hidden Activation | ReLU                           | Efficient non-linear activation                  |
| Pooling           | MaxPooling2D                   | Reduces feature-map dimensions                   |
| Global Pooling    | GlobalAveragePooling2D         | Reduces trainable parameters                     |
| Dropout           | 0.40                           | Helps reduce overfitting                         |
| Output Activation | Sigmoid                        | Produces binary probability                      |
| Optimizer         | Adam                           | Adaptive and beginner-friendly                   |
| Learning Rate     | 0.001                          | Suitable starting value                          |
| Loss Function     | Binary Cross-Entropy           | Suitable for binary classification               |
| Batch Size        | 32                             | Balance between memory and training speed        |
| Maximum Epochs    | 25                             | Provides sufficient training with early stopping |
| Augmentation      | Flip, Rotation, Zoom, Contrast | Improves robustness                              |
| Metrics           | Accuracy, Precision, Recall    | Measures classification performance              |

These values follow the documented design decision requirements for the mini project.

---

## 🖼️ Image Preprocessing

All images are resized to:

```text
224 × 224 × 3
```

Pixel values are normalized from approximately:

```text
0 – 255
```

to:

```text
0 – 1
```

Normalization helps make neural-network training more stable.

---

## 🔄 Data Augmentation

The training dataset uses mild augmentation:

* Random horizontal flip
* Random rotation
* Random zoom
* Random contrast

Example:

```python
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomContrast(0.10)
])
```

Augmentation helps the model handle variations such as product orientation, camera movement, zoom, and lighting differences.

**Important:** Augmentation is applied only to the training data.

---

## 🏋️ Model Training

The model uses:

### Optimizer

```text
Adam
```

### Learning Rate

```text
0.001
```

### Loss Function

```text
Binary Cross-Entropy
```

### Batch Size

```text
32
```

### Maximum Epochs

```text
25
```

The training process uses validation data to monitor model performance.

---

## 🛑 Callbacks and Regularization

Two callbacks are used:

### Early Stopping

Early stopping monitors validation loss and stops training when the model stops improving.

```text
patience = 5
restore_best_weights = True
```

### ReduceLROnPlateau

This callback reduces the learning rate when validation improvement slows down.

```text
factor = 0.5
patience = 2
```

These techniques help reduce unnecessary training and overfitting.

---

## 📊 Evaluation Metrics

The model is evaluated using:

### 1. Accuracy

Measures the overall percentage of correctly classified images.

### 2. Precision

Measures how many images predicted as defective are actually defective.

### 3. Recall

Measures how many actual defective images are correctly detected.

### 4. Confusion Matrix

The confusion matrix shows:

```text
                 Predicted
              Non-Defective  Defective
Actual
Non-Defective      TN            FP

Defective          FN            TP
```

---

## 🚨 Why Recall Is Important

For quality inspection, a **false negative** is particularly important.

```text
Actual Defective
       ↓
Predicted Non-Defective
       ↓
False Negative
```

This means a defective product could pass the inspection process.

Therefore, **recall for the defective class** is an important metric for this project.

---

## 📈 Training Visualizations

The notebook generates:

* Training Accuracy
* Validation Accuracy
* Training Loss
* Validation Loss

These graphs are used to determine:

* Whether training accuracy improves.
* Whether validation accuracy improves.
* Whether there is a large training-validation gap.
* Whether the model is overfitting.
* Whether early stopping was activated.

---

## 🧪 Testing on Unseen Images

At least five unseen images are tested after training.

Example:

```text
Prediction: Defective
Probability: 92.3%
Action: Send for manual inspection
```

The model uses a classification threshold of:

```text
0.50
```

For example:

```text
0.08 → Likely Non-Defective
0.91 → Likely Defective
```

---

# ⭐ Bonus Experiment

As part of the bonus task, one design choice is changed and the results are compared with the original model.

Possible changes include:

* Dropout: `0.40 → 0.20`
* Batch size: `32 → 64`
* Remove data augmentation
* Add another convolution layer
* Change learning rate
* Replace `GlobalAveragePooling2D()` with `Flatten()`

The comparison documents:

```text
Original Design:
Changed Design:
Reason for Change:
Original Accuracy:
New Accuracy:
Observation:
```

---

## 📊 Original vs Bonus Comparison

The notebook includes a comparison between the **original CNN model** and the **modified/bonus CNN model**.

The comparison can include:

| Metric               | Original Model | Bonus Model |
| -------------------- | -------------: | ----------: |
| Accuracy             |              — |           — |
| Precision            |              — |           — |
| Recall               |              — |           — |
| Training Behaviour   |              — |           — |
| Validation Behaviour |              — |           — |

The final values should be filled with the actual results obtained after running the notebook.

### Comparison Graphs

The project also compares the original and bonus experiments using visualizations such as:

* Accuracy comparison
* Loss comparison
* Metric comparison

This makes it easier to understand how the selected design change affected model performance.

---

## 📁 Project Structure

```text
S.GayathriG40-AIML/
│
├── CNN_Implementation.ipynb
├── README.md
├── decision.long.md
├── model.comparison.md
└── requirements.txt
```

> Dataset files should be kept in the appropriate local dataset directory and should not be unnecessarily committed to the repository.

---

## 📋 Project Deliverables

The completed project includes:

* [ ] Jupyter Notebook / Google Colab Notebook
* [ ] Dataset description
* [ ] Data loading implementation
* [ ] Data augmentation
* [ ] CNN implementation
* [ ] Model summary
* [ ] Documented architecture choices
* [ ] Optimizer and training choices
* [ ] Accuracy graph
* [ ] Loss graph
* [ ] Test accuracy
* [ ] Precision
* [ ] Recall
* [ ] Confusion matrix
* [ ] Five unseen-image predictions
* [ ] Completed design decision table
* [ ] Bonus experiment
* [ ] Original vs bonus comparison
* [ ] Short conclusion

These deliverables correspond to the required mini-project submission items.

---

## ✅ Conclusion

This project demonstrates how to build and evaluate a CNN for binary image classification.

The implementation focuses not only on achieving predictions but also on understanding **why each design choice was made**, including image size, convolution filters, activation functions, pooling, dropout, optimizer, learning rate, loss function, batch size, augmentation, and evaluation metrics.

The bonus experiment further demonstrates how changing a single design choice can affect model performance and training behaviour.

Overall, the project provides practical experience in:

* CNN implementation
* Image preprocessing
* Data augmentation
* Model regularization
* Model evaluation
* Overfitting analysis
* Design decision documentation
* Experimental comparison

The expected learning outcomes include building a basic CNN, understanding convolution and pooling, selecting appropriate training components, applying regularization, interpreting training curves, identifying overfitting, and evaluating binary classifiers.

