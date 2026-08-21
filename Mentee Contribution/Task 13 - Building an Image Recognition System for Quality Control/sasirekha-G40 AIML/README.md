# Automated Casting Defect Detection

A real-world, modular AI/ML project that uses a Convolutional Neural
Network (CNN) to automatically classify images of manufactured casting
products as **defective** or **non-defective**, with an interactive
Streamlit dashboard for live inspection.

---

## 1. Project Overview

Manufacturing companies inspect products before shipping them to
customers. Traditionally, human inspectors visually examine each part
and decide whether it passes quality control. This project automates
the first pass of that inspection using a CNN trained on casting
product images.

## 2. Business Problem

Manual inspection becomes difficult when:

- Thousands of products are manufactured every day.
- Defects are small or hard to notice.
- Inspectors become fatigued after reviewing many products.
- Different inspectors reach different conclusions on the same part.
- Products move quickly through the production line.

An automated first-pass classifier can flag likely-defective parts
for manual review consistently and at production speed.

## 3. Objective

Given an image of a casting product, predict:

```
0 = Non-defective
1 = Defective
```

This is a **binary image classification** problem. The model does not
localize or categorize the defect type -- it only determines whether a
defect is present.

## 4. Dataset

**Dataset:** Casting Product Image Data for Quality Inspection (Kaggle)

| Original folder | Meaning | Binary label |
|---|---|---:|
| `ok_front` | Product without a visible defect | `0` |
| `def_front` | Product with a visible defect | `1` |

The class mapping is enforced **explicitly** in `src/config.py` and
`src/data_loader.py` (via the `class_names` argument to
`image_dataset_from_directory`), rather than relying on alphabetical
folder ordering.

Exact dataset size and class balance must be verified after downloading
the dataset -- run `notebooks/01_data_exploration.ipynb` to generate
real counts; do not assume figures not present here.

## 5. Machine Learning Approach

1. **Image preprocessing** -- resize to 224x224, normalize pixels to
   `[0, 1]` (via a `Rescaling` layer inside the model).
2. **Data augmentation** -- mild, realistic transformations applied
   only to the training split (see Section 13).
3. **CNN** -- three convolution/pooling blocks, global average
   pooling, dropout, and a sigmoid output neuron.
4. **Training** -- Adam optimizer, binary cross-entropy loss, with
   early stopping, learning-rate reduction, and checkpointing.
5. **Validation** -- a held-out 20% split of the training directory,
   used during training to monitor generalization.
6. **Testing** -- a completely separate `data/test/` directory, used
   only once, after training, for final evaluation.

## 6. Model Architecture

```
Input (224, 224, 3)
      |
Data augmentation (train-time only)
      |
Rescaling (1/255)
      |
Conv2D 32 + ReLU
      |
MaxPooling2D
      |
Conv2D 64 + ReLU
      |
MaxPooling2D
      |
Conv2D 128 + ReLU
      |
MaxPooling2D
      |
GlobalAveragePooling2D
      |
Dropout (0.40)
      |
Dense 64 + ReLU
      |
Dropout (0.30)
      |
Dense 1 + Sigmoid  -->  defect probability
```

Loss: `binary_crossentropy` | Optimizer: `Adam` (lr = 0.001) |
Metrics: `accuracy`, `precision`, `recall`

## 7. Technologies

- Python 3.10+
- TensorFlow / Keras
- NumPy, Pandas
- Matplotlib, Seaborn
- Scikit-learn
- Pillow
- Streamlit (dashboard)
- Jupyter

## 8. Project Structure

```
casting-quality-inspection/
│
├── data/
│   ├── train/
│   │   ├── ok_front/
│   │   └── def_front/
│   │
│   └── test/
│       ├── ok_front/
│       └── def_front/
│
├── models/
│   └── best_casting_defect_model.keras
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_analysis.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
│
├── reports/
│   ├── figures/
│   ├── metrics/
│   ├── project_report.md
│   └── interview_questions.md
│
├── sample_images/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 9. Installation

```bash
python -m venv .venv
```

Activate the virtual environment:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 10. Dataset Setup

1. Download **"Casting Product Image Data for Quality Inspection"**
   from Kaggle.
2. Place the images so the folder structure looks exactly like this:

```
data/
├── train/
│   ├── ok_front/    <- non-defective training images
│   └── def_front/   <- defective training images
│
└── test/
    ├── ok_front/    <- non-defective test images
    └── def_front/   <- defective test images
```

3. The `test/` directory must be images the model will **never** see
   during training or validation.

## 11. Training

```bash
python -m src.train
```

This will:

- Validate the dataset structure.
- Build the training/validation split (80/20) from `data/train/`.
- Train the CNN for up to 25 epochs (early stopping may finish sooner).
- Save the best model to `models/best_casting_defect_model.keras`.
- Save `reports/metrics/model_summary.txt`.
- Save `reports/figures/training_accuracy.png` and `training_loss.png`.

## 12. Evaluation

```bash
python -m src.evaluate
```

This will:

- Load the best saved model.
- Evaluate it on `data/test/` only.
- Print and save the classification report and confusion matrix.
- Report false positives / false negatives and their rates.
- Run a threshold analysis across `[0.30, 0.40, 0.50, 0.60, 0.70]`
  and save `reports/metrics/threshold_analysis.csv` plus a
  precision/recall-vs-threshold plot.

## 13. Run the Dashboard (Streamlit)

```bash
streamlit run streamlit_app.py
```

Then open the local URL printed in your terminal (usually
`http://localhost:8501`).

