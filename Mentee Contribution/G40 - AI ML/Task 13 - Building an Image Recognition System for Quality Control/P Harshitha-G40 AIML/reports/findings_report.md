
# Casting Defect Detection - Findings

## Dataset

Training images: 5307
Validation images: 1326
Test images: 715

## Model

Model: Convolutional Neural Network (CNN)

Image size: 224 x 224

Optimizer: Adam

Loss function: Binary Crossentropy

Classification threshold: 0.50

## Test Results

Accuracy: 0.8280

Precision: 0.8300

Recall: 0.9161

F1 Score: 0.8709

ROC-AUC: 0.8919

## Conclusion

The CNN model was evaluated on the casting defect test dataset.

The model classifies casting products into:

- Non-defective
- Defective

Products predicted as defective are recommended for manual inspection,
while products predicted as non-defective may proceed on the production line.
