# Automated Casting Defect Detection Using a CNN

This project is a binary image classification system that analyzes casting product images and predicts whether a part is **Non-defective (0)** or **Defective (1)** using TensorFlow/Keras.

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

## Results

The model achieved the following results on the test dataset:

| Metric                  |        Result |
| ----------------------- | ------------: |
| Test Accuracy           |     **70.1%** |
| Precision – Defective   |      **0.86** |
| Recall – Defective      |      **0.63** |
| False Negatives at 0.50 | **167 / 453** |

### Decision Threshold

The default classification threshold of `0.50` resulted in a relatively high number of missed defective parts. Therefore, different probability thresholds were tested.

| Threshold | False Negatives | False Positives | Precision | Recall |
| --------- | --------------: | --------------: | --------: | -----: |
| 0.30      |              78 |              72 |     0.839 |  0.828 |
| 0.40      |             120 |              47 |     0.876 |  0.735 |
| 0.50      |             167 |              47 |     0.859 |  0.631 |
| 0.60      |             229 |              47 |     0.827 |  0.494 |

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

## Notes

* Label mapping: `0 = ok_front (Non-defective)`, `1 = def_front (Defective)`.
* Data augmentation is applied only to the training dataset.
* False negatives are analyzed separately from false positives because a missed defective part is considered the more costly error in this quality-control application.
* The final decision threshold is **0.30**, based on the threshold comparison performed in the notebook.

## Conclusion

The CNN model was able to classify casting product images into defective and non-defective categories with a test accuracy of **70.1%**.

Threshold tuning improved the detection of defective parts by increasing recall and reducing false negatives. The threshold of **0.30** was selected as the final operating point because it provides a better balance between detecting defects and limiting unnecessary manual inspections.

Full implementation, visualizations, evaluation results, and the detailed findings summary are available in the notebook.
