# Building an Image Recognition System for Quality Control

## 1. Case Overview

Manufacturing companies inspect products before sending them to customers. Traditionally, workers visually examine each product and decide whether it is acceptable or defective.

Manual inspection can become difficult when:

* Thousands of products are manufactured every day.
* Defects are small or difficult to notice.
* Inspectors become tired after reviewing many products.
* Different inspectors make different decisions.
* Products move quickly through the production line.

In this task, students will build a **binary image classification system** that automatically examines an image of a manufactured product and predicts whether it is:

* **Non-defective — 0**
* **Defective — 1**

The system will use a **Convolutional Neural Network**, commonly called a CNN.

---

## 2. Task Title

**Automated Casting Defect Detection Using a Convolutional Neural Network**

---

## 3. Recommended Kaggle Dataset

### Dataset Name

**Casting Product Image Data for Quality Inspection**

This dataset contains images of manufactured casting products. The images represent products that passed inspection and products containing casting defects. It was created for industrial quality-inspection and automation use cases.

### Dataset Classes

The dataset normally uses the following folder names:

| Original folder | Meaning                          | Binary label |
| --------------- | -------------------------------- | -----------: |
| `ok_front`      | Product without a visible defect |          `0` |
| `def_front`     | Product with a visible defect    |          `1` |

### Problem Type

This is a **binary classification problem** because the model has only two possible outputs:

```text
0 = Non-defective
1 = Defective
```

The task does not require students to identify the exact defect type or draw a box around the defect. The model only determines whether a defect is present.

---

## 4. Business Scenario

A casting manufacturer produces metal components such as pump impellers.

A camera is installed above the inspection area. When a product reaches the inspection point:

1. The camera captures an image.
2. The image is resized and prepared for the model.
3. The CNN analyses the image.
4. The model returns a defect probability.
5. The product is classified as defective or non-defective.
6. Defective products are sent for manual review or removed from the production line.

### Example Output

```text
Prediction: Defective
Defect probability: 94.7%
Action: Send product for manual inspection
```

---

## 5. Learning Objectives

After completing this case, students should be able to:

* Understand binary image classification.
* Load images from folders.
* Resize and normalize images.
* apply data augmentation.
* Design a basic CNN architecture.
* Train a neural network using image data.
* Understand loss, accuracy, epochs and batch size.
* Identify overfitting and underfitting.
* Apply regularization techniques.
* Evaluate a model using precision, recall and a confusion matrix.
* Use the trained model to predict a new product image.

---

## 6. Concepts Mapped to the Case

### 6.1 Neural Network Architecture Design

Architecture design means deciding:

* How many layers the model should contain.
* How many filters should be used.
* Which activation functions should be used.
* How image features should be reduced.
* How the final binary prediction should be produced.

A beginner-friendly CNN can use:

```text
Input image
    ↓
Data augmentation
    ↓
Image normalization
    ↓
Convolution layer
    ↓
Max-pooling layer
    ↓
Convolution layer
    ↓
Max-pooling layer
    ↓
Convolution layer
    ↓
Global average pooling
    ↓
Dropout
    ↓
Sigmoid output
```

---

### 6.2 CNN Architecture for Visual Tasks

A CNN learns visual patterns directly from images.

The initial layers may learn simple features such as:

* Edges
* Lines
* Curves
* Light and dark regions

Deeper layers may learn more complex features such as:

* Cracks
* Holes
* Rough surfaces
* Irregular boundaries
* Damaged casting regions

#### Important CNN Components

| Component                | Purpose                                               |
| ------------------------ | ----------------------------------------------------- |
| `Conv2D`                 | Detects visual features such as edges and defects     |
| `ReLU`                   | Helps the network learn non-linear patterns           |
| `MaxPooling2D`           | Reduces image size while retaining important features |
| `GlobalAveragePooling2D` | Converts feature maps into a smaller feature vector   |
| `Dropout`                | Reduces overfitting                                   |
| `Dense`                  | Produces the final prediction                         |
| `Sigmoid`                | Produces a value between 0 and 1                      |

---

### 6.3 Training Dynamics and Optimization

Training dynamics describe how the model learns over multiple epochs.

#### Epoch

One epoch means the model has processed the complete training dataset once.

For example:

```text
Epoch 1  → Model sees all training images once
Epoch 2  → Model sees all training images again
Epoch 20 → Model has seen the dataset twenty times
```

#### Batch Size

Batch size is the number of images processed before the model updates its internal weights.

A suitable beginner value is:

```python
batch_size = 32
```

#### Loss Function

Use binary cross-entropy because there are only two classes.

```python
loss="binary_crossentropy"
```

A lower loss generally indicates that the model's predictions are getting closer to the correct answers.

#### Optimizer

Use the Adam optimizer.

```python
optimizer="adam"
```

