Production-Grade Ensemble CNN Classifier
An image classification system that trains three different CNN architectures on the CIFAR-10 dataset, combines their predictions using multiple ensemble voting strategies, and evaluates whether the ensemble is worth deploying in production compared with the best individual CNN.

The project compares model accuracy, precision, recall, F1-score, robustness, inference latency, throughput, model size, parameters, and memory usage to make a practical production deployment decision.

Setup
Install the required Python libraries:

pip install -r requirements.txt
Execution Order
Run each script from inside the src/ directory:

cd src

python data_loader.py         # Download data and visualize samples
python train.py               # Train and save all three CNN models
python evaluate.py            # Evaluate individual CNNs
python ensemble.py            # Run majority, soft and weighted-soft voting
python benchmark.py           # Measure latency, throughput, size and memory
python robustness_test.py     # Test accuracy under image distortions
python predict.py             # Example production inference
All generated plots, CSV files, confusion matrices, training histories, and benchmark results are saved in:

results/
Project Structure
ensemble-cnn-classifier/
│
│
├── notebooks/
|── src/
├── models/
├── results/
└── README.md
1. Project Overview
The project trains three different CNN architectures on CIFAR-10:

CNN Baseline
CNN Regularized
CNN Deep
Their individual performance is compared with three ensemble strategies:

Majority Voting
Soft Voting
Weighted Soft Voting
The project also evaluates the models under image distortions and benchmarks their production performance in terms of latency, throughput, model size, parameters, and memory usage.

The goal is not only to find the most accurate model, but also to determine whether the additional computational cost of an ensemble is justified.

2. What Is a CNN?
A Convolutional Neural Network (CNN) is a neural network architecture designed for image-related tasks.

CNNs learn hierarchical visual features through convolutional layers. Early layers learn simple features such as edges and textures, while deeper layers learn more complex shapes, patterns, and object-level features.

3. What Is Ensemble Learning?
Ensemble learning combines predictions from multiple machine learning models to produce a final prediction instead of relying on a single model.

In this project, three different CNN models are combined to improve prediction performance and robustness.

4. Why Use an Ensemble?
Different CNN architectures can learn different representations and make different classification errors.

Combining their predictions can:

Reduce the impact of individual model errors
Improve prediction stability
Increase overall accuracy
Improve robustness to certain image distortions
The ensemble is useful when the individual models are sufficiently diverse.

5. Dataset Description
The project uses the CIFAR-10 dataset.

CIFAR-10 contains 10 classes of color images:

Airplane
Automobile
Bird
Cat
Deer
Dog
Frog
Horse
Ship
Truck
Each image has a resolution of 32 × 32 pixels with three color channels.

The same dataset split is used across all three CNNs to ensure a fair comparison.

6. Data Preprocessing
The image pixels are normalized to the range:

[0, 1]
A fixed dataset split is used:

70% Training
15% Validation
15% Testing
The same split is shared across all three CNN models so that their performance can be compared fairly.

7. Data Augmentation
Data augmentation is applied only to the training data.

The augmentation techniques include:

Random horizontal flipping
Random rotation
Random zoom
Random translation
Random brightness adjustment
Random contrast adjustment
The purpose of augmentation is to increase the variety of training examples and improve the model's ability to generalize to unseen images.

8. CNN Baseline
The baseline CNN uses a relatively simple convolutional and pooling architecture.

It provides a reference point for comparing the performance of the more advanced CNN architectures.

9. CNN Regularized
The regularized CNN introduces additional regularization techniques, including:

Batch Normalization
Dropout
These techniques are intended to improve generalization and reduce overfitting.

10. CNN Deep
The deep CNN uses additional convolutional layers to learn more complex visual representations.

It also uses Global Average Pooling before the final classification layer.

Among the three individual CNN models, this architecture achieved the highest test accuracy.

11. Training Configuration
The CNN models are trained using:

Configuration	Value
Optimizer	Adam
Learning Rate	0.001
Batch Size	32
Maximum Epochs	30
Loss Function	Categorical Cross-Entropy
Early Stopping	Patience = 5
Model Checkpointing	Best validation accuracy
Early stopping monitors validation loss and restores the best-performing weights.

