"""
Training Pipeline for Automated Casting Defect Detection System
Compiles model, configures regularization callbacks, fits dataset, saves best weights, and plots training history.
"""

import os
import tensorflow as tf
from src.data_loader import load_casting_datasets
from src.model import build_casting_cnn_model
from src.utils import plot_training_history, ensure_directories

def train_model(
    train_dir="data/train",
    test_dir="data/test",
    model_save_path="models/best_casting_defect_model.keras",
    reports_dir="reports",
    epochs=15,
    batch_size=32,
    learning_rate=0.001
):
    """
    Train CNN model with Adam optimizer, binary cross-entropy, and regularization callbacks.
    
    Args:
        train_dir: Path to training image directory.
        test_dir: Path to test image directory.
        model_save_path: Filepath to save best trained model (.keras format).
        reports_dir: Path to output report graphs directory.
        epochs: Maximum number of training epochs.
        batch_size: Training batch size.
        learning_rate: Initial Adam optimizer learning rate.
        
    Returns:
        tuple: (trained_model, history)
    """
    ensure_directories([os.path.dirname(model_save_path), reports_dir])

    # 1. Load Datasets
    train_dataset, validation_dataset, _ = load_casting_datasets(
        train_dir=train_dir,
        test_dir=test_dir,
        batch_size=batch_size
    )

    # 2. Build CNN Model
    print("\nBuilding CNN Architecture...")
    model = build_casting_cnn_model()
    model.summary()

    # 3. Compile Model
    print("\nCompiling model with Adam optimizer and binary crossentropy loss...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")
        ]
    )

    # 4. Configure Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=0.000001,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=model_save_path,
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        )
    ]

    # 5. Fit Model
    print(f"\nStarting model training for up to {epochs} epochs...")
    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=epochs,
        callbacks=callbacks
    )

    # 6. Save Training History Visualizations
    print("\nPlotting and saving training performance graphs...")
    plot_training_history(history, save_dir=reports_dir)

    print(f"\nTraining completed successfully! Best model saved to '{model_save_path}'.")
    return model, history

if __name__ == "__main__":
    train_model()
