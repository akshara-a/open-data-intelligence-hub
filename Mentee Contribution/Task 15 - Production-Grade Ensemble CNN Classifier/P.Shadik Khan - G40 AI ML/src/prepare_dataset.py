from pathlib import Path
import random
import shutil

# Source dataset
SOURCE_DIR = Path(r"C:\Users\patan\Downloads\archive (3)\casting_512x512\casting_512x512")

# Task 15 destination
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Reproducible split
SEED = 42
random.seed(SEED)

# Split ratios
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

CLASSES = ["def_front", "ok_front"]


def prepare_directories():
    """Create train, validation and test directories."""
    for split in ["train", "validation", "test"]:
        for class_name in CLASSES:
            folder = DATA_DIR / split / class_name
            folder.mkdir(parents=True, exist_ok=True)


def split_files(files):
    """Shuffle and split files into train, validation and test."""
    random.shuffle(files)

    total = len(files)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]

    return train_files, val_files, test_files


def copy_files(files, destination):
    """Copy image files to destination."""
    for file_path in files:
        shutil.copy2(file_path, destination / file_path.name)


def main():
    print("=" * 60)
    print("TASK 15 - DATASET PREPARATION")
    print("=" * 60)

    if not SOURCE_DIR.exists():
        raise FileNotFoundError(
            f"Dataset not found: {SOURCE_DIR}"
        )

    prepare_directories()

    total_copied = 0

    for class_name in CLASSES:
        source_class_dir = SOURCE_DIR / class_name

        if not source_class_dir.exists():
            raise FileNotFoundError(
                f"Class folder not found: {source_class_dir}"
            )

        files = [
            file_path
            for file_path in source_class_dir.iterdir()
            if file_path.is_file()
        ]

        print(f"\nClass: {class_name}")
        print(f"Original images: {len(files)}")

        train_files, val_files, test_files = split_files(files)

        copy_files(
            train_files,
            DATA_DIR / "train" / class_name
        )

        copy_files(
            val_files,
            DATA_DIR / "validation" / class_name
        )

        copy_files(
            test_files,
            DATA_DIR / "test" / class_name
        )

        print(f"Train:      {len(train_files)}")
        print(f"Validation: {len(val_files)}")
        print(f"Test:       {len(test_files)}")

        total_copied += len(files)

    print("\n" + "=" * 60)
    print(f"Total images processed: {total_copied}")
    print(f"Dataset output: {DATA_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()