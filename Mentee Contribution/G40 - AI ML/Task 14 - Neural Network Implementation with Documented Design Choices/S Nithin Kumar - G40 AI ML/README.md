# Binary Image Classification Using a Convolutional Neural Network

## 1. Project Overview

This mini project implements a Convolutional Neural Network (CNN) for binary image classification of casting products.

The model classifies product images into two categories:

* `def_front` — Defective
* `ok_front` — Non-defective

The project focuses on building a CNN while documenting the reasoning behind important design choices such as image size, convolution layers, filters, activation functions, pooling, dropout, optimizer, learning rate, loss function, batch size, epochs, data augmentation, and evaluation metrics.

## 2. Objective

The objective is to develop a CNN-based quality-inspection model that can identify whether a casting product image is defective or non-defective.

A particular focus is placed on recall because incorrectly classifying a defective product as non-defective can allow a defective product to pass inspection.

## 3. Dataset

Dataset:

**Casting Product Image Data for Quality Inspection**

The dataset contains two classes:

```text
def_front
ok_front
```

The dataset is kept outside Git tracking because of its size.

Expected dataset structure:

```text
data/
└── casting_data/
    ├── train/
    │   ├── def_front/
    │   └── ok_front/
    └── test/
        ├── def_front/
        └── ok_front/
```

## 4. Dataset Split

The project used:

* Training images: 5,307
* Validation images: 1,326
* Test images: 715

The training data was divided using an 80/20 training-validation split.

## 5. Technology Stack

* Python
* TensorFlow 2.21.0
* Keras
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook

## 6. CNN Architecture

The implemented architecture is:

```text
Input: 224 × 224 × 3
        ↓
Data Augmentation
        ↓
Rescaling / Normalization
        ↓
Conv2D — 32 filters, 3 × 3, ReLU
        ↓
MaxPooling2D
        ↓
Conv2D — 64 filters, 3 × 3, ReLU
        ↓
MaxPooling2D
        ↓
Conv2D — 128 filters, 3 × 3, ReLU
        ↓
MaxPooling2D
        ↓
GlobalAveragePooling2D
        ↓
Dropout — 0.40
        ↓
Dense — 64, ReLU
        ↓
Dense — 1, Sigmoid
```

Total trainable parameters:

**101,569**

## 7. Design Choices

| Design Decision     | Selected Value                 | Reason                                               |
| ------------------- | ------------------------------ | ---------------------------------------------------- |
| Image size          | 224 × 224                      | Balances image detail and computational requirements |
| Problem type        | Binary classification          | Two product classes                                  |
| Model               | CNN                            | Suitable for image feature extraction                |
| Convolution filters | 32, 64, 128                    | Learns increasingly complex visual features          |
| Kernel size         | 3 × 3                          | Efficient local feature extraction                   |
| Hidden activation   | ReLU                           | Efficient non-linear activation                      |
| Pooling             | MaxPooling2D                   | Reduces feature-map dimensions and computation       |
| Global pooling      | GlobalAveragePooling2D         | Reduces trainable parameters                         |
| Output activation   | Sigmoid                        | Produces a binary probability                        |
| Optimizer           | Adam                           | Adaptive and suitable for this task                  |
| Learning rate       | 0.001                          | Starting learning rate used for Adam                 |
| Loss                | Binary Cross-Entropy           | Appropriate for binary classification                |
| Batch size          | 32                             | Balances memory usage and training stability         |
| Maximum epochs      | 25                             | Provides sufficient training with callbacks          |
| Dropout             | 0.40                           | Helps reduce overfitting                             |
| Augmentation        | Flip, rotation, zoom, contrast | Improves robustness to image variations              |
| Metrics             | Accuracy, Precision, Recall    | Measures overall and class-related performance       |

## 8. Data Augmentation

The following augmentation techniques were applied to the training data:

* Random horizontal flip
* Random rotation
* Random zoom
* Random contrast

