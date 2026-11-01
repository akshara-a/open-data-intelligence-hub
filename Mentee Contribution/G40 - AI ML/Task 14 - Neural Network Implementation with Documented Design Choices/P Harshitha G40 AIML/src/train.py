import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25

MODEL_PATH = "models/best_cnn_model.keras"
MODEL_SUMMARY_PATH = "reports/model_summary.txt"
HISTORY_PATH = "reports/history.json"


def build_model():
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.05),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10)
    ], name="data_augmentation")

    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),

        data_augmentation,

        layers.Rescaling(1.0 / 255),

        layers.Conv2D(
            32,
            3,
            activation="relu",
            name="conv2d_1"
        ),
        layers.MaxPooling2D(
            name="maxpool_1"
        ),

        layers.Conv2D(
            64,
            3,
            activation="relu",
            name="conv2d_2"
        ),
        layers.MaxPooling2D(
            name="maxpool_2"
        ),

        layers.Conv2D(
            128,
            3,
            activation="relu",
            name="conv2d_3"
        ),
        layers.MaxPooling2D(
            name="maxpool_3"
        ),

        layers.GlobalAveragePooling2D(
            name="global_avg_pool"
        ),

        layers.Dropout(
            0.40,
            name="dropout"
        ),

        layers.Dense(
            64,
            activation="relu",
            name="dense_hidden"
        ),

        layers.Dense(
            1,
            activation="sigmoid",
            name="output_layer"
        )
    ], name="Casting_CNN_Classifier")

    return model


def main():

    # Create required folders
    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # --------------------------------------------------
    # Load Training Dataset
    # --------------------------------------------------

    train_dataset = tf.keras.utils.image_dataset_from_directory(
        "data/train",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=True,
        seed=42
    )

    # --------------------------------------------------
    # Load Validation Dataset
    # --------------------------------------------------

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        "data/validation",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )

    # --------------------------------------------------
    # Improve Dataset Performance
    # --------------------------------------------------

    train_dataset = train_dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    validation_dataset = validation_dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    # --------------------------------------------------
    # Build CNN Model
    # --------------------------------------------------

    model = build_model()

    # --------------------------------------------------
    # Compile Model
    # --------------------------------------------------

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(
                name="precision"
            ),
            tf.keras.metrics.Recall(
                name="recall"
            )
        ]
    )

    # --------------------------------------------------
    # Save Model Summary
    # --------------------------------------------------

    with open(
        MODEL_SUMMARY_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        model.summary(
            print_fn=lambda x: f.write(x + "\n")
        )

    print("Model summary saved to:", MODEL_SUMMARY_PATH)

    # --------------------------------------------------
    # Callbacks
    # --------------------------------------------------

    callbacks = [

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2
        )
    ]

    # --------------------------------------------------
    # Train Model
    # --------------------------------------------------

    print("\nStarting CNN model training...\n")

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    # --------------------------------------------------
    # Save Best Model
    # --------------------------------------------------

    model.save(MODEL_PATH)

    print(
        f"\nModel saved successfully to {MODEL_PATH}"
    )

    # --------------------------------------------------
    # Save Training History
    # --------------------------------------------------

    history_dict = {
        key: [float(value) for value in values]
        for key, values in history.history.items()
    }

    with open(
        HISTORY_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            history_dict,
            f,
            indent=4
        )

    print(
        f"Training history saved to {HISTORY_PATH}"
    )

    print("\nTraining finished successfully!")


if __name__ == "__main__":
    main()