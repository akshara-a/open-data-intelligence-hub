$content = @'
# Findings Report - Ensemble CNN Classifier with Performance Benchmarks

## Dataset
CIFAR-10 (10 classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck), 32x32 RGB images. 42,500 training images, 7,500 validation images, 10,000 held-out test images, using a fixed 70/15/15 split shared across all three CNNs and the ensemble for fair comparison.

## Architectures
Three diverse CNNs: a baseline (2 conv+pool blocks, Dense), a regularized model (BatchNorm + Dropout after each conv block), and a deeper model (4 conv layers, BatchNorm, GlobalAveragePooling instead of Flatten). Each design choice documented inline in the notebook.

## Individual CNN Results
| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| CNN Baseline | 70.38% | 70.42% | 70.38% | 70.29% |
| CNN Regularized | 72.62% | 72.72% | 72.62% | 72.26% |
| CNN Deep | 79.61% | 80.30% | 79.61% | 79.45% |

## Ensemble Results
| Strategy | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Majority Voting | 78.81% | 78.88% | 78.81% | 78.72% |
| Soft Voting | 81.22% | 81.43% | 81.22% | 81.04% |
| Weighted Soft Voting | 81.56% | 81.79% | 81.56% | 81.38% |

Weighted voting weights derived from validation accuracy only, never from the test set.

## Production Benchmark
| Model | Avg Latency (ms) | Throughput (img/s) | Size (MB) | Parameters | Memory (MB) |
|---|---|---|---|---|---|
| CNN Baseline | 74.59 | 936.00 | 3.65 | 315,722 | -9.15 |
| CNN Regularized | 88.88 | 987.35 | 6.30 | 545,482 | 1.66 |
| CNN Deep | 72.85 | 907.73 | 1.88 | 158,122 | 1.67 |
| Ensemble (Sequential) | 222.28 | 283.26 | 11.82 | 1,019,326 | 1.30 |

## Robustness Testing
CNN Deep vs Ensemble Soft Voting under image perturbations (300-sample subset):

| Condition | CNN Deep | Ensemble (Soft) |
|---|---|---|
| Original | 81.0% | 84.0% |
| Rotated | 58.5% | 66.0% |
| Blurred | 31.0% | 37.0% |
| Noisy | 45.5% | 57.5% |
| Dark | 68.0% | 68.5% |
| Bright | 73.5% | 78.0% |
| Cropped | 55.5% | 47.5% |

The ensemble improved over CNN Deep on original, rotated, blurred, noisy, dark, and bright images, but performed worse on cropped images.

## Production Trade-off
Best individual CNN (CNN Deep) vs best ensemble (Weighted Soft Voting):
- Accuracy: +1.95 percentage points (79.61% -> 81.56%)
- Latency: +149.4 ms (72.85 ms -> 222.28 ms)
- Throughput: -624.5 img/sec (907.7 -> 283.3)
- Model size: 1.88 MB -> 11.82 MB (~6.3x)
- Parameters: 158,122 -> 1,019,326 (~6.4x)

## Final Recommendation
CNN Deep achieved 79.61% test accuracy with 72.85 ms latency and roughly 908 img/sec throughput, using only 1.88 MB and 158K parameters. The Weighted Soft Voting ensemble reached 81.56% accuracy but cost 222.28 ms latency, dropped throughput to 283 img/sec, and required about 6x the storage and parameters. The ensemble was also more robust to noise, blur, and rotation. Recommended: deploy the ensemble for offline or batch use cases (dataset labeling, quality-control pipelines) where accuracy and robustness matter more than speed. For real-time applications with latency budgets under roughly 100 ms, deploy CNN Deep alone.

## Required Questions

**Q1: What is an ensemble?**
An ensemble combines predictions from multiple machine learning models into one final prediction instead of relying on a single model, similar to asking several experts for their opinion before deciding.

**Q2: Why is this system called an Ensemble CNN Classifier?**
Each member model (CNN Baseline, CNN Regularized, CNN Deep) is itself a CNN doing image classification. The ensemble layer only combines their outputs; it is not itself a CNN.

**Q3: Why might three CNN models perform better together than one?**
Each architecture learns slightly different patterns from the same data. The baseline learns raw features quickly but overfits, the regularized model generalizes more cautiously, and the deep model with GlobalAveragePooling captures more complex spatial features. Combined, the strongest predictions dominate and individual errors get outvoted.

**Q4: Why should the CNN models be different from each other?**
Identical models trained identically tend to make the same mistakes, so combining them adds nothing. Diversity in depth, regularization, and pooling means the models err on different images, which lets the ensemble correct individual mistakes.

**Q5: What is the difference between Majority Voting and Soft Voting?**
Majority (hard) voting counts each model's top predicted class and takes the most common one. Soft voting averages the full probability distributions, so a model's confidence, not just its top pick, influences the final result. Soft voting (81.22%) clearly outperformed majority voting (78.81%) here.

**Q6: Which ensemble strategy produced the highest accuracy?**
Weighted Soft Voting, at 81.56%, followed by Soft Voting at 81.22% and Majority Voting at 78.81%.

**Q7: Did the ensemble outperform every individual CNN?**
Yes. Weighted Soft Voting (81.56%) beat the best individual model, CNN Deep (79.61%), by 1.95 percentage points.

**Q8: What was the accuracy difference between the best CNN and the ensemble?**
1.95 percentage points (79.61% to 81.56%).

**Q9: What happened to inference latency after introducing the ensemble?**
Latency rose from 72.85 ms (CNN Deep alone) to 222.28 ms (sequential ensemble), an increase of about 149.4 ms, since all three models run one after another.

**Q10: What happened to throughput?**
Throughput dropped from 907.73 img/sec (CNN Deep) to 283.26 img/sec (ensemble), a loss of about 624.5 img/sec.

**Q11: Was the ensemble more robust against noisy or modified images?**
Mostly yes. The ensemble improved over CNN Deep on original (+3%), rotated (+7.5%), blurred (+6%), noisy (+12%), dark (+0.5%), and bright (+4.5%) images. It performed worse only on cropped images (-8%), where CNN Deep alone was stronger.

**Q12: Would you deploy the ensemble in production? Explain using your benchmark evidence.**
CNN Deep achieved 79.61% test accuracy with 72.85 ms latency and roughly 908 img/sec throughput, using only 1.88 MB and 158K parameters. The Weighted Soft Voting ensemble reached 81.56% accuracy but cost 222.28 ms latency, dropped throughput to 283 img/sec, and required about 6x the storage and parameters. The ensemble was also meaningfully more robust to noise, blur, and rotation. Recommendation: deploy the ensemble for offline batch use cases where accuracy and robustness matter more than speed; deploy CNN Deep alone for real-time applications with strict latency requirements.
'@
Set-Content -Encoding utf8 -Path findings_report.md -Value $content