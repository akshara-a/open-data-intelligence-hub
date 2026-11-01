
# Task 14 - Binary Image Classification Using CNN

## Project Title
Binary Image Classification Using a Convolutional Neural Network

## Objective
The objective of this project is to build a Convolutional Neural Network (CNN)
that classifies casting product images into two categories:

- Class 0: Non-defective (`ok_front`)
- Class 1: Defective (`def_front`)

The project also documents the reasoning behind the major CNN architecture
and training design choices.

---

## Dataset

Dataset:
Casting Product Image Data for Quality Inspection

Source:
Kaggle - Real Life Industrial Dataset of Casting Product

Classes:

- `ok_front`  -> Non-defective -> Class 0
- `def_front` -> Defective     -> Class 1

Dataset contains separate training and testing folders.

The training dataset was further divided into:

- 80% Training
- 20% Validation

The original test dataset was kept separate for final evaluation.

---

## Technology Stack

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- Scikit-learn
- Google Colab
- NVIDIA Tesla T4 GPU

---

## Hardware Used

The project was trained using:

- GPU: NVIDIA Tesla T4
- TensorFlow GPU acceleration
- Google Colab environment

GPU acceleration was used to reduce CNN training time.

---

## Input Configuration

Image Size:

224 x 224 x 3

Batch Size:

32

The image size of 224 x 224 was selected because it provides enough visual
detail while keeping memory usage and computation manageable.

---

## Data Normalization

Image pixel values originally range from 0 to 255.

The following normalization was used:

Rescaling(1.0 / 255)

This converts pixel values approximately to the range 0 to 1 and improves
training stability.

---

## Data Augmentation

The training dataset uses mild augmentation:

- Random Horizontal Flip
- Random Rotation: 0.05
- Random Zoom: 0.10
- Random Contrast: 0.10

Data augmentation improves model robustness against small variations in
orientation, camera position, zoom and lighting.

Augmentation is applied only during model training.

---

## CNN Architecture

The CNN architecture is:

Input: 224 x 224 x 3

Data Augmentation

Rescaling 1/255

Conv2D
- Filters: 32
- Kernel: 3 x 3
- Activation: ReLU

MaxPooling2D

Conv2D
- Filters: 64
- Kernel: 3 x 3
- Activation: ReLU

MaxPooling2D

Conv2D
- Filters: 128
- Kernel: 3 x 3
- Activation: ReLU

MaxPooling2D

GlobalAveragePooling2D

Dropout
- Rate: 0.40

Dense
- Units: 64
- Activation: ReLU

Output Dense Layer
- Units: 1
- Activation: Sigmoid

---

## Architecture Design Choices

### CNN Filters

32 -> 64 -> 128

The number of filters increases in deeper layers so the CNN can learn
increasingly complex visual patterns.

### Kernel Size

3 x 3 kernels were selected because they efficiently extract local visual
features such as edges, textures and defect patterns.

### ReLU Activation

ReLU is used in hidden layers because it is computationally efficient and
works well for CNN image classification.

### Max Pooling

MaxPooling2D reduces feature-map dimensions and computational requirements
while preserving important activations.

### Global Average Pooling

GlobalAveragePooling2D was selected instead of a large Flatten layer to
reduce the number of trainable parameters.

### Dropout

Dropout = 0.40

Dropout helps reduce overfitting by randomly disabling neurons during
training.

### Output Layer

Dense(1, activation="sigmoid")

Sigmoid produces a probability between 0 and 1 and is suitable for binary
classification.

---

## Training Configuration

Optimizer:
Adam

Learning Rate:
0.001

Loss Function:
Binary Cross-Entropy

Batch Size:
32

Maximum Epochs:
25

Metrics:

- Accuracy
- Precision
- Recall

---

## Callbacks

### EarlyStopping

- Monitor: Validation Loss
- Patience: 5
- Restore Best Weights: True

EarlyStopping prevents unnecessary training when validation performance
stops improving.

### ReduceLROnPlateau

- Monitor: Validation Loss
- Factor: 0.5
- Patience: 2

This reduces the learning rate when validation improvement slows down.

---

## Training Results

During training:

- Training accuracy improved significantly.
- Final training accuracy was approximately 89%.
- Validation accuracy reached approximately 86%.
- Training and validation accuracy remained reasonably close.
- No severe overfitting was observed.
- The model completed all 25 epochs.
- Best-performing model weights were restored after training.

Exact final test values are available in the Jupyter Notebook output.

---

## Model Evaluation

The model was evaluated using:

- Test Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- True Negatives
- False Positives
- False Negatives
- True Positives

---

## Importance of Recall

Recall for the defective class is particularly important.

A False Negative means:

Actual Defective Product
        |
        v
Predicted Non-defective

This is dangerous in quality inspection because a defective product could
incorrectly pass inspection.

Therefore, detecting as many actual defective products as possible is an
important objective of the model.

---

## Unseen Image Testing

At least five unseen images from the test dataset were evaluated.

For each image, the system reports:

- Actual Class
- Predicted Class
- Prediction Probability
- Recommended Action

For defective predictions:

Action: Send for manual inspection

For non-defective predictions:

Action: Pass

---

## Bonus Experiment

One design choice was changed:

Original Dropout:
0.40

Changed Dropout:
0.20

Reason:

The experiment investigates whether reducing dropout allows the model to
learn more information and improve classification performance.

The original and modified models were compared using the same test dataset.

Metrics compared:

- Accuracy
- Precision
- Recall
- Loss

Exact comparison results are available in the notebook.

---

## Design Decision Summary

| Design Decision | Selected Value |
|---|---|
| Image Size | 224 x 224 |
| Problem Type | Binary Classification |
| Model Type | CNN |
| Conv Filters | 32, 64, 128 |
| Kernel Size | 3 x 3 |
| Hidden Activation | ReLU |
| Pooling | MaxPooling2D |
| Global Pooling | GlobalAveragePooling2D |
| Output Activation | Sigmoid |
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Loss Function | Binary Cross-Entropy |
| Batch Size | 32 |
| Maximum Epochs | 25 |
| Dropout | 0.40 |
| Augmentation | Flip, Rotation, Zoom, Contrast |
| Metrics | Accuracy, Precision, Recall |

---

## Files Included in Submission

The final submission package may contain:

1. `Task_14_Binary_Image_Classification_CNN.ipynb`
2. `README.md`
3. `task14_cnn_model.keras`
4. `task14_bonus_model.keras`
5. `casting_dataset/`

The original downloaded dataset ZIP and Google Colab `sample_data` folder
are intentionally excluded.

---

## Conclusion

A Convolutional Neural Network was successfully implemented for automated
casting product defect classification.

The CNN learned visual features using three convolutional layers with
increasing filter sizes. Data augmentation, normalization, dropout,
EarlyStopping and learning-rate reduction were used to improve robustness
and generalization.

The model was evaluated using accuracy, precision, recall, F1-score and a
confusion matrix.

For industrial quality inspection, defective-class recall is especially
important because false negatives can allow defective products to pass
inspection.

The project demonstrates the complete workflow of designing, training,
evaluating and comparing a binary CNN image classifier.
