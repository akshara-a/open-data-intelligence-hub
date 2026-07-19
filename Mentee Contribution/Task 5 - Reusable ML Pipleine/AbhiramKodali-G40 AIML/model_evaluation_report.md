# Model Evaluation Report

## Dataset Summary

- Rows: 40
- Columns: 11
- Duplicate rows: 0
- Target column: `Churn`
- Churn distribution:

| Churn   |   count |
|:--------|--------:|
| No      |      22 |
| Yes     |      18 |

## Missing Values

|                 |   0 |
|:----------------|----:|
| CustomerID      |   0 |
| Gender          |   0 |
| Age             |   1 |
| Tenure          |   0 |
| MonthlyCharges  |   0 |
| TotalCharges    |   1 |
| ContractType    |   0 |
| PaymentMethod   |   1 |
| InternetService |   4 |
| SupportTickets  |   1 |
| Churn           |   0 |

## Train-Test Split

The project uses an 80:20 split through `test_size=0.2`.
This means 80% of the rows are used to train the model and 20% are held back for testing.
`random_state=42` makes the split repeatable, and `stratify=y` keeps the churn and non-churn ratio similar in both sets.

## Evaluation Results

- Accuracy: 1.00

## Confusion Matrix

Rows represent actual labels and columns represent predicted labels.

```text
[[4 0]
 [0 4]]
```

## Classification Report

```text
              precision    recall  f1-score   support

          No       1.00      1.00      1.00         4
         Yes       1.00      1.00      1.00         4

    accuracy                           1.00         8
   macro avg       1.00      1.00      1.00         8
weighted avg       1.00      1.00      1.00         8

```

## Business Interpretation

For churn prediction, recall for the `Yes` class is especially important because the business wants to find as many likely-to-leave customers as possible. Customers predicted as likely to churn can be prioritized for retention actions such as support follow-up, discounts, personalized plans, or renewal offers.
