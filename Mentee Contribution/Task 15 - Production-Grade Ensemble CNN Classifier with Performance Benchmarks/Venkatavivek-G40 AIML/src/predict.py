"""Production Single/Batch Inference Execution Pipeline."""

import time
import numpy as np
import tensorflow as tf
from ensemble import soft_voting_predict


class ProductionEnsembleInferenceEngine:
    """Production wrapper for loading saved models and conducting inference."""

    def __init__(
        self,
        model_paths: list[str],
        class_names: list[str],
        confidence_threshold: float = 0.70,
    ):
        """Initializes model instances and serving parameters."""
        self.models = [tf.keras.models.load_model(p) for p in model_paths]
        self.class_names = class_names
        self.threshold = confidence_threshold

    def predict_single(self, raw_image: np.ndarray) -> dict:
        """Executes full serving pipeline on a single un-normalized input image (H, W, C).

        Args:
            raw_image: Standard 0-255 RGB image array.

        Returns:
            Dictionary payload matching production REST schema specification.
        """
        start_time = time.perf_counter()

        # Preprocess single image
        norm_img = np.expand_dims(
            raw_image.astype("float32") / 255.0, axis=0
        )

        model_probs = {}
        prob_distributions = []

        for idx, model in enumerate(self.models):
            probs = model.predict(norm_img, verbose=0)[0]
            prob_distributions.append(probs)
            model_probs[f"cnn_{idx + 1}"] = float(np.max(probs))

        # Soft Voting Aggregation
        ensemble_probs = soft_voting_predict(
            [np.expand_dims(p, axis=0) for p in prob_distributions]
        )[0]
        top_class_idx = int(np.argmax(ensemble_probs))
        confidence = float(ensemble_probs[top_class_idx])

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        decision = (
            "ACCEPT" if confidence >= self.threshold else "MANUAL_REVIEW"
        )

        return {
            "predictedClass": self.class_names[top_class_idx],
            "confidence": round(confidence, 4),
            "decision": decision,
            "inferenceTimeMs": round(elapsed_ms, 2),
            "modelConfidences": model_probs,
        }