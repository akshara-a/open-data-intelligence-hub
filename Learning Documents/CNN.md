# Convolutional Neural Networks (CNNs) — A Detailed Beginner-Friendly Guide

## 1. What Is a CNN?

A **CNN**, or **Convolutional Neural Network**, is a deep-learning model designed mainly to process images.

A CNN can learn visual patterns such as:

- Edges
- Lines
- Corners
- Curves
- Colours
- Textures
- Shapes
- Object parts
- Complete objects
- Defects such as scratches, cracks, dents, and missing components

For example, in a manufacturing quality-control system, a CNN can inspect an image and classify the product as:

- Good
- Scratched
- Cracked
- Dented
- Missing a component
- Incorrectly assembled

The CNN is not normally given manually written rules such as:

> A crack is a dark line that is 20 pixels long.

Instead, it is shown many labelled examples:

```text
product_001.jpg → Good
product_002.jpg → Crack
product_003.jpg → Scratch
```

During training, the CNN automatically learns the visual patterns associated with each label.

---

## 2. How Does a Computer See an Image?

Humans see an image as an object or scene.

A computer sees an image as a collection of numbers.

### 2.1 Grayscale image

A grayscale image has one number for each pixel.

```text
0   = black
255 = white
Values between 0 and 255 represent shades of grey
```

A small grayscale image may be represented as:

```text
0    0    0    0
0   255  255   0
0   255  255   0
0    0    0    0
```

To the computer, this image is simply a matrix.

### 2.2 Colour image

A colour image normally contains three colour channels:

```text
R = Red
G = Green
B = Blue
```

Each pixel has three values.

```text
Red pixel   = [255, 0, 0]
Green pixel = [0, 255, 0]
Blue pixel  = [0, 0, 255]
White pixel = [255, 255, 255]
Black pixel = [0, 0, 0]
```

A colour image with a height and width of 224 pixels has the shape:

```text
224 × 224 × 3
```

This means:

- 224 pixels high
- 224 pixels wide
- 3 colour channels

The total number of input values is:

```text
224 × 224 × 3 = 150,528
```

---

## 3. Why Not Use a Normal Neural Network?

Suppose all 150,528 image values are connected directly to a fully connected layer containing 1,000 neurons.

The approximate number of connections would be:

```text
150,528 × 1,000 = 150,528,000
```

That is more than 150 million weights in a single layer.

This creates several problems:

- High memory usage
- Slow training
- Large training-data requirements
- Greater risk of overfitting
- Poor use of the image's spatial structure

In an image, nearby pixels are closely related. A group of neighbouring dark pixels may form a line, edge, or crack.

A CNN takes advantage of this by examining **small local regions** instead of connecting every image pixel to every neuron.

---

## 4. Overall CNN Architecture

A simple CNN commonly follows this flow:

```text
Input Image
     ↓
Convolution Layer
     ↓
ReLU Activation
     ↓
Pooling Layer
     ↓
Convolution Layer
     ↓
ReLU Activation
     ↓
Pooling Layer
     ↓
Global Average Pooling or Flatten
     ↓
Dense Layer
     ↓
Output Prediction
```

For quality control:

```text
Product Image
     ↓
Detect edges and colour changes
     ↓
Detect textures and small shapes
     ↓
Detect crack or scratch patterns
     ↓
Predict product condition
```

---

# Part 1 — Feature Extraction

## 5. Convolution Layer

The convolution layer is the central component of a CNN.

It uses a small matrix called a:

- **Filter**
- **Kernel**

These terms are commonly used interchangeably.

A typical filter size is:

```text
3 × 3
```

Example:

```text
 1   0  -1
 1   0  -1
 1   0  -1
```

The filter moves across the image.

At every position, it:

1. Selects a small image region.
2. Multiplies image values by filter values.
3. Adds the multiplication results.
4. Produces one output value.

This process is called **convolution**.

---

## 6. Simple Convolution Example

Consider this image region:

```text
1   1   0
1   1   0
0   0   0
```

Filter:

```text
1    0   -1
1    0   -1
1    0   -1
```

Multiply the corresponding values:

