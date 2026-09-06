from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"

CLASS_NAMES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]

IMAGE_SIZE = (96, 96)   # Faster and sufficient for NEU-DET texture classification
SEED = 42
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15
BATCH_SIZE = 32
MAX_EPOCHS = 25
LEARNING_RATE = 3e-4

def find_dataset_dir():
    """Find the NEU-DET image folder automatically."""
    candidates = [
        ROOT / "data" / "raw" / "NEU-DET" / "train" / "images",
        ROOT / "data" / "NEU-DET" / "train" / "images",
        ROOT / "data" / "raw" / "images",
        ROOT / "data" / "images",
    ]
    for candidate in candidates:
        if candidate.exists() and all((candidate / c).exists() for c in CLASS_NAMES):
            return candidate
    return candidates[0]

DATASET_DIR = find_dataset_dir()
