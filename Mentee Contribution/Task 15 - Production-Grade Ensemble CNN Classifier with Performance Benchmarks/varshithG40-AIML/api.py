"""
api.py
======
High-performance FastAPI backend server for the Production-Grade Ensemble CNN Classifier.
Serves:
  - REST API endpoints for live inference, perturbations, benchmarks, and dataset previews
  - Static modern HTML/CSS/JS frontend dashboard
"""

import os
import io
import time
import base64
import numpy as np
from PIL import Image
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn

from src.data_loader import prepare_dataset, CLASSES
from src.preprocessing import load_full_dataset, preprocess_image, IDX_TO_CLASS, IMAGE_SIZE
from src.predict import ProductionPredictor
from src.robustness_test import (
    apply_rotation, apply_gaussian_blur, apply_gaussian_noise, apply_illumination, apply_center_crop
)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
DATA_DIR = os.path.join(ROOT_DIR, "data")

app = FastAPI(title="Ensemble CNN Classifier API", version="2.0.0")

# CORS middleware for seamless communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Predictor Instance
predictor: Optional[ProductionPredictor] = None


@app.on_event("startup")
def startup_event():
    global predictor
    print("[API] Initializing Production Predictor and loading models...")
    prepare_dataset(force=False)
    predictor = ProductionPredictor(confidence_threshold=0.70)
    print("[API] Production Predictor loaded and ready.")


def image_to_base64(img: Image.Image, format="JPEG") -> str:
    buffered = io.BytesIO()
    img.save(buffered, format=format, quality=90)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": predictor is not None,
        "classes": CLASSES,
        "dataset_resolution": f"{IMAGE_SIZE[0]}x{IMAGE_SIZE[1]}"
    }


@app.get("/api/dataset/samples")
def get_dataset_samples():
    """Returns metadata and base64 thumbnails for test partition samples."""
    _, _, (X_test, y_test), test_paths = load_full_dataset()
    samples = []
    
    for idx in range(len(X_test)):
        img_arr = (X_test[idx] * 255).astype(np.uint8)
        pil_img = Image.fromarray(img_arr)
        b64 = image_to_base64(pil_img)
        actual_label = IDX_TO_CLASS[int(np.argmax(y_test[idx]))]
        
        samples.append({
            "id": idx,
            "filename": os.path.basename(test_paths[idx]),
            "label": actual_label,
            "thumbnail": f"data:image/jpeg;base64,{b64}"
        })
        
    return {"total": len(samples), "samples": samples}


@app.post("/api/predict")
async def predict_image(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[int] = Form(None),
    strategy: str = Form("soft"),
    confidence_threshold: float = Form(0.70)
):
    """
    Runs multi-model inference and ensemble voting on uploaded image or sample index.
    """
    global predictor
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded yet.")
        
    predictor.confidence_threshold = confidence_threshold
    
    # 1. Process Input Image
    if file is not None:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
        processed_input = np.array(pil_img.resize(IMAGE_SIZE)) / 255.0
        img_b64 = image_to_base64(pil_img)
    elif sample_id is not None:
        _, _, (X_test, y_test), _ = load_full_dataset()
        if sample_id < 0 or sample_id >= len(X_test):
            raise HTTPException(status_code=400, detail="Invalid sample_id.")
        processed_input = X_test[sample_id]
        pil_img = Image.fromarray((processed_input * 255).astype(np.uint8))
        img_b64 = image_to_base64(pil_img)
    else:
        raise HTTPException(status_code=400, detail="Must provide either 'file' or 'sample_id'.")

    # 2. Run Inference
    resp = predictor.predict(
        processed_input,
        ensemble_strategy=strategy,
        include_debug_models=True
    )
    
    resp["inputImageBase64"] = f"data:image/jpeg;base64,{img_b64}"
    resp["strategyUsed"] = strategy
    resp["confidenceThreshold"] = confidence_threshold
    
    return resp


@app.post("/api/perturb")
async def perturb_and_test(
    sample_id: int = Form(0),
    rotation_deg: float = Form(0.0),
    blur_ksize: int = Form(0),
    noise_sigma: float = Form(0.0),
    illumination: float = Form(1.0),
    crop_ratio: float = Form(1.0)
):
    """
    Applies live image perturbations and runs real-time multi-model stress testing.
    """
    global predictor
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded.")
        
    _, _, (X_test, y_test), _ = load_full_dataset()
    base_img = X_test[sample_id:sample_id+1].copy()
    
    # Apply perturbations sequentially
    pert_img = base_img
    if rotation_deg != 0.0:
        pert_img = apply_rotation(pert_img, rotation_deg)
    if blur_ksize > 1:
        if blur_ksize % 2 == 0:
            blur_ksize += 1
        pert_img = apply_gaussian_blur(pert_img, blur_ksize, sigma=2.0)
    if noise_sigma > 0.0:
        pert_img = apply_gaussian_noise(pert_img, mean=0.0, sigma=noise_sigma)
    if illumination != 1.0:
        pert_img = apply_illumination(pert_img, illumination)
    if crop_ratio < 1.0 and crop_ratio > 0.3:
        pert_img = apply_center_crop(pert_img, crop_ratio)

    single_pert = pert_img[0]
    pil_pert = Image.fromarray((single_pert * 255).astype(np.uint8))
    b64_pert = image_to_base64(pil_pert)
    
    # Run prediction on perturbed image
    resp = predictor.predict(single_pert, ensemble_strategy="soft", include_debug_models=True)
    resp["perturbedImageBase64"] = f"data:image/jpeg;base64,{b64_pert}"
    resp["actualLabel"] = IDX_TO_CLASS[int(np.argmax(y_test[sample_id]))]
    
    return resp


@app.get("/api/benchmarks")
def get_benchmarks():
    """Returns final unified comparison table and performance benchmark records."""
    csv_final = os.path.join(RESULTS_DIR, "final_comparison.csv")
    csv_bench = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    
    import pandas as pd
    final_data = []
    bench_data = []
    
    if os.path.exists(csv_final):
        df_f = pd.read_csv(csv_final)
        final_data = df_f.to_dict(orient="records")
        
    if os.path.exists(csv_bench):
        df_b = pd.read_csv(csv_bench)
        bench_data = df_b.to_dict(orient="records")
        
    return {
        "final_comparison": final_data,
        "detailed_benchmarks": bench_data
    }


@app.get("/api/robustness")
def get_robustness_metrics():
    """Returns robustness benchmark table."""
    csv_rob = os.path.join(RESULTS_DIR, "robustness_results.csv")
    import pandas as pd
    if os.path.exists(csv_rob):
        df_r = pd.read_csv(csv_rob)
        return {"robustness_results": df_r.to_dict(orient="records")}
    return {"robustness_results": []}


# Serve Results Static Images (Training Curves, Confusion Matrices, Robustness Plots)
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")

# Serve Frontend App Assets (HTML/CSS/JS)
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
