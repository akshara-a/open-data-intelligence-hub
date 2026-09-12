# Binary Image Classification Using a CNN

## Project Overview

This project implements a Convolutional Neural Network (CNN) for automated binary image classification of casting products.

The model classifies casting product images into two categories:

- **Defective**
- **Non-defective**

The goal is to support automated quality inspection and identify defective casting products using computer vision.

## Dataset

The dataset contains casting product images organized into two classes:

```text
data/
├── train/
│   ├── def_front/
│   └── ok_front/
└── test/
    ├── def_front/
    └── ok_front/