1. Upload a casting product image.
2. Adjust the **Decision Threshold** slider if desired (default 0.40).
3. Click **🔍 Inspect Product**.
4. Read the prediction, defect probability, threshold used, and
   recommended action.

The model is loaded once (via `@st.cache_resource`) and reused across
interactions, not reloaded on every click.

## 15. Evaluation Metrics

- **Accuracy** -- overall percentage of correct predictions.
- **Precision** -- of all products predicted defective, how many
  actually were? High precision means fewer good products are
  incorrectly flagged.
- **Recall** -- of all genuinely defective products, how many did the
  model catch? Recall is critical here: a missed defect (false
  negative) can reach the customer.
- **False positive** -- a good product incorrectly flagged as
  defective (unnecessary manual review).
- **False negative** -- a defective product incorrectly classified as
  good (the costliest error in this application).
- **Confusion matrix** -- full breakdown of TN / FP / FN / TP.

## 16. Threshold Tuning

The default classification threshold is `0.50`. Lowering it (e.g. to
`0.40` or `0.30`) generally increases recall (catches more true
defects) but also increases false positives (more good parts sent for
unnecessary manual review). There is no single "correct" threshold --
it should be chosen based on the relative cost, in a specific factory,
of a missed defect versus an unnecessary manual inspection. See
`reports/metrics/threshold_analysis.csv` after running evaluation for
the actual trade-off curve on this dataset.

## 17. Business Impact

An automated first-pass classifier can provide **faster, more
consistent** initial screening than manual inspection alone,
especially at high production volumes, while still routing uncertain
or flagged parts to a human for final judgment.

## 18. Limitations

- Model quality depends entirely on the dataset used to train it.
- Performance may degrade under different lighting, camera angle, or
  camera hardware than the training images used.
- Defect types not represented in the training data may not be
  detected reliably (domain shift).
- False positives and false negatives are both possible; this system
  is a decision-support tool, not a replacement for human judgment in
  a production line.
- The model classifies whole images; it does not localize or draw
  bounding boxes around the specific defect.

## 19. Future Improvements

- Transfer learning with MobileNetV2 or EfficientNet.
- Batch normalization.
- Class weighting for imbalanced datasets.
- Grad-CAM visualization to show which image regions drove a
  prediction.
- Conversion to TensorFlow Lite for edge/embedded deployment.
- Direct webcam-based inspection integration.
- Ongoing model monitoring and periodic retraining as new production
  images become available.

None of the items in this section have been implemented in the current
codebase; they are documented as possible next steps only.

---

## Project Workflow

```
Dataset
   |
Data Validation
   |
Train/Validation Split
   |
Image Resize
   |
Normalization
   |
Data Augmentation
   |
CNN Training
   |
Validation
   |
Best Model Checkpoint
   |
Test Evaluation
   |
Threshold Analysis
   |
Saved Model
   |
Streamlit Application
   |
Human Inspection Decision
```

---

## HOW TO RUN THIS PROJECT FROM ZERO

**Step 1.** Open the project folder in VS Code.

**Step 2.** Create a virtual environment:
```bash
python -m venv .venv
```

**Step 3.** Activate it:
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

**Step 4.** Install requirements:
```bash
pip install -r requirements.txt
```

**Step 5.** Place the dataset in `data/train/` and `data/test/` as
described in Section 10.

**Step 6.** Run data exploration:
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

**Step 7.** Train the model:
```bash
python -m src.train
```

**Step 8.** Evaluate the model:
```bash
python -m src.evaluate
```

**Step 9.** Run the Streamlit dashboard:
```bash
streamlit run streamlit_app.py
```

**Step 10.** Upload a new casting image in the browser tab that opens
and click **🔍 Inspect Product**.

---

## Reproducibility

A fixed random seed (`42`, see `src/config.py`) is used for the
train/validation split and for Python/NumPy/TensorFlow seeding
(`src/utils.py: set_global_seeds`), so results are as reproducible as
practical across runs on the same machine and library versions.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| TensorFlow fails to install | Ensure you're using Python 3.10 or 3.11 (TensorFlow may not yet support the very latest Python release); try `pip install --upgrade pip` first. |
| Wrong Python version | Check with `python --version`; recreate the virtual environment with a supported interpreter if needed. |
| `FileNotFoundError` for dataset paths | Confirm the exact folder names `data/train/ok_front`, `data/train/def_front`, `data/test/ok_front`, `data/test/def_front`. |
| "No trained model found" in Streamlit | Run `python -m src.train` before launching the app. |
| Permission denied writing to `models/` or `reports/` | Check folder permissions, or run the terminal with appropriate privileges. |
| "Port already in use" when launching Streamlit | Close the other process, or run `streamlit run streamlit_app.py --server.port 8502`. |
| Streamlit doesn't open automatically | Manually open the local URL printed in the terminal (usually `http://localhost:8501`). |
| CUDA / GPU errors | The project runs on CPU by default; GPU is optional. If TensorFlow can't find your GPU, training still works on CPU, only slower. |
| Out-of-memory during training | Reduce `BATCH_SIZE` in `src/config.py`. |
| Folder structure errors during `image_dataset_from_directory` | Re-check Section 10 -- class folder names must be exactly `ok_front` and `def_front`. |

---

## License / Attribution

Dataset: "Casting Product Image Data for Quality Inspection" (Kaggle).
Please review the dataset's license on Kaggle before redistribution.
