import os
import io
import glob
import numpy as np
from PIL import Image
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Casting Quality Inspection AI",
    description="Deep Learning CNN Binary Image Classification Interface",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model once at startup
MODEL_PATH = "models/cnn_casting_model.keras"
model = None

if os.path.exists(MODEL_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Loaded trained CNN model successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Warning: Model file not found at {MODEL_PATH}")

# Ensure static directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("plots", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/plots", StaticFiles(directory="plots"), name="plots")
app.mount("/data", StaticFiles(directory="data"), name="data")

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocesses raw bytes into (1, 224, 224, 3) tensor."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    img_batch = np.expand_dims(img_array, axis=0) # shape (1, 224, 224, 3)
    return img_batch

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_file = "static/index.html"
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Frontend loading... Please refresh.</h1>")

@app.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Trained CNN model is not loaded.")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    
    contents = await file.read()
    try:
        input_tensor = preprocess_image(contents)
        raw_pred = model.predict(input_tensor, verbose=0)[0][0]
        prob_defective = float(raw_pred)
        
        is_defective = prob_defective >= 0.5
        confidence = prob_defective * 100 if is_defective else (1.0 - prob_defective) * 100
        
        status_label = "Defective" if is_defective else "Non-defective"
        class_id = 1 if is_defective else 0
        action = "Send for manual inspection & quarantine" if is_defective else "Passed automated quality check"
        badge_color = "danger" if is_defective else "success"
        
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "prediction": status_label,
            "class_id": class_id,
            "defective_probability": round(prob_defective, 4),
            "confidence_percent": round(confidence, 1),
            "action_recommendation": action,
            "badge_color": badge_color
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/api/samples")
async def get_unseen_samples():
    """Returns list of unseen sample images available for 1-click testing."""
    unseen_files = sorted(glob.glob("data/unseen/*.png"))
    samples = []
    for filepath in unseen_files:
        filename = os.path.basename(filepath)
        label = "Defective" if "def_front" in filename else "Non-defective"
        samples.append({
            "id": filename,
            "filename": filename,
            "path": f"/data/unseen/{filename}",
            "ground_truth": label
        })
    return JSONResponse({"samples": samples})

@app.get("/api/decision-table")
async def get_decision_table():
    """Returns the 16 Design Decision items."""
    table = [
        {"decision": "Image size", "value": "224 x 224", "reason": "Balance between detail and computation"},
        {"decision": "Problem type", "value": "Binary classification", "reason": "Two output classes (Non-defective vs Defective)"},
        {"decision": "Model type", "value": "CNN", "reason": "Suitable for spatial image pattern extraction"},
        {"decision": "Conv filters", "value": "32, 64, 128", "reason": "Learn increasingly complex features"},
        {"decision": "Kernel size", "value": "3 x 3", "reason": "Efficient local feature extraction"},
        {"decision": "Hidden activation", "value": "ReLU", "reason": "Efficient and prevents vanishing gradients"},
        {"decision": "Pooling", "value": "MaxPooling", "reason": "Reduces feature map spatial dimensions"},
        {"decision": "Output activation", "value": "Sigmoid", "reason": "Produces binary probability [0.0, 1.0]"},
        {"decision": "Optimizer", "value": "Adam", "reason": "Adaptive learning rates and beginner-friendly"},
        {"decision": "Learning rate", "value": "0.001", "reason": "Reasonable Adam starting value"},
        {"decision": "Loss", "value": "Binary Cross-Entropy", "reason": "Loss metric specifically for binary targets"},
        {"decision": "Batch size", "value": "32", "reason": "Balanced memory usage and gradient stability"},
        {"decision": "Epochs", "value": "Maximum 25", "reason": "Sufficient training protected by early stopping"},
        {"decision": "Dropout", "value": "0.40", "reason": "Helps reduce hidden neuron overfitting"},
        {"decision": "Augmentation", "value": "Flip, rotation, zoom, contrast", "reason": "Improves model real-world robustness"},
        {"decision": "Metrics", "value": "Accuracy, Precision, Recall", "reason": "Evaluate overall accuracy and defect detection safety"}
    ]
    return JSONResponse({"decision_table": table})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
