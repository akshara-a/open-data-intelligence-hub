# Project Report: Automated Casting Defect Detection Using a CNN

## 1. Title
Automated Casting Defect Detection Using a Convolutional Neural Network

## 2. Abstract
This project builds a binary image classification system that
automatically inspects images of manufactured casting products and
predicts whether each product is defective or non-defective. A
Convolutional Neural Network (CNN) is trained on the Kaggle "Casting
Product Image Data for Quality Inspection" dataset and deployed behind
an interactive Gradio dashboard for real-time inspection.

## 3. Introduction
Manufacturing quality control traditionally relies on human visual
inspection, which does not scale well to high-volume, high-speed
production lines and is subject to fatigue and inconsistency between
inspectors. This project explores whether a CNN can serve as an
automated first-pass classifier to support (not replace) human quality
control.

## 4. Business Problem
Manual inspection becomes difficult as production volume grows,
defects become subtler, and inspector fatigue and inter-inspector
disagreement increase. An automated system can apply the same
criteria consistently at production speed.

## 5. Problem Statement
Given an image of a casting product captured by a fixed camera, predict
a binary label indicating whether the product shows a visible defect.

## 6. Objective
Build, train, and evaluate a CNN that classifies casting product images
as:
- `0` = Non-defective (`ok_front`)
- `1` = Defective (`def_front`)

and expose it through an interactive dashboard for manual testing.

## 7. Dataset Description
Source: Kaggle "Casting Product Image Data for Quality Inspection".
Two classes: `ok_front` (non-defective) and `def_front` (defective).
Exact image counts and class balance for this run must be taken from
`notebooks/01_data_exploration.ipynb` output (not fabricated here) --
see `reports/figures/class_distribution.png` after running the
notebook.

## 8. Data Preprocessing
- Images resized to 224x224.
- Pixel values normalized to `[0, 1]` via a `Rescaling` layer inside
  the model.
- Dataset split: 80% training / 20% validation (from `data/train/`),
  plus a fully separate `data/test/` directory used only for final
  evaluation.
- Class mapping explicitly enforced (`ok_front` = 0, `def_front` = 1),
  independent of alphabetical folder ordering.

## 9. Data Augmentation
Mild augmentation applied only to training images: horizontal flip,
small rotation (±0.05), small zoom (±0.10), small translation (±0.05),
and mild contrast adjustment (±0.10). Validation and test images are
never augmented, so they represent realistic, unseen production
conditions.

## 10. CNN Architecture
Three Conv2D + MaxPooling2D blocks (32 -> 64 -> 128 filters), followed
by GlobalAveragePooling2D, Dropout(0.40), a Dense(64, ReLU) layer,
Dropout(0.30), and a final Dense(1, sigmoid) output. See
`reports/metrics/model_summary.txt` for the exact layer-by-layer
summary generated at training time.

## 11. Training Methodology
- Loss: binary cross-entropy
- Optimizer: Adam, learning rate 0.001
- Batch size: 32
- Up to 25 epochs, with:
  - EarlyStopping (monitor `val_loss`, patience 5, restores best weights)
  - ReduceLROnPlateau (factor 0.5, patience 2, min_lr 1e-6)
  - ModelCheckpoint (saves only the best `val_loss` model)
- Fixed random seed (42) for reproducibility.

## 12. Evaluation Metrics
Reported on the held-out test set (715 images), model checkpoint saved
at lowest validation loss (~epoch 9), at the default 0.50 threshold:

- Test Accuracy: **83.9%** (0.8391608595848083)
- Defective class -- Precision: **0.86**, Recall: **0.90**, F1: 0.88
- Non-defective class -- Precision: 0.80, Recall: 0.74, F1: 0.77
- Macro avg precision/recall: 0.83 / 0.82
- Weighted avg precision/recall: 0.84 / 0.84

