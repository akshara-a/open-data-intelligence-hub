import os
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
# pyrefly: ignore [missing-import]
from PIL import Image

# Create required folders
os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("sample_images", exist_ok=True)

# ============================================================
# 1. Environment & Setup
# ============================================================

print("TensorFlow Version:", tf.__version__)

train_directory = "data/train"
test_directory = "data/test"

image_size = (224, 224)
batch_size = 32

# IMPORTANT:
# 0 = Non-defective
# 1 = Defective
class_names = ["ok_front", "def_front"]

# ============================================================
# 2. Data Loading & Splitting
# ============================================================

print("\n--- Loading Datasets ---")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_directory,
    class_names=class_names,
    validation_split=0.20,
    subset="training",
    seed=42,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary"
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    train_directory,
    class_names=class_names,
    validation_split=0.20,
    subset="validation",
    seed=42,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary"
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_directory,
    class_names=class_names,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="binary",
    shuffle=False
)

# Improve input pipeline performance
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)
test_dataset = test_dataset.prefetch(AUTOTUNE)

# ============================================================
# 3. Data Augmentation
# ============================================================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.10),
    layers.RandomTranslation(0.05, 0.05),
    layers.RandomContrast(0.10)
], name="data_augmentation")

# ============================================================
# 4. CNN Model
# ============================================================

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    data_augmentation,

    layers.Rescaling(1.0 / 255),

    layers.Conv2D(32, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, kernel_size=3, activation="relu"),
    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.40),

    layers.Dense(64, activation="relu"),

    layers.Dropout(0.30),

    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
    ]
)

print("\n--- Model Created ---")
model.summary()

# ============================================================
# 5. Load Existing Best Model
# ============================================================

model_save_path = "models/best_casting_defect_model.keras"

if os.path.exists(model_save_path):

    print(
        f"\nLoading pre-trained best model from "
        f"{model_save_path}..."
    )

    model = tf.keras.models.load_model(
        model_save_path
    )

else:

    print("\nNo saved model found.")

    print("Training a new model...")

    callbacks = [

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ModelCheckpoint(
            model_save_path,
            monitor="val_accuracy",
            save_best_only=True
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2
        )
    ]

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=20,
        callbacks=callbacks
    )

# ============================================================
# 6. Model Evaluation
# ============================================================

print("\n--- Evaluating Model ---")

test_results = model.evaluate(
    test_dataset,
    verbose=1
)

print("\nTest Results:")

for metric_name, value in zip(
    model.metrics_names,
    test_results
):
    print(
        f"{metric_name}: {value:.4f}"
    )

# ============================================================
# 7. Predictions on Test Dataset
# ============================================================

print("\n--- Generating Predictions ---")

y_true = []
y_probability = []

for images, labels in test_dataset:

    probabilities = model.predict(
        images,
        verbose=0
    ).flatten()

    y_probability.extend(
        probabilities
    )

    y_true.extend(
        labels.numpy().flatten().astype(int)
    )

y_true = np.array(y_true)
y_probability = np.array(y_probability)

# Convert probability to class
y_pred = (
    y_probability >= 0.50
).astype(int)

# ============================================================
# 8. Classification Report
# ============================================================

print("\n--- Classification Report ---")

report = classification_report(
    y_true,
    y_pred,
    target_names=[
        "Non-defective",
        "Defective"
    ],
    digits=4
)

print(report)

# Save classification report
with open(
    "reports/classification_report.txt",
    "w"
) as file:

    file.write(report)

# ============================================================
# 9. Confusion Matrix
# ============================================================

print("\n--- Confusion Matrix ---")

cm = confusion_matrix(
    y_true,
    y_pred
)

print(cm)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=[
        "Non-defective",
        "Defective"
    ],
    yticklabels=[
        "Non-defective",
        "Defective"
    ]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Casting Defect Detection - Confusion Matrix")

plt.tight_layout()

