"""
Evaluate both models on a held-out split.
NER: seqeval span-level precision/recall/F1.
Clause: sklearn classification report.
Also runs a noise-robustness test.
"""
import json
import random
import torch
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification
from seqeval.metrics import classification_report as ner_report
from sklearn.metrics import classification_report as cls_report
from dataset import NERDataset, ClauseDataset, NER_LABELS, CLAUSE_LABELS
from model import BertBiLSTMCRF

random.seed(42)


def split_data(path, val_frac=0.2):
    with open(path, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f]
    random.shuffle(rows)
    n = int(len(rows) * val_frac)
    return rows[n:], rows[:n]


def evaluate_ner(val_rows):
    print("\n=== NER Evaluation ===")
    with open("data/annotated/_val_ner.jsonl", "w", encoding="utf-8") as f:
        for r in val_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ds = NERDataset("data/annotated/_val_ner.jsonl")
    dl = DataLoader(ds, batch_size=8)
    model = BertBiLSTMCRF(num_labels=len(NER_LABELS))
    model.load_state_dict(torch.load("ner_model.pt", map_location="cpu"))
    model.eval()

    true_seqs, pred_seqs = [], []
    with torch.no_grad():
        for batch in dl:
            preds = model(input_ids=batch["input_ids"],
                          attention_mask=batch["attention_mask"])
            for p_row, l_row in zip(preds, batch["labels"]):
                p_tags, t_tags = [], []
                for p, l in zip(p_row, l_row.tolist()):
                    if l == -100:
                        continue
                    p_tags.append(NER_LABELS[p])
                    t_tags.append(NER_LABELS[l])
                pred_seqs.append(p_tags)
                true_seqs.append(t_tags)

    print(ner_report(true_seqs, pred_seqs, digits=4))


def evaluate_clause(val_rows):
    print("\n=== Clause Classification Evaluation ===")
    with open("data/annotated/_val_clause.jsonl", "w", encoding="utf-8") as f:
        for r in val_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ds = ClauseDataset("data/annotated/_val_clause.jsonl")
    dl = DataLoader(ds, batch_size=8)
    model = BertForSequenceClassification.from_pretrained("clause_model")
    model.eval()

    y_true, y_pred = [], []
    with torch.no_grad():
        for batch in dl:
            out = model(input_ids=batch["input_ids"],
                        attention_mask=batch["attention_mask"])
            preds = out.logits.argmax(dim=-1).tolist()
            y_pred.extend(preds)
            y_true.extend(batch["labels"].tolist())

    print(cls_report(y_true, y_pred, target_names=CLAUSE_LABELS, digits=4))


def ocr_noise(text):
    """Simulate OCR errors: char swaps, dropped punctuation."""
    text = text.replace(".", "").replace(",", "")
    chars = list(text)
    for _ in range(5):
        i = random.randrange(len(chars) - 1)
        chars[i], chars[i + 1] = chars[i + 1], chars[i]
    return "".join(chars)


def evaluate_robustness(val_rows):
    print("\n=== Robustness to OCR Noise (NER F1) ===")
    noisy = []
    for r in val_rows:
        noisy.append({"text": ocr_noise(r["text"]),
                      "clause": r["clause"], "entities": r["entities"]})
    with open("data/annotated/_val_ner_noisy.jsonl", "w", encoding="utf-8") as f:
        for r in noisy:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    ds = NERDataset("data/annotated/_val_ner_noisy.jsonl")
    dl = DataLoader(ds, batch_size=8)
    model = BertBiLSTMCRF(num_labels=len(NER_LABELS))
    model.load_state_dict(torch.load("ner_model.pt", map_location="cpu"))
    model.eval()

    true_seqs, pred_seqs = [], []
    with torch.no_grad():
        for batch in dl:
            preds = model(input_ids=batch["input_ids"],
                          attention_mask=batch["attention_mask"])
            for p_row, l_row in zip(preds, batch["labels"]):
                p_tags, t_tags = [], []
                for p, l in zip(p_row, l_row.tolist()):
                    if l == -100:
                        continue
                    p_tags.append(NER_LABELS[p])
                    t_tags.append(NER_LABELS[l])
                pred_seqs.append(p_tags)
                true_seqs.append(t_tags)
    print(ner_report(true_seqs, pred_seqs, digits=4))


if __name__ == "__main__":
    _, val = split_data("data/annotated/train.jsonl", val_frac=0.2)
    print(f"Evaluating on {len(val)} held-out samples.")
    evaluate_ner(val)
    evaluate_clause(val)
    evaluate_robustness(val)