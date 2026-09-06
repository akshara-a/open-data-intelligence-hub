import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import Image
from .config import DATASET_DIR, CLASS_NAMES, SEED, TRAIN_RATIO, VALIDATION_RATIO, RESULTS_DIR

def validate_dataset():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            "NEU-DET images were not found. Expected a folder containing these six folders:\n"
            + ", ".join(CLASS_NAMES) + f"\nCurrent expected location: {DATASET_DIR}"
        )

    rows = []
    for label, class_name in enumerate(CLASS_NAMES):
        class_dir = DATASET_DIR / class_name
        if not class_dir.exists():
            raise FileNotFoundError(f"Missing class folder: {class_dir}")

        images = sorted(
            list(class_dir.glob("*.jpg")) +
            list(class_dir.glob("*.jpeg")) +
            list(class_dir.glob("*.png"))
        )

        valid_count = 0
        for image_path in images:
            try:
                with Image.open(image_path) as img:
                    img.verify()
                rows.append({
                    "path": str(image_path.resolve()),
                    "class_name": class_name,
                    "label": label,
                })
                valid_count += 1
            except Exception:
                print(f"Skipping unreadable image: {image_path}")

        if valid_count == 0:
            raise FileNotFoundError(f"No valid images found for class: {class_name}")

    df = pd.DataFrame(rows)
    counts = df["class_name"].value_counts()
    print("\nDataset found:", DATASET_DIR)
    print("Images per class:")
    print(counts.reindex(CLASS_NAMES).to_string())
    print("Total valid images:", len(df))
    return df

def create_or_load_splits(force_recreate=False):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    train_file = RESULTS_DIR / "train_split.csv"
    val_file = RESULTS_DIR / "validation_split.csv"
    test_file = RESULTS_DIR / "test_split.csv"

    if not force_recreate and train_file.exists() and val_file.exists() and test_file.exists():
        train_df = pd.read_csv(train_file)
        val_df = pd.read_csv(val_file)
        test_df = pd.read_csv(test_file)

        all_paths_exist = all(
            pd.Series(df["path"]).map(lambda p: str(p) != "" and __import__("pathlib").Path(p).exists()).all()
            for df in [train_df, val_df, test_df]
        )
        if all_paths_exist:
            return train_df, val_df, test_df

        print("Old split files contain invalid paths. Recreating splits...")

    df = validate_dataset()

    train_df, temp_df = train_test_split(
        df,
        test_size=(1 - TRAIN_RATIO),
        random_state=SEED,
        stratify=df["label"],
        shuffle=True,
    )

    val_fraction_of_temp = VALIDATION_RATIO / (1 - TRAIN_RATIO)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=(1 - val_fraction_of_temp),
        random_state=SEED,
        stratify=temp_df["label"],
        shuffle=True,
    )

    train_df.to_csv(train_file, index=False)
    val_df.to_csv(val_file, index=False)
    test_df.to_csv(test_file, index=False)

    print(f"\nSplit sizes: train={len(train_df)}, validation={len(val_df)}, test={len(test_df)}")
    return train_df, val_df, test_df