Model checkpointing saves the model with the best validation accuracy.

12. Individual CNN Results
The individual CNN models achieved the following test results:

Model	Accuracy	Precision	Recall	F1-Score
CNN Baseline	69.79%	70.31%	69.79%	69.73%
CNN Regularized	71.20%	72.02%	71.20%	71.07%
CNN Deep	80.21%	80.31%	80.21%	80.02%
The CNN Deep model was the best individual CNN, achieving 80.21% test accuracy.

13. Ensemble Results
Three ensemble strategies were evaluated:

Majority Voting
Soft Voting
Weighted Soft Voting
The results were:

Model / Strategy	Accuracy	Precision	Recall	F1-Score
CNN Baseline	69.79%	70.31%	69.79%	69.73%
CNN Regularized	71.20%	72.02%	71.20%	71.07%
CNN Deep	80.21%	80.31%	80.21%	80.02%
Majority Voting	78.31%	78.53%	78.31%	78.30%
Soft Voting	81.27%	81.16%	81.27%	81.09%
Weighted Soft Voting	81.58%	81.44%	81.58%	81.39%
Best Ensemble Strategy
Weighted Soft Voting achieved the highest accuracy of 81.58%.

The weights used for weighted voting were derived from validation accuracy only, without using test-set information.

14. Ensemble Accuracy Improvement
The best individual model was CNN Deep, with an accuracy of:

80.21%

The best ensemble was Weighted Soft Voting, with an accuracy of:

81.58%

Therefore, the ensemble improved accuracy by:

1.37 percentage points

This shows that the ensemble provided a measurable accuracy improvement over the best individual CNN.

15. Voting Strategies
Majority Voting
Each CNN produces a class prediction. The final class is selected based on the majority of the three model predictions.

Soft Voting
The probability distributions from the three CNNs are averaged, and the class with the highest average probability is selected.

Soft voting considers model confidence rather than only the final class prediction.

Weighted Soft Voting
Weighted soft voting combines the probability distributions while assigning each CNN a weight based on its validation accuracy.

This strategy achieved the highest test accuracy of 81.58%.

16. Robustness Testing
The models were evaluated on several modified versions of the test images:

Original
Rotated
Blurred
Noisy
Dark
Bright
Cropped
The results were:

Condition	CNN Baseline	CNN Regularized	CNN Deep	Ensemble Soft
Original	69.5%	75.0%	82.5%	85.0%
Rotated	55.5%	57.0%	62.5%	69.5%
Blurred	44.0%	36.0%	38.0%	44.5%
Noisy	59.5%	48.0%	51.0%	59.0%
Dark	42.5%	44.5%	76.5%	67.5%
Bright	61.0%	63.0%	75.5%	75.5%
Cropped	38.5%	35.5%	58.0%	51.0%
Robustness Analysis
The Soft Voting ensemble performed better than CNN Deep under several distortions:

Rotated: +7.0 percentage points
Blurred: +6.5 percentage points
Noisy: +8.0 percentage points
Original: +2.5 percentage points
However, CNN Deep performed better under some conditions:

Dark: CNN Deep was 9.0 percentage points better
Cropped: CNN Deep was 7.0 percentage points better
Bright: Both achieved 75.5%
Therefore, the ensemble improves robustness for several types of image distortion, but it is not universally better under every condition.

17. Production Benchmark Results
The models were benchmarked for inference performance.

Metric	CNN Baseline	CNN Regularized	CNN Deep	Ensemble Sequential
Average Latency	~114.62 ms	~94.55 ms	~79.99 ms	~277.30 ms
Minimum Latency	~66.44 ms	~64.64 ms	~65.58 ms	~209.59 ms
Maximum Latency	~428.45 ms	~264.55 ms	~126.23 ms	~817.94 ms
Throughput	~420.27 img/sec	~417.94 img/sec	~396.06 img/sec	~80.54 img/sec
Model Size	~3.65 MB	~6.30 MB	~1.88 MB	~11.83 MB
Parameters	315,722	545,482	158,122	1,019,326
Memory Usage	~-69.52 MB	~-13.52 MB	~4.37 MB	~23.50 MB
The benchmark shows that CNN Deep provides the best balance among the individual CNNs, with approximately 80 ms latency, 396 images/sec throughput, and a model size of approximately 1.88 MB.

