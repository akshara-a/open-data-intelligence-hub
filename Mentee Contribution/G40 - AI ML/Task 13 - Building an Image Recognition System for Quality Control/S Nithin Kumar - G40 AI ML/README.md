# Casting Defect Detection using CNN

## Project Overview

This project detects whether a casting product is defective or non-defective using a Convolutional Neural Network (CNN).

The model classifies casting images into two classes:

- `def_front` – Defective casting
- `ok_front` – Non-defective casting

## Dataset

The dataset is organized into training and testing folders.

```text
casting_data/
├── train/
│   ├── def_front/
│   └── ok_front/
└── test/
    ├── def_front/
    └── ok_front/