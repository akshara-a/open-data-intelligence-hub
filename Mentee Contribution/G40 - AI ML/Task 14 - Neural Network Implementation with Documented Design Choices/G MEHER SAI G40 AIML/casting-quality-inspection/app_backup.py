
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt


# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Casting Quality Inspector",
    page_icon="🔍",
    layout="wide"
)


MODEL_PATH = Path(
    "models/final_mobilenetv2_finetuned.keras"
)

IMAGE_SIZE = (224, 224)

THRESHOLD = 0.50


# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    return model


model = load_model()
base_model = None

for layer in model.layers:
    if isinstance(layer, tf.keras.Model):
        base_model = layer
        break

if base_model is None:
    st.error("MobileNetV2 base model not found.")
    st.stop()

print("Base model:", base_model.name)


# ==========================================
# IMAGE PREPROCESSING
# ==========================================

def preprocess_image(image):

    image = image.convert("RGB")

    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.array(
        image
    ).astype("float32")

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array

def make_gradcam_heatmap(
    image_tensor,
    model,
    base_model,
    last_conv_layer
):

    conv_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=last_conv_layer.output
    )

    with tf.GradientTape() as tape:

        conv_outputs = conv_model(
            image_tensor,
            training=False
        )

        layer_index = base_model.layers.index(
            last_conv_layer
        )

        x = conv_outputs

        for layer in base_model.layers[
            layer_index + 1:
        ]:
            x = layer(
                x,
                training=False
            )

        # Outer classifier
        x = model.layers[2](x)

        x = model.layers[3](
            x,
            training=False
        )

        x = model.layers[4](
            x,
            training=False
        )

        x = model.layers[5](
            x,
            training=False
        )

        predictions = model.layers[6](
            x,
            training=False
        )

        class_score = predictions[:, 0]

    grads = tape.gradient(
        class_score,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(1, 2)
    )

    conv_outputs = conv_outputs[0]
    pooled_grads = pooled_grads[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    heatmap /= (
        tf.reduce_max(heatmap) + 1e-8
    )

    return heatmap.numpy()

candidate_layers = []

for layer in base_model.layers:

    try:
        if len(layer.output.shape) == 4:
            candidate_layers.append(layer)
    except:
        pass

last_conv_layer = candidate_layers[-1]

print(
    "Grad-CAM layer:",
    last_conv_layer.name
)
# ==========================================
# TITLE
# ==========================================

st.title(
    "🔍 Casting Quality Inspector"
)

st.write(
    "AI-powered visual inspection for "
    "casting defects using MobileNetV2."
)


# ==========================================
# IMAGE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload a casting image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    )

    st.image(
        image,
        caption="Uploaded Casting",
        width=500
    )


    # ======================================
    # PREDICTION
    # ======================================

    input_image = preprocess_image(
        image
    )

    probability = float(
        model.predict(
            input_image,
            verbose=0
        )[0][0]
    )
    heatmap = make_gradcam_heatmap(
        input_image,
        model,
        base_model,
        last_conv_layer
    )
    heatmap_uint8 = np.uint8(
        255 * heatmap
    )

    jet = plt.colormaps["jet"]

    jet_colors = jet(
        np.arange(256)
    )[:, :3]

    jet_heatmap = jet_colors[
        heatmap_uint8
    ]

    jet_heatmap = tf.keras.utils.array_to_img(
        jet_heatmap
    )

    jet_heatmap = jet_heatmap.resize(
        (IMAGE_SIZE[1], IMAGE_SIZE[0])
    )

    jet_heatmap = tf.keras.utils.img_to_array(
        jet_heatmap
    )

    original_image = np.array(
        image.resize(IMAGE_SIZE)
    ).astype("float32")

    overlay = (
            original_image * 0.6 +
            jet_heatmap * 0.4
    )

    overlay = np.clip(
        overlay,
        0,
        255
    ).astype("uint8")


    if probability >= THRESHOLD:

        prediction = "DEFECTIVE"

    else:

        prediction = "NON-DEFECTIVE"


    # ======================================
    # RESULT
    # ======================================

    st.subheader(
        "Inspection Result"
    )

    st.metric(
        "Defective Probability",
        f"{probability:.2%}"
    )

    st.write(
        f"### Prediction: {prediction}"
    )
    st.subheader(
        "🔎 AI Explanation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            original_image.astype("uint8"),
            caption="Original Casting",
            use_container_width=True
        )

    with col2:

        st.image(
            overlay,
            caption="Grad-CAM Attention",
            use_container_width=True
        )

    st.caption(
        "Red/yellow regions indicate areas that "
        "contributed more strongly to the model's prediction."
    )
