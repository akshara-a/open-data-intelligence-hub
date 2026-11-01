# Binary Image Classification Using a Convolutional Neural Network

## 1. Project Overview

This project implements a CNN-based binary image classification system for casting quality inspection.

The model classifies casting product images into:

- **Class 0 — Non-defective:** `ok_front`
- **Class 1 — Defective:** `def_front`

> This is an educational college mini-project and is not validated for real industrial quality-control deployment.

## 2. Objective

Build a CNN that automatically classifies casting images as defective or non-defective while documenting the major design decisions.

## 3. Dataset Structure

```text
data/
├── train/
│   ├── ok_front/
│   └── def_front/
└── test/
    ├── ok_front/
    └── def_front/
```

| Folder | Meaning | Label |
|---|---|---:|
| `ok_front` | Non-defective | 0 |
| `def_front` | Defective | 1 |

The dataset images are not included. Add the actual images to these folders.

## 4. Technologies

- Python 3.10+
- TensorFlow / Keras
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- Pillow
- Jupyter Notebook
- Streamlit (optional)
- VS Code

## 5. Project Structure

```text
cnn_casting_quality/
├── data/
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
├── models/
├── report
│   ├── figures
│   ├── metrics
│   ├── interview_questions.md
│   ├── project_report.md
├── app.py
├── requirements.txt
├── run_project.bat
├── README.md
└── document.md
```

## 6. Environment Setup

From the VS Code terminal:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 7. What Is `run_project.bat`?

`run_project.bat` is an optional Windows batch file that can create the virtual environment, activate it, install dependencies, and show the next commands.

You **do not need to run it** if you are setting up the project manually in VS Code.

## 8. Correct Execution Order

You do **not** need to run every notebook before `train.py`.

Recommended order:

```text
01_dataset_exploration.ipynb

`03_cnn_training.ipynb` is an alternative to `python -m src.train`. Do not unnecessarily train the model twice.

## 9. CNN Architecture

```text
Input: 224 × 224 × 3
        ↓
Data Augmentation
        ↓
Rescaling 1/255
        ↓
Conv2D — 32 filters, 3×3, ReLU
        ↓
MaxPooling2D
        ↓
Conv2D — 64 filters, 3×3, ReLU
        ↓
MaxPooling2D
        ↓
Conv2D — 128 filters, 3×3, ReLU
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

## 10. Design Decisions

| Design Decision | Selected Value | Reason |
|---|---|---|
| Image size | 224 × 224 | Balance detail and computation |
| Model | CNN | Suitable for images |
| Conv filters | 32 → 64 → 128 | Increasing feature complexity |
| Kernel | 3 × 3 | Efficient local feature extraction |
| Activation | ReLU | Non-linearity and efficient computation |
| Pooling | MaxPooling2D | Reduces spatial dimensions |
| Global pooling | GlobalAveragePooling2D | Reduces parameters |
| Dropout | 0.40 | Helps reduce overfitting |
| Output | Sigmoid | Binary probability |
| Optimizer | Adam | Adaptive optimization |
| Learning rate | 0.001 | Reasonable starting value |
| Loss | Binary Cross-Entropy | Suitable for binary classification |
| Batch size | 32 | Memory/training balance |
| Maximum epochs | 25 | Limits training time |
| Augmentation | Flip, rotation, zoom, contrast | Improves robustness |
| Metrics | Accuracy, Precision, Recall | Multiple performance views |

## 11. Dataset Exploration

Run:

```text
notebooks/01_dataset_exploration.ipynb
```

It checks:

- Number of images in each class
- Class distribution
- Image dimensions
- Sample images

Do not report numerical results until the notebook has actually been executed.

## 12. Preprocessing

Run:

```text
notebooks/02_data_preprocessing.ipynb
```

The project uses:

- 224 × 224 RGB images
- 80/20 validation split from the training directory
- Pixel rescaling by `1/255`
- Data augmentation
- Separate test data

## 13. Training

Recommended command:

```powershell
python -m src.train
```

Training uses:

- Adam optimizer
- Binary cross-entropy
- Maximum 25 epochs
- EarlyStopping
- ReduceLROnPlateau
- ModelCheckpoint
- Dataset prefetching

The best model is saved to:

```text
models/best_model.keras
```

## 14. Laptop-Friendly Settings

The project is configured with:

```text
Image size: 224 × 224
Batch size: 32
Maximum epochs: 25
EarlyStopping: enabled
ReduceLROnPlateau: enabled
Prefetching: enabled
```

If memory usage is too high, change `BATCH_SIZE` in `src/config.py` to:

```python
BATCH_SIZE = 16
```

or:

```python
BATCH_SIZE = 8
```

If the laptop becomes very hot, stop training and allow it to cool.

## 15. Evaluation

After training, run:

```powershell
python -m src.evaluate
```


## 16. Unseen Image Prediction

Put real unseen images in:

```text
sample_images/
```

Then:

```powershell
python -m src.predict sample_images/example.jpg
```


Compare:

```text
Dropout = 0.40
```

with:

```text
Dropout = 0.20
```

Only record accuracy and other metrics after actually running both experiments.

## 17. Optional Streamlit Application

Run:

```powershell
streamlit run app.py
```

This provides a simple image-upload demonstration.

It is an educational interface and should not be treated as an industrial inspection system.

## 18. Important Output Files

After execution:

```text
models/
└── best_model.keras

outputs/
├── training_history.json
├── model_summary.txt
├── plots/
│   ├── accuracy_curve.png
│   ├── loss_curve.png
│   └── class_distribution.png
├── confusion_matrix/
│   └── confusion_matrix.png
└── predictions/
    └── classification_report.txt
```

## 19. Common Errors

### Dataset not found

Verify:

```text
data/train/ok_front
data/train/def_front
data/test/ok_front
data/test/def_front
```

### Model not found

Run:

```powershell
python -m src.train
```

### No GPU

CPU training is supported.

### Out of memory

Reduce the batch size to 16 or 8 in `src/config.py`.

### Prediction image not found

Use the actual filename:

```powershell
python -m src.predict sample_images/your_image.jpg
```

## 20. Final Workflow

```text
Dataset
   ↓
Dataset Exploration
   ↓
Preprocessing
   ↓
CNN Training
   ↓
Validation
   ↓
Best Model
   ↓
Test Evaluation
   ↓
Confusion Matrix
   ↓
Unseen Image Prediction
   ↓
Optional Bonus Experiment
```

## 21. Conclusion

This project demonstrates an end-to-end CNN workflow for binary casting-quality image classification, including dataset exploration, preprocessing, augmentation, model training, evaluation, confusion-matrix analysis, unseen-image prediction, and an optional Streamlit interface.

**Do not fabricate model accuracy, precision, recall, confusion matrices, or unseen-image predictions. Generate them by running the project.**
