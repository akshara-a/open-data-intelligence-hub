# Task 14: Neural Network Implementation with Documented Design Choices

## 1. Project Objective
Built a binary image classification system (Non-defective vs Defective) using a Convolutional Neural Network (CNN). The primary objective was to document the architectural and hyperparameter design choices for the model.

## 2. Design Decision Table

| Design Decision | Selected Value | Reason |
|---|---|---|
| Image size | 224 x 224 | Balance between detail and computation |
| Problem type | Binary classification | Two output classes |
| Model type | CNN | Suitable for learning spatial features in images |
| Conv filters | 32, 64, 128 | Learn increasingly complex features deeper in the network |
| Kernel size | 3 x 3 | Efficient local feature extraction |
| Hidden activation | ReLU | Efficient, prevents vanishing gradients, and commonly used |
| Pooling | MaxPooling2D | Reduces feature dimensions and computational load |
| Output activation | Sigmoid | Produces binary probability (0 to 1) |
| Optimizer | Adam | Adaptive learning rate and beginner-friendly |
| Learning rate | 0.001 | Reasonable Adam starting value to ensure stable training |
| Loss | Binary Cross-Entropy | Mathematically suited for two-class probability output |
| Batch size | 32 | Balanced memory consumption and stable training updates |
| Epochs | Maximum 25 | Enough training time; combined with early stopping to prevent overfitting |
| Dropout | 0.40 | Randomly drops neurons to help reduce overfitting |
| Augmentation | Flip, rotation, zoom, contrast | Improves robustness against real-world camera variations |
| Metrics | Accuracy, Precision, Recall | Recall is prioritized to prevent defective products from passing inspection |

## 3. Bonus Experiment Documentation

- **Changed Design:** Dropout rate
- **Original Design:** `Dropout(0.40)`
- **Reason for Change:** To see if the model was dropping too many features (underfitting) or if reducing the dropout rate would lead to faster memorization and potential overfitting.
- **Original Accuracy:** 50.0%
- **New Accuracy (0.20 Dropout):** 84.0%
- **Observation:** Reducing the dropout rate allowed the model to retain more network connections during training. On this specific synthetic dataset, reducing the dropout rate to 0.20 significantly improved the accuracy from 50% to 84%, allowing the model to learn the visual features much more effectively without dropping too much critical information.

## 4. Why Recall Matters
In industrial quality control, a **False Negative** (predicting a defective product as non-defective) is a critical failure because it allows a broken product to be shipped to a customer. Therefore, maximizing **Recall** for the defective class is prioritized over pure accuracy.
