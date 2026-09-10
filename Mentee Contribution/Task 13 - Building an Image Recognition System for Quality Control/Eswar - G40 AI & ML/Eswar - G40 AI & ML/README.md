# Automated Casting Defect Detection Using a CNN

This project is a binary image classification system that analyzes casting product
images and predicts whether a part is **Non-defective (0)** or **Defective (1)** using
TensorFlow/Keras.

**Dataset:** [Casting Product Image Data for Quality Inspection](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product) (Kaggle)

## Folder Structure

```text
Eswar - G40 AI & ML/
│
├── notebooks/
│   └── casting_defect_detection.ipynb   # Main notebook
│
├── models/
│   ├── best_casting_defect_model.keras   # Best checkpoint (lowest val_loss)
│   └── casting_defect_model_final.keras  # Final saved model
│
├── reports/
│   ├── accuracy_graph.png
│   ├── loss_graph.png
│   ├── confusion_matrix.png
│   ├── sample_ok_front.png
│   └── sample_def_front.png
│
├── requirements.txt
└── README.md
```

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the dataset from Kaggle and arrange it as `casting_data/train/{ok_front,def_front}`
   and `casting_data/test/{ok_front,def_front}` next to the notebook.
3. Open `notebooks/casting_defect_detection.ipynb` and run all cells in order.
4. The best model is saved automatically to `models/best_casting_defect_model.keras`.
5. Training/evaluation plots are saved to `reports/`.
6. Add a few unseen images to `sample_images/` for the Task 8 predictions.

## Summary

- Label `0` = Non-defective, label `1` = Defective.
- CNN with 3 convolution + max-pooling blocks, global average pooling, dropout, and a
  sigmoid output.
- Adam optimizer, binary cross-entropy loss, early stopping, learning-rate reduction,
  and model checkpointing.
- Evaluated with accuracy, precision, recall, a confusion matrix, and a comparison of
  classification thresholds (0.30–0.60).
- False negatives (a defective part passed as good) are treated as the
  highest-priority error.

See `notebooks/casting_defect_detection.ipynb` for the full implementation and the
findings-report section at the end for results once training is complete.

## Results (trained on the real Kaggle dataset)

Trained on the actual `casting_data` train split (6,633 images: 3,758 defective /
2,875 non-defective) and evaluated on the held-out test split (715 images: 453
defective / 262 non-defective). Training ran for 12 epochs at 224×224 resolution
before it was stopped at the best checkpoint (lowest validation loss).

| Metric | Value |
|---|---|
| Test accuracy | 84.2% |
| Test precision | 86.3% |
| Test recall | 89.2% |
| Test loss | 0.388 |

**Confusion matrix (test set, threshold = 0.50):**

| | Predicted Non-defective | Predicted Defective |
|---|---|---|
| **Actual Non-defective** | 198 (TN) | 64 (FP) |
| **Actual Defective** | 49 (FN) | 404 (TP) |

- False negatives (49): defective parts misclassified as good — the
  highest-priority error, since these would reach the customer.
- False positives (64): good parts flagged as defective — wasted manual
  re-inspection, lower cost than a false negative.

**Threshold comparison** (trading off FP against FN):

| Threshold | FP | FN | Precision | Recall |
|---|---|---|---|---|
| 0.30 | 95 | 21 | 82.0% | 95.4% |
| 0.40 | 85 | 32 | 83.2% | 92.9% |
| 0.50 | 64 | 49 | 86.3% | 89.2% |
| 0.60 | 48 | 67 | 88.9% | 85.2% |

For a quality-control setting where letting a defective part through is worse than
flagging a good one for a second look, a lower threshold (e.g. 0.30–0.40) trades
some extra false positives for meaningfully fewer false negatives.

**Training behavior:** the first 4 epochs showed almost no learning (the model was
effectively predicting "defective" for everything, matching the ~59% class-majority
baseline). It began discriminating properly from epoch 5 onward, validation loss
dropped from 0.68 to 0.39 by epoch 12, and a mid-training dip around epoch 9–10
recovered once the learning-rate scheduler kicked in. This pattern — a slow start
followed by a rapid improvement — is common for a CNN trained from scratch (no
pretrained weights) with fairly heavy data augmentation.

**Possible next steps:** transfer learning with a pretrained backbone (e.g.
MobileNetV2) would likely reach higher accuracy faster; more training epochs beyond
12 may still yield further gains, as validation loss was still improving when
training stopped; Grad-CAM visualization would help confirm the model is attending
to the actual defect regions rather than incidental image artifacts.
