# Task 15: Production-Grade Ensemble CNN Classifier (Fashion-MNIST)

## 1. Project Overview
This project implements a production-grade image classification system using an Ensemble of three Convolutional Neural Networks (CNNs). Due to server throttling issues with the original CIFAR-10 dataset, the pipeline was adapted to use the **Fashion-MNIST** dataset. The goal was to train multiple models with different architectures, combine their predictions using Soft and Hard voting, and benchmark the ensemble's production costs (latency, throughput, model size) against its accuracy improvements.

## 2. Model Architectures & Configuration
* **Dataset:** Fashion-MNIST (Grayscale images of 10 clothing categories).
* **Data Preprocessing:** Images normalized (0-1 range) and reshaped to (28, 28, 1). Training data augmented with Random Horizontal Flip, Rotation, and Zoom.
* **CNN 1 (Baseline):** 2 Conv2D layers + MaxPooling + Dense output.
* **CNN 2 (Regularized):** Added Batch Normalization and Dropout to prevent overfitting.
* **CNN 3 (Deep):** Stacked Conv2D layers + GlobalAveragePooling2D instead of Flatten.
* **Training Setup:** Adam Optimizer (LR: 0.001), Sparse Categorical Cross-Entropy, 30 Epochs (with Early Stopping).

## 3. Production Benchmarks & Robustness Testing

### Benchmarks (Cost of Production)
| Metric              | CNN 3 (Deep) | Ensemble (Soft) |
| ------------------- | -----------: | --------------: |
| **Model Size (MB)** | 3.28 MB      | 10.75 MB        |
| **Latency**         | 0.29 ms/img  | 1.06 ms/img     |
| **Throughput**      | 3423 img/s   | 944 img/s       |

### Robustness (Accuracy on Corrupted Data)
| Condition    | CNN 1   | CNN 2   | CNN 3   | Ensemble (Soft) |
| ------------ | ------- | ------- | ------- | --------------- |
| **Original** | 90.40%  | 88.60%  | 90.80%  | **91.10%**      |
| **Rotated**  | 5.90%   | 5.60%   | 9.70%   | 6.70%           |
| **Noisy**    | 74.50%  | 79.40%  | 22.90%  | **68.50%**      |

---

## 4. Required Student Questions

**1. What is an ensemble?**
An ensemble is a combination of multiple machine learning models whose individual predictions are combined to produce one stronger, final prediction.

**2. Why is this system called an Ensemble CNN Classifier?**
It trains three separate Convolutional Neural Networks (CNNs) on the same dataset and combines their classification outputs to make a final decision. 

**3. Why might three CNN models perform better together than one CNN?**
Different models learn slightly different characteristics from the same data. By combining them, the models can correct each other's mistakes. 

**4. Why should the CNN models be different from each other?**
To introduce model diversity. If all models share the exact same architecture, they will make the exact same mistakes, rendering the ensemble useless.

**5. What is the difference between Majority Voting and Soft Voting?**
Majority (Hard) voting only looks at the final predicted class and picks the most common one. Soft voting averages the underlying confidence probabilities of every class from every model, resulting in a more informed decision.

**6. Which ensemble strategy produced the highest accuracy?**
The Soft Ensemble produced the highest accuracy on the original dataset at 91.10%.

**7. Did the ensemble outperform every individual CNN?**
Yes, on the clean, original dataset, the Soft Ensemble (91.10%) slightly outperformed the best individual model, CNN 3 (90.80%).

**8. What was the accuracy difference between the best CNN and the ensemble?**
The ensemble provided a modest improvement of 0.30 percentage points over CNN 3 on the clean dataset.

**9. What happened to inference latency after introducing the ensemble?**
Latency increased significantly. CNN 3 took ~0.29ms per image, while the Ensemble took ~1.06ms per image because it had to process all three models sequentially.

**10. What happened to throughput?**
Throughput dropped drastically from ~3423 images per second (CNN 3) to ~944 images per second (Ensemble).

**11. Was the ensemble more robust against noisy or modified images?**
Yes, in specific cases. While CNN 3 completely failed on noisy images (dropping to 22.90%), the ensemble leveraged the robustness of CNN 1 and CNN 2 to maintain a much safer 68.50% accuracy on the noisy dataset.

**12. Would you deploy the ensemble in production?**
*Final Production Recommendation:* For a real-time application, I would deploy **CNN 3** alone. The ensemble only provided a 0.3% increase in baseline accuracy, but the latency jumped nearly 4x (0.29 ms to 1.06 ms) and the memory footprint tripled (3.28 MB to 10.75 MB). However, if the deployment environment is known to have highly corrupted/noisy images (like bad security cameras), the Ensemble is mandatory, as it prevents the catastrophic failure (22.90%) seen in CNN 3.