```text
(1 × 1)  + (1 × 0)  + (0 × -1)
(1 × 1)  + (1 × 0)  + (0 × -1)
(0 × 1)  + (0 × 0)  + (0 × -1)
```

Add the results:

```text
1 + 0 + 0
+ 1 + 0 + 0
+ 0 + 0 + 0
= 2
```

The output value at this position is:

```text
2
```

The filter then moves to the next image position and repeats the calculation.

---

## 7. What Does a Filter Detect?

Different filters learn to respond to different visual patterns.

Examples include:

- Vertical edges
- Horizontal edges
- Diagonal edges
- Corners
- Curves
- Colour changes
- Rough textures
- Thin dark lines
- Surface irregularities

One convolution layer may learn:

```text
Filter 1 → vertical edges
Filter 2 → horizontal edges
Filter 3 → curves
Filter 4 → rough textures
Filter 5 → thin crack-like lines
```

The filters are usually **not manually created**.

At the beginning of training, their values are mostly random. Training gradually adjusts them so that they become useful for the required task.

---

## 8. Feature Maps

The output produced by one filter is called a **feature map**.

A feature map indicates where a particular pattern was detected.

```text
Original Image
      ↓
Vertical-edge filter
      ↓
Feature map highlighting vertical edges
```

If a convolution layer has 32 filters, it produces 32 feature maps.

Suppose the input shape is:

```text
224 × 224 × 3
```

After applying 32 filters with `same` padding, the output may be:

```text
224 × 224 × 32
```

The last number represents the number of feature maps.

---

## 9. Stride

**Stride** controls how many pixels the filter moves at a time.

### Stride = 1

The filter moves one pixel at a time.

```text
Position 1 → Position 2 → Position 3
```

This preserves more detail.

### Stride = 2

The filter moves two pixels at a time.

This produces a smaller feature map and reduces computation, but some detail may be lost.

```text
Stride 1 → larger output
Stride 2 → smaller output
```

---

## 10. Padding

Without padding, a convolution operation normally makes the feature map smaller.

Example:

```text
Input image: 5 × 5
Filter:      3 × 3
Stride:      1
Padding:     none
```

Output:

```text
3 × 3
```

To preserve more border information, zeros can be added around the image.

This is called **padding**.

Original image:

```text
1  2  3
4  5  6
7  8  9
```

After adding a zero border:

```text
0  0  0  0  0
0  1  2  3  0
0  4  5  6  0
0  7  8  9  0
0  0  0  0  0
```

Common padding options:

```text
valid → no padding
same  → preserve approximately the same width and height
```

TensorFlow example:

```python
layers.Conv2D(
    filters=32,
    kernel_size=(3, 3),
    padding="same"
)
```

---

## 11. ReLU Activation

After convolution, a CNN commonly applies an activation function called **ReLU**.

ReLU stands for:

```text
Rectified Linear Unit
```

Formula:

```text
ReLU(x) = max(0, x)
```

Examples:

```text
ReLU(-10) = 0
ReLU(-2)  = 0
ReLU(0)   = 0
ReLU(4)   = 4
ReLU(12)  = 12
```

In simple terms:

```text
Negative value → changed to zero
Positive value → kept unchanged
```

### Why is ReLU needed?

Without activation functions, multiple neural-network layers would behave like one simple linear calculation.

ReLU enables the CNN to learn complex relationships.

A crack may depend on several visual conditions:

- A thin line
- A particular direction
- A dark colour
- An irregular shape
- A surrounding surface texture

ReLU helps the network learn these non-linear combinations.

---

## 12. Pooling Layer

Pooling reduces the width and height of feature maps.

The most common type is **max pooling**.

A typical configuration is:

```text
2 × 2 pooling window
```

The pooling layer examines each `2 × 2` area and keeps the largest value.

Example:

```text
1   5
2   3
```

Output:

```text
5
```

### Complete max-pooling example

Input feature map:

```text
1   3   2   4
5   6   1   2
7   2   8   1
3   4   2   9
```

Maximum values from each `2 × 2` region:

```text
6   4
7   9
```

The `4 × 4` feature map becomes `2 × 2`.

