import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.utils import load_img, img_to_array


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = tf.keras.models.load_model(
    "models/casting_defect_cnn.keras"
)

print("Trained model loaded successfully!")


# ==========================================
# SETTINGS
# ==========================================

IMAGE_SIZE = (224, 224)

TEST_DIR = "data/casting_data/test"

CLASS_NAMES = [
    "ok_front",
    "def_front"
]


# ==========================================
# COLLECT 5 TEST IMAGES
# ==========================================

test_images = []

for class_name in CLASS_NAMES:

    folder = os.path.join(
        TEST_DIR,
        class_name
    )

    files = []

    for filename in os.listdir(folder):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            files.append(
                os.path.join(folder, filename)
            )

    # Take up to 3 images from each class
    for image_path in files[:3]:

        test_images.append(
            (image_path, class_name)
        )


# Select exactly 5
test_images = test_images[:5]


print("\n================================")
print("5 IMAGE PREDICTIONS")
print("================================")


# ==========================================
# CREATE RESULTS FOLDER
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results"
)


# ==========================================
# PREDICT IMAGES
# ==========================================

prediction_results = []

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

    if probability >= 0.5:

        predicted_class = "def_front"

    else:

        predicted_class = "ok_front"

    defect_probability = probability * 100

    prediction_results.append(
        (
            image_path,
            actual_class,
            predicted_class,
            defect_probability
        )
    )

    print("\n-----------------------------")

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


# ==========================================
# SAVE PREDICTION RESULTS
# ==========================================

print("\n================================")
print("5 IMAGE TEST COMPLETED!")
print("================================")