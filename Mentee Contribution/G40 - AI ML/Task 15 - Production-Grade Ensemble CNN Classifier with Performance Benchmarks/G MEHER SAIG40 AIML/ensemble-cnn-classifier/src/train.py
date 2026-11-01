import os
import numpy as np
import tensorflow as tf

from data_loader import load_cifar10
from augmentation import create_data_augmentation

from models.baseline_cnn import build_baseline_cnn
from models.regularized_cnn import build_regularized_cnn
from models.deep_cnn import build_deep_cnn


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "cnn3"

BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001
PATIENCE = 5


# ============================================================
# PROJECT PATHS
# ============================================================

SRC_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    SRC_DIR
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "results"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# MODEL SELECTION
# ============================================================

if MODEL_NAME == "cnn1":

    model = build_baseline_cnn()

    model_filename = "cnn_baseline.keras"
    history_filename = "cnn1_history.npy"

elif MODEL_NAME == "cnn2":

    model = build_regularized_cnn()

    model_filename = "cnn_regularized.keras"
    history_filename = "cnn2_history.npy"

elif MODEL_NAME == "cnn3":

    model = build_deep_cnn()

    model_filename = "cnn_deep.keras"
    history_filename = "cnn3_history.npy"

else:

    raise ValueError(
        f"Unsupported MODEL_NAME: {MODEL_NAME}"
    )


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("LOADING DATASET")
print("=" * 60)

(
    x_train,
    y_train,
    x_val,
    y_val,
    x_test,
    y_test
) = load_cifar10()


# ============================================================
# DATA AUGMENTATION
# ============================================================

print("\nCreating data augmentation pipeline...")

augmentation = create_data_augmentation()


# ============================================================
# TRAINING DATASET
# ============================================================

print("\nCreating training pipeline...")

train_dataset = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)
)

train_dataset = train_dataset.shuffle(
    buffer_size=len(x_train),
    seed=42,
    reshuffle_each_iteration=True
)

train_dataset = train_dataset.batch(
    BATCH_SIZE
)

train_dataset = train_dataset.map(
    lambda images, labels: (
        augmentation(
            images,
            training=True
        ),
        labels
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)

train_dataset = train_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# VALIDATION DATASET
# ============================================================

validation_dataset = tf.data.Dataset.from_tensor_slices(
    (x_val, y_val)
)

validation_dataset = validation_dataset.batch(
    BATCH_SIZE
)

validation_dataset = validation_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# TEST DATASET
# ============================================================

test_dataset = tf.data.Dataset.from_tensor_slices(
    (x_test, y_test)
)

test_dataset = test_dataset.batch(
    BATCH_SIZE
)

test_dataset = test_dataset.prefetch(
    tf.data.AUTOTUNE
)


# ============================================================
# COMPILE MODEL
# ============================================================

print("\n" + "=" * 60)
print(f"BUILDING {MODEL_NAME.upper()}")
print("=" * 60)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=LEARNING_RATE
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# ============================================================
# CALLBACKS
# ============================================================

checkpoint_path = os.path.join(
    MODEL_DIR,
    model_filename
)

history_path = os.path.join(
    RESULTS_DIR,
    history_filename
)


checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    monitor="val_accuracy",
    mode="max",
    save_best_only=True,
    verbose=1
)


early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=PATIENCE,
    restore_best_weights=True,
    verbose=1
)


reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-6,
    verbose=1
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print(f"STARTING {MODEL_NAME.upper()} TRAINING")
print("=" * 60)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    callbacks=[
        checkpoint,
        early_stopping,
        reduce_lr
    ],
    verbose=1
)


# ============================================================
# SAVE HISTORY
# ============================================================

np.save(
    history_path,
    history.history
)


# ============================================================
# FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL TEST EVALUATION")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(
    test_dataset,
    verbose=1
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 60)
print(f"{MODEL_NAME.upper()} TRAINING COMPLETE")
print("=" * 60)

print(
    f"Test Loss     : {test_loss:.4f}"
)

print(
    f"Test Accuracy : {test_accuracy:.4f}"
)

print(
    f"Test Accuracy : {test_accuracy * 100:.2f}%"
)

print(
    f"\nBest model saved to:\n"
    f"{checkpoint_path}"
)

print(
    f"\nTraining history saved to:\n"
    f"{history_path}"
)