### Why use pooling?

Pooling:

- Reduces computation
- Reduces memory usage
- Retains strong feature responses
- Helps control overfitting
- Gives some tolerance to small object movements

For example, a scratch may appear a few pixels to the left because of minor product-placement differences. Pooling helps the CNN still recognize it.

---

## 13. How CNN Layers Learn Progressively

CNN layers learn visual features in a hierarchy.

### Early layers

The first layers normally learn simple patterns:

- Edges
- Lines
- Colour changes
- Corners

### Middle layers

Middle layers combine those basic patterns:

- Curves
- Circles
- Surface textures
- Small shapes
- Repeated patterns

### Deeper layers

Deeper layers combine features into meaningful concepts:

- Crack
- Scratch
- Missing screw
- Product corner
- Eye
- Wheel
- Face

The hierarchy looks like:

```text
Pixels
  ↓
Edges
  ↓
Lines and curves
  ↓
Textures and shapes
  ↓
Object parts
  ↓
Complete object or defect
```

Quality-control example:

```text
Pixels
  ↓
Dark and bright edges
  ↓
Thin irregular line
  ↓
Crack-like structure
  ↓
Defective product
```

---

## 14. Increasing the Number of Filters

A CNN often increases the number of filters in deeper layers.

Example:

```text
First convolution layer  → 32 filters
Second convolution layer → 64 filters
Third convolution layer  → 128 filters
```

Earlier layers detect a small number of simple patterns. Deeper layers need more filters to represent many complex combinations.

At the same time, pooling reduces spatial size.

```text
Input:              224 × 224 × 3
After Conv 1:       224 × 224 × 32
After Pooling 1:    112 × 112 × 32
After Conv 2:       112 × 112 × 64
After Pooling 2:     56 × 56 × 64
After Conv 3:        56 × 56 × 128
After Pooling 3:     28 × 28 × 128
```

Width and height decrease, while the number of learned feature types increases.

---

# Part 2 — Classification

## 15. Flatten Layer

After the convolution and pooling layers, the output is still multidimensional.

Example:

```text
28 × 28 × 128
```

A **Flatten** layer converts this into one long list.

```text
28 × 28 × 128 = 100,352 values
```

Output:

```text
[0.2, 0.0, 1.4, 0.7, 0.1, ...]
```

This vector can be passed into a fully connected layer.

A disadvantage is that flattening can create a very large number of parameters.

---

## 16. Global Average Pooling

Modern CNNs often use **Global Average Pooling** instead of Flatten.

Suppose the final output is:

```text
7 × 7 × 128
```

There are 128 feature maps. Global average pooling calculates one average value for each map.

Result:

```text
128 values
```

Without it, flattening would create:

```text
7 × 7 × 128 = 6,272 values
```

Benefits:

- Fewer parameters
- Lower memory usage
- Faster training
- Lower risk of overfitting

TensorFlow example:

```python
layers.GlobalAveragePooling2D()
```

---

## 17. Dense Layer

A fully connected layer is also called a **Dense layer**.

It combines all the learned features to make the final decision.

Suppose the CNN has detected:

- A thin dark line
- An irregular edge
- A rough surrounding texture
- A long connected shape

The Dense layer may combine this evidence and predict:

```text
Crack
```

Example:

```python
layers.Dense(128, activation="relu")
```

This Dense layer contains 128 neurons.

---

## 18. Output Layer

The output layer depends on the task.

### 18.1 Binary classification

Binary classification has two possible classes.

Example:

```text
Good
Defective
```

The model normally uses one output neuron with a **sigmoid** activation.

```python
layers.Dense(1, activation="sigmoid")
```

Sigmoid produces a value between 0 and 1.

Example:

```text
Output = 0.92
```

This may mean:

```text
92% estimated probability of being defective
```

A simple decision rule could be:

```text
Below 0.5 → Good
0.5 or above → Defective
```

### 18.2 Multi-class classification

Multi-class classification has more than two classes.

Example:

- Good
- Crack
- Scratch
- Dent
- Missing component

The model uses one output neuron per class and a **softmax** activation.

```python
layers.Dense(5, activation="softmax")
```

