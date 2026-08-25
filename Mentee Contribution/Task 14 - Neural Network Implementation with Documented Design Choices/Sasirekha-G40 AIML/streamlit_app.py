"""
Streamlit dashboard for the Automated Casting Quality Inspection system.

Run locally from the project root with:

    streamlit run streamlit_app.py

For Streamlit Community Cloud deployment, point the app to this same
file (streamlit_app.py) -- no host/port configuration needed, the
platform handles that automatically.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src import config
from src.predict import CastingDefectPredictor
from src.utils import get_logger

logger = get_logger(__name__)

st.set_page_config(
    page_title="Automated Casting Quality Inspection",
    page_icon="🏭",
    layout="wide",
)


@st.cache_resource
def load_predictor():
    """
    Load the model once and cache it across reruns/sessions -- Streamlit
    reruns the whole script on every interaction, so without caching the
    model would reload on every click, which is far too slow.
    """
    return CastingDefectPredictor()


st.title("🏭 Automated Casting Quality Inspection")
st.write(
    "Upload an image of a casting product to automatically check it for "
    "visible defects using a trained CNN."
)

try:
    predictor = load_predictor()
    model_load_error = None
except FileNotFoundError as e:
    predictor = None
    model_load_error = str(e)

if model_load_error:
    st.error(
        f"⚠️ No trained model found at `{config.BEST_MODEL_PATH}`.\n\n"
        f"Please train the model first by running:\n\n"
        f"```\npython -m src.train\n```"
    )

left_col, right_col = st.columns(2)

with left_col:
    uploaded_image = st.file_uploader(
        "Upload Casting Product Image",
        type=["jpg", "jpeg", "png", "bmp"],
    )

    threshold = st.slider(
        "Decision Threshold",
        min_value=0.0,
        max_value=1.0,
        value=config.DEFAULT_THRESHOLD,
        step=0.05,
        help="Probability above this value is classified as Defective.",
    )

    inspect_clicked = st.button("🔍 Inspect Product", type="primary")

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded image", use_container_width=True)

with right_col:
    if inspect_clicked:
        if predictor is None:
            st.warning("Model not available. Train it first (see message above).")
        elif uploaded_image is None:
            st.warning("Please upload a casting product image before clicking **Inspect Product**.")
        else:
            try:
                from PIL import Image

                pil_image = Image.open(uploaded_image)
                result = predictor.predict(pil_image, threshold=threshold)

                is_defective = result["predicted_class"] == "Defective"
                prediction_label = "🔴 DEFECTIVE" if is_defective else "🟢 NON-DEFECTIVE"

                st.subheader(f"Prediction: {prediction_label}")
                st.metric("Defect Probability", f"{result['defect_probability']:.1%}")
                st.metric("Decision Threshold", f"{result['threshold']:.0%}")
                st.write(f"**Recommended action:** {result['recommended_action']}")
                st.caption(
                    "Probability represents the model's estimated likelihood "
                    "that the product belongs to the defective class."
                )
            except Exception:
                logger.exception("Prediction failed")
                st.error(
                    "Something went wrong while processing this image. "
                    "Please make sure it is a valid image file (JPG/PNG) "
                    "and try again."
                )
    else:
        st.info("Upload an image and click **Inspect Product** to see results here.")

st.markdown("---")
st.caption(
    "**Class mapping:** `ok_front` = Non-defective (0) | "
    "`def_front` = Defective (1)\n\n"
    "This tool is a decision-support aid for quality-control teams and "
    "does not replace human inspection."
)
