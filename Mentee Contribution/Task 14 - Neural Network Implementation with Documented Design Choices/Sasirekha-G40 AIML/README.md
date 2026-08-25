# Binary Image Classification Using CNN

## Overview
A college mini-project that classifies casting product images as **Non-defective (`ok_front`)** or **Defective (`def_front`)** using a CNN.

## Dataset
Use the **Casting Product Image Data for Quality Inspection** dataset. Dataset images are intentionally not included.

```text
data/
├── train/
│   ├── ok_front/
│   └── def_front/
└── test/
    ├── ok_front/
    └── def_front/
```

## Project Structure
```text
cnn_casting_quality/
├── data/
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_cnn_training.ipynb
│   ├── 04_model_evaluation.ipynb
│   ├── 05_unseen_image_prediction.ipynb
│   └── 06_bonus_experiment.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
├── models/
├── outputs/
├── sample_images/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── run_project.bat
```

## Setup
```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execution Order
```powershell
python -m src.train
python -m src.evaluate
python -m src.predict sample_images/example.jpg
streamlit run app.py
```
Run the first three only after adding the dataset. Streamlit is optional.

## Hardware
Configuration is centralized in `src/config.py`: image size 224×224, batch size 32, maximum 25 epochs, learning rate 0.001, dropout 0.40. Training uses EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, and `prefetch(tf.data.AUTOTUNE)`. No full training is started automatically.

## Architecture
Input 224×224×3 → augmentation → Rescaling → Conv2D(32) → MaxPooling → Conv2D(64) → MaxPooling → Conv2D(128) → MaxPooling → GlobalAveragePooling2D → Dropout(0.40) → Dense(64, ReLU) → Dense(1, sigmoid).

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

## Evaluation
The test directory is kept separate from the training/validation split. Outputs are saved under `outputs/`. Defective-class recall is especially important because an actual defective product predicted as non-defective is a false negative.

This is a student mini-project and is **not production-ready**.

## Results
Do not invent metrics. Record them only after execution:
```text
Test Accuracy: [Run the project to obtain]
Precision: [Run the project to obtain]
Recall: [Run the project to obtain]
```

## Bonus Experiment
Compare dropout 0.40 vs 0.20. Do not report numbers until both experiments are actually run.

## Common Errors
- **Dataset missing:** check all four expected class directories.
- **No GPU:** CPU training is supported; TensorFlow prints the detected devices.
- **Out of memory:** lower `BATCH_SIZE` to 16 or 8 in `src/config.py`.
- **Slow/hot laptop:** stop training, let the laptop cool, reduce batch size if needed, and rely on early stopping.
- **Missing model:** run `python -m src.train`.
- **Missing image:** place a real image in `sample_images/`.

## Viva — 20 Questions
1. What is a CNN? — A neural network designed to learn spatial patterns from images.
2. What is convolution? — Applying learnable filters over local image regions.
3. What is a filter? — Learnable weights that respond to visual patterns.
4. What is a kernel? — The small spatial weight window used by convolution.
5. Why 3×3 kernels? — Efficient local feature extraction.
6. Why ReLU? — Non-linearity with simple computation.
7. Why pooling? — Reduces spatial dimensions and computation.
8. Why normalize? — Scaling pixels to roughly 0–1 helps stable optimization.
9. What is augmentation? — Transforming training images to improve robustness.
10. Why dropout? — Helps reduce overfitting.
11. Why sigmoid? — Produces a probability for binary class 1.
12. Why binary cross-entropy? — Suitable for binary classification with sigmoid.
13. Why Adam? — Adaptive optimization and convenient starting point.
14. What is learning rate? — Step size for parameter updates.
15. What is batch size? — Samples processed per weight update.
16. What is an epoch? — One complete pass through training data.
17. What is EarlyStopping? — Stops training when validation performance stops improving.
18. What is precision? — Fraction of predicted positives that are truly positive.
19. What is recall? — Fraction of actual positives correctly detected.
20. What is a false negative? — A defective item incorrectly predicted as non-defective.