Example output:

```text
Good               0.02
Crack              0.75
Scratch            0.12
Dent               0.08
Missing component  0.03
```

The class with the highest probability is selected:

```text
Prediction = Crack
```

---

# Part 3 — How a CNN Learns

## 19. Complete Training Cycle

CNN training repeatedly follows these steps:

```text
1. Give the CNN a batch of images
2. CNN makes predictions
3. Compare predictions with correct labels
4. Calculate the loss
5. Send the error backward
6. Update filters and weights
7. Repeat
```

The forward movement from image to prediction is called **forward propagation**.

The backward movement used to calculate updates is called **backpropagation**.

---

## 20. Forward Propagation

During forward propagation:

```text
Product image
     ↓
Convolution layers
     ↓
Pooling layers
     ↓
Extracted features
     ↓
Dense layer
     ↓
Prediction
```

The model uses its current filters and weights to make a prediction.

---

## 21. Loss Function

The loss function measures how wrong the prediction is.

Suppose:

```text
Correct label = Defective = 1
```

Prediction:

```text
0.20
```

The prediction is far from the correct answer, so the loss is relatively high.

A prediction of:

```text
0.95
```

is much closer to the correct answer, so the loss is lower.

The goal of training is to minimize loss.

Common loss functions:

```text
Binary classification → Binary Cross-Entropy
Multi-class classification → Categorical Cross-Entropy
```

---

## 22. Backpropagation

Backpropagation determines how much each model weight contributed to the error.

Conceptually:

```text
Prediction error
      ↓
Output layer
      ↓
Dense layers
      ↓
Convolution layers
      ↓
Calculate required weight changes
```

The optimizer then applies those changes.

Filters that were not useful are adjusted. After many training updates, they become better at detecting relevant features.

---

## 23. Optimizer

The optimizer controls how the model's weights are updated.

Common optimizers include:

- Adam
- SGD
- RMSprop

**Adam** is often a good starting point for beginners.

Example:

```python
optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)
```

---

## 24. Learning Rate

The **learning rate** determines the size of each weight update.

Example:

```text
Learning rate = 0.001
```

### Learning rate too high

- Weight updates are too large
- Loss may jump up and down
- Training may become unstable
- The model may fail to converge

### Learning rate too low

- Weight updates are extremely small
- Training becomes slow
- Many more epochs may be needed

A commonly used starting value with Adam is:

```text
0.001
```

However, the best learning rate depends on the model and dataset.

---

## 25. Epoch, Batch, and Iteration

### Epoch

One epoch means the model has processed the entire training dataset once.

```text
1 epoch = one complete pass through all training images
```

If there are 1,000 images and training runs for 20 epochs, the complete dataset is processed 20 times.

### Batch

A batch is a small group of images processed together.

```text
Dataset size = 1,000 images
Batch size   = 32 images
```

The model processes 32 images, calculates loss, and updates its weights.

### Iteration

One iteration means one batch has been processed.

```text
1,000 ÷ 32 ≈ 32 iterations per epoch
```

---

# Part 4 — Preparing the Data

## 26. Training, Validation, and Test Data

A dataset is commonly divided into three parts.

### Training set

Used to update model weights.

Example:

```text
70%
```

### Validation set

Used during development to:

- Measure generalization
- Detect overfitting
- Tune model settings
- Choose the best model checkpoint

Example:

```text
15%
```

### Test set

Used only after training to measure final performance.

Example:

```text
15%
```

A typical split:

```text
Training   = 70%
Validation = 15%
Testing    = 15%
```

The test set must contain images the model did not use for training.

---

## 27. Dataset Folder Structure

For binary classification:

```text
dataset/
│
├── train/
│   ├── good/
│   │   ├── good_001.jpg
│   │   ├── good_002.jpg
│   │   └── good_003.jpg
│   │
│   └── defective/
│       ├── defect_001.jpg
│       ├── defect_002.jpg
│       └── defect_003.jpg
│
├── validation/
│   ├── good/
│   └── defective/
│
└── test/
    ├── good/
    └── defective/
```

TensorFlow can load this structure automatically.

