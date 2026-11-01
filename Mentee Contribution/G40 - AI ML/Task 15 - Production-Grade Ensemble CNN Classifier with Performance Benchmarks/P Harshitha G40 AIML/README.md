# Production-Grade Ensemble CNN Classifier with Performance Benchmarks

## 1. Project Overview

This project implements a production-oriented image classification system using three different Convolutional Neural Network (CNN) models and an ensemble prediction strategy.

The project focuses on:

- Training multiple CNN architectures
- Comparing individual CNN performance
- Combining predictions using ensemble methods
- Evaluating accuracy, precision, recall and F1-score
- Measuring inference latency and throughput
- Comparing model size, parameter count and memory usage
- Testing robustness under image perturbations
- Determining whether ensemble inference provides enough benefit to justify its additional production cost

The models used are:

1. **CNN 1 – Baseline CNN**
2. **CNN 2 – Regularized CNN**
3. **CNN 3 – Deep CNN**

Ensemble methods implemented:

- Majority / Hard Voting
- Soft Voting
- Weighted Soft Voting

---

## 2. Project Objective

The main objective is to determine whether combining multiple CNN models produces a better production solution than deploying the best individual CNN.

The project evaluates:

- Classification performance
- Ensemble performance
- Robustness
- Inference latency
- Throughput
- Memory consumption
- Model size
- Number of parameters
- Production trade-offs

---

## 3. Project Structure

