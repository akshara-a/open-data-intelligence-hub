"""
Training pipeline for the casting defect CNN.

Run from the project root with:

    python -m src.train
"""

import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(0)  # 0 = use all cores
tf.config.threading.set_inter_op_parallelism_threads(0)
import io

import matplotlib.pyplot as plt
import tensorflow as tf

from src import config
from src.data_loader import load_train_validation_test_datasets
from src.model import create_and_compile_model
from src.utils import get_logger, set_global_seeds

logger = get_logger(__name__)


def build_callbacks() -> list:
    """
    Build the regularization / production-robustness callbacks:

    - EarlyStopping: stops training once validation loss stops improving,
      and restores the best-performing weights.
    - ReduceLROnPlateau: shrinks the learning rate when training stalls,
      allowing finer weight updates instead of overshooting.
    - ModelCheckpoint: saves only the best model (by validation loss) to
      disk, so the final saved model is not necessarily the last epoch.
    """
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=config.REDUCE_LR_FACTOR,
            patience=config.REDUCE_LR_PATIENCE,
            min_lr=config.REDUCE_LR_MIN_LR,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(config.BEST_MODEL_PATH),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]


def save_model_summary(model: tf.keras.Model) -> None:
    """Print the model summary to the console and save it to a text file."""
    stream = io.StringIO()
    model.summary(print_fn=lambda line: stream.write(line + "\n"))
    summary_text = stream.getvalue()

    print(summary_text)

    config.MODEL_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(config.MODEL_SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write(summary_text)

    logger.info("Model summary saved to: %s", config.MODEL_SUMMARY_PATH)


def plot_training_history(history: tf.keras.callbacks.History) -> None:
    """
    Generate and save the training/validation accuracy and loss graphs
    to reports/figures/.
    """
    training_accuracy = history.history["accuracy"]
    validation_accuracy = history.history["val_accuracy"]
    training_loss = history.history["loss"]
    validation_loss = history.history["val_loss"]

    epochs_range = range(1, len(training_accuracy) + 1)

    # Accuracy plot
    plt.figure(figsize=(8, 5))
    plt.plot(epochs_range, training_accuracy, label="Training Accuracy")
    plt.plot(epochs_range, validation_accuracy, label="Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(config.TRAINING_ACCURACY_PLOT, dpi=200)
    plt.close()
    logger.info("Saved: %s", config.TRAINING_ACCURACY_PLOT)

    # Loss plot
    plt.figure(figsize=(8, 5))
    plt.plot(epochs_range, training_loss, label="Training Loss")
    plt.plot(epochs_range, validation_loss, label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(config.TRAINING_LOSS_PLOT, dpi=200)
    plt.close()
    logger.info("Saved: %s", config.TRAINING_LOSS_PLOT)


def main():
    set_global_seeds(config.RANDOM_SEED)

    logger.info("Loading dataset")
    train_dataset, validation_dataset, test_dataset = load_train_validation_test_datasets()

    logger.info("Creating model")
    model = create_and_compile_model()
    save_model_summary(model)

    callbacks = build_callbacks()

    logger.info("Starting training (up to %d epochs, early stopping enabled)", config.EPOCHS)
    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=config.EPOCHS,
        callbacks=callbacks,
    )

    logger.info("Saving best model to: %s", config.BEST_MODEL_PATH)
    # ModelCheckpoint already saved the best-validation-loss weights to disk.
    # We also explicitly save here in case training completed without a
    # checkpoint improvement being triggered (e.g. very short runs).
    model.save(config.BEST_MODEL_PATH)

    plot_training_history(history)

    logger.info(
        "Training complete. Run `python -m src.evaluate` to evaluate on "
        "the held-out test dataset."
    )


if __name__ == "__main__":
    main()
