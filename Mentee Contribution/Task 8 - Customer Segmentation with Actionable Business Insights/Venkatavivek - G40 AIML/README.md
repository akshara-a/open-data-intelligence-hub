# Customer Segmentation with Actionable Business Insights

## Overview

This project segments e-commerce customers using K-Means clustering and converts the resulting segments into business recommendations. It also includes regression, classification, and hyperparameter optimization.

## Project Structure

```text
customer-segmentation-project/
├── data/
│   └── customer_data.csv
├── notebooks/
│   └── customer_segmentation.ipynb
├── src/
│   ├── data_preprocessing.py
│   ├── clustering.py
│   ├── regression.py
│   ├── classification.py
│   └── model_evaluation.py
├── reports/
│   ├── customer_segments.csv
│   ├── cluster_profile.csv
│   ├── business_insights.md
│   └── visualizations/
├── README.md
└── requirements.txt
```

## Workflow

1. Understand the business problem.
2. Perform EDA.
3. Clean, encode, and scale the data.
4. Run K-Means for several values of `k`.
5. Compare Elbow and Silhouette methods.
6. Profile and name the customer segments.
7. Predict customer value with Linear/Ridge Regression.
8. Predict purchase likelihood with Logistic Regression.
9. Tune models with GridSearchCV.
10. Convert results into business recommendations.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

On Windows:

```bash
.venv\Scripts\activate
```

Then open `notebooks/customer_segmentation.ipynb`.

## Google Colab

Upload the entire repository or clone it into Colab, then open the notebook. Update `ROOT` if the repository is stored under a different path.

## Important Note

The included CSV is a small demonstration dataset so that the repository is runnable immediately. For a final academic project, replace it with a sufficiently large public or realistic dataset and document its source.
