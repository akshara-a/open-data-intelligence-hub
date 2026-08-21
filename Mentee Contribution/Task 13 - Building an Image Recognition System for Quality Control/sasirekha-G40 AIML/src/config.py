"""
Centralized configuration for the Casting Quality Inspection project.

All paths are built with pathlib relative to the project root, so the
project works after being copied to a different computer or cloned
from GitHub, regardless of operating system.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------
# config.py lives in <root>/src/config.py, so the root is two levels up.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Dataset paths
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"

# ---------------------------------------------------------------------------
# Model paths
# ---------------------------------------------------------------------------
MODELS_DIR = PROJECT_ROOT / "models"
BEST_MODEL_PATH = MODELS_DIR / "best_casting_defect_model.keras"

# ---------------------------------------------------------------------------
# Report / output paths
# ---------------------------------------------------------------------------
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"

TRAINING_ACCURACY_PLOT = FIGURES_DIR / "training_accuracy.png"
TRAINING_LOSS_PLOT = FIGURES_DIR / "training_loss.png"
CONFUSION_MATRIX_PLOT = FIGURES_DIR / "confusion_matrix.png"
THRESHOLD_RECALL_PLOT = FIGURES_DIR / "threshold_vs_recall.png"

MODEL_SUMMARY_PATH = METRICS_DIR / "model_summary.txt"
CLASSIFICATION_REPORT_PATH = METRICS_DIR / "classification_report.json"
TEST_METRICS_PATH = METRICS_DIR / "test_metrics.json"
CONFUSION_MATRIX_JSON_PATH = METRICS_DIR / "confusion_matrix.json"
THRESHOLD_ANALYSIS_PATH = METRICS_DIR / "threshold_analysis.csv"

# ---------------------------------------------------------------------------
# Sample images (used for ad-hoc single-image prediction / demos)
# ---------------------------------------------------------------------------
SAMPLE_IMAGES_DIR = PROJECT_ROOT / "sample_images"

# ---------------------------------------------------------------------------
# Image / dataset parameters
# ---------------------------------------------------------------------------
IMAGE_SIZE = (128, 128)      # (height, width) fed into the CNN
BATCH_SIZE = 64
VALIDATION_SPLIT = 0.20      # 20% of the TRAIN directory becomes validation
RANDOM_SEED = 42             # fixed seed for reproducible splits

# ---------------------------------------------------------------------------
# Class mapping
# ---------------------------------------------------------------------------
# IMPORTANT: This order is enforced explicitly everywhere in the project
# (data_loader.py passes this exact list as `class_names` to
# image_dataset_from_directory) so the mapping never silently depends on
# alphabetical folder ordering.
#
#   ok_front  -> 0 -> Non-defective
#   def_front -> 1 -> Defective
CLASS_FOLDER_NAMES = ["ok_front", "def_front"]
CLASS_DISPLAY_NAMES = ["Non-defective", "Defective"]
CLASS_MAPPING = {"ok_front": 0, "def_front": 1}

# ---------------------------------------------------------------------------
# Training hyperparameters
# ---------------------------------------------------------------------------
LEARNING_RATE = 0.001
EPOCHS = 25

EARLY_STOPPING_PATIENCE = 5
REDUCE_LR_FACTOR = 0.5
REDUCE_LR_PATIENCE = 2
REDUCE_LR_MIN_LR = 1e-6

DROPOUT_1 = 0.40   # after GlobalAveragePooling2D
DROPOUT_2 = 0.30   # after the dense layer

# ---------------------------------------------------------------------------
# Prediction / decision threshold
# ---------------------------------------------------------------------------
DEFAULT_THRESHOLD = 0.40  # selected after reviewing threshold_analysis.csv:
# cuts false negatives roughly in half vs. 0.50 (21 vs 47) at a small
# accuracy cost, prioritizing recall on the defective class per the
# project's quality-control objective.
THRESHOLDS_TO_EVALUATE = [0.30, 0.40, 0.50, 0.60, 0.70]

# ---------------------------------------------------------------------------
# Ensure output directories exist whenever config is imported
# ---------------------------------------------------------------------------
for directory in (MODELS_DIR, FIGURES_DIR, METRICS_DIR, SAMPLE_IMAGES_DIR):
    directory.mkdir(parents=True, exist_ok=True)
