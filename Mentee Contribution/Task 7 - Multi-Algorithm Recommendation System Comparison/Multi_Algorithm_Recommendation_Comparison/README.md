# Multi-Algorithm Recommendation System Comparison

## Contents
- `main.ipynb` — Main Colab/Jupyter notebook implementing and comparing 5 algorithms:
  Popularity-Based, User-Based CF, Item-Based CF, SVD (Matrix Factorization), and
  Content-Based Filtering, evaluated with Precision@K, Recall@K, F1@K, RMSE, and
  catalog coverage.
- `ecommerce_dataset.csv` — Same e-commerce interaction dataset used for a fair,
  apples-to-apples comparison across algorithms.

## How to Run
1. Open `main.ipynb` in Google Colab (File > Upload notebook) or Jupyter.
2. Upload `ecommerce_dataset.csv` to the same Colab session (or place it in the same
   folder if running locally).
3. Run all cells top to bottom (Runtime > Run all).

## Dataset Columns
| Column | Description |
|---|---|
| user_id | Unique customer identifier |
| product_id | Unique product identifier |
| product_name | Product name |
| category | Product category |
| price | Product price ($) |
| rating | Rating given by user (1-5) |
| quantity | Quantity purchased/interacted with |
| purchased | 1 if the interaction resulted in a purchase, else 0 |
| timestamp | Date of interaction |
