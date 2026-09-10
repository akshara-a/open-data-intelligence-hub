"""
robustness_test.py
==================
Evaluates out-of-distribution robustness and prediction stability under image perturbations:
  1. Original Clean Test Set
  2. Rotated Images (+/- 30 degrees)
  3. Blurred Images (Gaussian Blur)
  4. Noisy Images (Additive Gaussian Noise)
  5. Darkened Images (0.5x illumination)
  6. Brightened Images (1.5x illumination)
  7. Cropped Images (Center Zoom/Crop)
Saves results to results/robustness_results.csv and results/robustness_comparison.png.
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from tensorflow import keras

from .preprocessing import load_full_dataset
from .ensemble import EnsembleClassifier

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")


def apply_rotation(images: np.ndarray, angle: float = 30.0) -> np.ndarray:
    """Rotates images by given angle around center."""
    rotated = []
    h, w = images.shape[1], images.shape[2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    for img in images:
        rot = cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
        rotated.append(rot)
    return np.array(rotated, dtype=np.float32)


def apply_gaussian_blur(images: np.ndarray, ksize: int = 5, sigma: float = 2.0) -> np.ndarray:
    """Applies Gaussian smoothing filter to simulate lens defocus/blur."""
    blurred = []
    for img in images:
        b = cv2.GaussianBlur(img, (ksize, ksize), sigma)
        blurred.append(b)
    return np.array(blurred, dtype=np.float32)


def apply_gaussian_noise(images: np.ndarray, mean: float = 0.0, sigma: float = 0.15) -> np.ndarray:
    """Adds zero-mean Gaussian noise simulating sensor noise."""
    noisy = images + np.random.normal(mean, sigma, images.shape)
    return np.clip(noisy, 0.0, 1.0).astype(np.float32)


def apply_illumination(images: np.ndarray, factor: float = 0.5) -> np.ndarray:
    """Scales image brightness simulating low-light or over-exposed conditions."""
    adjusted = images * factor
    return np.clip(adjusted, 0.0, 1.0).astype(np.float32)


def apply_center_crop(images: np.ndarray, crop_ratio: float = 0.75) -> np.ndarray:
    """Crops central region and resizes back to original dimensions."""
    cropped = []
    h, w = images.shape[1], images.shape[2]
    ch, cw = int(h * crop_ratio), int(w * crop_ratio)
    y1, x1 = (h - ch) // 2, (w - cw) // 2
    for img in images:
        crop = img[y1:y1+ch, x1:x1+cw]
        resized = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)
        cropped.append(resized)
    return np.array(cropped, dtype=np.float32)


def evaluate_robustness_suite():
    """
    Executes perturbation stress-testing across CNN 1, CNN 2, CNN 3, and the Ensemble.
    """
    print("\n=======================================================")
    print(" Running Robustness & Stability Stress-Testing Suite")
    print("=======================================================")
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    _, _, (X_test, y_test), _ = load_full_dataset()
    y_true = np.argmax(y_test, axis=1)
    
    # Load Models
    m1 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_baseline.keras"))
    m2 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_regularized.keras"))
    m3 = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_deep.keras"))
    ensemble = EnsembleClassifier([m1, m2, m3])
    
    perturbations = {
        "Original (Clean)": X_test,
        "Rotated (+30°)": apply_rotation(X_test, 30.0),
        "Gaussian Blur": apply_gaussian_blur(X_test, 5, 2.0),
        "Gaussian Noise": apply_gaussian_noise(X_test, 0.0, 0.15),
        "Darkened (0.5x)": apply_illumination(X_test, 0.5),
        "Brightened (1.5x)": apply_illumination(X_test, 1.5),
        "Center Cropped": apply_center_crop(X_test, 0.75)
    }
    
    results = []
    for cond_name, X_pert in perturbations.items():
        # Evaluate CNN 1
        p1 = np.argmax(m1.predict(X_pert, verbose=0), axis=1)
        acc1 = accuracy_score(y_true, p1)
        
        # Evaluate CNN 2
        p2 = np.argmax(m2.predict(X_pert, verbose=0), axis=1)
        acc2 = accuracy_score(y_true, p2)
        
        # Evaluate CNN 3
        p3 = np.argmax(m3.predict(X_pert, verbose=0), axis=1)
        acc3 = accuracy_score(y_true, p3)
        
        # Evaluate Ensemble (Soft Voting)
        _, p_ens = ensemble.predict_soft_voting(X_pert)
        acc_ens = accuracy_score(y_true, p_ens)
        
        results.append({
            "Condition": cond_name,
            "CNN 1 (Baseline) (%)": round(acc1 * 100, 2),
            "CNN 2 (Regularized) (%)": round(acc2 * 100, 2),
            "CNN 3 (Deeper) (%)": round(acc3 * 100, 2),
            "Ensemble (Soft Voting) (%)": round(acc_ens * 100, 2),
            "Ensemble Advantage (%)": round((acc_ens - max(acc1, acc2, acc3)) * 100, 2)
        })
        
    df_robustness = pd.DataFrame(results)
    csv_path = os.path.join(RESULTS_DIR, "robustness_results.csv")
    df_robustness.to_csv(csv_path, index=False)
    print(f"[SAVE] Robustness results saved to: {csv_path}")
    print("\n", df_robustness.to_string(index=False))
    
    # Plot Robustness Comparison Chart
    plot_robustness_chart(df_robustness, os.path.join(RESULTS_DIR, "robustness_comparison.png"))
    return df_robustness


def plot_robustness_chart(df: pd.DataFrame, save_path: str):
    """
    Renders grouped comparison bar chart for all perturbation conditions.
    """
    conditions = df["Condition"].tolist()
    x = np.arange(len(conditions))
    width = 0.20
    
    plt.figure(figsize=(12, 6), dpi=300)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    plt.bar(x - 1.5*width, df["CNN 1 (Baseline) (%)"], width, label="CNN 1 (Baseline)", color="#94a3b8")
    plt.bar(x - 0.5*width, df["CNN 2 (Regularized) (%)"], width, label="CNN 2 (Regularized)", color="#3b82f6")
    plt.bar(x + 0.5*width, df["CNN 3 (Deeper) (%)"], width, label="CNN 3 (Deeper)", color="#8b5cf6")
    plt.bar(x + 1.5*width, df["Ensemble (Soft Voting) (%)"], width, label="Ensemble (Soft Voting)", color="#10b981", edgecolor="#047857", linewidth=1.5)
    
    plt.title("Robustness Stress-Test: Individual CNNs vs Ensemble Under Perturbations", fontsize=13, fontweight="bold", pad=14)
    plt.xlabel("Image Condition / Perturbation Type", fontsize=11, fontweight="bold", labelpad=10)
    plt.ylabel("Test Accuracy (%)", fontsize=11, fontweight="bold", labelpad=10)
    plt.xticks(x, conditions, rotation=15, ha="right", fontsize=10)
    plt.ylim([0, 110])
    plt.legend(frameon=True, fontsize=10, loc="upper right")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[PLOT] Saved robustness comparison chart: {save_path}")


if __name__ == "__main__":
    evaluate_robustness_suite()
