import os
import numpy as np
import pandas as pd
import tensorflow as tf

from data_loader import load_cifar10_subset

print("=" * 60)
print("MODEL DISAGREEMENT AND CONFIDENCE ANALYSIS")
print("=" * 60)

# ---------------------------------------------------------
# Load test data
# ---------------------------------------------------------
print("\nLoading test dataset...")

X_test, y_test = load_cifar10_subset()

X_test = X_test.astype("float32") / 255.0

# Use 50 images to keep the laptop workload small
X_test = X_test[:50]
y_test = y_test[:50]

print("Test images:", X_test.shape)

# ---------------------------------------------------------
# Load models
# ---------------------------------------------------------
print("\nLoading models...")

model_paths = {
    "CNN1_Baseline": "models/cnn_baseline.keras",
    "CNN2_Regularized": "models/cnn_regularized.keras",
    "CNN3_Deep": "models/cnn_deep.keras"
}

models = {}

for name, path in model_paths.items():
    models[name] = tf.keras.models.load_model(path)
    print("Loaded:", name)

# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------
print("\nGenerating predictions...")

predictions = {}
probabilities = {}

for name, model in models.items():
    probs = model.predict(X_test, verbose=0)
    probabilities[name] = probs
    predictions[name] = np.argmax(probs, axis=1)

# ---------------------------------------------------------
# Prediction agreement
# ---------------------------------------------------------
p1 = predictions["CNN1_Baseline"]
p2 = predictions["CNN2_Regularized"]
p3 = predictions["CNN3_Deep"]

all_agree = (p1 == p2) & (p2 == p3)
any_disagree = ~all_agree

all_agree_rate = np.mean(all_agree)
disagreement_rate = np.mean(any_disagree)

print("\n" + "=" * 60)
print("AGREEMENT ANALYSIS")
print("=" * 60)

print(f"All three models agree: {all_agree_rate:.2%}")
print(f"Models disagree: {disagreement_rate:.2%}")

# ---------------------------------------------------------
# Pairwise disagreement
# ---------------------------------------------------------
d12 = np.mean(p1 != p2)
d13 = np.mean(p1 != p3)
d23 = np.mean(p2 != p3)

print("\nPairwise disagreement:")
print(f"CNN1 vs CNN2: {d12:.2%}")
print(f"CNN1 vs CNN3: {d13:.2%}")
print(f"CNN2 vs CNN3: {d23:.2%}")

# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------
confidences = {}

for name in models:
    confidences[name] = np.max(probabilities[name], axis=1)

print("\nAverage confidence:")

for name, conf in confidences.items():
    print(f"{name}: {np.mean(conf):.4f}")

# ---------------------------------------------------------
# Ensemble confidence
# ---------------------------------------------------------
ensemble_probs = (
    probabilities["CNN1_Baseline"]
    + probabilities["CNN2_Regularized"]
    + probabilities["CNN3_Deep"]
) / 3.0

ensemble_predictions = np.argmax(ensemble_probs, axis=1)
ensemble_confidence = np.max(ensemble_probs, axis=1)

print(f"Soft Voting Ensemble: {np.mean(ensemble_confidence):.4f}")

# ---------------------------------------------------------
# Save detailed results
# ---------------------------------------------------------
results = pd.DataFrame({
    "True_Label": y_test,
    "CNN1_Prediction": p1,
    "CNN2_Prediction": p2,
    "CNN3_Prediction": p3,
    "Ensemble_Prediction": ensemble_predictions,
    "CNN1_Confidence": confidences["CNN1_Baseline"],
    "CNN2_Confidence": confidences["CNN2_Regularized"],
    "CNN3_Confidence": confidences["CNN3_Deep"],
    "Ensemble_Confidence": ensemble_confidence,
    "All_Models_Agree": all_agree
})

os.makedirs("results", exist_ok=True)

output_path = "results/disagreement_results.csv"
results.to_csv(output_path, index=False)

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
summary = pd.DataFrame({
    "Metric": [
        "All Models Agreement Rate",
        "Overall Disagreement Rate",
        "CNN1 vs CNN2 Disagreement",
        "CNN1 vs CNN3 Disagreement",
        "CNN2 vs CNN3 Disagreement",
        "CNN1 Average Confidence",
        "CNN2 Average Confidence",
        "CNN3 Average Confidence",
        "Ensemble Average Confidence"
    ],
    "Value": [
        all_agree_rate,
        disagreement_rate,
        d12,
        d13,
        d23,
        np.mean(confidences["CNN1_Baseline"]),
        np.mean(confidences["CNN2_Regularized"]),
        np.mean(confidences["CNN3_Deep"]),
        np.mean(ensemble_confidence)
    ]
})

summary_path = "results/disagreement_summary.csv"
summary.to_csv(summary_path, index=False)

print("\nResults saved to:")
print(os.path.abspath(output_path))
print(os.path.abspath(summary_path))

print("\n" + "=" * 60)
print("DISAGREEMENT ANALYSIS COMPLETED")
print("=" * 60)