```python
import tensorflow as tf

train_dataset = tf.keras.utils.image_dataset_from_directory(
    "dataset/train",
    image_size=(224, 224),
    batch_size=32,
    label_mode="binary"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    "dataset/validation",
    image_size=(224, 224),
    batch_size=32,
    label_mode="binary"
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    "dataset/test",
    image_size=(224, 224),
    batch_size=32,
    label_mode="binary",
    shuffle=False
)
```

---

## 28. Image Normalization

Image pixel values normally range from 0 to 255.

They are commonly converted to values between 0 and 1.

```text
Original pixel = 128
Normalized pixel = 128 ÷ 255 = 0.502
```

TensorFlow:

```python
layers.Rescaling(1.0 / 255)
```

Normalization helps make training more stable.

---

## 29. Data Augmentation

Data augmentation creates slightly modified versions of training images.

Possible transformations include:

- Small rotation
- Horizontal flip
- Small zoom
- Brightness adjustment
- Contrast adjustment
- Small translation
- Random crop

Example:

```python
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10)
])
```

### Why augmentation helps

The model should not depend on one exact:

- Camera angle
- Product position
- Brightness level
- Background condition

Augmentation provides more realistic variety and helps reduce overfitting.

### Important caution

Augmentation must represent possible real-world conditions.

For example:

- Small rotation may be realistic.
- Slight brightness changes may be realistic.
- A vertical flip may be unrealistic.
- Excessive cropping may remove the defect.
- Horizontal flipping may be wrong when left and right are meaningful.

---

# Part 5 — Overfitting and Regularization

## 30. Overfitting

Overfitting happens when the model performs extremely well on training images but poorly on new images.

Example:

```text
Training accuracy   = 99%
Validation accuracy = 72%
```

The model may have memorized:

- Background colours
- Camera positions
- Lighting patterns
- Specific products
- Image noise

Instead of learning the true defect pattern.

---

## 31. Underfitting

Underfitting happens when the model has not learned the task well enough.

Example:

```text
Training accuracy   = 60%
Validation accuracy = 58%
```

Possible causes:

- Model is too simple
- Too few epochs
- Poor learning rate
- Incorrect labels
- Low-quality images
- Excessive regularization
- Important information is missing

---

## 32. Techniques to Reduce Overfitting

Common methods include:

- More training data
- Data augmentation
- Dropout
- Early stopping
- Weight regularization
- Batch normalization
- Smaller network
- Transfer learning

---

## 33. Dropout

Dropout temporarily disables some neurons during training.

```python
layers.Dropout(0.5)
```

A dropout rate of `0.5` means approximately half of the selected neurons are ignored during each training step.

This prevents the network from relying too heavily on a small set of neurons.

Important:

```text
Dropout is active during training.
Dropout is disabled during prediction.
```

---

## 34. Batch Normalization

Batch normalization helps keep intermediate model values in a stable range.

A common block is:

```text
Convolution
     ↓
Batch Normalization
     ↓
ReLU
     ↓
Pooling
```

TensorFlow:

```python
layers.Conv2D(32, (3, 3), padding="same"),
layers.BatchNormalization(),
layers.ReLU()
```

Possible benefits:

- More stable training
- Faster convergence
- Easier optimization
- Some regularization effect

---

## 35. Early Stopping

Early stopping stops training when validation performance has stopped improving.

```python
tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)
```

Meaning:

- Monitor validation loss.
- Wait for five non-improving epochs.
- Stop training.
- Restore the weights from the best epoch.

This helps prevent the model from continuing to memorize training data.

---

# Part 6 — Complete CNN Implementation

## 36. Install the Required Library

```bash
pip install tensorflow
```

Optional libraries:

```bash
pip install numpy matplotlib scikit-learn
```

---

## 37. Beginner-Friendly CNN Model

