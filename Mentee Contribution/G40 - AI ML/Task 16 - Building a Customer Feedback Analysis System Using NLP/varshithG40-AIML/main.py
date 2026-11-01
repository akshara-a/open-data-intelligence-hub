"""
Command-Line Interface (CLI) for Customer Feedback Analysis System
Supports:
- train: Train all models and save checkpoints
- evaluate: Evaluate models on test dataset with full reports and confusion matrix
- analyze: Analyze a single feedback text in real-time
- batch: Analyze an entire CSV file and export results
- compare: Compare classical TF-IDF model against Transformer (DistilBERT)
"""

import os
import sys
import argparse
import pandas as pd

from src.pipeline import CustomerFeedbackAnalyzer
from src.transformer_model import compare_tfidf_vs_transformer


def cmd_train(args):
    """Trains sentiment and multi-label category models."""
    print("=" * 60)
    print("Training Customer Feedback NLP Models...")
    print("=" * 60)
    analyzer = CustomerFeedbackAnalyzer(data_path=args.data)
    analyzer.train_and_initialize()
    print(f"\n[SUCCESS] Models trained successfully and saved to '{analyzer.models_dir}/'")
    print(f"- Sentiment Classes: {analyzer.sentiment_model.classes_}")
    print(f"- Multi-label Categories: {analyzer.category_model.classes_}")
    print(f"- Indexed feedback items: {len(analyzer.similarity_engine.corpus_df)}")


def cmd_evaluate(args):
    """Evaluates the models on test data."""
    print("=" * 60)
    print("Evaluating Customer Feedback NLP Models...")
    print("=" * 60)
    analyzer = CustomerFeedbackAnalyzer(data_path=args.data)
    analyzer.load_or_train()

    df = pd.read_csv(args.data)
    texts = df["feedback"].astype(str).tolist()
    sentiments = df["sentiment"].astype(str).tolist()
    categories = df["categories"].astype(str).tolist()

    # Evaluate Sentiment Classifier
    print("\n--- 1. Sentiment Classification Evaluation ---")
    sentiment_eval = analyzer.sentiment_model.evaluate(texts, sentiments)
    print(f"Accuracy:  {sentiment_eval['accuracy'] * 100:.2f}%")
    print(f"Precision: {sentiment_eval['precision'] * 100:.2f}%")
    print(f"Recall:    {sentiment_eval['recall'] * 100:.2f}%")
    print(f"F1 Score:  {sentiment_eval['f1_score'] * 100:.2f}%")
    print("\nConfusion Matrix (Rows: Actual, Cols: Predicted):")
    print(f"Classes: {sentiment_eval['classes']}")
    for row in sentiment_eval["confusion_matrix"]:
        print(f"  {row}")

    # Evaluate Multi-label Category Classifier
    print("\n--- 2. Multi-label Category Classification Evaluation ---")
    cat_eval = analyzer.category_model.evaluate(texts, categories)
    print(f"Micro F1 Score:      {cat_eval['micro_f1'] * 100:.2f}%")
    print(f"Macro F1 Score:      {cat_eval['macro_f1'] * 100:.2f}%")
    print(f"Micro Precision:     {cat_eval['micro_precision'] * 100:.2f}%")
    print(f"Micro Recall:        {cat_eval['micro_recall'] * 100:.2f}%")
    print(f"Hamming Loss:        {cat_eval['hamming_loss']:.4f} (lower is better)")

    print("\nTop Category Indicative Terms:")
    top_terms = analyzer.category_model.get_top_category_keywords(n_top=3)
    for cat, terms in top_terms.items():
        term_strs = [f"{t[0]} ({t[1]})" for t in terms]
        print(f"  [{cat}]: {', '.join(term_strs)}")


def cmd_analyze(args):
    """Analyzes a single feedback text input."""
    feedback_text = args.text
    analyzer = CustomerFeedbackAnalyzer(data_path=args.data)
    analyzer.load_or_train()

    res = analyzer.analyze(feedback_text, top_k_similar=args.top_k)

    print("\n" + "=" * 70)
    print("CUSTOMER FEEDBACK NLP ANALYSIS REPORT")
    print("=" * 70)
    print(f"Input Text:       \"{res['raw_text']}\"")
    print(f"Cleaned Text:     \"{res['cleaned_text']}\"")
    print(f"Lemmatized:       {res['lemmatized_tokens']}")
    print("-" * 70)
    print(f"Sentiment:        {res['sentiment'].upper()} (Confidence: {res['sentiment_confidence']*100:.1f}%)")
    print("Sentiment Scores:")
    for sent, score in res["sentiment_scores"].items():
        bar = "#" * int(score * 20)
        print(f"  - {sent.capitalize():<10}: {score*100:>5.1f}%  {bar}")

    print("-" * 70)
    print(f"Categories:       {', '.join(res['categories'])}")
    print("Category Scores (active if >= 35%):")
    for cat, score in sorted(res["category_scores"].items(), key=lambda x: x[1], reverse=True):
        marker = "[*]" if cat in res["categories"] else "[ ]"
        print(f"  {marker} {cat:<16}: {score*100:>5.1f}%")

    print("-" * 70)
    print("Important Keywords / Keyphrases:")
    for kw, score in res["keywords_with_scores"]:
        print(f"  * {kw:<24} (TF-IDF: {score:.3f})")

    print("-" * 70)
    print("Semantically Similar Past Customer Feedback:")
    if res["similar_feedback"]:
        for idx, sim in enumerate(res["similar_feedback"], 1):
            print(f"  {idx}. [{sim['similarity_percentage']}] \"{sim['feedback']}\"")
            print(f"     -> Sentiment: {sim['sentiment']}, Categories: {sim['categories']}")
    else:
        print("  No similar feedback above threshold.")
    print("=" * 70 + "\n")


def cmd_compare(args):
    """Compares classical TF-IDF model against Transformer (DistilBERT)."""
    print("=" * 75)
    print("TF-IDF + Logistic Regression vs Transformer (DistilBERT) Comparison")
    print("=" * 75)
    analyzer = CustomerFeedbackAnalyzer(data_path=args.data)
    analyzer.load_or_train()

    comparison = compare_tfidf_vs_transformer(tfidf_classifier=analyzer.sentiment_model)

    for item in comparison:
        print(f"\nFeedback: \"{item['text']}\"")
        print(f"  - TF-IDF Sentiment:      {item['tfidf_sentiment'].upper()}")
        print(f"  - Transformer Sentiment: {item['transformer_sentiment'].upper()} (conf: {item['transformer_confidence']*100:.1f}%)")
        print(f"  - Linguistic Note:       {item['key_difference']}")
    print("\n" + "=" * 75)


def main():
    parser = argparse.ArgumentParser(description="Customer Feedback NLP Analysis System CLI")
    parser.add_argument("--data", default="data/feedback.csv", help="Path to feedback dataset")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # train
    subparsers.add_parser("train", help="Train sentiment and category classifiers")

    # evaluate
    subparsers.add_parser("evaluate", help="Evaluate models on test metrics")

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Analyze single feedback string")
    p_analyze.add_argument("text", type=str, help="Customer feedback text to analyze")
    p_analyze.add_argument("--top-k", type=int, default=3, help="Number of similar feedback items to show")

    # compare
    subparsers.add_parser("compare", help="Compare TF-IDF model vs Transformer")

    args = parser.parse_args()

    if args.command == "train":
        cmd_train(args)
    elif args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "compare":
        cmd_compare(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