The optimizer changes the neural-network weights so that prediction errors gradually decrease.

#### Learning Rate

The learning rate controls how large each weight update should be.

A suitable starting value is:

```python
learning_rate = 0.001
```

A learning rate that is too high may cause unstable learning. A learning rate that is too low may cause very slow learning.

---

### 6.4 Regularization for Production Robustness

A model should work not only on its training images but also on new images captured in the factory.

A model that performs well on training data but poorly on new data is experiencing **overfitting**.

The following regularization methods should be used:

* Data augmentation
* Dropout
* Early stopping
* Learning-rate reduction
* A separate validation dataset
* A separate test dataset

---

## 7. Data Preparation

### 7.1 Recommended Dataset Split

Use the following approximate split:

| Dataset section | Percentage | Purpose                                   |
| --------------- | ---------: | ----------------------------------------- |
| Training        |    70%–80% | Used to teach the model                   |
| Validation      |    10%–20% | Used to monitor the model during training |
| Testing         |    10%–20% | Used for final evaluation                 |

The test dataset must not be used for training.

### 7.2 Image Size

Resize all images to the same size:

```python
image_size = (224, 224)
```

Neural networks require images in a consistent shape.

### 7.3 Normalization

Image pixels usually contain values between `0` and `255`.

Normalize them to values between `0` and `1`:

```python
pixel_value = pixel_value / 255.0
```

Normalization helps the model train more consistently.

---

## 8. Data Augmentation

### 8.1 What Is Data Augmentation?

Data augmentation creates slightly modified versions of training images.

For example, one original image can be randomly:

* Rotated
* Zoomed
* Shifted
* Flipped
* Adjusted for contrast

This allows the model to learn that a defect remains a defect even when the camera angle, position or lighting changes slightly.

### 8.2 Required Augmentation

Use mild augmentation because unrealistic transformations could change the appearance of an industrial product.

```python
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomTranslation(
        height_factor=0.05,
        width_factor=0.05
    ),
    tf.keras.layers.RandomContrast(0.10)
])
```

### 8.3 Augmentation Explanation

| Augmentation        | Purpose                                                             |
| ------------------- | ------------------------------------------------------------------- |
| Horizontal flip     | Simulates a product viewed from the opposite horizontal orientation |
| Rotation            | Simulates a slightly rotated camera or product                      |
| Zoom                | Simulates the camera being closer or farther away                   |
| Translation         | Simulates the product being slightly off-centre                     |
| Contrast adjustment | Simulates small lighting differences                                |

### 8.4 Important Rule

Apply augmentation only to the **training images**.

Do not augment:

* Validation images
* Test images
* Images used for the final demonstration

Validation and test images should represent real unseen data.

Avoid extreme transformations such as:

* Large rotations
* Heavy cropping
* Strong blurring
* Extreme colour changes
* Transformations that remove the defect

---

## 9. Beginner-Friendly Implementation

### 9.1 Required Libraries

```bash
pip install tensorflow matplotlib scikit-learn seaborn
```

Main libraries:

| Library          | Use                                         |
| ---------------- | ------------------------------------------- |
| TensorFlow/Keras | Creating and training the CNN               |
| Matplotlib       | Displaying images and training graphs       |
| Scikit-learn     | Confusion matrix and classification metrics |
| NumPy            | Numerical operations                        |

---

### 9.2 Import Libraries

```python
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras import layers, models
from sklearn.metrics import classification_report, confusion_matrix
```

---

### 9.3 Load the Images

Update the paths based on the downloaded Kaggle dataset.

```python
train_directory = "casting_data/train"
test_directory = "casting_data/test"

image_size = (224, 224)
batch_size = 32

# The order is specified so:
# ok_front  = 0
# def_front = 1
class_names = ["ok_front", "def_front"]

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_directory,
    class_names=class_names,
    validation_split=0.20,
    subset="training",
    seed=42,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    train_directory,
    class_names=class_names,
    validation_split=0.20,
    subset="validation",
    seed=42,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary"
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_directory,
    class_names=class_names,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary",
    shuffle=False
)
```

---

### 9.4 Improve Dataset Performance

```python
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)
test_dataset = test_dataset.prefetch(AUTOTUNE)
```

Prefetching prepares the next batch of images while the current batch is being processed.

---

### 9.5 Create the Data-Augmentation Pipeline

```python
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomTranslation(0.05, 0.05),
    layers.RandomContrast(0.10)
], name="data_augmentation")
```

---

### 9.6 Build the CNN

```python
model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    data_augmentation,
    layers.Rescaling(1.0 / 255),

    layers.Conv2D(32, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.40),

    layers.Dense(64, activation="relu"),
    layers.Dropout(0.30),

    layers.Dense(1, activation="sigmoid")
])

model.summary()
```

