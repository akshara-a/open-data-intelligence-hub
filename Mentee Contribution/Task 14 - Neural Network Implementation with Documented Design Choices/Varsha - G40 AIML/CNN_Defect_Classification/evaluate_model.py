import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.utils import load_img, img_to_array


# ============================================================
# STEP 1: LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = "models/casting_defect_cnn.keras"

model = tf.keras.models.load_model(MODEL_PATH)

print("========================================")
print("Trained model loaded successfully!")
print("========================================")


# ============================================================
# STEP 2: SETTINGS
# ============================================================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32

TEST_DIR = "data/casting_data/test"

# Class 0 = Non-defective
# Class 1 = Defective
CLASS_NAMES = ["ok_front", "def_front"]


# ============================================================
# STEP 3: LOAD TEST DATASET
# ============================================================

test_dataset = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    class_names=CLASS_NAMES,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    shuffle=False
)

print("\nTest dataset loaded successfully!")
print("Class names:", test_dataset.class_names)


# ============================================================
# STEP 4: EVALUATE MODEL
# ============================================================

results = model.evaluate(test_dataset, verbose=1)

print("\n========================================")
print("TEST RESULTS")
print("========================================")

print("Loss      :", results[0])
print("Accuracy  :", results[1])
print("Precision :", results[2])
print("Recall    :", results[3])


# ============================================================
# STEP 5: GET ACTUAL LABELS
# ============================================================

y_true = np.concatenate(
    [y.numpy().flatten() for x, y in test_dataset]
)

print("\nActual labels collected successfully!")


# ============================================================
# STEP 6: GET MODEL PREDICTIONS
# ============================================================

y_probability = model.predict(test_dataset, verbose=1)

y_pred = (
    y_probability.flatten() >= 0.5
).astype(int)

print("Predictions generated successfully!")


# ============================================================
# STEP 7: CLASSIFICATION REPORT
# ============================================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_true,
        y_pred,
        target_names=[
            "Non-defective",
            "Defective"
        ]
    )
)


# ============================================================
# STEP 8: CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(y_true, y_pred)

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(cm)


# ============================================================
# STEP 9: CREATE RESULTS FOLDER
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# STEP 10: PLOT CONFUSION MATRIX
# ============================================================

plt.figure(figsize=(6, 5))

plt.imshow(cm)

plt.title("Confusion Matrix")

plt.xlabel("Predicted Label")

plt.ylabel("Actual Label")

plt.xticks(
    [0, 1],
    ["Non-defective", "Defective"]
)

plt.yticks(
    [0, 1],
    ["Non-defective", "Defective"]
)


# Display numbers inside matrix

for i in range(2):
    for j in range(2):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )


plt.tight_layout()


# ============================================================
# STEP 11: SAVE CONFUSION MATRIX
# ============================================================

CONFUSION_MATRIX_PATH = os.path.join(
    RESULTS_DIR,
    "confusion_matrix.png"
)

plt.savefig(
    CONFUSION_MATRIX_PATH
)

plt.show()

print("\nConfusion matrix saved successfully!")
print(
    "Saved at:",
    CONFUSION_MATRIX_PATH
)


# ============================================================
# STEP 12: TEST 5 UNSEEN IMAGES
# ============================================================

print("\n========================================")
print("TESTING 5 UNSEEN IMAGES")
print("========================================")


test_images = []


# Collect images from both classes

for class_name in CLASS_NAMES:

    folder = os.path.join(
        TEST_DIR,
        class_name
    )

    class_files = []

    for filename in os.listdir(folder):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            image_path = os.path.join(
                folder,
                filename
            )

            class_files.append(
                image_path
            )


    # Take first 3 from each class
    # This ensures both classes are represented

    for image_path in class_files[:3]:

        test_images.append(
            (
                image_path,
                class_name
            )
        )


# Select only 5 images

test_images = test_images[:5]


# ============================================================
# STEP 13: PREDICT EACH IMAGE
# ============================================================

for image_path, actual_class in test_images:

    image = load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    image_array = img_to_array(image)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    probability = model.predict(
        image_array,
        verbose=0
    )[0][0]


    # Probability >= 0.5 = Defective

    if probability >= 0.5:

        predicted_class = "def_front"

    else:

        predicted_class = "ok_front"


    defect_probability = probability * 100


    print("\n--------------------------------")
    print(
        "Image:",
        os.path.basename(image_path)
    )

    print(
        "Actual:",
        actual_class
    )

    print(
        "Predicted:",
        predicted_class
    )

    print(
        "Defective Probability:",
        f"{defect_probability:.2f}%"
    )


# ============================================================
# PROJECT COMPLETED
# ============================================================

print("\n========================================")
print("MODEL EVALUATION COMPLETED!")
print("========================================")