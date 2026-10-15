# Building an Image Recognition System for Quality Control

## Automated Casting Defect Detection Using CNN

**Name:** P.Shadik Khan  
**Batch:** G40 AI ML

## 1. Objective

The objective of this project is to build an image recognition system for quality control using a Convolutional Neural Network (CNN).

The model classifies casting product images into two categories:

- **Defective**
- **Non-defective**

## 2. Dataset

The casting image dataset contains two classes:

- `def_front` - Defective casting
- `ok_front` - Non-defective casting

### Dataset Split

| Dataset | Defective | Non-defective | Total |
|---|---:|---:|---:|
| Training | 624 | 415 | 1039 |
| Validation | 166* | 41* | 207 |
| Testing | 157 | 104 | 261 |

\*Validation images are created automatically from the training directory using an 80/20 split.

## 3. Project Structure

```text
P.Shadik Khan - G40 AI ML/
│
├── data/
│   ├── train/
│   │   ├── def_front/
│   │   └── ok_front/
│   │
│   └── test/
│       ├── def_front/
│       └── ok_front/
│
├── notebooks/
│   └── casting_defect_detection.ipynb
│
├── models/
│   └── best_casting_defect_model.keras
│
├── sample_images/
│   ├── cast_def_0_0.jpeg
│   ├── cast_def_0_100.jpeg
│   ├── cast_def_0_1015.jpeg
│   ├── cast_ok_0_1018.jpeg
│   └── cast_ok_0_1021.jpeg
│
├── reports/
│   ├── confusion_matrix.png
│   ├── accuracy_graph.png
│   └── loss_graph.png
│
├── requirements.txt
└── README.md