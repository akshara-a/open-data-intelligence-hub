# Mini Project: Neural Network Implementation with Documented Design Choices

## 1. Project Title

**Binary Image Classification Using a Convolutional Neural Network**

---

## 2. Objective

Build a simple neural network that classifies images into two categories:

- **Class 0: Non-defective**
- **Class 1: Defective**

The goal is to implement a working CNN and clearly document the reason behind each important design choice.

Students should explain why they selected:

- Input image size
- CNN layers
- Number of filters
- Activation functions
- Pooling
- Dropout
- Optimizer
- Learning rate
- Loss function
- Batch size
- Epoch count
- Data augmentation
- Evaluation metrics

---

## 3. Recommended Dataset

Use the Kaggle dataset:

**Casting Product Image Data for Quality Inspection**

Binary classes:

```text
ok_front  -> Non-defective
def_front -> Defective
```

This keeps the task beginner-friendly and focused on binary classification.

---

## 4. Technology Stack

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook or Google Colab

Install packages:

```bash
pip install tensorflow numpy matplotlib scikit-learn
```

---

## 5. Task 1: Load the Dataset

Resize all images to:

```python
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
```

Example:

```python
import tensorflow as tf

train_dataset = tf.keras.utils.image_dataset_from_directory(
    "data/train",
    image_size=(224, 224),
    batch_size=32,
    label_mode="binary"
)
```

---

## 6. Design Choice: Image Size

Use:

```text
224 x 224 x 3
```

### Why?

- Neural networks need a consistent input size.
- 224 x 224 keeps enough visual detail for this project.
- It is computationally manageable for beginners.

### Example Documentation

> I selected 224 x 224 because it provides sufficient image detail while keeping training time and memory usage manageable.

---

## 7. Normalize the Images

```python
normalization_layer = tf.keras.layers.Rescaling(1.0 / 255)
```

### Why?

Image pixels usually range from `0` to `255`.

Normalization converts them to approximately:

```text
0 to 1
```

This generally makes neural-network training more stable.

---

## 8. Data Augmentation

Use mild augmentation:

```python
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomContrast(0.10)
])
```

### Why?

Augmentation helps the model handle small real-world variations such as:

- Product orientation
- Slight camera movement
- Zoom differences
- Lighting differences

Apply augmentation only to the **training data**.

---

## 9. Build the CNN

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

---

## 10. Architecture Design Choices

### Conv2D: 32 Filters

```python
layers.Conv2D(32, 3, activation="relu")
```

The first convolution layer learns simple visual features such as edges, lines, and surface patterns.

### Conv2D: 64 Filters

```python
layers.Conv2D(64, 3, activation="relu")
```

The second layer learns more detailed shapes and visual patterns.

### Conv2D: 128 Filters

```python
layers.Conv2D(128, 3, activation="relu")
```

Deeper layers can learn more complex patterns that may represent defects.

The architecture increases filters as:

```text
32 -> 64 -> 128
```

---

## 11. Design Choice: ReLU

Use:

```python
activation="relu"
```

ReLU is commonly used in CNN hidden layers because it is simple, efficient, and allows the model to learn non-linear patterns.

---

## 12. Design Choice: Max Pooling

Use:

```python
layers.MaxPooling2D()
```

Pooling:

- Reduces feature-map dimensions
- Reduces computation
- Keeps important visual information
- Helps reduce overfitting

---

## 13. Design Choice: Global Average Pooling

Use:

```python
layers.GlobalAveragePooling2D()
```

It summarizes each feature map and reduces the number of trainable parameters compared with a large `Flatten()` layer.

---

## 14. Design Choice: Dropout

Use:

```python
layers.Dropout(0.40)
```

Dropout randomly disables some neurons during training and helps reduce overfitting.

---

## 15. Design Choice: Output Layer

Use:

```python
layers.Dense(1, activation="sigmoid")
```

This is a binary classification problem. Sigmoid produces a probability between `0` and `1`.

Example:

```text
0.08 -> likely non-defective
0.91 -> likely defective
```

