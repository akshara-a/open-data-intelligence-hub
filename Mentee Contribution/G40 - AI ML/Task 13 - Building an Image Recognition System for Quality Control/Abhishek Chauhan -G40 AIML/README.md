# Automated Casting Defect Detection Using a CNN

Binary image classification system that inspects images of cast metal
products (e.g. pump impellers) and predicts whether each item is
**Non-defective (0)** or **Defective (1)**. Two models are trained and
compared: a custom CNN built from scratch, and a transfer-learning model
built on Xception (ImageNet weights).

---

## 1. Dataset

**Casting Product Image Data for Quality Inspection** (Kaggle, by
`ravirajsinh45`).

| Folder      | Meaning                          | Label |
|-------------|-----------------------------------|------:|
| `ok_front`  | Product without a visible defect  |     0 |
| `def_front` | Product with a visible defect     |     1 |

Download the dataset from Kaggle and place it so the folder structure
matches:

```text
casting_data/
├── train/
│   ├── ok_front/
│   └── def_front/
└── test/
    ├── ok_front/
    └── def_front/
```

Update `train_directory` and `test_directory` at the top of the notebook
to point at your local copy of these folders (the notebook currently
points at a Kaggle-hosted path).

---

## 2. Project Structure

```text
casting-quality-inspection/
│
├── data/
│   ├── train/
│   │   ├── ok_front/
│   │   └── def_front/
│   └── test/
│       ├── ok_front/
│       └── def_front/
│
├── notebooks/
│   └── casting_defect_detection_notebook.ipynb
│
├── models/
│   ├── best_manual_cnn.keras
│   ├── best_xception_model.keras
│   ├── final_manual_cnn.keras
│   └── final_xception_model.keras
│
├── reports/
│   ├── confusion_matrix.png
│   ├── accuracy_graph.png
│   ├── loss_graph.png
│   └── Findings_Report.docx
│
├── requirements.txt
└── README.md
```

---

## 3. Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

A GPU is strongly recommended for the Xception transfer-learning
section — it trains fine on CPU too, just considerably slower.

---

## 4. Running the Notebook

1. Open `casting_defect_detection_notebook.ipynb` in Jupyter or Google
   Colab.
2. Update `train_directory` and `test_directory` (Section 1) to point at
   your local dataset copy.
3. Run all cells top to bottom:
   - **Section 1** — dataset overview, class counts, sample images.
   - **Section 2** — 224×224 resizing, 80/20 train/validation split from
     the training folder, held-out test folder.
   - **Section 3** — data augmentation pipeline (training data only).
   - **Section 4–6** — build, train, and evaluate the custom CNN.
   - **Section 7** — predictions on unseen sample images.
   - **Section 8–9** — build, train, and evaluate the Xception
     transfer-learning model.
   - **Section 10** — predictions on the same unseen images with
     Xception, for side-by-side comparison.
   - **Section 11** — saves both trained models to `.keras` files.
4. Training graphs and the confusion matrices are generated inline —
   export them (right-click → Save Image, or `plt.savefig(...)`) into
   `reports/` if you need standalone PNG files for submission.

Expect the custom CNN to take a few minutes on GPU (~25 epochs, early
stopping usually ends training around epoch 19). The Xception model
trains for 15 epochs and takes noticeably longer per epoch since it is a
larger network, even with the base frozen.

---

## 5. Using a Trained Model to Predict a New Image

```python
import tensorflow as tf

model = tf.keras.models.load_model("models/final_xception_model.keras")

def predict_product(image_path, model, threshold=0.50):
    image = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    image_array = tf.expand_dims(tf.keras.utils.img_to_array(image), axis=0)
    defect_probability = float(model.predict(image_array, verbose=0)[0][0])
    predicted_class = "Defective" if defect_probability >= threshold else "Non-defective"
    return defect_probability, predicted_class

prob, label = predict_product("sample_images/product_01.jpeg", model)
print(f"Prediction: {label}")
print(f"Defect probability: {prob:.1%}")
```

Note: the Xception model expects images preprocessed with
`xception.preprocess_input` — this is already wired into the model
graph, so raw 0–255 images can be passed directly, as in the snippet
above.

---

## 6. Results Summary

| Model                | Test Accuracy | Precision (Defective) | Recall (Defective) | False Negatives |
|-----------------------|--------------:|-----------------------:|--------------------:|-----------------:|
| Custom CNN            |         84.1% |                   83.3% |                93.6% |               29 |
| Xception (transfer)   |         98.7% |                   99.3% |                98.7% |                6 |

See `Findings_Report.docx` for the full discussion, including
overfitting/underfitting analysis, error analysis on false negatives,
and a recommendation on which model to deploy.

---

## 7. Notes

- Data augmentation (flip, rotation, zoom, translation, contrast) is
  applied only to training data, inside the model graph, so it never
  touches validation or test images.
- Both models use binary cross-entropy loss, the Adam optimizer, early
  stopping on `val_loss`, learning-rate reduction on plateau, and
  checkpointing of the best-validation-loss weights.
- The classification threshold defaults to 0.50. For stricter quality
  control (prioritizing recall over precision, to reduce false
  negatives), lower the threshold — see Section 13 of the task brief
  for a suggested range (0.30–0.60) to evaluate.
