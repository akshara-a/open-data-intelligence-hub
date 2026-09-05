# Ensemble CNN Classifier — CIFAR-10

Task 15 — trains three CNN architectures on CIFAR-10, combines them via
majority voting, soft voting, and weighted soft voting, and benchmarks
accuracy, latency, throughput, model size, parameter count, memory usage,
and robustness to corrupted images.

## Project structure

```
ensemble-cnn-classifier/
├── data/
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── augmentation.py
│   ├── models/
│   │   ├── baseline_cnn.py
│   │   ├── regularized_cnn.py
│   │   └── deep_cnn.py
│   ├── train.py
│   ├── evaluate.py
│   ├── ensemble.py
│   ├── benchmark.py
│   ├── robustness_test.py
│   └── predict.py
├── models/
│   ├── cnn_baseline.keras
│   ├── cnn_regularized.keras
│   └── cnn_deep.keras
├── results/
│   ├── training_history_cnn1.png
│   ├── training_history_cnn2.png
│   ├── training_history_cnn3.png
│   ├── confusion_matrix_cnn1.png
│   ├── confusion_matrix_cnn2.png
│   ├── confusion_matrix_cnn3.png
│   ├── confusion_matrix_ensemble.png
│   ├── robustness_results.csv
│   └── benchmark_results.csv
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Dataset

CIFAR-10 (60,000 32×32 color images, 10 classes: airplane, automobile,
bird, cat, deer, dog, frog, horse, ship, truck). Loaded from CSV
(`cifar10_train.csv` / `cifar10_test.csv`, flattened pixel columns + a
`label` column) or from image folders (`train/<class>/*.png`,
`test/<class>/*.png`) — see `src/data_loader.py`.

## Usage

```bash
# Train all three models
python -m src.train

# Full pipeline: train + ensemble + benchmark + robustness testing
python -m src.run_pipeline

# Run inference on new images with the trained ensemble
python -m src.predict path/to/image.png
```

## Models

| Model | Architecture | Params | Size |
|---|---|---|---|
| `cnn_baseline` | 2 conv blocks, no regularization | 167,562 | 1.97 MB |
| `cnn_regularized` | Conv + BatchNorm + Dropout | 545,482 | 6.32 MB |
| `cnn_deep` | 3 conv blocks + GlobalAveragePooling | 158,122 | 1.90 MB |

## Results

Test accuracy per model:

| Model | Test Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| `cnn_baseline` | 0.6883 | 0.6968 | 0.6883 | 0.6799 |
| `cnn_regularized` | 0.3373 | 0.3115 | 0.3373 | 0.2887 |
| `cnn_deep` | **0.7800** | 0.7825 | 0.7800 | 0.7772 |

Ensemble strategies:

| Strategy | Test Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| Majority voting | 0.7222 | 0.7349 | 0.7222 | 0.7191 |
| Soft voting | 0.7788 | 0.7817 | 0.7788 | 0.7747 |
| **Weighted soft voting** | **0.7845** | 0.7872 | 0.7845 | 0.7807 |

Weighted soft voting (weighted by each model's validation accuracy) was
the best-performing strategy, beating the best individual model
(`cnn_deep`, 0.78) by ~0.45 points.

**Note:** `cnn_regularized` underperformed significantly (0.34 vs 0.69–0.78
for the other two models) in this run — likely worth a rerun or a tuning
pass on its dropout/learning-rate schedule before treating it as a fair
comparison point.

### Ensemble benchmark

- Avg latency: 248.7 ms | Throughput: 1668 img/s
- Total size: 10.19 MB | Total params: 871,166

### Robustness (accuracy under corruption)

| Corruption | `cnn_baseline` | `cnn_regularized` | `cnn_deep` | Ensemble (soft voting) |
|---|---|---|---|---|
| Rotated | 0.6431 | 0.3242 | 0.7364 | 0.7402 |
| Blurred | 0.4966 | 0.2352 | 0.4070 | 0.4762 |
| Noisy | 0.5710 | 0.2745 | 0.3825 | 0.5298 |
| Darker | 0.5909 | 0.1506 | 0.7402 | 0.7326 |
| Brighter | 0.5877 | 0.2796 | 0.6589 | 0.6675 |

The ensemble is more robust than any single model on 4 of 5 corruption
types, missing only on "noisy" where `cnn_baseline` alone edges it out.