The sequential ensemble requires significantly more computation because all three CNNs must perform inference.

18. Production Trade-Off Analysis
The best individual CNN and the best ensemble can be compared as follows:

Metric	CNN Deep	Weighted Soft Voting Ensemble	Difference
Accuracy	80.21%	81.58%	+1.37 percentage points
Latency	~80 ms	~277 ms	+197 ms
Throughput	~396 img/sec	~80 img/sec	-316 img/sec
Memory	~4.4 MB	~23.5 MB	+19.1 MB
Model Size	~1.88 MB	~11.83 MB	+9.95 MB
Parameters	158,122	1,019,326	+861,204
The ensemble provides a 1.37 percentage-point accuracy improvement, but this comes with a substantial increase in computational cost.

The ensemble:

Increases inference latency by approximately 197 ms
Reduces throughput by approximately 316 images/sec
Increases memory usage by approximately 19.1 MB
Increases model size by approximately 9.95 MB
Uses approximately 861,204 additional parameters
19. Model Disagreement Analysis
The three CNN models produce diverse predictions, which is useful for ensemble learning.

When the models agree with high confidence, the prediction can be considered more reliable.

Model disagreement is more likely to occur with:

Visually ambiguous images
Unusual lighting
Occlusions
Classes with visually similar features
The diversity between the CNN models helps explain why combining their predictions can improve overall performance.

20. Production Prediction Pipeline
The project also includes a production-style prediction function.

The ensemble uses Soft Voting to generate the final prediction and confidence score.

A confidence threshold of:

0.80
is used for the final decision.

The prediction pipeline returns:

Predicted class
Confidence score
Inference time
Final decision
The decision is:

Accept when confidence is at least 0.80
Manual Review when confidence is below 0.80
This provides a simple mechanism for sending uncertain predictions for additional review.

21. Final Recommendation
Offline / Batch Processing
For offline or batch processing where accuracy and robustness are more important than inference speed, the Weighted Soft Voting ensemble is recommended.

It achieved:

81.58% accuracy

compared with:

80.21% for CNN Deep

The ensemble also demonstrated improved robustness on rotated, blurred, and noisy images.

The additional 1.37 percentage-point accuracy improvement can justify the increased computational cost in applications where processing speed is not the primary constraint.

Real-Time Applications
For latency-sensitive real-time applications, CNN Deep is recommended.

CNN Deep provides:

80.21% accuracy
Approximately 80 ms average latency
Approximately 396 images/sec throughput
Approximately 1.88 MB model size
Approximately 158,122 parameters
Lower memory requirements than the ensemble
Therefore, CNN Deep provides a better accuracy-speed-resource trade-off for real-time inference.

22. Final Conclusion
The project demonstrates that ensemble learning can improve image classification performance by combining predictions from multiple CNN architectures.

The CNN Deep model was the strongest individual model, achieving 80.21% test accuracy.

The Weighted Soft Voting ensemble achieved the highest overall accuracy of 81.58%, providing a 1.37 percentage-point improvement over CNN Deep.

However, the accuracy improvement comes with increased production cost. The sequential ensemble increased latency from approximately 80 ms to 277 ms, reduced throughput from approximately 396 to 80 images/sec, and increased memory usage from approximately 4.4 MB to 23.5 MB.

Robustness testing showed that the ensemble was particularly effective against rotated, blurred, and noisy images, while CNN Deep performed better under dark and cropped conditions.

Overall:

Weighted Soft Voting Ensemble → Best choice for offline/batch processing where accuracy and robustness are prioritized.
CNN Deep → Best choice for real-time applications where latency, throughput, and resource efficiency are important.
The project therefore demonstrates that the best production model is not necessarily the model with the highest accuracy alone; deployment decisions should also consider latency, throughput, memory, model size, robustness, and application requirements.