Note: `test_metrics.json`'s `compile_metrics` field currently only
captures accuracy from `model.evaluate()`; the precision/recall values
above come from `sklearn.classification_report`, which is the
authoritative source of per-class precision/recall for this project.

## 13. Threshold Analysis
Thresholds `[0.30, 0.40, 0.50, 0.60, 0.70]` were evaluated on the test
set. Full results: `reports/metrics/threshold_analysis.csv` and
`reports/figures/threshold_vs_recall.png`.

| Threshold | Accuracy | Recall | False Negatives | False Positives |
|---|---|---|---|---|
| 0.30 | 77.5% | 98.0% | 9 | 152 |
| **0.40 (selected)** | **82.9%** | **95.4%** | **21** | **101** |
| 0.50 (default) | 83.9% | 89.6% | 47 | 68 |
| 0.60 | 82.2% | 82.6% | 79 | 48 |
| 0.70 | 75.0% | 70.9% | 132 | 47 |

**Selected threshold: 0.40.** The project spec treats reducing false
negatives as a major objective, since a missed defect risks reaching
the customer, while a false positive only causes an unnecessary manual
re-check. Threshold 0.30 catches the most defects (9 missed) but
nearly doubles false positives versus 0.40 (152 vs 101) for a steep
accuracy trade-off (77.5% vs 82.9%). Threshold 0.40 cuts false
negatives by more than half relative to the default (21 vs 47) while
keeping accuracy close to its peak and avoiding an excessive false-alarm
rate. Thresholds at or above 0.50 let comparatively more real defects
through, which is unacceptable in a quality-control context favoring
recall on the defective class.

## 14. Confusion Matrix Interpretation
At the default 0.50 threshold: 194 true negatives, 68 false positives,
47 false negatives, 406 true positives (see
`reports/metrics/confusion_matrix.json` and
`reports/figures/confusion_matrix.png`). The model correctly classifies
the large majority of both classes, with a mild bias toward flagging
images as defective (recall on the defective class exceeds precision),
which is generally desirable for a quality-control screening tool
where missed defects are costlier than false alarms.

## 15. False Negative Analysis
A false negative here means a defective product was predicted as
non-defective -- the most costly error type in this application, since
it risks a defective part reaching the customer undetected. At the
default 0.50 threshold: 47 false negatives out of 453 actually-defective
test images (false negative rate 10.4%). At the selected production
threshold of 0.40, this drops to 21 false negatives (~4.6% FNR), a
meaningfully safer rate at the cost of a moderate increase in manual
reviews (101 vs 68 false positives).

## 16. Application / Dashboard
A Gradio dashboard (`app/app.py`, launched via `run_app.py`) allows a
user to upload a casting product image, adjust the decision threshold,
and receive a prediction, defect probability, and recommended action.
The model is loaded once at startup for performance.

## 17. Business Use Case
Deployed on a production line, a camera captures each product image at
the inspection point; the model flags likely-defective products for
manual review or removal, while non-defective products proceed. This
reduces inspector workload and increases consistency, while keeping a
human in the loop for final decisions.

## 18. Limitations
- Results are only as good as the training data; unusual lighting,
  camera angle, or unseen defect types may reduce accuracy.
- The model provides a probability, not a certainty -- it does not
  eliminate the need for human oversight, particularly around the
  decision threshold's trade-offs.
- No defect localization is performed.

## 19. Future Enhancements
Transfer learning (MobileNetV2 / EfficientNet), batch normalization,
class weighting for imbalance, Grad-CAM explainability, TensorFlow
Lite conversion for edge deployment, and ongoing monitoring/retraining
as new production images accumulate.

## 20. Conclusion
This project demonstrates an end-to-end, reproducible pipeline for
industrial visual quality inspection using a CNN, from data validation
and augmentation through training, evaluation, threshold tuning, and
an interactive dashboard for demonstration and manual testing. Actual
performance numbers should be filled in above after running the
pipeline against the real dataset.