```python
import tensorflow as tf
from tensorflow.keras import layers, models

data_augmentation = tf.keras.Sequential([
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10)
])

model = models.Sequential([
    # Input image: 224 × 224 RGB
    layers.Input(shape=(224, 224, 3)),

    # Create realistic image variations during training
    data_augmentation,

    # Convert pixels from 0–255 to 0–1
    layers.Rescaling(1.0 / 255),

    # Block 1: basic edges and colour changes
    layers.Conv2D(32, (3, 3), padding="same"),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling2D((2, 2)),

    # Block 2: textures and simple shapes
    layers.Conv2D(64, (3, 3), padding="same"),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling2D((2, 2)),

    # Block 3: complex defect patterns
    layers.Conv2D(128, (3, 3), padding="same"),
    layers.BatchNormalization(),
    layers.ReLU(),
    layers.MaxPooling2D((2, 2)),

    # Convert each feature map to one value
    layers.GlobalAveragePooling2D(),

    # Combine extracted features
    layers.Dense(128, activation="relu"),

    # Reduce overfitting
    layers.Dropout(0.5),

    # Binary output: good or defective
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()
```

---

## 38. Understanding the Model Line by Line

### Input

```python
layers.Input(shape=(224, 224, 3))
```

The model expects:

- Height: 224 pixels
- Width: 224 pixels
- Channels: 3 RGB channels

### Convolution

```python
layers.Conv2D(32, (3, 3), padding="same")
```

Meaning:

- Learn 32 filters
- Each filter is `3 × 3`
- Keep approximately the same width and height

### Batch normalization

```python
layers.BatchNormalization()
```

Stabilizes the intermediate feature values.

### ReLU

```python
layers.ReLU()
```

Replaces negative values with zero and enables non-linear learning.

### Max pooling

```python
layers.MaxPooling2D((2, 2))
```

Reduces width and height by approximately half.

### Global average pooling

```python
layers.GlobalAveragePooling2D()
```

Converts each final feature map into one average value.

### Dense layer

```python
layers.Dense(128, activation="relu")
```

Combines all extracted visual evidence.

### Dropout

```python
layers.Dropout(0.5)
```

Helps reduce overfitting.

### Output

```python
layers.Dense(1, activation="sigmoid")
```

Produces a value between 0 and 1.

---

## 39. Compile the Model

```python
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
```

For multi-class classification, the final layer and loss would change.

```python
layers.Dense(number_of_classes, activation="softmax")
```

Possible loss:

```python
loss="sparse_categorical_crossentropy"
```

---

## 40. Train with Callbacks

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
    ),

    tf.keras.callbacks.ModelCheckpoint(
        filepath="best_quality_model.keras",
        monitor="val_loss",
        save_best_only=True
    )
]

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=30,
    callbacks=callbacks
)
```

### ReduceLROnPlateau

Reduces the learning rate when validation loss stops improving.

### ModelCheckpoint

Saves the best model during training.

---

## 41. Evaluate the Model

```python
test_loss, test_accuracy = model.evaluate(test_dataset)

print("Test loss:", test_loss)
print("Test accuracy:", test_accuracy)
```

Accuracy alone may not be enough for quality control. Precision, recall, F1-score, and the confusion matrix should also be checked.

---

## 42. Make a Prediction

```python
import tensorflow as tf

image = tf.keras.utils.load_img(
    "sample_product.jpg",
    target_size=(224, 224)
)

image_array = tf.keras.utils.img_to_array(image)

# Add batch dimension:
# (224, 224, 3) becomes (1, 224, 224, 3)
image_array = tf.expand_dims(image_array, axis=0)

prediction = model.predict(image_array, verbose=0)[0][0]

if prediction >= 0.5:
    print(f"Defective: {prediction:.2%}")
else:
    print(f"Good: {(1 - prediction):.2%}")
