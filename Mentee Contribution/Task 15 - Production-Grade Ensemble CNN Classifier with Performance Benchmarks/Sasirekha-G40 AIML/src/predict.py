import argparse
import json
import time
import numpy as np
import tensorflow as tf
from PIL import Image
from .config import IMAGE_SIZE, MODELS_DIR, CLASS_NAMES
from .ensemble import majority_vote, soft_vote, weighted_soft_vote

MODEL_NAMES = ["cnn_baseline", "cnn_regularized", "cnn_deep"]

def load_image(path):
    image = Image.open(path).convert("RGB").resize(IMAGE_SIZE)
    return np.asarray(image, dtype=np.float32)[None] / 255.0

def main():
    parser = argparse.ArgumentParser(description="Production-style steel defect prediction")
    parser.add_argument("image", help="Path to a JPG/PNG image")
    parser.add_argument("--method", choices=["majority", "soft", "weighted"], default="soft")
    parser.add_argument("--threshold", type=float, default=0.80)
    args = parser.parse_args()

    image = load_image(args.image)
    models = [tf.keras.models.load_model(MODELS_DIR / f"{name}.keras") for name in MODEL_NAMES]

    start = time.perf_counter()
    probabilities = [model.predict(image, verbose=0) for model in models]

    if args.method == "majority":
        label = int(majority_vote(probabilities)[0])
        averaged = np.mean(np.stack(probabilities), axis=0)
    elif args.method == "weighted":
        label_arr, averaged = weighted_soft_vote(probabilities, [0.25, 0.35, 0.40])
        label = int(label_arr[0])
    else:
        label_arr, averaged = soft_vote(probabilities)
        label = int(label_arr[0])

    confidence = float(averaged[0, label])
    output = {
        "predictedClass": CLASS_NAMES[label],
        "confidence": round(confidence, 6),
        "decision": "accept" if confidence >= args.threshold else "manual_review",
        "inferenceTimeMs": round((time.perf_counter() - start) * 1000, 3),
        "ensembleMethod": args.method,
        "individualModelPredictions": {
            name: CLASS_NAMES[int(prob[0].argmax())]
            for name, prob in zip(MODEL_NAMES, probabilities)
        },
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
