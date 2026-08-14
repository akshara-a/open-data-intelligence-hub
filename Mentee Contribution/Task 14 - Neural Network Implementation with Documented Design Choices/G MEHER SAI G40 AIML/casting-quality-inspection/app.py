import streamlit as st
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Casting Quality Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = Path(
    "models/final_mobilenetv2_finetuned.keras"
)

IMAGE_SIZE = (224, 224)

# Keep this at 0.50 for now.
# We will replace it with the properly locked threshold later.
THRESHOLD = 0.50


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return tf.keras.models.load_model(
        MODEL_PATH
    )


model = load_model()


# ============================================================
# FIND MOBILENETV2 BASE MODEL
# ============================================================

base_model = None

for layer in model.layers:

    if isinstance(layer, tf.keras.Model):

        base_model = layer
        break


if base_model is None:

    st.error(
        "MobileNetV2 base model could not be found."
    )

    st.stop()


# ============================================================
# FIND GRAD-CAM LAYER
# ============================================================

candidate_layers = []

for layer in base_model.layers:

    try:

        if len(layer.output.shape) == 4:
            candidate_layers.append(layer)

    except Exception:

        pass


last_conv_layer = candidate_layers[-1]


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

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


# ============================================================
# GRAD-CAM
# ============================================================

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

        layer_index = (
            base_model.layers.index(
                last_conv_layer
            )
        )

        x = conv_outputs

        for layer in base_model.layers[
            layer_index + 1:
        ]:

            x = layer(
                x,
                training=False
            )

        # Outer model classifier
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


# ============================================================
# HEADER
# ============================================================

st.title(
    "🔍 Casting Quality Inspector"
)

st.markdown(
    """
    ### AI-powered industrial visual inspection

    Detect potential casting defects using a
    **fine-tuned MobileNetV2** deep-learning model
    with **Grad-CAM explainability**.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Inspection System")

    st.markdown(
        """
        **Model**

        Fine-tuned MobileNetV2

        **Task**

        Casting Defect Detection

        **Input**

        224 × 224 RGB

        **Classes**

        🟢 Non-defective

        🔴 Defective

        **Explainability**

        Grad-CAM
        """
    )

    st.divider()

    st.info(
        "Upload a casting image to perform "
        "an AI-based quality inspection."
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.divider()

st.subheader(
    "📤 Upload Casting Image"
)

uploaded_file = st.file_uploader(
    "Choose a casting image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    help="Upload an image of a casting component."
)


# ============================================================
# INSPECTION
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    input_image = preprocess_image(
        image
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    probability = float(
        model.predict(
            input_image,
            verbose=0
        )[0][0]
    )

    if probability >= THRESHOLD:

        prediction = "DEFECTIVE"

        confidence = probability

    else:

        prediction = "NON-DEFECTIVE"

        confidence = 1 - probability


    # --------------------------------------------------------
    # ORIGINAL IMAGE
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🖼️ Uploaded Casting"
    )

    image_col, result_col = st.columns(
        [1, 1]
    )

    with image_col:

        st.image(
            image,
            caption="Input Casting",
            width="stretch"
        )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with result_col:

        st.subheader(
            "📊 Inspection Result"
        )

        if prediction == "DEFECTIVE":

            st.error(
                "🔴 DEFECTIVE"
            )

        else:

            st.success(
                "🟢 NON-DEFECTIVE"
            )

        st.metric(
            "Confidence",
            f"{confidence:.2%}"
        )

        st.metric(
            "Defective Probability",
            f"{probability:.2%}"
        )

        st.progress(
            probability,
            text=(
                f"Defective probability: "
                f"{probability:.2%}"
            )
        )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📋 Inspection Summary"
    )

    summary1, summary2, summary3 = st.columns(3)

    with summary1:

        st.metric(
            "Classification",
            prediction
        )

    with summary2:

        st.metric(
            "Confidence",
            f"{confidence:.2%}"
        )

    with summary3:

        st.metric(
            "Threshold",
            f"{THRESHOLD:.2f}"
        )


    # --------------------------------------------------------
    # GRAD-CAM
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔎 AI Explainability"
    )

    st.markdown(
        """
        **Grad-CAM** highlights image regions that
        contributed strongly to the model's prediction.
        """
    )

    heatmap = make_gradcam_heatmap(
        input_image,
        model,
        base_model,
        last_conv_layer
    )


    # --------------------------------------------------------
    # CREATE OVERLAY
    # --------------------------------------------------------

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

    jet_heatmap = (
        tf.keras.utils.array_to_img(
            jet_heatmap
        )
    )

    jet_heatmap = jet_heatmap.resize(
        (
            IMAGE_SIZE[1],
            IMAGE_SIZE[0]
        )
    )

    jet_heatmap = (
        tf.keras.utils.img_to_array(
            jet_heatmap
        )
    )

    original_image = np.array(
        image.resize(
            IMAGE_SIZE
        )
    ).astype("float32")

    overlay = (
        original_image * 0.6
        +
        jet_heatmap * 0.4
    )

    overlay = np.clip(
        overlay,
        0,
        255
    ).astype("uint8")


    # --------------------------------------------------------
    # DISPLAY EXPLANATION
    # --------------------------------------------------------

    explain1, explain2 = st.columns(2)

    with explain1:

        st.image(
            original_image.astype(
                "uint8"
            ),
            caption="Original Casting",
            width="stretch"
        )

    with explain2:

        st.image(
            overlay,
            caption="Grad-CAM Attention",
            width="stretch"
        )


    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    if prediction == "DEFECTIVE":

        st.warning(
            "The model identified visual features "
            "associated with a defective casting. "
            "The Grad-CAM visualization shows regions "
            "that contributed strongly to this decision."
        )

    else:

        st.info(
            "The model did not identify strong visual "
            "evidence associated with a defective casting. "
            "The Grad-CAM visualization shows regions "
            "that contributed to the prediction."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">

    <h4>🔍 Casting Quality Inspector</h4>

    <p>
    Fine-tuned MobileNetV2 • Grad-CAM Explainability
    </p>

    <p style="font-size:13px;">
    Deep Learning Computer Vision Project
    </p>

    </div>
    """,
    unsafe_allow_html=True
)