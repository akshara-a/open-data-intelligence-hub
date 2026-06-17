import json
import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "salary_model.pkl"
METADATA_PATH = ROOT / "model_metadata.json"

app = Flask(__name__, static_folder=".", static_url_path="")

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)

with METADATA_PATH.open("r", encoding="utf-8") as metadata_file:
    metadata = json.load(metadata_file)


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.route("/metadata")
def get_metadata():
    return jsonify(metadata)


@app.route("/predict", methods=["POST"])
def predict_salary():
    request_data = request.get_json(silent=True) or {}
    country = request_data.get("Country")
    years = request_data.get("YearsCodePro")
    remote_work = request_data.get("RemoteWork")

    if country is None or years is None or remote_work is None:
        return jsonify({"error": "Country, YearsCodePro, and RemoteWork are required."}), 400

    try:
        years_value = float(years)
    except (TypeError, ValueError):
        return jsonify({"error": "YearsCodePro must be a number."}), 400

    features = pd.DataFrame([
        {
            "Country": country,
            "YearsCodePro": years_value,
            "RemoteWork": remote_work,
        }
    ])

    try:
        predicted_value = model.predict(features)[0]
        
        # Calculate career trajectory
        trajectory_years = [1, 3, 5, 10, 15]
        trajectory_features = pd.DataFrame([
            {
                "Country": country,
                "YearsCodePro": float(y),
                "RemoteWork": remote_work,
            } for y in trajectory_years
        ])
        trajectory_preds = model.predict(trajectory_features)
        trajectory = [{"years": y, "salary": round(float(p), 2)} for y, p in zip(trajectory_years, trajectory_preds)]
        
    except Exception as exc:
        return jsonify({"error": f"Prediction failed: {str(exc)}"}), 500

    return jsonify({
        "predictedSalary": round(float(predicted_value), 2),
        "trajectory": trajectory
    })


@app.route("/<path:path>")
def static_file(path: str):
    return send_from_directory(ROOT, path)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", debug=False, port=port)
