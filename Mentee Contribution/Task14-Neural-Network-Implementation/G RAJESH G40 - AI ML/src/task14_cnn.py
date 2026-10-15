import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras import layers, models
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# TASK 14: NEURAL NETWORK IMPLEMENTATION
# Binary Image Classification Using CNN
# ============================================================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25

TRAIN_DIR = r"..\Task13-Casting-Defect-Detection\data\casting_data\train"
TEST_DIR = r"..\Task13-Casting-Defect-Detection\data\casting_data\test"

OUTPUT_DIR = "outputs"
MODEL_DIR = "models"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


print("=" * 60)
print("TASK 14: CNN BINARY IMAGE CLASSIFICATION")
print("=" * 60)


# ============================================================
# 1. LOAD TRAINING DATASET
# ============================================================

print("\nLoading training dataset...")

full_train_dataset = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=True,
    seed=42
)


# ============================================================
# 2. LOAD TEST DATASET
# ============================================================

print("\nLoading test dataset...")

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)


print("\nClass names:")
print(full_train_dataset.class_names)


# ============================================================
# 3. CREATE TRAIN / VALIDATION SPLIT
# ============================================================

dataset_size = tf.data.experimental.cardinality(
    full_train_dataset
).numpy()

validation_batches = int(dataset_size * 0.2)

train_dataset = full_train_dataset.skip(
    validation_batches
)

validation_dataset = full_train_dataset.take(
    validation_batches
)


print("\nDataset split created:")
print("Total batches:", dataset_size)
print("Training batches:", dataset_size - validation_batches)
print("Validation batches:", validation_batches)


# ============================================================
# 4. OPTIMIZE DATA PIPELINE
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)

test_dataset = test_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# ============================================================
# 5. DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10)
], name="data_augmentation")


# ============================================================
# 6. BUILD CNN MODEL
# ============================================================

print("\nBuilding CNN model...")

model = models.Sequential([

    layers.Input(shape=(224, 224, 3)),

    # Data augmentation
    data_augmentation,

    # Normalize pixels
    layers.Rescaling(1.0 / 255),

    # CNN Layer 1
    layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # CNN Layer 2
    layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # CNN Layer 3
    layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),

    layers.MaxPooling2D(),

    # Reduce parameters
    layers.GlobalAveragePooling2D(),

    # Reduce overfitting
    layers.Dropout(0.40),

    # Dense layer
    layers.Dense(
        64,
        activation="relu"
    ),

    # Binary classification
    layers.Dense(
        1,
        activation="sigmoid"
    )

])


# ============================================================
# 7. MODEL SUMMARY
# ============================================================

print("\nMODEL SUMMARY")
print("=" * 60)

model.summary()


# ============================================================
# 8. COMPILE MODEL
# ============================================================

print("\nCompiling model...")

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    loss="binary_crossentropy",

    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(
            name="precision"
        ),
        tf.keras.metrics.Recall(
            name="recall"
        )
    ]

)


# ============================================================
# 9. CALLBACKS
# ============================================================

callbacks = [

    tf.keras.callbacks.EarlyStopping(

        monitor="val_loss",

        patience=5,

        restore_best_weights=True

    ),

    tf.keras.callbacks.ReduceLROnPlateau(

        monitor="val_loss",

        factor=0.5,

        patience=2

    )

]


# ============================================================
# 10. TRAIN MODEL
# ============================================================

print("\nStarting model training...")
print("=" * 60)


history = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=EPOCHS,

    callbacks=callbacks

)


# ============================================================
# 11. SAVE MODEL
# ============================================================

model_path = os.path.join(
    MODEL_DIR,
    "casting_defect_cnn.keras"
)

model.save(model_path)

print("\nModel saved successfully!")
print("Location:", model_path)


# ============================================================
# 12. ACCURACY GRAPH
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training and Validation Accuracy")
plt.legend()
plt.grid()

accuracy_path = os.path.join(
    OUTPUT_DIR,
    "accuracy_graph.png"
)

plt.savefig(
    accuracy_path,
    bbox_inches="tight"
)

plt.close()

print("\nAccuracy graph saved!")


# ============================================================
# 13. LOSS GRAPH
# ============================================================

plt.figure(figsize=(8, 6))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.grid()

loss_path = os.path.join(
    OUTPUT_DIR,
    "loss_graph.png"
)

plt.savefig(
    loss_path,
    bbox_inches="tight"
)

plt.close()

print("\nLoss graph saved!")


# ============================================================
# 14. EVALUATE MODEL
# ============================================================

print("\nEvaluating model on test dataset...")
print("=" * 60)


test_results = model.evaluate(
    test_dataset,
    return_dict=True
)


print("\nTEST RESULTS")

for metric, value in test_results.items():

    print(f"{metric}: {value:.4f}")


# ============================================================
# 15. GENERATE PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

probabilities = model.predict(
    test_dataset
)

predictions = (
    probabilities.flatten() >= 0.5
).astype(int)


# ============================================================
# 16. GET ACTUAL LABELS
# ============================================================

actual_labels = np.concatenate([

    labels.numpy().flatten()

    for images, labels in test_dataset

]).astype(int)


# ============================================================
# 17. CONFUSION MATRIX
# ============================================================

print("\nCONFUSION MATRIX")
print("=" * 60)

matrix = confusion_matrix(
    actual_labels,
    predictions
)

print(matrix)


# ============================================================
# 18. SAVE CONFUSION MATRIX
# ============================================================

display = ConfusionMatrixDisplay(

    confusion_matrix=matrix,

    display_labels=[
        "def_front",
        "ok_front"
    ]

)

display.plot()

plt.title("Confusion Matrix")

confusion_path = os.path.join(
    OUTPUT_DIR,
    "confusion_matrix.png"
)

plt.savefig(
    confusion_path,
    bbox_inches="tight"
)

plt.close()

print("\nConfusion matrix saved!")


# ============================================================
# 19. TEST FIVE SAMPLE IMAGES
# ============================================================

print("\nTESTING FIVE SAMPLE IMAGES")
print("=" * 60)

sample_images = []
sample_labels = []


for images, labels in test_dataset:

    for image, label in zip(images, labels):

        sample_images.append(image)

        sample_labels.append(
            int(label.numpy().flatten()[0])
        )

        if len(sample_images) == 5:
            break

    if len(sample_images) == 5:
        break


for index, image in enumerate(sample_images):

    image_batch = tf.expand_dims(
        image,
        axis=0
    )

    probability = model.predict(
        image_batch,
        verbose=0
    )[0][0]


    # Class order:
    # 0 = def_front
    # 1 = ok_front

    if probability >= 0.5:

        predicted_class = "ok_front"

    else:

        predicted_class = "def_front"


    if sample_labels[index] == 1:

        actual_class = "ok_front"

    else:

        actual_class = "def_front"


    if predicted_class == "def_front":

        action = "Send for manual inspection"

    else:

        action = "Approved as non-defective"


    print(f"\nImage {index + 1}")

    print(
        f"Actual Class: {actual_class}"
    )

    print(
        f"Prediction: {predicted_class}"
    )

    print(
        f"Probability: {probability * 100:.2f}%"
    )

    print(
        f"Action: {action}"
    )


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)

print("TASK 14 COMPLETED SUCCESSFULLY!")

print("=" * 60)


print("\nGenerated files:")

print("- CNN Model")
print("- Accuracy Graph")
print("- Loss Graph")
print("- Confusion Matrix")
print("- Test Evaluation Results")