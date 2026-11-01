# Task 16 - Getting Started with Transformers

This repository contains a simple project to demonstrate the usage of Hugging Face Transformers for sentiment analysis, specifically following the concepts outlined in introductory machine learning tasks.

## Project Structure

- `data/sample_texts.csv`: Contains a list of sample text statements for sentiment analysis.
- `notebooks/transformers_demo.ipynb`: A simple Jupyter notebook demonstrating the `pipeline` API.
- `src/sentiment_analysis.py`: A Python script that reads the sample texts, runs the Hugging Face sentiment analysis pipeline, and outputs the results.
- `results/sentiment_results.csv`: Contains the output of the sentiment analysis script, with labels and confidence scores.
- `requirements.txt`: Python dependencies required to run the project.

## How to Run

1. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the sentiment analysis script:**
   Navigate to the root directory of this project and execute:
   ```bash
   python src/sentiment_analysis.py
   ```

3. **Check the results:**
   The analyzed sentiments will be saved in `results/sentiment_results.csv`.

## Using the Notebook

You can also explore the notebook `notebooks/transformers_demo.ipynb` for an interactive demonstration of how the `transformers` library handles sentiment classification.
