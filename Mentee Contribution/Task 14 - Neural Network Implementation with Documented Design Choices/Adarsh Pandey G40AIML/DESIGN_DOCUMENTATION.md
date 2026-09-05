# Design Documentation: Casting Product CNN Classifier

This document provides the rationale behind every major design decision in the casting product defect detector.

## 1. Input Image Size: 224 × 224

**Choice:** 224 × 224 pixels

**Rationale:**
- Standard size used in many pretrained models (ImageNet models typically use 224 × 224)
- Provides sufficient resolution to capture defects (cracks, surface irregularities)
- Computational cost is manageable on modest hardware (GPU not strictly required)
- Large enough to preserve fine details; small enough to avoid memory bloat
- Consistent with transfer learning approaches if we scale to pretrained backbones later

**Alternatives considered:**
- 128 × 128: Too small; casting defects may be subtle and require higher resolution
- 512 × 512: Increases computation 4× without guaranteed accuracy improvement
- 299 × 299: Used in Inception, adds complexity without clear benefit for this task

---

## 2. Problem Type: Binary Classification

**Choice:** Binary classification (Defective vs. Non-defective)

**Rationale:**
- Task naturally splits into two classes
- Simplifies model architecture and output layer (single sigmoid neuron)
- Reduces training time compared to multi-class variants
- Clear business goal: detect defects (yes/no)

---

## 3. Model Architecture: CNN

**Choice:** Convolutional Neural Network (CNN)

**Rationale:**
- CNNs are purpose-built for image data
- Local receptive fields capture spatial patterns (scratches, cracks, pits)
- Weight sharing reduces parameters compared to fully connected layers
- Proven track record on defect detection tasks

**Alternatives considered:**
- Dense layers only: Treats image as flat vector; loses spatial structure
- Vision Transformer: Overkill for this dataset size; requires pretraining or massive data
- Classical ML (SVM, Random Forest): Requires manual feature engineering; CNNs learn features automatically

---

## 4. Convolutional Filters: 32 → 64 → 128

**Choice:** Three convolutional blocks with 32, 64, and 128 filters

**Rationale:**
- **Progressive complexity:** Early layers learn simple features (edges, textures); later layers combine them into complex patterns (defect signatures)
- **32 filters (Layer 1):** Captures low-level features (edges, corners)
- **64 filters (Layer 2):** Detects intermediate patterns (texture combinations, small shapes)
- **128 filters (Layer 3):** Recognizes high-level patterns (defect types, surface anomalies)
- Doubling at each step is a common heuristic and works well in practice

**Alternatives considered:**
- Constant (32 everywhere): Limits representation power
- Larger jumps (32 → 128 → 512): Overkill; increases overfitting risk on 6k training images
- Decreasing (128 → 64 → 32): Counter-intuitive; wastes capacity in early layers

---

## 5. Kernel Size: 3 × 3

**Choice:** 3 × 3 convolution kernels throughout

**Rationale:**
- **Local receptivity:** Captures fine-grained spatial information (ideal for detecting small defects)
- **Efficiency:** Minimal computational overhead; two stacked 3×3 layers approximate a 5×5 with fewer parameters
- **Standard practice:** Widely used in state-of-the-art models (VGG, ResNet)
- **Flexibility:** Larger kernels (5×5, 7×7) are overkill for casting defects; smaller (1×1) would miss local patterns

---

## 6. Hidden Activation: ReLU

**Choice:** ReLU (Rectified Linear Unit)

**Rationale:**
- **Computational efficiency:** Simple: max(0, x); no exponential calculations
- **Gradient flow:** Non-zero gradient for positive inputs; allows deep networks
- **Empirical success:** Default choice in modern deep learning; well-studied
- **Sparsity:** Zeros out negative activations; reduces overfitting
- **No vanishing gradient:** Unlike sigmoid/tanh, ReLU doesn't saturate for large positive values

