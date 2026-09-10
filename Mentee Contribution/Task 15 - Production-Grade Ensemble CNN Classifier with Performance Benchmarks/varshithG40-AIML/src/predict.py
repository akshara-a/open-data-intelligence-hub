"""
predict.py
==========
Production inference engine implementing the complete prediction pipeline (Sections 61-64):
  Input Image -> Validation -> Preprocessing -> Parallel/Sequential CNN Execution ->
  Soft/Weighted Ensembling -> Confidence Scoring -> Threshold Gating -> Structured Output.
"""

import os
import sys
import time
from typing import Union, Dict, Any
import numpy as np
from PIL import Image
from tensorflow import keras

# Support both package-level and direct execution
try:
    from .preprocessing import preprocess_image, IDX_TO_CLASS
    from .ensemble import EnsembleClassifier
except (ImportError, ValueError):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.preprocessing import preprocess_image, IDX_TO_CLASS
    from src.ensemble import EnsembleClassifier

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")


class ProductionPredictor:
    """
    Production-grade inference handler with model caching, confidence scoring,
    threshold checking, and model disagreement telemetry.
    """
    def __init__(self, confidence_threshold: float = 0.70):
        self.confidence_threshold = confidence_threshold
        self.ensemble = EnsembleClassifier()
        self.ensemble.load_models_from_disk()
        # Default validation weights: Baseline=0.33, Regularized=0.33, Deep=0.34
        self.ensemble.model_weights = np.array([0.333, 0.333, 0.334], dtype=np.float32)

    def predict(
        self,
        image_input: Union[str, Image.Image, np.ndarray],
        ensemble_strategy: str = "soft",
        include_debug_models: bool = True
    ) -> Dict[str, Any]:
        """
        Executes end-to-end production prediction.
        Returns a standardized production response dictionary.
        """
        t_start = time.perf_counter()
        
        # 1. Validation & Preprocessing
        x = preprocess_image(image_input)  # (1, 128, 128, 3)
        
        # 2. Individual Model Inferences
        all_probs = self.ensemble.get_individual_probabilities(x)  # (3, 1, 2)
        p1 = all_probs[0, 0]
        p2 = all_probs[1, 0]
        p3 = all_probs[2, 0]
        
        c1_class = IDX_TO_CLASS[int(np.argmax(p1))]
        c2_class = IDX_TO_CLASS[int(np.argmax(p2))]
        c3_class = IDX_TO_CLASS[int(np.argmax(p3))]
        
        # 3. Ensemble Strategy Application
        if ensemble_strategy == "majority":
            maj_pred = int(self.ensemble.predict_majority_voting(x)[0])
            predicted_class = IDX_TO_CLASS[maj_pred]
            mean_p = np.mean([p1, p2, p3], axis=0)
            confidence = float(mean_p[maj_pred])
            final_probs = {"cat": float(mean_p[0]), "dog": float(mean_p[1])}
        elif ensemble_strategy == "weighted":
            w_probs, w_preds = self.ensemble.predict_weighted_soft_voting(x)
            predicted_class = IDX_TO_CLASS[int(w_preds[0])]
            confidence = float(np.max(w_probs[0]))
            final_probs = {"cat": float(w_probs[0][0]), "dog": float(w_probs[0][1])}
        else:  # default soft voting
            s_probs, s_preds = self.ensemble.predict_soft_voting(x)
            predicted_class = IDX_TO_CLASS[int(s_preds[0])]
            confidence = float(np.max(s_probs[0]))
            final_probs = {"cat": float(s_probs[0][0]), "dog": float(s_probs[0][1])}

        # 4. Disagreement Telemetry
        individual_preds = [c1_class, c2_class, c3_class]
        unique_votes = set(individual_preds)
        is_unanimous = len(unique_votes) == 1
        
        # 5. Confidence Threshold Decision Gating (Section 62)
        if confidence < self.confidence_threshold:
            decision = "Manual Review Required (Low Confidence)"
        else:
            decision = f"Automated Acceptance ({predicted_class.upper()})"
            
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        
        response = {
            "predictedClass": predicted_class,
            "confidence": round(confidence, 4),
            "confidenceScorePct": f"{confidence * 100:.2f}%",
            "decision": decision,
            "meetsConfidenceThreshold": confidence >= self.confidence_threshold,
            "isUnanimous": is_unanimous,
            "probabilities": final_probs,
            "inferenceTimeMs": round(elapsed_ms, 2)
        }
        
        if include_debug_models:
            response["individualModels"] = {
                "cnn1_baseline": {
                    "predictedClass": c1_class,
                    "confidence": round(float(np.max(p1)), 4),
                    "catProb": round(float(p1[0]), 4),
                    "dogProb": round(float(p1[1]), 4)
                },
                "cnn2_regularized": {
                    "predictedClass": c2_class,
                    "confidence": round(float(np.max(p2)), 4),
                    "catProb": round(float(p2[0]), 4),
                    "dogProb": round(float(p2[1]), 4)
                },
                "cnn3_deep": {
                    "predictedClass": c3_class,
                    "confidence": round(float(np.max(p3)), 4),
                    "catProb": round(float(p3[0]), 4),
                    "dogProb": round(float(p3[1]), 4)
                }
            }
            
        return response


if __name__ == "__main__":
    predictor = ProductionPredictor()
    dummy_img = np.random.rand(128, 128, 3).astype(np.float32)
    res = predictor.predict(dummy_img)
    import json
    print(json.dumps(res, indent=2))
