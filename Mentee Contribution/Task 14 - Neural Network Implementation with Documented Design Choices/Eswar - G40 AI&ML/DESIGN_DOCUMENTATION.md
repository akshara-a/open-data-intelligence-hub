# Design Documentation — Binary Image Classification Using a CNN

Task 14 — Mini Project: Neural Network Implementation with Documented Design Choices

This document explains the reasoning behind every major design decision made while
building the casting-defect classifier, as required by the project brief.

---

## 1. Input Image Size

**Selected value:** `224 x 224 x 3`

**Reason:** Neural networks require a fixed input size. 224x224 keeps enough visual
detail to spot small casting defects (surface irregularities, edge damage) while
staying computationally manageable for training on a laptop or Colab session. A
larger size (e.g. 512x512) would add detail but slow training substantially for
limited extra benefit at this project's scale; a much smaller size (e.g. 64x64)
risks losing the fine detail defects actually show up in.

## 2. CNN Layers (Architecture Depth)

**Selected value:** 3 convolution + max-pooling blocks, followed by global average
pooling and two dense layers.

**Reason:** Three convolutional blocks give the network enough depth to progress from
low-level features (edges, texture) to higher-level, defect-specific patterns,
without the added training cost and overfitting risk of a much deeper network — which
isn't necessary for a binary classification task on a dataset of this size.

## 3. Number of Filters

**Selected value:** `32 -> 64 -> 128` (doubling at each block)

**Reason:** The first layer only needs a small number of filters to learn simple,
general features like edges and surface texture. Deeper layers need more filters to
represent the larger number of possible combinations of those simple features into
complex, defect-specific shapes. Doubling at each stage is a standard, proven
pattern that balances representational power against parameter count.

## 4. Activation Functions

**Selected value:** ReLU (hidden layers), Sigmoid (output layer)

**Reason (ReLU):** ReLU is simple to compute, avoids the vanishing-gradient problems
that older activations (like sigmoid or tanh) have in deep networks, and is the
standard default for CNN hidden layers.

**Reason (Sigmoid):** This is a binary classification problem, so the output layer
needs a single probability between 0 and 1 — sigmoid is the natural choice, mapping
directly to "probability the image is defective."

## 5. Pooling

**Selected value:** `MaxPooling2D()` after each convolution block; `GlobalAveragePooling2D()`
before the dense layers.

**Reason (MaxPooling):** Shrinks the feature maps after each convolution block,
which reduces computation for subsequent layers and keeps the strongest activations
— the features most likely to represent a defect — while discarding redundant detail.

**Reason (GlobalAveragePooling instead of Flatten):** Flatten would produce a very
large number of parameters going into the first dense layer, increasing overfitting
risk on a dataset this size. GlobalAveragePooling2D instead condenses each feature
map to a single average value, drastically cutting the parameter count while still
preserving what each filter detected overall.

## 6. Dropout

**Selected value:** `0.40`, applied once after global average pooling.

**Reason:** Dropout randomly disables 40% of neurons during each training step,
which forces the network to spread what it learns across multiple features instead
of over-relying on any single one — a direct defense against overfitting. 0.40 is a
moderately strong setting, chosen because the training set (~6,600 images) is small
enough that overfitting is a real risk, but not so small that a more aggressive rate
would be needed.

## 7. Optimizer

**Selected value:** Adam, learning rate `0.001`

**Reason:** Adam adapts its effective learning rate per parameter automatically,
which means it generally converges reliably with little manual tuning — a good
default for a first CNN project. Alternatives like plain SGD typically need more
careful learning-rate scheduling to perform comparably.

## 8. Learning Rate

