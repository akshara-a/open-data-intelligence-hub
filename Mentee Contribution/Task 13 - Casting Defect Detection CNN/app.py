from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "casting_defect_cnn.keras"

IMAGE_SIZE = (128, 128)


# Page settings
st.set_page_config(
    page_title="Casting Defect Detection",
    page_icon="🔍",
    layout="centered"
)


st.title("🔍 Casting Defect Detection CNN")
st.write(
    "Upload a casting image to predict whether it is defective or OK."
)


@st.cache_resource
def load_trained_model():
    return load_model(MODEL_PATH)


model = load_trained_model()


uploaded_file = st.file_uploader(
    "Upload a casting image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Casting Image",
        use_container_width=True
    )

    image_resized = image.resize(IMAGE_SIZE)

    image_array = img_to_array(image_resized)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array, verbose=0)[0][0]

    if prediction >= 0.5:
        result = "OK Casting"
        confidence = prediction * 100
    else:
        result = "Defective Casting"
        confidence = (1 - prediction) * 100

    st.subheader("Prediction Result")

    if result == "OK Casting":
        st.success(result)
    else:
        st.error(result)

    st.write(f"Confidence: **{confidence:.2f}%**")