```text
Task 15 - Ensemble CNN Classifier/
│
├── data/
│
├── models/
│   ├── cnn_baseline.keras
│   ├── cnn_regularized.keras
│   └── cnn_deep.keras
│
├── notebooks/
│
├── results/
│   ├── training_history_cnn1.png
│   ├── training_history_cnn2.png
│   ├── training_history_cnn3.png
│   ├── confusion_matrix_cnn1.png
│   ├── confusion_matrix_cnn2.png
│   ├── confusion_matrix_cnn3.png
│   ├── confusion_matrix_ensemble.png
│   ├── benchmark_results.csv
│   └── robustness_results.csv
│
├── src/
│   ├── augmentation.py
│   ├── benchmark.py
│   ├── data_loader.py
│   ├── ensemble.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── robustness_test.py
│   ├── train.py
│   └── models/
│
├── README.md
└── requirements.txt

4. CNN Models
CNN 1 – Baseline CNN
The baseline model provides a simple reference architecture.
Best validation accuracy:
68.63%
Test accuracy:
68.48%

CNN 2 – Regularized CNN
The second model uses regularization techniques to improve generalization and reduce overfitting.
Best validation accuracy:
73.58%
Test accuracy:
72.42%

CNN 3 – Deep CNN
The third model uses a deeper architecture to learn more complex image features.
Best validation accuracy:
79.77%

Test accuracy:
79.53%
CNN 3 achieved the best individual classification performance.

5. Training Results
The three CNN models were trained successfully.
Model	Best Validation Accuracy
CNN 1 – Baseline	68.63%
CNN 2 – Regularized	73.58%
CNN 3 – Deep	79.77%
CNN 3 achieved the highest validation accuracy.
The training process also used early stopping for CNN 1 when validation performance stopped improving.
Training curves were saved in the results/ directory.

6. Individual Model Evaluation
Each trained CNN was evaluated independently on the test dataset.
Metric	CNN 1	CNN 2	CNN 3
Accuracy	68.48%	72.42%	79.53%
Precision	69.33%	72.46%	79.54%
Recall	68.45%	72.43%	79.53%
F1-Score	68.29%	72.05%	79.38%
Loss	0.9344	0.7778	0.6061
Best Individual Model
CNN 3 is the strongest individual model based on all major evaluation metrics.
It achieved:
Accuracy: 79.53%
Precision: 79.54%
Recall: 79.53%
F1-score: 79.38%
Loss: 0.6061
Confusion matrices were generated for all three CNN models.

7. Ensemble Methods
Three ensemble strategies were implemented.
7.1 Majority / Hard Voting
Each CNN produces one predicted class.
The class receiving the majority of votes becomes the final prediction.
7.2 Soft Voting
The prediction probabilities from all three CNNs are averaged.
The class with the highest average probability becomes the final prediction.
7.3 Weighted Soft Voting
The prediction probabilities are combined using weights based on validation accuracy.
Validation accuracies:
CNN 1 = 68.63%
CNN 2 = 73.58%
CNN 3 = 79.77%
Calculated weights:
CNN 1 = 0.3092
CNN 2 = 0.3315
CNN 3 = 0.3593
CNN 3 receives the highest weight because it achieved the highest validation accuracy.

8. Ensemble Performance
The ensemble methods produced the following test results.
Method	Accuracy	Precision	Recall	F1-Score
CNN 1	68.48%	69.33%	68.45%	68.29%
CNN 2	72.42%	72.46%	72.43%	72.05%
CNN 3	79.53%	79.54%	79.53%	79.38%
Majority Voting	76.40%	76.41%	76.41%	76.23%
Soft Voting	78.67%	78.54%	78.65%	78.39%
Weighted Soft Voting	79.12%	78.95%	79.11%	78.85%
9. Ensemble vs Best Individual CNN
The best individual model was CNN 3 with:
Accuracy = 79.53%
The best ensemble method was Weighted Soft Voting:
Accuracy = 79.12%
Therefore:
CNN 3                  = 79.53%
Weighted Soft Voting   = 79.12%
Difference             = -0.41 percentage points

# Conclusion
The ensemble did not improve overall test accuracy over CNN 3 in this experiment.
Although ensemble learning can improve robustness in certain situations, the additional inference cost does not provide enough accuracy improvement here to justify replacing CNN 3 for a general production deployment.

10. Production Benchmarking
Production benchmarking was performed on the CPU device.
Model	Parameters	Model Size (MB)	Avg Latency (ms)	Throughput (img/s)	Est. Memory (MB)
CNN 1 – Baseline	545,098	2.08	0.506	1960.0	87.1
CNN 2 – Regularized	2,194,186	8.38	0.673	1486.0	124.5
CNN 3 – Deep	305,514	1.18	1.570	637.1	174.3
Soft-Voting Ensemble	3,044,798	11.65	2.504	398.2	248.9
Benchmark results are stored in:
results/benchmark_results.csv
Benchmark observations
CNN 1
CNN 1 provides the fastest inference:
Average latency: 0.506 ms
Throughput: 1960 img/s
Memory: 87.1 MB
It is the strongest choice when low latency and high throughput are the primary requirements.

CNN 2
CNN 2 has:
2,194,186 parameters
8.38 MB model size
0.673 ms average latency
1486 img/s throughput
124.5 MB estimated memory
It provides better accuracy than CNN 1 but has a larger model.

CNN 3
CNN 3 provides the best classification accuracy:
Accuracy: 79.53%
Model size: 1.18 MB
Parameters: 305,514
Average latency: 1.570 ms
Throughput: 637.1 img/s
Estimated memory: 174.3 MB
CNN 3 provides the best accuracy among the three individual models.
Soft-Voting Ensemble
The ensemble has the highest computational cost:
3,044,798 parameters
11.65 MB model size
2.504 ms average latency
398.2 img/s throughput
248.9 MB estimated memory
The ensemble therefore has significantly higher resource requirements than deploying one CNN.

11. Robustness Testing
The models were tested under several image perturbations:
Original images
Rotation
Gaussian blur
Gaussian noise
Darkening
Brightening
Cropping and resizing

Results:
Perturbation	CNN 1	CNN 2	CNN 3	Ensemble
Original	70.02%	74.51%	79.49%	79.79%
Rotated (+30°)	48.54%	54.10%	59.96%	58.89%
Blurred (Gaussian)	39.26%	41.70%	20.51%	39.55%
Noisy (Gaussian)	45.21%	41.50%	47.95%	47.07%
Darkened (0.5x)	56.54%	64.65%	74.32%	71.48%
Brightened (1.5x)	66.89%	70.70%	75.10%	76.07%
Cropped & Resized	48.83%	59.77%	54.79%	60.45%
Robustness results are stored in:
results/robustness_results.csv

12. Robustness Analysis
The robustness experiment shows that ensemble learning does not improve performance under every type of perturbation.
Strong ensemble cases
The ensemble performed well for:
Original images: 79.79%
Brightened images: 76.07%
Cropped and resized images: 60.45%
CNN 3 strengths
CNN 3 achieved the highest individual accuracy for:
Rotation: 59.96%
Gaussian noise: 47.95%
Darkening: 74.32%
Brightening: 75.10%
Gaussian blur
Gaussian blur was particularly difficult for CNN 3:
CNN 1 = 39.26%
CNN 2 = 41.70%
CNN 3 = 20.51%
Ensemble = 39.55%
CNN 2 performed best under this perturbation.
Overall observation
The results demonstrate that ensemble methods can provide useful robustness for some input conditions, but they do not consistently outperform the strongest individual CNN.

13. Production Recommendation
Based on the complete evaluation, CNN 3 is recommended as the primary production model when classification accuracy is the most important requirement.
Recommended model: CNN 3 – Deep CNN
Reasons:
Highest test accuracy: 79.53%
Highest precision: 79.54%
Highest recall: 79.53%
Highest F1-score: 79.38%
Lowest test loss: 0.6061
Smallest model size: 1.18 MB
Although CNN 3 has higher latency than CNN 1, it provides substantially better classification performance.

14. When to Use the Ensemble
The ensemble can be considered when robustness or prediction diversity is more important than raw inference efficiency.
However, the current experiment shows:
Best Individual CNN:
CNN 3 = 79.53%
Best Ensemble:
Weighted Soft Voting = 79.12%
The ensemble therefore introduces additional computational cost without improving overall test accuracy.
For this experiment, deploying all three models together is not justified when the main objective is maximizing test accuracy at reasonable production cost.

15. Production Trade-Off Summary
Requirement	Recommended Option
Highest accuracy	CNN 3
Highest precision	CNN 3
Highest recall	CNN 3
Highest F1-score	CNN 3
Lowest latency	CNN 1
Highest throughput	CNN 1
Lowest memory	CNN 1
Smallest model size	CNN 3
Best overall accuracy/cost balance	CNN 3
Robustness for selected perturbations	Ensemble can help
Lowest overall inference cost	CNN 1

16. Limitations
The following limitations should be considered:
The models were benchmarked on CPU.
Ensemble inference requires running multiple CNN models.
Ensemble methods did not improve overall test accuracy over CNN 3.
Robustness varied significantly depending on the perturbation.
Gaussian blur caused a substantial performance reduction.
Production deployment on GPU or specialized hardware may produce different latency and throughput results.

17. Key Insights
CNN 3 achieved the best individual classification performance.
CNN 2 improved substantially over the baseline CNN.
Majority Voting performed worse than CNN 3.
Soft Voting performed better than Majority Voting but still did not exceed CNN 3.
Weighted Soft Voting was the strongest ensemble method but reached only 79.12%.
CNN 3 achieved 79.53%, exceeding the best ensemble by 0.41 percentage points.
CNN 1 provided the fastest inference and highest throughput.
The ensemble required substantially more memory and computation.
The ensemble improved performance for some robustness conditions, particularly brightening and cropping.
The best production choice depends on the balance between accuracy, latency and resource cost.

18. Final Conclusion
This project successfully implemented a production-oriented Ensemble CNN Classifier using three different CNN architectures.
The models were trained, independently evaluated, combined using multiple voting strategies, benchmarked for production performance and tested under image perturbations.
The final results show that:
CNN 3 Test Accuracy       = 79.53%
Weighted Ensemble Accuracy = 79.12%
Therefore, the ensemble did not outperform the best individual CNN in overall test accuracy.
Considering both classification performance and production cost, CNN 3 is the recommended model for deployment in this experiment.
The ensemble remains useful as an alternative when robustness and model diversity are more important than minimum inference cost.

19. Generated Results
The project generates the following artifacts:

results/
├── training_history_cnn1.png
├── training_history_cnn2.png
├── training_history_cnn3.png
├── confusion_matrix_cnn1.png
├── confusion_matrix_cnn2.png
├── confusion_matrix_cnn3.png
├── confusion_matrix_ensemble.png
├── benchmark_results.csv
└── robustness_results.csv

Trained models:

models/
├── cnn_baseline.keras
├── cnn_regularized.keras
└── cnn_deep.keras

20. How to Run
Install dependencies
pip install -r requirements.txt

Train the CNN models
python src/train.py

Evaluate individual CNNs
python src/evaluate.py

Run ensemble evaluation
python src/ensemble.py

Run production benchmarking
python src/benchmark.py

Run robustness testing
python src/robustness_test.py

21. Technologies Used
Python
PyTorch
Torchvision
NumPy
Pandas
Scikit-learn
Matplotlib
Seaborn
Pillow
SciPy
PSUtil

Final Status
✅ Dataset preparation
✅ CNN 1 training
✅ CNN 2 training
✅ CNN 3 training
✅ Individual model evaluation
✅ Confusion matrices
✅ Majority Voting
✅ Soft Voting
✅ Weighted Soft Voting
✅ Production benchmarking
✅ Robustness testing
✅ Production comparison
✅ Deployment recommendation

Task 15 execution completed successfully.