import numpy as np
import tensorflow as tf

from sklearn.metrics import accuracy_score

from src.predict import get_predictions
from src.ensemble import soft_voting


def make_robustness_variants(
    images
):

    tensor = tf.convert_to_tensor(
        images,
        dtype=tf.float32
    )

    variants = {}

    variants["Original"] = tensor

    variants["Rotated"] = tf.image.rot90(
        tensor,
        k=1
    )

    variants["Blurred"] = tf.nn.avg_pool2d(
        tensor,
        ksize=3,
        strides=1,
        padding="SAME"
    )

    noise = tf.random.normal(
        tf.shape(tensor),
        mean=0.0,
        stddev=0.08
    )

    variants["Noisy"] = tf.clip_by_value(
        tensor + noise,
        0.0,
        1.0
    )

    variants["Darkened"] = tf.clip_by_value(
        tensor * 0.55,
        0.0,
        1.0
    )

    variants["Brightened"] = tf.clip_by_value(
        tensor * 1.35,
        0.0,
        1.0
    )

    return {
        name: value.numpy()
        for name, value in variants.items()
    }


def run_robustness_test(
    models,
    X_test,
    y_test
):

    variants = make_robustness_variants(
        X_test
    )

    results = []

    for condition, images in variants.items():

        probabilities = []

        model_predictions = []

        for model in models:

            probability, prediction = (
                get_predictions(
                    model,
                    images
                )
            )

            probabilities.append(
                probability
            )

            model_predictions.append(
                prediction
            )

        _, ensemble_prediction = (
            soft_voting(
                probabilities
            )
        )

        results.append({

            "condition": condition,

            "cnn1_accuracy":
                accuracy_score(
                    y_test,
                    model_predictions[0]
                ),

            "cnn2_accuracy":
                accuracy_score(
                    y_test,
                    model_predictions[1]
                ),

            "cnn3_accuracy":
                accuracy_score(
                    y_test,
                    model_predictions[2]
                ),

            "ensemble_accuracy":
                accuracy_score(
                    y_test,
                    ensemble_prediction
                )
        })

    return results