```

Possible result:

```text
Defective: 94.21%
```

---

# Part 7 — Evaluating a Quality-Control CNN

## 43. Why Accuracy Is Not Enough

Suppose the dataset contains:

```text
950 good products
50 defective products
```

A model that predicts every product as good would achieve:

```text
950 ÷ 1,000 = 95% accuracy
```

However, it would detect zero defects.

This is why additional metrics are essential.

---

## 44. Confusion Matrix Terms

### True Positive

The product is defective, and the model correctly predicts defective.

### True Negative

The product is good, and the model correctly predicts good.

### False Positive

The product is good, but the model predicts defective.

Business effect:

- A valid product may be rejected unnecessarily.

### False Negative

The product is defective, but the model predicts good.

Business effect:

- A defective product may reach the customer.

In many quality-control systems, false negatives are the most dangerous errors.

---

## 45. Precision

Precision asks:

> When the model predicts defective, how often is it correct?

```text
Precision =
True Positives
─────────────────────────────
True Positives + False Positives
```

High precision means fewer false alarms.

---

## 46. Recall

Recall asks:

> Of all truly defective products, how many were detected?

```text
Recall =
True Positives
─────────────────────────────
True Positives + False Negatives
```

High recall is often especially important when missing a defect is expensive or unsafe.

---

## 47. F1-Score

F1-score balances precision and recall.

```text
F1 =
2 × Precision × Recall
────────────────────────
Precision + Recall
```

It is useful when:

- Classes are imbalanced
- Both false positives and false negatives matter

---

## 48. Confusion Matrix Example

```text
                         Predicted
                    Good          Defective

Actual Good         900              50

Actual Defective     10              40
```

Interpretation:

- 900 good products correctly accepted
- 50 good products incorrectly rejected
- 10 defective products incorrectly accepted
- 40 defective products correctly rejected

The 10 false negatives may be the most serious issue.

---

## 49. Confidence Thresholds

The default binary threshold is often 0.5, but production systems may use a safer three-level decision.

```text
Probability below 0.30:
Accept as good

Probability from 0.30 to 0.80:
Send for manual inspection

Probability above 0.80:
Reject as defective
```

This creates three decisions:

```text
Accept
Manual review
Reject
```

The correct thresholds should be selected using validation data and business-risk requirements.

---

# Part 8 — Transfer Learning

## 50. CNN from Scratch

A CNN trained from scratch starts with random filters.

Advantages:

- Full architectural control
- Useful for learning
- Can work for highly specialized images

Disadvantages:

- Usually needs more images
- Requires more training time
- May perform poorly with a small dataset

---

## 51. Transfer Learning

Transfer learning reuses a CNN already trained on a large image dataset.

Common pretrained models:

- MobileNet
- ResNet
- EfficientNet
- DenseNet
- VGG

These models have already learned general visual features such as:

- Edges
- Shapes
- Curves
- Textures
- Object parts

You then train a smaller final portion of the network using your own quality-control images.

Transfer learning is often the best practical starting point when the dataset is small.

---

## 52. Transfer-Learning Example

```python
import tensorflow as tf
from tensorflow.keras import layers, models

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Keep pretrained layers unchanged initially
base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),

    tf.keras.applications.mobilenet_v2.preprocess_input,

    base_model,

    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4),
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
```

Here, MobileNetV2 acts as the feature extractor. The final layer learns the difference between good and defective products.

---

# Part 9 — Classification, Detection, and Segmentation

## 53. Image Classification

Classification answers:

> What is present in the image?

Example:

```text
This image contains a defective product.
```

It does not show the exact defect location.

Use classification when the only required answer is:

```text
Good or defective?
```

---

## 54. Object Detection

Object detection answers:

> What is present, and where is it?

Example:

```text
Crack found inside a bounding box.
```

Common detection models:

- YOLO
- Faster R-CNN
- SSD

Use object detection when the system must show where one or more defects are located.

---

## 55. Image Segmentation

Segmentation classifies individual pixels.

Example:

```text
These exact pixels belong to the crack.
```

Common segmentation models:

- U-Net
- Mask R-CNN
- DeepLab

Use segmentation when the exact shape, area, or size of a defect is required.

---

## 56. Which Approach Should Be Used?

Use **classification** when:

```text
You only need to decide whether the image is good or defective.
```

Use **object detection** when:

```text
You must locate one or more defects using bounding boxes.
```

Use **segmentation** when:

```text
You need the exact pixel-level defect region.
```

---

# Part 10 — Production Quality-Control Workflow

## 57. End-to-End Workflow

```text
1. Product reaches the inspection station
2. Camera captures an image
3. Image is resized
4. Pixel values are normalized
5. CNN extracts visual features
6. CNN predicts defect probability or class
7. Confidence thresholds are applied
8. Product is accepted, rejected, or reviewed
9. Prediction and image are stored for auditing
```

Architecture:

```text
Factory Camera
      ↓
