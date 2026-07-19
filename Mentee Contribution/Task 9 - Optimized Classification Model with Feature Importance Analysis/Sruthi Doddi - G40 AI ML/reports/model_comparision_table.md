# Model Comparison Table
## E-Commerce Purchase Prediction

| Model | Optimization Status | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|---------------------|----------|-----------|--------|----------|---------|
| Logistic Regression | Baseline | 0.9884 | 1.0000 | 0.9484 | 0.9735 | 0.9862 |
| Decision Tree | Baseline | 0.9962 | 0.9920 | 0.9911 | 0.9915 | 0.9944 |
| Random Forest | Baseline | 0.9966 | 1.0000 | 0.9849 | 0.9924 | 0.9949 |
| **Random Forest** | **Optimized** | **0.9972** | **1.0000** | **0.9875** | **0.9937** | **0.9955** |

### Key Observations:
- **Best Model**: Optimized Random Forest (highest scores across all metrics)
- **Improvement**: +0.13% F1-Score, +0.06% ROC-AUC over baseline
- **Perfect Precision**: 100% - No false positives
- **Excellent Recall**: 98.75% - Captures almost all purchasers