# Business Report - Task 14 Binary Image Classification Using a CNN

## 1. Executive Summary

This project develops a Convolutional Neural Network (CNN) for automated binary classification of casting product images. The objective is to distinguish defective products from non-defective products and support quality-control activities.

The model was evaluated on 715 test images and achieved an overall accuracy of 77.76%. The model performed particularly well in identifying defective products, achieving a precision of 94.92%, recall of 75.97%, and F1-score of 84.40%.

## 2. Business Problem

Manufacturing quality control often depends on manual visual inspection. Manual inspection can require significant time and may lead to inconsistent decisions.

An automated CNN-based inspection system can support the quality-control process by:

- Screening casting product images automatically.
- Reducing the workload of inspectors.
- Supporting faster identification of potential defects.
- Improving consistency in inspection workflows.

## 3. Model Performance

The CNN model achieved the following evaluation results:

| Metric | Score |
|---|---:|
| Accuracy | 77.76% |
| Defective Precision | 94.92% |
| Defective Recall | 75.97% |
| Defective F1 Score | 84.40% |

The classification report shows strong precision for the defective class. When the model predicts a product as defective, the prediction is highly reliable based on the test results.

## 4. Classification Analysis

For the defective class:

- Precision was 0.95.
- Recall was 0.76.
- F1-score was 0.84.

For the non-defective class:

- Precision was 0.48.
- Recall was 0.85.
- F1-score was 0.61.

The lower precision for non-defective predictions indicates that some products predicted as non-defective may require additional review depending on the cost of inspection errors.

## 5. Business Value

A successful automated inspection system could provide several benefits:

1. Faster initial screening of manufactured products.
2. Reduced repetitive workload for quality-control teams.
3. More consistent image-based inspection.
4. Better scalability when the volume of inspected products increases.
5. Support for early identification of defective products.

## 6. Business Recommendations

1. Use the CNN as an inspection-support system together with human quality inspectors.
2. Prioritize review of uncertain predictions.
3. Continue collecting additional non-defective images to improve class balance.
4. Monitor defective recall because missed defects can have a direct manufacturing cost.
5. Test the model under real production lighting and camera conditions.
6. Periodically retrain the model using newly collected production data.

## 7. Deployment Considerations

Before full production deployment, the organization should:

- Define the acceptable cost of false positives and false negatives.
- Validate performance on real production-line images.
- Monitor model accuracy, precision, recall and F1-score.
- Establish human-review procedures for uncertain predictions.
- Ensure image acquisition conditions are consistent.

## 8. Conclusion

The CNN demonstrates useful potential for automated casting defect detection. With an accuracy of 77.76% and strong defective-class precision, the model can provide meaningful support for manufacturing quality control.

However, the current system should be used as a decision-support tool rather than a completely autonomous inspection system. Further improvements in dataset balance, real-world testing and model optimization can improve reliability for production deployment.
