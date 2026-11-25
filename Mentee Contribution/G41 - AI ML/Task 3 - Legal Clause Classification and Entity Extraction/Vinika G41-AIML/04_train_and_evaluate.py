"""
STEP 4 - Train and evaluate the clause classifier

Model: a small BiLSTM on top of the (frozen) pretrained BERT embeddings.
  BERT embeddings [tokens x 768] -> BiLSTM (64 units each way) -> max pooling
  -> dropout -> linear layer -> 4 scores -> softmax -> 4 probabilities

  - BiLSTM reads the token sequence left-to-right AND right-to-left.
  - Softmax turns the scores into probabilities. The biggest one is the "confidence".
    It comes from the trained model (nothing is invented), but it is not perfectly calibrated.
  - Simplification: the backward LSTM also sees the padding embeddings (small approximation).

Metrics:
  - Precision (per class): of all clauses the model CALLED class X, how many really are X.
    High precision = few false alarms. This matters most in legal work.
  - Recall (per class): of all clauses that really ARE class X, how many the model found.
  - F1: balance of precision and recall.

Also includes a simple TF-IDF + Logistic Regression BASELINE for comparison.
The baseline is NOT the architecture requested in the problem statement.

Run:  python 04_train_and_evaluate.py   (after step 3)
"""
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from common import DATA_DIR, OUTPUT_DIR, RANDOM_SEED, class_names, other_id
from model_tools import BiLSTMClassifier, predict_probs, get_device

EPOCHS = 15
BATCH_SIZE = 32

torch.manual_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
device = get_device()
print("Using device:", device)

# we collect everything we print, and save it to outputs/metrics_report.txt at the end
report_lines = []


def show(text=""):
    print(text)
    report_lines.append(str(text))


# %% Load the data and the embeddings from step 3
ready_file = os.path.join(DATA_DIR, "dataset_ready.csv")
emb_file = os.path.join(OUTPUT_DIR, "embeddings.pt")
if not os.path.exists(ready_file) or not os.path.exists(emb_file):
    print("Missing files from step 3. Please run 03_preprocess_tokenize_embed.py first.")
    raise SystemExit

df = pd.read_csv(ready_file)
saved = torch.load(emb_file)
X_all = saved["X"].float()       # back to float32
mask_all = saved["mask"]
y_all = saved["y"].numpy()
print("Clauses:", len(df), "| embeddings:", tuple(X_all.shape))

# %% Train / test split: 80% / 20%
# We stratify by class AND source, so both real and synthetic rows appear in train and test
df["strat_key"] = df["label"] + " | " + df["source"]
train_idx, test_idx = train_test_split(np.arange(len(df)), test_size=0.2,
                                       random_state=RANDOM_SEED, stratify=df["strat_key"])

train_t = torch.tensor(train_idx, dtype=torch.long)
test_t = torch.tensor(test_idx, dtype=torch.long)
X_train, mask_train, y_train = X_all[train_t], mask_all[train_t], torch.tensor(y_all[train_idx], dtype=torch.long)
X_test, mask_test = X_all[test_t], mask_all[test_t]
y_test = y_all[test_idx]

test_df = df.iloc[test_idx].copy()
test_df.to_csv(os.path.join(DATA_DIR, "test_set.csv"), index=False)   # used later for the noise test
show("Train size: " + str(len(train_idx)) + " | Test size: " + str(len(test_idx)))

# %% Train the BiLSTM
clf_model = BiLSTMClassifier().to(device)
train_data = TensorDataset(X_train, mask_train, y_train)
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(clf_model.parameters(), lr=0.001)

show("")
show("Training for " + str(EPOCHS) + " epochs (the test set is NOT used for training or tuning)")
train_losses = []
for epoch in range(EPOCHS):
    clf_model.train()
    total_loss = 0
    for xb, mb, yb in train_loader:
        xb, mb, yb = xb.to(device), mb.to(device), yb.to(device)
        optimizer.zero_grad()                 # clear old gradients
        logits = clf_model(xb, mb)            # forward pass
        loss = loss_fn(logits, yb)            # how wrong are we?
        loss.backward()                       # backpropagation
        optimizer.step()                      # update the weights
        total_loss += loss.item() * len(yb)
    avg_loss = total_loss / len(train_data)
    train_losses.append(avg_loss)
    print("Epoch", epoch + 1, "of", EPOCHS, "- training loss:", round(avg_loss, 4))