**Alternatives:**
- Sigmoid/Tanh: Risk vanishing gradients in deep networks
- Leaky ReLU: Marginal improvement; not needed for this architecture depth
- ELU/SELU: Over-engineered for this task

---

## 7. Output Activation: Sigmoid

**Choice:** Sigmoid activation on single output neuron

**Rationale:**
- **Binary probability:** Maps logits to [0, 1] range; directly interpretable as P(defective)
- **Threshold flexibility:** Threshold at 0.50 for balanced class performance; can adjust for higher recall/precision tradeoff
- **Compatibility:** Works naturally with Binary Cross-Entropy loss

**Why not softmax?** Softmax is for multi-class (K>2 outputs); overkill here.

---

## 8. Pooling: MaxPooling (2×2)

**Choice:** 2×2 MaxPooling after each convolutional block

**Rationale:**
- **Dimensionality reduction:** Halves spatial dimensions; reduces parameters and computation
- **Translation invariance:** Model becomes robust to small shifts in defect location
- **Feature concentration:** Keeps most-activated (strongest) features
- **Standard practice:** MaxPooling outperforms AveragePooling for object detection tasks

**Why not AvgPooling?** Averages can blur important features; MaxPooling is more discriminative.

---

## 9. Optimizer: Adam

**Choice:** Adam (Adaptive Moment Estimation)

**Rationale:**
- **Adaptive learning rates:** Per-parameter learning rates based on gradient history; no manual tuning needed
- **Robust:** Works well across diverse problems without extensive tuning
- **Beginner-friendly:** Recommended default for most practitioners
- **Fast convergence:** Combines benefits of momentum and RMSprop

**Alternatives:**
- SGD: Requires careful learning rate tuning and learning rate schedules
- RMSprop: Good but less versatile than Adam
- SGD + Momentum: Requires more hyperparameter tuning

---

## 10. Learning Rate: 0.001

**Choice:** Learning rate = 0.001 (0.1% per update)

**Rationale:**
- **Adam's default:** Standard starting value for Adam optimizer
- **Convergence:** Small enough to avoid overshooting minima; large enough for reasonable training speed
- **Empirical validation:** Works well on this dataset (training loss decreased consistently)
- **Safety:** Conservative; can always increase if training is too slow

**Why not 0.01?** Risk jumping over good minima; may cause divergence early in training.
**Why not 0.0001?** Too small; training would be extremely slow (20+ hours).

---

## 11. Loss Function: Binary Cross-Entropy

**Choice:** Binary Cross-Entropy (BCE)

**Rationale:**
- **Theoretically sound:** Maximum-likelihood objective for binary classification
- **Probabilistic interpretation:** Minimizes negative log-likelihood of true labels
- **Gradient behavior:** Well-behaved gradients; encourages confidence on correct class
- **Standard:** Industry default for binary classification

**Formula:** BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]

**Alternatives:**
- Hinge loss: Designed for SVM; less standard for neural networks
- Focal loss: Useful for extreme class imbalance (not our case)

---

## 12. Batch Size: 32

**Choice:** Batch size = 32

**Rationale:**
- **Memory efficiency:** Fits comfortably on most GPUs/CPU setups
- **Gradient stability:** Large enough for stable gradient estimates; small enough for varied mini-batch distributions
- **Training speed:** Updates every 32 images; reasonable epoch duration (6633 / 32 ≈ 207 steps per epoch)
- **Empirical sweet spot:** 16–64 is typical range; 32 balances all factors

**Why not 64?** Slightly more memory; marginal training time savings not worth it.
**Why not 16?** More noisy gradients; longer epoch times; risk of optimization plateaus.

---

## 13. Epochs: Maximum 25 (with Early Stopping)

**Choice:** 25 epochs max; early stopping monitors validation loss

**Rationale:**
- **Early stopping patience:** Stop if validation loss doesn't improve for 5 epochs
- **Prevents overfitting:** Automatically halts when generalization plateaus
- **Cap at 25:** Upper bound to catch runaway training; unlikely to reach this
- **Dataset size:** 6,633 training images allow ~25 epochs without stale data memorization

