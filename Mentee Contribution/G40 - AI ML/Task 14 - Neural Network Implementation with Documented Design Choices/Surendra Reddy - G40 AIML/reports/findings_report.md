$content = @(
"# Findings Report - Neural Network Implementation with Documented Design Choices",
"",
"## Dataset",
"Kaggle Casting Product Image Data for Quality Inspection. 6,633 training images (2,875 ok_front / 3,758 def_front), 80/20 train/validation split; 715 held-out test images.",
"",
"## Architecture",
"3-block CNN (32 -> 64 -> 128 filters) with global average pooling, dropout, and a sigmoid output. Each design choice is documented inline in the notebook.",
"",
"## Original Design Results (dropout = 0.40)",
"Test accuracy: 95.7 percent. Precision (Defective): 97.7 percent. Recall (Defective): 95.4 percent.",
"",
"## Bonus Experiment (dropout = 0.20)",
"Changed only the dropout rate from 0.40 to 0.20. Test accuracy improved to 98.3 percent, precision to 100 percent, recall to 97.6 percent, with false negatives dropping from 21 to 11 out of 453 defective test images.",
"",
"## Conclusion",
"The CNN reliably classifies casting products as defective or non-defective. Lowering dropout to 0.20 improved every metric, suggesting the original 0.40 rate over-regularized the model for this dataset size. See the notebook for the full Design Decision Table and per-choice reasoning."
)
Set-Content -Encoding utf8 -Path reports\findings_report.md -Value $content