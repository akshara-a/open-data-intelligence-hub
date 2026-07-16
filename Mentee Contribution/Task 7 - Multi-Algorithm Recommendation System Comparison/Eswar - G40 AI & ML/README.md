# Multi-Algorithm Recommendation System Comparison

## Project Overview

This project implements multiple machine learning algorithms to build an e-commerce recommendation system that scores and ranks products for customers, and compares how well each algorithm performs.

## Dataset

`ecommerce_customer_data.csv` — 3,900 rows, one row per customer, with the following relevant columns:

| Column | Description |
|---|---|
| `Customer ID` | Unique identifier for each customer |
| `Age`, `Gender`, `Location` | Customer demographics |
| `Item Purchased`, `Category` | The product bought and its category |
| `Purchase Amount (USD)` | Price paid |
| `Season`, `Size`, `Color` | Transaction details |
| `Review Rating` | Rating given by the customer (2.5–5.0) |
| `Subscription Status`, `Previous Purchases`, `Frequency of Purchases`, `Payment Method` | Customer behavior/profile fields |

**Important data characteristic:** each customer appears **exactly once** — there's no repeat-purchase history per user. This rules out classic user-based/item-based collaborative filtering (which needs multiple shared ratings per user), so the four algorithms below are adapted to work with single-interaction data.

## Algorithms Implemented

1. **Popularity-Based Recommender** — ranks items by a weighted average review rating (Bayesian-style shrinkage so items with few purchases don't dominate).
2. **Content-Based Recommender (Demographic Category Affinity)** — learns which product categories each (gender, age-group) segment tends to favor, and scores items accordingly.
3. **KNN Demographic-Based Collaborative Filtering** — finds the 15 nearest customers by profile similarity (age, location, season, subscription status, purchase frequency, payment method) and recommends what those similar customers bought.
4. **Regression-Based Rating Prediction (Random Forest)** — predicts a customer's likely review rating for an item from their profile + item category; used as the recommendation score.

## Evaluation

Since each customer has only one true purchase, standard Precision/Recall isn't directly applicable. Instead, this project uses **Hit Rate@5 with leave-one-out negative sampling**, a standard recommender-systems technique:

- For each test customer, mix their actual purchased item with 9 random items they didn't buy (10 candidates total).
- Ask each algorithm to rank all 10.
- Check whether the real item lands in the top 5.
- A purely random ranker scores **0.50** on this metric — results are read relative to that baseline.

The Regression-Based model is also evaluated with RMSE on its predicted rating vs. the actual rating for real purchases.

## Results Summary

| Algorithm | Hit Rate@5 | Notes |
|---|---|---|
| Content-Based (Demographic Affinity) | 0.512 | Best of the four, but only marginally above chance |
| Popularity-Based | 0.505 | Essentially at the random baseline |
| KNN Demographic CF | 0.491 | Slightly below baseline |
| Regression-Based (Random Forest) | 0.477 | Slightly below baseline; RMSE = 0.74 on real ratings |

**Honest finding:** all four algorithms land close to the 0.50 random baseline. This isn't a bug — it reflects that this dataset has a single purchase per customer and limited correlation between demographics and what's purchased/rated, leaving little personalization signal for any algorithm to exploit. See the full discussion in `multi_algo_recommendation.ipynb` and the Word report.

## How to Run

1. Open `multi_algo_recommendation.ipynb` in Google Colab or Jupyter.
2. Make sure `ecommerce_customer_data.csv` is uploaded to the same directory (or Colab's file panel).
3. Run all cells in order.

## Files in This Submission

- `ecommerce_customer_data.csv` — dataset (already provided from a previous task)
- `multi_algo_recommendation.ipynb` — notebook with all four algorithms, evaluation, and visualizations
- `Multi-Algorithm_Recommendation_System_Comparison_Report.docx` — written comparison report
- `README.md` — this file
