import os
import sys
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Allow importing files from the src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_and_prepare_data
from models import (
    build_baseline_cnn,
    build_regularized_cnn,
    build_deep_cnn
)


# ============================================================
# CONFIGURATION
# ============================================================

EPOCHS = 20
BATCH_SIZE = 64
LEARNING_RATE = 0.001

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# DATA AUGMENTATION
# ============================================================

def create_data_generator():

    datagen = ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True
    )

    return datagen


# ============================================================
# COMPILE MODEL
# ============================================================

def compile_model(model):

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ============================================================
# TRAIN ONE MODEL
# ============================================================

def train_model(model, model_name, X_train, y_train, X_val, y_val):

    print("\n" + "=" * 70)
    print(f"TRAINING: {model_name.upper()}")
    print("=" * 70)

    checkpoint_path = os.path.join(
        MODEL_DIR,
        f"{model_name}.keras"
    )

    callbacks = [

        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        ModelCheckpoint(
            checkpoint_path,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),

        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=0.00001,
            verbose=1
        )
    ]

    datagen = create_data_generator()

    history = model.fit(
        datagen.flow(
            X_train,
            y_train,
            batch_size=BATCH_SIZE
        ),
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )

    return history


# ============================================================
# MAIN TRAINING PIPELINE
# ============================================================

def main():

    # Load dataset
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        class_names
    ) = load_and_prepare_data()

    # --------------------------------------------------------
    # CNN 1 - BASELINE
    # --------------------------------------------------------

    baseline_model = build_baseline_cnn()

    compile_model(baseline_model)

    train_model(
        baseline_model,
        "baseline_cnn",
        X_train,
        y_train,
        X_val,
        y_val
    )

    # Clear session to free memory
    tf.keras.backend.clear_session()

    # --------------------------------------------------------
    # CNN 2 - REGULARIZED
    # --------------------------------------------------------

    regularized_model = build_regularized_cnn()

    compile_model(regularized_model)

    train_model(
        regularized_model,
        "regularized_cnn",
        X_train,
        y_train,
        X_val,
        y_val
    )

    tf.keras.backend.clear_session()

    # --------------------------------------------------------
    # CNN 3 - DEEP
    # --------------------------------------------------------

    deep_model = build_deep_cnn()

    compile_model(deep_model)

    train_model(
        deep_model,
        "deep_cnn",
        X_train,
        y_train,
        X_val,
        y_val
    )

    print("\n" + "=" * 70)
    print("ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 70)

    print("\nSaved models:")

    for file in os.listdir(MODEL_DIR):
        print("-", file)


if __name__ == "__main__":
    main()