Image Capture Service
      ↓
Image Preprocessing
      ↓
CNN Model
      ↓
Prediction + Confidence
      ↓
Decision Engine
   ↙       ↓        ↘
Accept   Review    Reject
```

---

## 58. Important Production Considerations

### Camera consistency

Try to use a fixed:

- Camera position
- Camera distance
- Image resolution
- Focus
- Product orientation

### Lighting consistency

Shadows and brightness variations can confuse the model.

Controlled lighting is highly recommended.

### Background consistency

The model may accidentally learn background patterns instead of defects.

Use a consistent and simple background when possible.

### Label quality

Incorrect labels teach the model incorrect behaviour.

Labels should be reviewed by people who understand the defect categories.

### Defect coverage

The dataset should contain:

- Small defects
- Large defects
- Different defect locations
- Different production batches
- Different surface colours
- Realistic lighting variation
- Normal products that look similar to defective products

### Data leakage

Images of the same physical product should not be placed in both training and test sets.

Otherwise, test performance may appear unrealistically high.

### Real-world monitoring

After deployment, monitor:

- Prediction confidence
- False-negative rate
- False-positive rate
- Changes in lighting or camera position
- New defect types
- Changes in product design
- Performance across production batches

---

# Part 11 — Quick Reference

## 59. CNN Terminology

| Concept | Simple meaning |
|---|---|
| Pixel | The smallest element of an image |
| Channel | Colour information such as red, green, and blue |
| Filter or kernel | A small matrix used to detect a pattern |
| Convolution | Moving a filter across an image |
| Feature map | Output showing where a feature was found |
| ReLU | Changes negative values to zero |
| Pooling | Reduces feature-map width and height |
| Stride | Number of pixels the filter moves |
| Padding | Extra border added around an image |
| Flatten | Converts feature maps into one long vector |
| Global average pooling | Produces one average value per feature map |
| Dense layer | Combines features to make a prediction |
| Sigmoid | Produces a binary-class probability |
| Softmax | Produces probabilities for multiple classes |
| Loss | Measures prediction error |
| Optimizer | Updates model weights |
| Learning rate | Controls the size of weight updates |
| Epoch | One complete pass through the training dataset |
| Batch | A small group of images processed together |
| Iteration | One processed batch |
| Backpropagation | Calculates how weights should change |
| Dropout | Temporarily disables neurons during training |
| Overfitting | Model memorizes training data |
| Transfer learning | Reuses a pretrained CNN |

---

## 60. Final Practical Example

Suppose a CNN must identify cracks in metal components.

```text
Input image
     ↓
First layers detect edges
     ↓
Middle layers detect thin lines and surface textures
     ↓
Deeper layers detect irregular connected crack patterns
     ↓
Dense layer combines the evidence
     ↓
Output: Crack probability = 96%
     ↓
Decision: Reject product
```

The CNN does not understand a crack exactly as a person does. It learns a mathematical pattern that frequently appears in images labelled as cracks.

---

# Final Summary

A CNN processes an image in stages:

```text
Image pixels
     ↓
Edges and colour changes
     ↓
Lines, curves, and textures
     ↓
Shapes and object parts
     ↓
Object or defect pattern
     ↓
Final prediction
```

For quality control:

```text
Capture product image
        ↓
Preprocess the image
        ↓
CNN extracts visual patterns
        ↓
Predict good or defective
        ↓
Accept, reject, or send for manual review
```

The most important ideas are:

1. **Convolution layers** extract visual features.
2. **ReLU** enables the model to learn complex patterns.
3. **Pooling** reduces feature-map size.
4. **Deeper layers** learn more meaningful features.
5. **Dense and output layers** make the final prediction.
6. **Loss and backpropagation** help the model learn.
7. **Validation and test data** measure generalization.
8. **Regularization** helps prevent overfitting.
9. **Precision and recall** are important for quality control.
10. **Transfer learning** is often the best starting point for small datasets.