Augmentation helps the model handle small variations in product orientation, camera movement, zoom, and lighting.

Normalization was applied using:

```python
Rescaling(1.0 / 255)
```

which converts pixel values from approximately 0–255 to 0–1.

## 9. Training Configuration

The model was compiled using:

```text
Optimizer: Adam
Learning Rate: 0.001
Loss: Binary Cross-Entropy
Batch Size: 32
Maximum Epochs: 25
```

Two callbacks were used:

* EarlyStopping
* ReduceLROnPlateau

EarlyStopping monitors validation loss and restores the best model weights.

ReduceLROnPlateau reduces the learning rate when validation improvement slows.

## 10. Training Results

The model was trained for 25 epochs.

At Epoch 25:

```text
Training Accuracy:   89.79%
Training Loss:        0.2495
Validation Accuracy: 82.28%
Validation Loss:      0.3822
```

The best visible validation accuracy was approximately:

```text
88.91%
```

at Epoch 24.

Training and validation accuracy/loss graphs are available in the `outputs` directory.

## 11. Test Results

The final test evaluation produced:

| Metric         | Result |
| -------------- | -----: |
| Test Accuracy  | 90.77% |
| Test Precision | 84.27% |
| Test Recall    | 91.98% |
| Test Loss      | 0.2245 |

These results indicate that the CNN achieved good classification performance on the unseen test dataset.

## 12. Confusion Matrix

The confusion matrix was:

```text
[[408, 45],
 [ 21, 241]]
```

The class order used by the dataset was:

```text
0 → def_front
1 → ok_front
```

Therefore:

* 408 defective products were correctly classified as defective.
* 45 defective products were incorrectly classified as OK.
* 21 OK products were incorrectly classified as defective.
* 241 OK products were correctly classified as OK.

The 45 defective products incorrectly classified as OK represent false-negative cases and are especially important in a quality-inspection application.

## 13. Unseen Image Testing

Five unseen test images were selected and evaluated using the trained CNN.

For each image, the project records:

* Image name
* Predicted class
* Prediction probability
* Recommended inspection action

A defective prediction is sent for manual inspection, while an OK prediction can pass the initial inspection stage.

## 14. Output Files

The project contains the following generated visualizations:

```text
outputs/
├── accuracy.png
├── loss.png
└── confusion_matrix.png
```

## 15. Project Structure

```text
Task 14 - CNN Image Classification/
│
├── data/
│   └── casting_data/
│       ├── train/
│       │   ├── def_front/
│       │   └── ok_front/
│       └── test/
│           ├── def_front/
│           └── ok_front/
│
├── outputs/
│   ├── accuracy.png
│   ├── loss.png
│   └── confusion_matrix.png
│
├── cnn_image_classification.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

The dataset inside `data/` is excluded from Git using `.gitignore`.

## 16. Installation

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## 17. Running the Project

1. Download the recommended Casting Product Image Data for Quality Inspection dataset.
2. Extract the dataset.
3. Place the dataset in the expected `data/casting_data/` structure.
4. Open `cnn_image_classification.ipynb` in Jupyter Notebook or VS Code.
5. Select a Python environment with the required dependencies.
6. Run the notebook cells from top to bottom.

## 18. Conclusion

A convolutional neural network was developed to classify casting product images into defective and non-defective categories.

The model used 224 × 224 RGB images, data augmentation, normalization, three convolutional blocks, max pooling, global average pooling, dropout, and a sigmoid output layer.

The CNN achieved approximately 90.77% test accuracy, 84.27% precision, and 91.98% recall. The confusion matrix identified 45 defective products incorrectly classified as non-defective, highlighting why recall and false-negative analysis are important for automated quality inspection.

Overall, the project demonstrates the implementation of a basic CNN, appropriate preprocessing and regularization techniques, model evaluation, and documentation of important neural-network design decisions.
