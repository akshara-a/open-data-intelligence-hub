# Business Report - Task 15 Production-Grade Ensemble CNN Classifier

## 1. Executive Summary

This project evaluates an ensemble of three Convolutional Neural Network models for automated casting product inspection. The objective is to support quality-control processes by identifying defective and non-defective casting images.

The evaluated ensemble achieved an accuracy of 63.96% on 197 test images. The model achieved high precision but low recall for the positive class, indicating that the current system requires further improvement before deployment in a production quality-control environment.

## 2. Business Problem

Manual visual inspection can be time-consuming and may produce inconsistent results. An automated image-classification system can support quality-control teams by providing fast initial screening of casting products.

The business objective is to:

- Reduce manual inspection workload.
- Improve consistency in quality-control decisions.
- Identify potentially defective or non-defective products quickly.
- Support scalable inspection workflows.

## 3. Model Performance

The ensemble evaluation produced the following results:

| Metric | Result |
|---|---:|
| Accuracy | 63.96% |
| Precision | 100.00% |
| Recall | 10.13% |
| F1 Score | 18.39% |

The confusion matrix was:

118 true negatives, 0 false positives, 71 false negatives, and 8 true positives.

The low recall indicates that the model currently misses a substantial number of positive-class samples. Therefore, accuracy alone should not be used to judge deployment readiness.

## 4. Operational Performance

Three CNN models were benchmarked.

- Baseline CNN: approximately 3.32 ms per image and 301.5 images per second.
- Regularized CNN: approximately 4.46 ms per image and 224.0 images per second.
- Deep CNN: approximately 12.66 ms per image and 79.0 images per second.

The baseline CNN provides the best inference speed and may be useful where low latency is a primary operational requirement.

## 5. Robustness Findings

The ensemble was tested under multiple image conditions.

- Original images: 63.96% accuracy.
- Gaussian noise level 20: 59.90% accuracy.
- Brightness 0.7: 59.90% accuracy.
- Brightness 1.3: 82.23% accuracy.
- Horizontal flip: 64.97% accuracy.

These results show that performance varies under different image conditions. Consistent camera and lighting conditions are important for reliable deployment.

## 6. Business Recommendations

1. Use the current system as an inspection-assistance tool rather than a fully autonomous decision system.
2. Maintain human review for uncertain or high-risk predictions.
3. Improve class balance and training data diversity.
4. Investigate probability-threshold tuning to improve recall.
5. Collect additional examples representing different lighting and noise conditions.
6. Monitor model performance continuously after deployment.
7. Prefer the baseline model when inference speed is more important than model complexity.

## 7. Deployment Considerations

Before deployment, the organization should:

- Define acceptable false-negative and false-positive costs.
- Establish human-review procedures.
- Monitor accuracy, precision, recall and F1 score.
- Test the system using production-like images.
- Retrain the model periodically with new inspection data.

## 8. Conclusion

The ensemble CNN demonstrates the potential of deep learning for automated casting inspection. However, the current evaluation results show that further optimization is required before autonomous production deployment. The system is more suitable as a decision-support tool while additional work is performed to improve recall, robustness and overall reliability.