# save the trained model and a plot of the loss
torch.save(clf_model.state_dict(), os.path.join(OUTPUT_DIR, "bilstm_model.pt"))
plt.figure(figsize=(6, 3))
plt.plot(range(1, EPOCHS + 1), train_losses, marker="o")
plt.xlabel("Epoch")
plt.ylabel("Training loss")
plt.title("Training loss (should go down)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "training_loss.png"))
plt.close()

# %% Predictions and main metrics on the test set
test_probs = predict_probs(clf_model, X_test, mask_test, device)
test_pred = test_probs.argmax(axis=1)        # predicted class number
test_conf = test_probs.max(axis=1)           # confidence of that prediction

show("")
show("===== BiLSTM results on the TEST set =====")
show("Accuracy       : " + str(round(accuracy_score(y_test, test_pred), 4)))
show("Macro precision: " + str(round(precision_score(y_test, test_pred, average="macro", zero_division=0), 4)))
show("Macro recall   : " + str(round(recall_score(y_test, test_pred, average="macro", zero_division=0), 4)))
show("Macro F1       : " + str(round(f1_score(y_test, test_pred, average="macro", zero_division=0), 4)))
show("")
show("Classification report (precision / recall / f1 per class):")
show(classification_report(y_test, test_pred, labels=list(range(len(class_names))),
                           target_names=class_names, digits=3, zero_division=0))

# %% Confusion matrix (rows = true class, columns = predicted class)
cm = confusion_matrix(y_test, test_pred, labels=list(range(len(class_names))))
show("Confusion matrix (rows = true, columns = predicted):")
show(str(cm))
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion matrix (test set)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"))
plt.close()

# %% Real vs synthetic test rows, and the mistakes
test_df["predicted"] = [class_names[i] for i in test_pred]
test_df["confidence"] = test_conf
show("")
show("Accuracy by data source (important for an honest picture):")
for source in test_df["source"].unique():
    part = test_df[test_df["source"] == source]
    acc = (part["label"] == part["predicted"]).mean()
    show("  " + source + " -> rows: " + str(len(part)) + " | accuracy: " + str(round(acc, 4)))

mistakes = test_df[test_df["label"] != test_df["predicted"]]
show("")
show("Number of mistakes on the test set: " + str(len(mistakes)))
test_df[["text", "label", "predicted", "confidence", "source"]].to_csv(
    os.path.join(OUTPUT_DIR, "test_predictions.csv"), index=False)
if len(mistakes) > 0:
    show("(all rows with their predictions are in outputs/test_predictions.csv)")

# %% Precision vs recall: only flag clauses when the model is confident enough
# Clauses below the threshold are treated as "Other" (not flagged). Only the 3 risk classes are scored.
show("")
show("Effect of the confidence threshold (3 risk classes only):")
show("threshold | precision | recall | clauses flagged")
for t in [0.0, 0.5, 0.7, 0.9]:
    pred_t = test_pred.copy()
    pred_t[test_conf < t] = other_id
    p = precision_score(y_test, pred_t, labels=[0, 1, 2], average="macro", zero_division=0)
    r = recall_score(y_test, pred_t, labels=[0, 1, 2], average="macro", zero_division=0)
    flagged = int((pred_t != other_id).sum())
    show("   " + str(t) + "    |  " + str(round(p, 3)) + "   | " + str(round(r, 3)) + "  | " + str(flagged))

# %% Baseline for comparison: TF-IDF + Logistic Regression (NOT the required architecture)
train_texts = list(df["clean_text"].iloc[train_idx])
test_texts = list(df["clean_text"].iloc[test_idx])
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
baseline = LogisticRegression(max_iter=1000)
baseline.fit(tfidf.fit_transform(train_texts), y_train.numpy())
base_pred = baseline.predict(tfidf.transform(test_texts))

show("")
show("===== Comparison with the simple TF-IDF baseline =====")
show("BASELINE accuracy        : " + str(round(accuracy_score(y_test, base_pred), 4)))
show("BASELINE macro precision : " + str(round(precision_score(y_test, base_pred, average="macro", zero_division=0), 4)))
show("BiLSTM   accuracy        : " + str(round(accuracy_score(y_test, test_pred), 4)))
show("BiLSTM   macro precision : " + str(round(precision_score(y_test, test_pred, average="macro", zero_division=0), 4)))

# %% Honest reading of the results
show("")
show("HOW TO READ THESE RESULTS HONESTLY:")
show(" - Very high scores (for example above 95%) do NOT mean real-world accuracy. The synthetic clauses")
show("   come from only a few templates, and the same templates appear in train and test.")
show(" - Compare the real vs synthetic accuracy above. Real LEDGAR rows cover only some of the classes.")
show(" - If the TF-IDF baseline scores about the same, BERT + BiLSTM is not giving a measurable benefit here.")
show(" - There is no real test data for Limitation of Liability and Force Majeure (unless LEDGAR had them).")

with open(os.path.join(OUTPUT_DIR, "metrics_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))
print()
print("Saved: outputs/bilstm_model.pt, metrics_report.txt, confusion_matrix.png, training_loss.png, test_predictions.csv")
