# Production-Grade Ensemble CNN Classifier with Performance Benchmarks

## 1. Project Overview

In this mini project, we build a production-grade image classification system using multiple Convolutional Neural Network (CNN) models.

Instead of training only one CNN and using its prediction, we train **multiple CNN models** and combine their predictions to produce one final result. This approach is called **Ensemble Learning**.

The project focuses on two important areas:
1. Improving classification quality using multiple CNN models.
2. Measuring whether the improvement is worth the additional production cost.

We compare:
- Individual CNN performance
- Ensemble CNN performance
- Robustness under noisy input
- Training/inference cost vs. accuracy gain

## 2. Project Structure

```
.
├── models/
│   ├── cnn_baseline.keras       # simple/shallow CNN
│   ├── cnn_deep.keras           # deeper CNN, higher capacity
│   └── cnn_regularized.keras    # CNN with BatchNorm + Dropout + L2
├── notebook/
│   └── task15_ensemble_cnn.ipynb   # end-to-end training + evaluation notebook
├── report/
│   ├── acc_loss.png              # training/validation accuracy & loss curves
│   ├── cnn_ensemble.png          # individual models vs ensemble accuracy
│   ├── cnn_independent.png       # standalone model accuracy comparison
│   └── robustness.png            # accuracy vs input noise level
├── requirements.txt
└── README.md
```

## 3. How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebook/task15_ensemble_cnn.ipynb
```

Running the notebook end-to-end will:
1. Load and preprocess the dataset (CIFAR-10 by default — swap in your own dataset if needed).
2. Train three CNN architectures (`cnn_baseline`, `cnn_deep`, `cnn_regularized`) and save them to `models/`.
3. Evaluate each model individually and as a soft-voting ensemble.
4. Generate all four report charts into `report/`.
5. Produce a cost-vs-benefit summary table comparing single-model vs ensemble accuracy, training time, and parameter count.

> **Note:** The `.keras` files in `models/` and the `.png` files in `report/` are placeholders in this scaffold. They are produced automatically the first time you run the notebook.

## 4. Models

| Model | Description |
|---|---|
| `cnn_baseline` | Shallow 2-conv-block CNN — fast, lower capacity |
| `cnn_deep` | Deeper CNN with more conv blocks — higher capacity |
| `cnn_regularized` | Same depth as baseline, with BatchNorm + Dropout + L2 for better generalization |

## 5. Ensemble Strategy

Predictions from all three models are combined using **soft voting** (averaging predicted class probabilities), then taking the argmax as the final prediction.

## 6. Evaluation Metrics

- Test accuracy (individual vs. ensemble)
- Training time and parameter count per model
- Robustness to Gaussian input noise (sigma = 0.0 to 0.3)
- Accuracy gain of ensemble vs. best single model, weighed against added inference/storage cost

## 7. Conclusion

See the final section of the notebook for the filled-in cost-vs-benefit recommendation once you've run it on your dataset.
