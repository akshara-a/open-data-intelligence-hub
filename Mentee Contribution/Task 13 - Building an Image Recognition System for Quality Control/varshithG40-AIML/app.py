"""
Flask Web Application Backend for Industrial Casting Defect Detection
Serves modern web UI and provides REST API for CNN model inference & heatmaps.
"""

import os
import sys
import base64
import numpy as np
import cv2
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

MODEL_PATH = "models/best_casting_defect_model.keras"
model = None

def load_keras_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"Loaded model successfully from '{MODEL_PATH}'.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Model file not found at '{MODEL_PATH}'. Run train.py first.")

load_keras_model()

def generate_defect_heatmap(img_np):
    """Generate visual defect heatmap highlighting surface cracks and anomalies."""
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding to detect surface anomalies & cracks
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Create colored heatmap overlay (Neon Red for defects)
    heatmap = cv2.applyColorMap(thresh, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_np, 0.65, heatmap, 0.35, 0)
    
    # Encode to base64 string
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    b64_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_str}"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/sample_images/<path:filename>")
def serve_sample_image(filename):
    return send_from_directory("sample_images", filename)

@app.route("/reports/<path:filename>")
def serve_report_image(filename):
    return send_from_directory("reports", filename)

@app.route("/api/samples", methods=["GET"])
def get_samples():
    sample_dir = "sample_images"
    samples = []
    if os.path.exists(sample_dir):
        files = sorted([f for f in os.listdir(sample_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
        for f in files:
            is_def = "def" in f.lower()
            samples.append({
                "filename": f,
                "url": f"/sample_images/{f}",
                "expected_class": "Defective" if is_def else "Non-defective"
            })
    return jsonify({"success": True, "samples": samples})

@app.route("/api/predict", methods=["POST"])
def predict():
    global model
    if model is None:
        load_keras_model()
        if model is None:
            return jsonify({"success": False, "error": "Model not loaded. Please run python -m src.train first."}), 500

    threshold = float(request.form.get("threshold", 0.50))
    sample_filename = request.form.get("sample_filename", None)
    
    img_np = None
    filename = "upload.jpg"

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filename = file.filename
        pil_img = Image.open(file.stream).convert('RGB')
        img_np = np.array(pil_img)
    elif sample_filename:
        sample_path = os.path.join("sample_images", sample_filename)
        if os.path.exists(sample_path):
            filename = sample_filename
            pil_img = Image.open(sample_path).convert('RGB')
            img_np = np.array(pil_img)
        else:
            return jsonify({"success": False, "error": f"Sample image '{sample_filename}' not found."}), 404
    else:
        return jsonify({"success": False, "error": "No image file or sample_filename provided."}), 400

    # Resize to 224x224 for CNN model input
    pil_resized = Image.fromarray(img_np).resize((224, 224))
    input_array = np.array(pil_resized, dtype=np.float32)
    input_batch = np.expand_dims(input_array, axis=0)

    # Perform CNN model prediction
    prob = float(model.predict(input_batch, verbose=0)[0][0])
    is_defective = prob >= threshold
    verdict = "Defective" if is_defective else "Non-defective"

    if is_defective:
        recommended_action = "🚨 Send product to manual review station / remove from assembly line."
    else:
        recommended_action = "🟢 Product passed quality inspection. Proceed on conveyor."

    # Encode original image to base64
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(np.array(pil_resized), cv2.COLOR_RGB2BGR))
    orig_b64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
    
    # Generate heatmap overlay
    heatmap_b64 = generate_defect_heatmap(np.array(pil_resized))

    return jsonify({
        "success": True,
        "filename": filename,
        "defect_probability": prob,
        "defect_percentage": round(prob * 100, 2),
        "threshold": threshold,
        "threshold_percentage": round(threshold * 100, 2),
        "verdict": verdict,
        "is_defective": is_defective,
        "recommended_action": recommended_action,
        "image_url": orig_b64,
        "heatmap_url": heatmap_b64,
        "dimensions": "224 x 224 px"
    })

if __name__ == "__main__":
    print("Starting AeroCast AI Industrial Server on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