The final layer contains one neuron because this is a binary-classification problem.

The sigmoid function produces a value between `0` and `1`.

Example:

```text
0.08 → Probably non-defective
0.94 → Probably defective
```

---

### 9.7 Compile the Model

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]
)
```

---

### 9.8 Configure Regularization Callbacks

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
        patience=2,
        min_lr=0.000001
    ),

    tf.keras.callbacks.ModelCheckpoint(
        filepath="best_casting_defect_model.keras",
        monitor="val_loss",
        save_best_only=True
    )
]
```

#### Callback Purposes

| Callback             | Purpose                                                    |
| -------------------- | ---------------------------------------------------------- |
| Early stopping       | Stops training when validation performance stops improving |
| Reduce learning rate | Slows down weight updates when learning becomes stuck      |
| Model checkpoint     | Saves the best version of the model                        |

---

### 9.9 Train the Model

```python
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25,
    callbacks=callbacks
)
```

Start with approximately `20–25` epochs. Early stopping may finish training before all epochs are completed.

---

## 10. Visualize Training Performance

```python
training_accuracy = history.history["accuracy"]
validation_accuracy = history.history["val_accuracy"]

training_loss = history.history["loss"]
validation_loss = history.history["val_loss"]

epochs = range(1, len(training_accuracy) + 1)

plt.figure(figsize=(8, 5))
plt.plot(epochs, training_accuracy, label="Training Accuracy")
plt.plot(epochs, validation_accuracy, label="Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training and Validation Accuracy")
plt.legend()
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(epochs, training_loss, label="Training Loss")
plt.plot(epochs, validation_loss, label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.show()
```

### Interpreting the Graphs

#### Good Learning

```text
Training accuracy increases.
Validation accuracy also increases.
Training and validation results remain reasonably close.
```

#### Possible Overfitting

```text
Training accuracy continues increasing.
Validation accuracy stops increasing or begins decreasing.
Validation loss begins increasing.
```

#### Possible Underfitting

```text
Both training and validation accuracy remain low.
The model may be too simple or may require additional training.
```

---

## 11. Evaluate the Model

### 11.1 Test Dataset Evaluation

```python
test_results = model.evaluate(test_dataset)

print("Test results:", test_results)
```

### 11.2 Generate Predictions

```python
prediction_probabilities = model.predict(test_dataset)

predicted_labels = (
    prediction_probabilities.flatten() >= 0.5
).astype(int)

actual_labels = np.concatenate([
    labels.numpy().flatten()
    for images, labels in test_dataset
]).astype(int)
```

### 11.3 Classification Report

```python
print(
    classification_report(
        actual_labels,
        predicted_labels,
        target_names=["Non-defective", "Defective"]
    )
)
```

### 11.4 Confusion Matrix

```python
matrix = confusion_matrix(
    actual_labels,
    predicted_labels
)

print(matrix)
```

The confusion matrix represents:

```text
                     Predicted
                 Good       Defective

Actual Good       TN            FP
Actual Defective  FN            TP
```

---

## 12. Evaluation Metrics

### Accuracy

Accuracy represents the percentage of all images classified correctly.

```text
Accuracy = Correct predictions / Total predictions
```

### Precision

Precision answers:

> Of all products predicted as defective, how many were actually defective?

High precision means fewer acceptable products are incorrectly rejected.

### Recall

Recall answers:

> Of all genuinely defective products, how many did the system detect?

Recall is especially important in quality control because a false negative allows a defective product to pass inspection.

### False Positive

A non-defective product is incorrectly classified as defective.

Possible consequence:

* An acceptable product is unnecessarily rejected or manually inspected.

### False Negative

A defective product is incorrectly classified as non-defective.

Possible consequence:

* A defective product may be delivered to a customer.

For this case, reducing false negatives should be treated as a major objective.

---

## 13. Adjusting the Classification Threshold

The default classification threshold is `0.50`.

```python
predicted_class = 1 if defect_probability >= 0.50 else 0
```

For a strict quality-control process, the threshold may be reduced:

```python
threshold = 0.40
predicted_class = 1 if defect_probability >= threshold else 0
```

A lower threshold may detect more defects, but it may also incorrectly reject more non-defective products.

Students should compare thresholds such as:

```text
0.30
0.40
0.50
0.60
```

The final threshold should be selected based on the balance between:

* Detecting defective products
* Avoiding unnecessary rejection of good products

---

## 14. Predict a Single Image

```python
def predict_product(image_path, model, threshold=0.50):
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    image_array = tf.keras.utils.img_to_array(image)
    image_array = tf.expand_dims(image_array, axis=0)

    defect_probability = float(
        model.predict(image_array, verbose=0)[0][0]
    )

    if defect_probability >= threshold:
        predicted_class = "Defective"
        recommended_action = "Send for manual inspection"
    else:
        predicted_class = "Non-defective"
        recommended_action = "Product may proceed"

    print(f"Prediction: {predicted_class}")
    print(f"Defect probability: {defect_probability:.2%}")
    print(f"Recommended action: {recommended_action}")
```

