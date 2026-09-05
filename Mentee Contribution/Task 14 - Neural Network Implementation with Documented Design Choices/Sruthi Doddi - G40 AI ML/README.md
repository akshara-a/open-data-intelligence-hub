# Neural Network Implementation with Documented Design Choices

**Binary Image Classification Using a Convolutional Neural Network**

This project is a binary image classification system that inspects casting product images and predicts whether a part is **Non-defective (0)** or **Defective (1)**, built using TensorFlow/Keras.

**Dataset:** [Real Life Industrial Dataset of Casting Product](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product) (Kaggle)

## Folder Structure

```text
casting-quality-inspection/
│
├── data/
│   ├── train/
│   │   ├── ok_front/       # Non-defective training images
│   │   └── def_front/      # Defective training images
│   │
│   └── test/
│       ├── ok_front/       # Non-defective test images
│       └── def_front/      # Defective test images
│
├── notebooks/
│   └── casting_defect_detection.ipynb    # Main notebook
│
├── models/                  # Trained model and checkpoint
├── sample_images/           # Optional demo images
├── reports/                 # Evaluation graphs and results
│
├── requirements.txt
└── README.md
```

## Dataset

The casting product images are organized into training and testing folders based on their classes:

```text
data/train/ok_front/
data/train/def_front/
data/test/ok_front/
data/test/def_front/
```

The notebook loads the images using the following relative paths:

```python
TRAIN_DIR = "../data/train"
TEST_DIR  = "../data/test"
```

### Class Labels

* `0` → `ok_front` (Non-defective)
* `1` → `def_front` (Defective)

## How to Run

1. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

2. Open the notebook:

```text
notebooks/casting_defect_detection.ipynb
```

3. Run all cells from beginning to end.

4. The notebook saves the generated models and evaluation outputs in the following locations:

```text
models/best_casting_defect_model.keras
models/casting_defect_model_final.keras

reports/accuracy_graph.png
reports/loss_graph.png
reports/confusion_matrix.png
reports/sample_ok_front.png
reports/sample_def_front.png
```

## Model Overview

A **Convolutional Neural Network (CNN)** is used for binary classification.

The model consists of:

* Three convolutional and max-pooling blocks
* Global Average Pooling
* Dropout for regularization
* A dense layer
* A single sigmoid output neuron for binary classification

Data augmentation is applied only to the training data. The augmentation techniques include:

* Horizontal flipping
* Rotation
* Zoom
* Translation
* Contrast adjustment

The model is trained using:

* **Optimizer:** Adam
* **Loss function:** Binary Cross-Entropy
* **Output activation:** Sigmoid

The training process is monitored using:

* Early stopping
* Learning-rate reduction on plateau
* Model checkpointing

## Documented Design Choices

The project documents the reasoning behind the major neural network design choices, including:

* Image size selection
* Number of convolutional layers
* Number of filters
* Kernel size
* Activation functions
* Pooling strategy
* Global Average Pooling
* Dropout and regularization
* Optimizer selection
* Learning rate
* Loss function
* Batch size
* Data augmentation
* Early stopping
* Classification threshold

The design choices are documented in detail in the notebook.

## Results

The model achieved the following results on the test dataset:

| Metric | Result |
| ------ | ------: |
| Test Accuracy | **70.1%** |
| Precision – Defective | **0.86** |
| Recall – Defective | **0.63** |
| False Negatives at 0.50 | **167 / 453** |

### Decision Threshold

The default classification threshold of `0.50` resulted in a relatively high number of missed defective parts. Therefore, different probability thresholds were tested.

| Threshold | False Negatives | False Positives | Precision | Recall |
| --------- | --------------: | --------------: | --------: | -----: |
| 0.30 | 78 | 72 | 0.839 | 0.828 |
| 0.40 | 120 | 47 | 0.876 | 0.735 |
| 0.50 | 167 | 47 | 0.859 | 0.631 |
| 0.60 | 229 | 47 | 0.827 | 0.494 |

Based on the threshold comparison, **0.30** was selected as the decision threshold.

At this threshold:

* False negatives decreased from **167 to 78**.
* Recall increased from **0.63 to 0.83**.
* Precision remained at approximately **0.84**.

This threshold was selected because, in a quality-control application, missing a defective part is more costly than sending a good part for an additional manual inspection.

## Overfitting Observation

The training results showed **mild overfitting**.

Training accuracy continued to increase and reached approximately **80.7% by epoch 14**, while validation accuracy remained lower and fluctuated. Validation loss reached its best value around **epoch 9** and increased afterward.

Early stopping was used to restore the model weights from the best validation epoch.

## Bonus Experiment

As a bonus experiment, the dropout rate was changed from:

**Original Design:** Dropout `0.40 / 0.30`

to:

**Changed Design:** Dropout `0.20 / 0.20`

### Reason for Change

The purpose of this experiment was to test whether reducing dropout, and therefore reducing the strength of regularization, would change the model's ability to fit the training data and improve its test performance.

### Results

| Configuration | Test Accuracy | Test Loss |
| ------------- | -------------: | ---------: |
| Original: 0.40 / 0.30 | 70.1% | 0.579 |
| Changed: 0.20 / 0.20 | **77.1%** | **0.567** |

### Observation

Lowering dropout from **0.40/0.30 to 0.20/0.20** improved test accuracy from **70.1% to 77.1%** and slightly reduced test loss from **0.579 to 0.567**.

This suggests the original dropout rate may have been too aggressive for this dataset size, limiting how much the model could learn during training.

With less regularization, the model was able to fit the data more effectively without an obvious increase in overfitting on the test set.

Therefore, based on this experiment, **0.20/0.20 dropout may be a better setting for this architecture and dataset than the original 0.40/0.30 configuration**.

## Deliverables Produced

The notebook includes the following:

* Dataset description and class counts
* Sample image visualization
* Image preprocessing
* Data augmentation
* CNN architecture and model summary
* Training configuration and callbacks
* Training and validation accuracy graphs
* Training and validation loss graphs
* Confusion matrix
* Classification report
* Threshold tuning comparison
* Predictions on unseen images
* Saved trained models
* Findings summary
* Documented design choices with reasoning
* Design decision table
* Bonus experiment comparing different dropout configurations

## Notes

* Label mapping: `0 = ok_front (Non-defective)`, `1 = def_front (Defective)`.
* Data augmentation is applied only to the training dataset.
* False negatives are analyzed separately from false positives because a missed defective part is considered the more costly error in this quality-control application.
* The final decision threshold is **0.30**, based on the threshold comparison performed in the notebook.
* The bonus experiment changed dropout from **0.40/0.30 to 0.20/0.20**.
* The reduced dropout configuration achieved **77.1% test accuracy**, compared with **70.1%** for the original configuration.

## Conclusion

The CNN model was able to classify casting product images into defective and non-defective categories with a test accuracy of **70.1%** using the original dropout configuration.

Threshold tuning improved the detection of defective parts by increasing recall and reducing false negatives. The threshold of **0.30** was selected as the final operating point because it provides a better balance between detecting defects and limiting unnecessary manual inspections.

The bonus dropout experiment showed that reducing dropout from **0.40/0.30 to 0.20/0.20** improved test accuracy from **70.1% to 77.1%** and reduced test loss from **0.579 to 0.567**.

Overall, the project demonstrates how CNN architecture, regularization, training strategies, and decision thresholds can be systematically selected and evaluated for an image-based quality-control application.