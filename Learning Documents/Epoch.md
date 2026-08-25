# Epoch Count in Neural Networks

## What Is an Epoch?

An **epoch** is one complete pass of the entire training dataset through the neural network.

For example, if your training dataset contains:

```text
1,000 images
```

then:

```text
1 epoch   = Model sees all 1,000 images once
10 epochs = Model goes through all 1,000 images 10 times
25 epochs = Model goes through all 1,000 images 25 times
```

---

## Why Do We Need Multiple Epochs?

A neural network usually cannot learn everything from the dataset in a single pass.

During each epoch, the model:

1. Makes predictions
2. Compares predictions with the correct answers
3. Calculates the error
4. Updates its weights
5. Tries to improve in the next epoch

So, with each epoch, the model gradually learns better patterns from the data.

---

## Example

```python
model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25
)
```

Here:

```text
epochs = 25
```

means the model is allowed to go through the complete training dataset up to **25 times**.

---

## Too Few Epochs

If the number of epochs is too low, the model may not have enough time to learn properly.

Example:

```text
Epochs = 2
```

Possible result:

```text
Low training accuracy
Low validation accuracy
```

This is commonly associated with **underfitting**.

---

## Too Many Epochs

If the model trains for too many epochs, it may start memorizing the training data instead of learning general patterns.

Example:

```text
Training Accuracy   = 99%
Validation Accuracy = 75%
```

This may indicate **overfitting**.

The model performs very well on training data but poorly on unseen data.

---

## Early Stopping

To avoid training for unnecessary epochs, we can use **Early Stopping**.

Example:

```python
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)
```

Then:

```python
model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=25,
    callbacks=[early_stopping]
)
```

Even though the maximum epoch count is `25`, training may stop earlier.

For example:

```text
Maximum Epochs = 25
Training stopped at Epoch 14
```

because the validation performance stopped improving.

---

## Epoch vs Batch

An **epoch** is a complete pass through the full dataset.

A **batch** is a smaller group of training samples processed at one time.

Example:

```text
Training Images = 1,000
Batch Size      = 100
```

Then approximately:

```text
1 Epoch = 10 Batches
```

because:

```text
1,000 / 100 = 10
```

---

## Simple Summary

| Term | Meaning |
|---|---|
| Epoch | One complete pass through the training dataset |
| Batch | Small group of training samples processed together |
| Batch Size | Number of samples in one batch |
| Epoch Count | Number of complete passes through the dataset |
| Early Stopping | Stops training when validation performance stops improving |

---

## One-Line Definition

> **Epoch count is the number of times a neural network processes the complete training dataset during training.**
