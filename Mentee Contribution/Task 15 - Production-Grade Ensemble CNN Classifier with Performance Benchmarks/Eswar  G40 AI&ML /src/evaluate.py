"""
evaluate.py

Per-model evaluation: accuracy/precision/recall/F1, confusion matrix,
latency, throughput, model size, and parameter count. Also handles the
train/val accuracy and loss curve plots.
"""

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def plot_history(history, name, results_dir="results"):
    epochs_range = range(1, len(history.history["accuracy"]) + 1)

    plt.figure(figsize=(7, 4))
    plt.plot(epochs_range, history.history["accuracy"], label="Training Accuracy")
    plt.plot(epochs_range, history.history["val_accuracy"], label="Validation Accuracy")
    plt.xlabel("Epoch"); plt.ylabel("Accuracy"); plt.legend()
    plt.title(f"{name} — Training vs Validation Accuracy")
    plt.savefig(os.path.join(results_dir, f"{name}_accuracy_graph.png"), dpi=150, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(epochs_range, history.history["loss"], label="Training Loss")
    plt.plot(epochs_range, history.history["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend()
    plt.title(f"{name} — Training vs Validation Loss")
    plt.savefig(os.path.join(results_dir, f"{name}_loss_graph.png"), dpi=150, bbox_inches="tight")
    plt.close()


def evaluate_and_record(name, model, data, mem_before, train_time, epochs_trained,
                         results, process, models_dir="models", results_dir="results",
                         class_names=None):
    test_images, test_labels = data["test_images"], data["test_labels"]
    val_images, val_labels = data["val_images"], data["val_labels"]

    probs = model.predict(test_images, batch_size=64, verbose=0)
    preds = np.argmax(probs, axis=1)
    acc = accuracy_score(test_labels, preds)
    prec = precision_score(test_labels, preds, average="macro", zero_division=0)
    rec = recall_score(test_labels, preds, average="macro", zero_division=0)
    f1 = f1_score(test_labels, preds, average="macro", zero_division=0)
    cm = confusion_matrix(test_labels, preds)

    if class_names:
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, cmap="Blues")
        plt.xticks(range(10), class_names, rotation=90); plt.yticks(range(10), class_names)
        plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.title(f"{name} Confusion Matrix")
        plt.colorbar(); plt.tight_layout()
        plt.savefig(os.path.join(results_dir, f"{name}_confusion_matrix.png"), dpi=150, bbox_inches="tight")
        plt.close()

    val_probs = model.predict(val_images, batch_size=64, verbose=0)
    val_preds = np.argmax(val_probs, axis=1)
    val_acc = accuracy_score(val_labels, val_preds)

    single_image = test_images[0:1]
    _ = model.predict(single_image, verbose=0)
    latencies = []
    for _ in range(100):
        t_start = time.time()
        model.predict(single_image, verbose=0)
        latencies.append((time.time() - t_start) * 1000)
    latencies = np.array(latencies)

    n_throughput = min(1000, len(test_images))
    t_start = time.time()
    model.predict(test_images[:n_throughput], batch_size=64, verbose=0)
    throughput = n_throughput / (time.time() - t_start)

    model_path = os.path.join(models_dir, f"{name}.keras")
    model_size_mb = os.path.getsize(model_path) / (1024 * 1024) if os.path.exists(model_path) else 0.0
    param_count = model.count_params()
    mem_after = process.memory_info().rss / (1024 * 1024)

    results[name] = {
        "epochs_trained": epochs_trained, "train_time_sec": train_time,
        "test_accuracy": float(acc), "test_precision_macro": float(prec),
        "test_recall_macro": float(rec), "test_f1_macro": float(f1),
        "validation_accuracy": float(val_acc), "confusion_matrix": cm.tolist(),
        "latency_ms_avg": float(latencies.mean()), "latency_ms_min": float(latencies.min()),
        "latency_ms_max": float(latencies.max()), "throughput_img_per_sec": float(throughput),
        "model_size_mb": float(model_size_mb), "param_count": int(param_count),
        "memory_delta_mb": float(mem_after - mem_before),
    }
    print(f"{name}: acc={acc:.4f} prec={prec:.4f} rec={rec:.4f} f1={f1:.4f} val_acc={val_acc:.4f}")
    print(f"{name}: latency_avg={latencies.mean():.2f}ms throughput={throughput:.1f}img/s "
          f"size={model_size_mb:.2f}MB params={param_count}")
    return results[name]