plt.savefig(
    "reports/confusion_matrix.png",
    dpi=300
)

plt.close()

# ============================================================
# 10. ROC Curve
# ============================================================

fpr, tpr, thresholds = roc_curve(
    y_true,
    y_probability
)

roc_auc = auc(
    fpr,
    tpr
)

plt.figure(figsize=(7, 5))

plt.plot(
    fpr,
    tpr,
    label=f"ROC Curve (AUC = {roc_auc:.4f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - Casting Defect Detection"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "reports/roc_curve.png",
    dpi=300
)

plt.close()

print(
    f"ROC-AUC: {roc_auc:.4f}"
)

# ============================================================
# 11. Single Image Prediction
# ============================================================

def predict_product(
    image_path,
    model,
    threshold=0.50
):

    try:

        # Check if image is valid
        with Image.open(image_path) as img:

            img.verify()

        # Load image
        image = tf.keras.utils.load_img(
            image_path,
            target_size=(224, 224)
        )

        # Convert image to array
        image_array = tf.keras.utils.img_to_array(
            image
        )

        # Add batch dimension
        image_array = tf.expand_dims(
            image_array,
            axis=0
        )

        # IMPORTANT:
        # The saved model already contains
        # the Rescaling layer.
        defect_probability = float(
            model.predict(
                image_array,
                verbose=0
            )[0][0]
        )

        if defect_probability >= threshold:

            predicted_class = "Defective (1)"

            recommended_action = (
                "Send product for manual inspection"
            )

        else:

            predicted_class = "Non-defective (0)"

            recommended_action = (
                "Product may proceed on production line"
            )

        print(
            f"Image: {os.path.basename(image_path)}"
        )

        print(
            f"Prediction: {predicted_class}"
        )

        print(
            f"Defect probability: "
            f"{defect_probability:.2%}"
        )

        print(
            f"Recommended action: "
            f"{recommended_action}"
        )

        print()

    except Exception as e:

        print(
            f"Skipping invalid image: "
            f"{os.path.basename(image_path)}"
        )

        print(
            f"Reason: {e}"
        )

        print()


# ============================================================
# 12. Sample Image Predictions
# ============================================================

print("\n--- Sample Image Predictions ---")

sample_files = [

    os.path.join(
        "sample_images",
        f
    )

    for f in os.listdir(
        "sample_images"
    )

    if f.lower().endswith(
        (
            ".jpeg",
            ".jpg",
            ".png"
        )
    )
]

print(
    "Sample files found:",
    len(sample_files)
)

for sample in sample_files:

    predict_product(
        sample,
        model,
        threshold=0.50
    )

# ============================================================
# 13. Save Final Findings
# ============================================================

accuracy = test_results[1]
precision = test_results[2]
recall = test_results[3]

f1_score = (
    2 * precision * recall /
    (precision + recall)
    if (precision + recall) > 0
    else 0
)

findings = f"""
# Casting Defect Detection - Findings

## Dataset

Training images: 5307
Validation images: 1326
Test images: 715

## Model

Model: Convolutional Neural Network (CNN)

Image size: 224 x 224

Optimizer: Adam

Loss function: Binary Crossentropy

Classification threshold: 0.50

## Test Results

Accuracy: {accuracy:.4f}

Precision: {precision:.4f}

Recall: {recall:.4f}

F1 Score: {f1_score:.4f}

ROC-AUC: {roc_auc:.4f}

## Conclusion

The CNN model was evaluated on the casting defect test dataset.

The model classifies casting products into:

- Non-defective
- Defective

Products predicted as defective are recommended for manual inspection,
while products predicted as non-defective may proceed on the production line.
"""

with open(
    "reports/findings_report.md",
    "w"
) as file:

    file.write(findings)

print("\n--- Pipeline Completed Successfully ---")

print(
    "Reports saved in the reports/ folder."
)

print(
    "Model saved in the models/ folder."
)