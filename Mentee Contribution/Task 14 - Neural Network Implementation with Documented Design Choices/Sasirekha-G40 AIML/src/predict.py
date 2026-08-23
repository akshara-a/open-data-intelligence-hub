"""
Single-image prediction utility.

Provides CastingDefectPredictor, which loads the trained model ONCE and
reuses it for every prediction (important for the Gradio dashboard's
performance -- the model must not be reloaded on every click).
"""

from pathlib import Path

import numpy as np
import tensorflow as tf

from src import config
from src.utils import get_logger

logger = get_logger(__name__)


class CastingDefectPredictor:
    """
    Wraps the trained Keras model to provide a simple, reusable
    prediction API for both scripts and the Gradio dashboard.
    """

    def __init__(self, model_path: Path = config.BEST_MODEL_PATH):
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"No trained model found at {self.model_path}.\n"
                f"Please run `python -m src.train` first to train and "
                f"save a model before making predictions."
            )

        logger.info("Loading model from: %s", self.model_path)
        self.model = tf.keras.models.load_model(self.model_path)
        logger.info("Model loaded and ready for predictions.")

    def _preprocess(self, image) -> np.ndarray:
        """
        Accepts either a file path (str/Path) or an already-loaded
        PIL.Image / numpy array (as provided by Gradio), and returns a
        (1, 224, 224, 3) float32 batch ready for the model.

        Note: the model itself contains a Rescaling(1/255) layer, so raw
        0-255 pixel values should be passed in here, NOT pre-normalized.
        """
        from PIL import Image

        if isinstance(image, (str, Path)):
            pil_image = Image.open(image).convert("RGB")
        elif isinstance(image, Image.Image):
            pil_image = image.convert("RGB")
        elif isinstance(image, np.ndarray):
            pil_image = Image.fromarray(image).convert("RGB")
        else:
            raise TypeError(
                f"Unsupported image type: {type(image)}. Expected a file "
                f"path, PIL.Image, or numpy array."
            )

        pil_image = pil_image.resize(config.IMAGE_SIZE)
        image_array = tf.keras.utils.img_to_array(pil_image)
        image_array = np.expand_dims(image_array, axis=0)
        return image_array

    def predict(self, image, threshold: float = config.DEFAULT_THRESHOLD) -> dict:
        """
        Run a prediction on a single image.

        Parameters
        ----------
        image : str | Path | PIL.Image.Image | numpy.ndarray
            The product image to classify.
        threshold : float
            Decision threshold applied to the defect probability.

        Returns
        -------
        dict with keys:
            predicted_class      : "Defective" | "Non-defective"
            defect_probability    : float in [0, 1]
            threshold             : the threshold used
            recommended_action    : human-readable next step
        """
        image_array = self._preprocess(image)
        defect_probability = float(self.model.predict(image_array, verbose=0)[0][0])

        if defect_probability >= threshold:
            predicted_class = "Defective"
            recommended_action = "Send product for manual inspection"
        else:
            predicted_class = "Non-defective"
            recommended_action = "Product may proceed"

        return {
            "predicted_class": predicted_class,
            "defect_probability": defect_probability,
            "threshold": threshold,
            "recommended_action": recommended_action,
        }


def predict_product(image_path, model=None, threshold: float = config.DEFAULT_THRESHOLD) -> dict:
    """
    Convenience function matching the original spec's `predict_product`
    signature, for quick scripts / notebooks. Prefer CastingDefectPredictor
    directly (or via this function with a pre-loaded model) when making
    many predictions, to avoid reloading the model each call.
    """
    if model is None:
        predictor = CastingDefectPredictor()
    else:
        predictor = CastingDefectPredictor.__new__(CastingDefectPredictor)
        predictor.model = model
        predictor.model_path = config.BEST_MODEL_PATH

    result = predictor.predict(image_path, threshold=threshold)

    print(f"Prediction: {result['predicted_class']}")
    print(f"Defect probability: {result['defect_probability']:.2%}")
    print(f"Recommended action: {result['recommended_action']}")

    return result


if __name__ == "__main__":
    # Example manual usage: python -m src.predict
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.predict <path_to_image> [threshold]")
        sys.exit(1)

    img_path = sys.argv[1]
    thr = float(sys.argv[2]) if len(sys.argv) > 2 else config.DEFAULT_THRESHOLD

    predict_product(img_path, threshold=thr)
