# Mini Project: Neural Network Implementation with Documented Design Choices

Binary image classifier (CNN) that predicts whether a casting product image is
**Non-defective (0)** or **Defective (1)**, with a short written reason behind every
major design decision — input size, architecture, activation, pooling, dropout,
optimizer, learning rate, loss, batch size, epochs, and augmentation.

**Dataset:** [Casting Product Image Data for Quality Inspection](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product) (Kaggle) — same dataset as Task 13.

## Folder Structure

```text
Eswar - G40 AI & ML/
├── README.md
├── requirements.txt
├── notebooks/
│   └── casting_cnn_documented_design.ipynb
├── models/
│   └── casting_cnn_documented.keras
└── reports/
    ├── accuracy_graph.png
    ├── loss_graph.png
    └── confusion_matrix.png
```

## How to Run

1. `pip install -r requirements.txt`
2. Download the dataset and arrange it as `casting_data/train/{ok_front,def_front}`
   and `casting_data/test/{ok_front,def_front}` next to the notebook.
3. Open `notebooks/casting_cnn_documented_design.ipynb` and run all cells in order.
4. The best checkpoint saves to `models/casting_cnn_documented.keras`; the
   accuracy/loss/confusion-matrix plots save to `reports/`.
5. For Task 9, swap the `REPLACE_ME` placeholders for five real filenames from
   `casting_data/test/ok_front/` and `casting_data/test/def_front/`.
6. The bonus-experiment cell trains a second model with dropout lowered from 0.40 to
   0.20, for direct comparison against the original.

## Design Decision Table

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

## Results

Trained on the real `casting_data` train split (6,633 images) and evaluated on the
held-out test split (715 images: 453 defective / 262 non-defective). Ran the full 15
epochs (early stopping never triggered — validation loss was still improving at the
end).

| Metric | Value |
|---|---|
| Test accuracy | 83.5% |
| Test precision | 81.3% |
| Test recall | 96.0% |
| Test loss | 0.404 |

**Confusion matrix (threshold = 0.50):**

| | Predicted Non-defective | Predicted Defective |
|---|---|---|
| **Actual Non-defective** | 162 (TN) | 100 (FP) |
| **Actual Defective** | 18 (FN) | 435 (TP) |

**Answers to the Task 6 questions:**

1. **Did training accuracy improve?** Yes, steadily from 56% to 81% across 15 epochs.
2. **Did validation accuracy improve?** Yes, from 59% to 84%, though with two sharp
   dips (epochs 7 and 10) before recovering.
3. **Is there a large gap between training and validation curves?** No — validation
   accuracy tracked slightly *above* training accuracy for most of the run, which is
   unusual but not concerning here: it reflects the validation set being a touch
   easier on those particular batches, not a modeling error.
4. **Is the model overfitting?** No signs of it — training and validation loss both
   decreased together through epoch 15, with validation loss actually finishing lower
   (0.39) than a simple training/validation gap would suggest is a problem.
5. **Did early stopping activate?** No — all 15 epochs ran. Validation loss was still
   trending down at the end, suggesting more epochs (up to the original cap of 25)
   would likely improve results further.

## Bonus Experiment

```text
Original Design:  Dropout = 0.40
Changed Design:   Dropout = 0.20
Reason:           Test whether less regularization improves accuracy on this dataset size
Original Accuracy: 83.5% (test)
New Accuracy:      Not yet run — see notebook's bonus-experiment cell
Observation:       Pending
```

## Conclusion

The model reaches 83.5% test accuracy with a strong 96.0% recall on the defective
class — meaning it catches the large majority of actual defects (18 missed out of
453), at the cost of flagging some good parts unnecessarily (100 false positives out
of 262). For a quality-control setting, that trade-off is reasonable: a false
positive costs a second manual look, while a false negative lets a bad part through.

The model isn't fully converged yet — validation loss was still improving at epoch
15, so training longer (up to the original 25-epoch cap) would likely push accuracy
higher still. Next steps worth trying: continue training past 15 epochs, transfer
learning with a pretrained backbone (e.g. MobileNetV2) for faster convergence, or
lowering the decision threshold below 0.50 to push recall even higher for this
safety-critical use case.