Initial classification threshold:

```text
0.50
```

---

## 16. Compile the Model

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]
)
```

---

## 17. Training Design Choices

### Adam Optimizer

Adam is beginner-friendly, adapts learning rates during optimization, and generally works well with limited tuning.

### Learning Rate: 0.001

A learning rate controls how much model weights change during training.

- Too high -> training may become unstable
- Too low -> training may become very slow

### Binary Cross-Entropy

Use:

```python
loss="binary_crossentropy"
```

This loss function is appropriate because there are only two classes.

### Batch Size: 32

Batch size 32 provides a reasonable balance between memory usage, training speed, and stable weight updates.

---

## 18. Regularization and Callbacks

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

### Why Early Stopping?

- Stops training when validation performance stops improving
- Reduces unnecessary training
- Helps prevent overfitting

### Why ReduceLROnPlateau?

It lowers the learning rate when validation improvement slows down.

---

## 19. Train the Model

```python
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25,
    callbacks=callbacks
)
```

Use a maximum of **25 epochs**. Early stopping may stop training before that point.

---

## 20. Plot Training Results

Students must plot:

- Training accuracy
- Validation accuracy
- Training loss
- Validation loss

Example:

```python
import matplotlib.pyplot as plt

plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend([
    "Training Accuracy",
    "Validation Accuracy"
])

plt.show()
```

Students should answer:

1. Did training accuracy improve?
2. Did validation accuracy improve?
3. Is there a large gap between the two?
4. Is the model overfitting?
5. Did early stopping activate?

---

## 21. Evaluate the Model

```python
test_results = model.evaluate(test_dataset)
print(test_results)
```

Report:

- Accuracy
- Precision
- Recall

---

## 22. Confusion Matrix

Generate predictions:

```python
import numpy as np

probabilities = model.predict(test_dataset)

predictions = (
    probabilities.flatten() >= 0.5
).astype(int)
```

Create a confusion matrix:

```python
from sklearn.metrics import confusion_matrix

matrix = confusion_matrix(
    actual_labels,
    predictions
)

print(matrix)
```

---

## 23. Why Recall Matters

A dangerous quality-control mistake is:

```text
Actual defective product
        +
Predicted non-defective
        =
False Negative
```

This means a defective item may pass inspection.

Students should explain why **recall for the defective class** is an important metric.

---

## 24. Test New Images

Test at least five unseen images.

Example expected output:

```text
Prediction: Defective
Probability: 92.3%
Action: Send for manual inspection
```

---

## 25. Required Design Decision Table

Students must include and complete this table.

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

---

## 26. Mini Project Deliverables

Students should submit:

- [ ] Jupyter Notebook or Google Colab notebook
- [ ] Dataset description
- [ ] Data-loading implementation
- [ ] Data augmentation
- [ ] CNN implementation
- [ ] `model.summary()` output
- [ ] Documented architecture choices
- [ ] Documented optimizer and training choices
- [ ] Accuracy graph
- [ ] Loss graph
- [ ] Test accuracy
- [ ] Precision
- [ ] Recall
- [ ] Confusion matrix
- [ ] Five unseen-image predictions
- [ ] Completed Design Decision Table
- [ ] Short conclusion

---

## 27. Bonus Experiment

Change **one** design choice and compare the results.

Choose one:

- Change dropout from `0.40` to `0.20`
- Change batch size from `32` to `64`
- Remove data augmentation
- Add another convolution layer
- Change the learning rate
- Replace `GlobalAveragePooling2D()` with `Flatten()`

Document:

```text
Original Design:
Changed Design:
Reason for Change:
Original Accuracy:
New Accuracy:
Observation:
```

---

## 28. Expected Learning Outcome

After completing this mini project, students should be able to:

- Build a basic CNN
- Understand convolution and pooling
- Explain architecture decisions
- Select a suitable optimizer and loss function
- Apply data augmentation
- Apply regularization
- Read training and validation curves
- Identify overfitting
- Evaluate a binary classifier
- Explain technical decisions instead of only writing code