Example:

```python
predict_product(
    "sample_images/product_01.jpeg",
    model,
    threshold=0.50
)
```

---

## 15. Student Tasks

### Task 1: Understand the Dataset

Students must:

* Download the Kaggle dataset.
* Identify the two classes.
* Count the images in each class.
* Display sample defective and non-defective images.
* Check whether the dataset is balanced.

### Task 2: Prepare the Data

Students must:

* Resize images to `224 × 224`.
* Create training, validation and testing datasets.
* Normalize pixel values.
* Verify binary labels.
* Prevent overlap between training and test images.

### Task 3: Apply Data Augmentation

Students must use at least four augmentation operations:

* Horizontal flip
* Small rotation
* Small zoom
* Small translation
* Contrast adjustment

Students must explain why augmentation is applied only to training data.

### Task 4: Build the CNN

Students must create a CNN containing:

* At least three convolution layers
* Max-pooling layers
* ReLU activation
* Global average pooling or flattening
* Dropout
* A single sigmoid output neuron

### Task 5: Train the Model

Students must configure:

* Adam optimizer
* Binary cross-entropy loss
* Batch size
* Epoch count
* Early stopping
* Model checkpointing

### Task 6: Monitor Training

Students must generate:

* Training accuracy graph
* Validation accuracy graph
* Training loss graph
* Validation loss graph

Students must identify whether the model is:

* Learning correctly
* Overfitting
* Underfitting

### Task 7: Evaluate the Model

Students must report:

* Test accuracy
* Precision
* Recall
* Confusion matrix
* False-positive count
* False-negative count

### Task 8: Test New Images

Students must:

* Select at least five unseen images.
* Generate a prediction for each image.
* Display the defect probability.
* Record whether each prediction was correct.
* Explain incorrect predictions.

---

## 16. Expected Deliverables

Students should submit:

1. A Jupyter Notebook or Google Colab notebook.
2. Dataset description.
3. Sample image visualization.
4. Data-preparation code.
5. Data-augmentation code.
6. CNN architecture.
7. Model summary.
8. Training configuration.
9. Accuracy and loss graphs.
10. Confusion matrix.
11. Classification report.
12. Predictions for unseen images.
13. Saved model file.
14. A short findings report.
15. A README containing execution instructions.

---

## 17. Suggested Project Folder Structure

```text
casting-quality-inspection/
│
├── data/
│   ├── train/
│   │   ├── ok_front/
│   │   └── def_front/
│   │
│   └── test/
│       ├── ok_front/
│       └── def_front/
│
├── notebooks/
│   └── casting_defect_detection.ipynb
│
├── models/
│   └── best_casting_defect_model.keras
│
├── sample_images/
│
├── reports/
│   ├── confusion_matrix.png
│   ├── accuracy_graph.png
│   └── loss_graph.png
│
├── requirements.txt
└── README.md
```

---

## 18. Minimum Acceptance Criteria

The solution is complete when:

* [ ] The task is implemented as binary classification.
* [ ] Label `0` represents non-defective products.
* [ ] Label `1` represents defective products.
* [ ] Training, validation and test data are separated.
* [ ] Image normalization is applied.
* [ ] Data augmentation is applied only during training.
* [ ] The model contains convolution and pooling layers.
* [ ] The final layer uses sigmoid activation.
* [ ] Binary cross-entropy is used.
* [ ] Early stopping is configured.
* [ ] Dropout is included.
* [ ] Accuracy and loss graphs are generated.
* [ ] Precision and recall are reported.
* [ ] A confusion matrix is generated.
* [ ] False negatives are specifically analysed.
* [ ] The model can predict a new image.
* [ ] The best trained model is saved.

---

## 19. Optional Advanced Improvements

After completing the basic CNN, students may experiment with:

* Transfer learning using MobileNetV2
* Transfer learning using EfficientNet
* Batch normalization
* Class weights for imbalanced data
* Threshold tuning
* Grad-CAM visualization
* A Streamlit demonstration application
* Webcam-based inspection
* Model conversion to TensorFlow Lite
* Comparing the custom CNN with a pretrained model

These improvements are optional. The primary task should remain a beginner-friendly binary classification problem.

---

## 20. Final Expected Outcome

The completed system should accept an image of a casting product and produce an output similar to:

```text
Product classification: Defective
Defect probability: 91.4%
Decision threshold: 50%
Recommended action: Reject or send for manual inspection
```

The project demonstrates how CNNs can support industrial quality-control teams by providing faster and more consistent initial product inspection.
