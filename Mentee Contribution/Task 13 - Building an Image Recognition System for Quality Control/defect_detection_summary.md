# Task 13: Automated Casting Defect Detection Summary

## Performance Summary
- **Binary Classification Target:** Non-defective (0) vs Defective (1)
- **Architecture:** 3 Convolutional Blocks + Global Average Pooling + Dropout Regularization
- **Threshold Policy:** 0.50 (Adjustable to 0.40 for strict defect sensitivity)

## Classification Report
               precision    recall  f1-score   support

Non-defective       0.00      0.00      0.00        50
    Defective       0.50      1.00      0.67        50

     accuracy                           0.50       100
    macro avg       0.25      0.50      0.33       100
 weighted avg       0.25      0.50      0.33       100