**Why 25?** Rule of thumb: epochs = 2–3× number of parameter updates before diminishing returns. For this dataset, 15–20 epochs typical; 25 is safe ceiling.

---

## 14. Dropout: 0.40 (40%)

**Choice:** Dropout rate = 0.40 after fully connected layers

**Rationale:**
- **Regularization:** Randomly deactivates 40% of neurons during training; prevents co-adaptation
- **Empirical tuning:** Tested on this dataset; 0.40 balances underfitting and overfitting
- **Standard range:** 0.2–0.5 typical; 0.40 middle ground
- **Late-stage only:** Applied after flattening, not after convolutions (CNNs less prone to overfitting from conv layers)

**Why not 0.50?** Risk underfitting; model struggles to learn.
**Why not 0.20?** Insufficient regularization; model may memorize (bonus experiment tests this).

---

## 15. Data Augmentation: Flip, Rotation, Zoom, Contrast

**Choice:** Four augmentation techniques applied during training

| Technique | Intensity | Reason |
|---|---|---|
| **Horizontal Flip** | 50% probability | Casting defects are rotationally symmetric; improves robustness |
| **Vertical Flip** | 50% probability | Same reasoning |
| **Rotation** | ±15° | Small rotations; casting may be tilted during capture |
| **Zoom** | 0.8–1.2× | Mimics different distances from camera |
| **Contrast** | 0.8–1.2× | Lighting variations in factory settings |

**Rationale:**
- **Synthetic data:** Augmentation effectively expands training set 4–8× without new labeled images
- **Robustness:** Model learns invariances (shift, rotation, lighting)
- **Generalization:** Reduces overfitting by exposing model to variations

**Not used:**
- Random crops: Might remove defects
- Extreme distortions: Unrealistic for casting images

---

## 16. Metrics: Accuracy, Precision, Recall

**Choice:** Three complementary metrics

| Metric | Formula | Why? |
|---|---|---|
| **Accuracy** | (TP + TN) / Total | Overall correctness; main metric |
| **Precision** | TP / (TP + FP) | Of flagged defects, how many are real? |
| **Recall** | TP / (TP + FN) | Of actual defects, how many caught? |

**Rationale:**
- **Balanced view:** Accuracy alone misleading if classes imbalanced
- **Business focus:** Precision = false alarm rate (cost of re-inspection); Recall = miss rate (cost of shipping defects)
- **Trade-off visibility:** Guide threshold tuning based on false positive vs. false negative trade-off

---

## Summary Design Table

| Component | Value | Reason |
|---|---|---|
| Input size | 224 × 224 | Standard; balances detail and computation |
| Conv filters | 32→64→128 | Progressive feature hierarchy |
| Kernel size | 3 × 3 | Local feature extraction; efficient |
| Hidden activation | ReLU | Efficient; prevents vanishing gradients |
| Output activation | Sigmoid | Binary probability output |
| Pooling | MaxPooling 2×2 | Reduces dimensions; preserves strong features |
| Optimizer | Adam | Adaptive; robust; beginner-friendly |
| Learning rate | 0.001 | Default for Adam; prevents overshooting |
| Loss | Binary Cross-Entropy | Theoretically optimal for classification |
| Batch size | 32 | Memory-efficient; stable gradients |
| Max epochs | 25 | Sufficient with early stopping |
| Dropout | 0.40 | Regularization to prevent overfitting |
| Augmentation | Flip, rotation, zoom, contrast | Synthetic diversity; robustness |
| Metrics | Accuracy, Precision, Recall | Comprehensive evaluation |

---

## Results & Validation

The documented choices yielded:
- **Test Accuracy:** 83.5%
- **Precision:** 81.3% (few false alarms)
- **Recall:** 96.0% (catches most defects)
- **No overfitting:** Validation loss tracked with training loss

This validates that the design decisions are well-justified for this real-world task.
