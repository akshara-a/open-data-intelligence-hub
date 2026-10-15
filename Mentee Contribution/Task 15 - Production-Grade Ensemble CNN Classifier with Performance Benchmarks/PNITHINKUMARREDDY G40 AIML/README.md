# Production-Grade Ensemble CNN Classifier

An image classification system that trains three diverse CNNs on the **Intel Image Classification** dataset (6 natural-scene classes), combines their predictions via Majority / Soft / Weighted Voting, and benchmarks the ensemble against the best individual model on accuracy, robustness, latency, throughput, memory, and model size to make a production deployment decision.

Full write-up of methodology, results, and the final recommendation: **[`report.md`](./report.md)**.

---

## 1. Directory Structure

Place the deliverables in the following layout:

```
ensemble-cnn-classifier/
├── README.md                                    ← this file
├── report.md                                     ← full project report
├── requirements.txt                              ← Python dependencies
├── notebooks/
│   └── production-grade-ensemble-cnn-classifier.ipynb
├── images/                                        ← report figures (referenced by report.md)
│   ├── acc_loss.png                              ← training/validation accuracy & loss curves
│   ├── cnn_independent.png                       ← confusion matrices, CNN1/CNN2/CNN3
│   ├── cnn_ensemble.png                          ← confusion matrices, Majority/Soft voting
│   └── robustness.png                            ← accuracy across perturbations
└── models/                                        ← saved trained models (produced by the notebook)
    ├── cnn_baseline.keras
    ├── cnn_regularized.keras
    └── cnn_deep.keras
```

> `models/` is created automatically by the notebook (`os.makedirs("models", exist_ok=True)`) the first time it's run — you don't need to create it by hand, just don't move/rename the `.keras` files afterward since the benchmarking cells look them up by that exact path.

---

## 2. Dataset

**[Intel Image Classification](https://www.kaggle.com/datasets/puneet6060/intel-image-classification)** (Kaggle) — 6 classes: `buildings`, `forest`, `glacier`, `mountain`, `sea`, `street`.

The notebook expects the standard Kaggle folder layout:

```
<dataset-root>/seg_train/seg_train/<class_name>/*.jpg
<dataset-root>/seg_test/seg_test/<class_name>/*.jpg
```

- **On Kaggle Notebooks:** attach the dataset via the Input panel; the notebook auto-discovers the path under `/kaggle/input`.
- **Locally:** download the dataset from Kaggle, unzip it, and edit `TRAIN_DIR_GUESS` / `TEST_DIR_GUESS` at the top of Part 1 to point at your local `seg_train/seg_train` and `seg_test/seg_test` folders (or place the extracted dataset under a local `/kaggle/input/...` path to match the auto-discovery logic unchanged).

---

## 3. Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**`requirements.txt`:**
```
tensorflow>=2.15
numpy
pandas
matplotlib
seaborn
scikit-learn
scipy
psutil
jupyter
```

A GPU is strongly recommended (the notebook auto-detects and uses one if available) — training all three CNNs on CPU will be substantially slower than the times logged in the report.

---

## 4. Running the Notebook

```bash
jupyter notebook notebooks/production-grade-ensemble-cnn-classifier.ipynb
```

Run all cells top to bottom. The notebook is organized into these stages:

| Part | What it does |
|---|---|
| 1 | Load dataset, split train/val/test, visualize samples, normalize |
| 2 | Data augmentation (training data only) |
| 3–5 | Build & train CNN1 (baseline), CNN2 (regularized), CNN3 (deep) |
| 5b | Plot training/validation accuracy & loss curves |
| 6 | Evaluate each CNN independently (accuracy, precision, recall, F1, confusion matrix) |
| 7 | Ensemble via Majority Voting, Soft Voting, and Weighted Voting |
| 8 | Production benchmark: latency, throughput, model size, parameter count, memory |
| 9 | Robustness testing under rotation, blur, noise, darkening, brightening |
| 10 | Model disagreement analysis |
| 11 | Final benchmark table + accuracy-vs-cost trade-off |
| 12–13 | Required-questions answers + final production recommendation |

Total runtime is dominated by the three training loops (Parts 3–5); everything from Part 6 onward (evaluation, benchmarking, robustness) runs in a few minutes once the three `.keras` models are saved.

---

## 5. Outputs

After a full run you should have:

- Three trained models in `models/*.keras`
- The four figures listed under `images/` above (regenerate them from the notebook's plotting cells if you re-run with a different dataset split or seed)
- Printed evaluation metrics, confusion matrices, benchmark tables, and the disagreement analysis inline in the notebook — all summarized in [`report.md`](./report.md)

---

## 6. Key Result (see `report.md` for full analysis)

| | Best Individual (CNN3_Deep) | Best Ensemble (Weighted Voting) |
|---|---|---|
| Accuracy | 81.20% | 82.40% (+1.20 pp) |
| Latency | 67.3 ms | 203.2 ms (+202%) |
| Model size | 1.87 MB | 182.81 MB |

**Recommendation:** deploy CNN3_Deep alone for latency-sensitive/real-time use cases; deploy the Weighted Voting ensemble for offline/batch workloads where accuracy and robustness to noisy or poorly-lit images matter more than speed. See `report.md` §21 for full reasoning, including a note that CNN2_Regularized failed to train properly and should be retrained before being relied on in production.