**Selected value:** `0.001` (Adam's typical default), reduced automatically via
`ReduceLROnPlateau` when validation loss plateaus.

**Reason:** 0.001 is high enough to make meaningful progress each training step
without being so high that training becomes unstable or overshoots good solutions.
Pairing it with `ReduceLROnPlateau` (halves the rate if validation loss stalls for 2
epochs) lets the model take larger steps early and smaller, more precise steps later
— without having to hand-pick a training schedule in advance.

## 9. Loss Function

**Selected value:** Binary cross-entropy

**Reason:** This is a two-class (binary) classification problem with a sigmoid
output, and binary cross-entropy is the standard loss function that directly
measures how far the predicted probability is from the true 0/1 label.

## 10. Batch Size

**Selected value:** `32`

**Reason:** 32 is a common middle ground: large enough to produce stable, reliable
gradient estimates at each step, small enough to fit comfortably in memory and keep
each training step fast, especially without a GPU.

## 11. Epoch Count

**Selected value:** Maximum 25 epochs, with early stopping (patience 5 on
validation loss, restoring the best weights seen).

**Reason:** A fixed cap of 25 gives the model enough room to fully learn the
patterns in the data, while early stopping prevents wasted training time and
overfitting once validation performance stops improving — the model automatically
stops at whichever epoch generalized best, rather than the last epoch trained.

## 12. Data Augmentation

**Selected value:** Random horizontal flip, small rotation (±5%), small zoom
(±10%), and mild contrast adjustment (±10%) — applied only to training data.

**Reason:** These are mild, realistic variations that mimic how a part might
actually be photographed on an inspection line — slightly different orientation,
zoom, or lighting — which helps the model generalize instead of memorizing exact
pixel positions from the training set. Augmentation is applied only to training
data because validation and test data must represent real, unmodified images the
model will see in production; augmenting them would make evaluation results
unrealistic.

## 13. Evaluation Metrics

**Selected value:** Accuracy, Precision, Recall, and a confusion matrix (with
particular attention to recall on the defective class).

**Reason:** Accuracy alone can be misleading on a dataset where one class is more
common than the other. Precision and recall break performance down by class, and
the confusion matrix makes the two error types explicit:

- **False negative** (defective part predicted non-defective) — the costlier
  mistake, since a defective part could reach the customer.
- **False positive** (non-defective part predicted defective) — costs only a
  redundant manual re-inspection.

Because a missed defect is more costly than an unnecessary re-check, **recall on
the defective class** is the single most important metric for this use case —
more important than overall accuracy.

---

## Completed Design Decision Table

| Design Decision | Selected Value | Reason |
|---|---|---|
| Image size | 224 x 224 | Balance between detail and computation |
| Problem type | Binary classification | Two output classes |
| Model type | CNN | Suitable for images |
| Conv filters | 32, 64, 128 | Learn increasingly complex features |
| Kernel size | 3 x 3 | Efficient local feature extraction |
| Hidden activation | ReLU | Efficient and commonly used |
| Pooling | MaxPooling | Reduces feature dimensions |
| Output activation | Sigmoid | Produces binary probability |
| Optimizer | Adam | Adaptive and beginner-friendly |
| Learning rate | 0.001 | Reasonable Adam starting value |
| Loss | Binary Cross-Entropy | Suitable for two classes |
| Batch size | 32 | Balanced memory and training |
| Epochs | Maximum 25 | Enough training with early stopping |
| Dropout | 0.40 | Helps reduce overfitting |
| Augmentation | Flip, rotation, zoom, contrast | Improves robustness |
| Metrics | Accuracy, Precision, Recall | Evaluate overall and defect performance |

---

## Conclusion

Trained for 15 epochs on the real dataset (6,633 training images, 715 test images),
the model reached **83.5% test accuracy**, **81.3% precision**, and **96.0% recall**
on the defective class (confusion matrix: TN=162, FP=100, FN=18, TP=435).

Training and validation loss decreased together throughout, with no widening gap —
no sign of overfitting. Early stopping never triggered, and validation loss was
still trending down at epoch 15, meaning the model likely hadn't fully converged and
more epochs (up to the original 25-epoch cap) would probably improve results
further.

The high recall (96.0%) is the most important number for this use case: only 18 of
453 actual defects were missed. The trade-off is 100 false positives — good parts
flagged for a redundant manual check — which is an acceptable cost in a
quality-control pipeline, since it errs on the side of catching defects rather than
missing them.

**Is it ready for production as-is?** Close, but not quite — 18 missed defects out
of 453 is a reasonable start but likely not low enough for a real inspection line.
**Next steps:** continue training past 15 epochs since loss was still improving;
try transfer learning with a pretrained backbone (e.g. MobileNetV2) for a stronger
starting point; and consider lowering the decision threshold below 0.50 to push
recall even higher, accepting more false positives in exchange for catching more of
the remaining missed defects.
