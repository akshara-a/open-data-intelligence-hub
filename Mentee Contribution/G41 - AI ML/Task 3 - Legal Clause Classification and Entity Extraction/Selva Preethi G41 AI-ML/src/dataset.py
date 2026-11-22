import json
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer

NER_LABELS = ["O", "B-ORG", "I-ORG", "B-DATE", "I-DATE", "B-MONEY", "I-MONEY"]
NER2ID = {l: i for i, l in enumerate(NER_LABELS)}
CLAUSE_LABELS = ["Indemnification", "Limitation of Liability",
                 "Force Majeure", "Other"]
CLAUSE2ID = {l: i for i, l in enumerate(CLAUSE_LABELS)}

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def chars_to_ner_labels(text, entities, offsets):
    labels = []
    span_map = [(e["start"], e["end"], e["type"]) for e in entities]
    for (s, e) in offsets:
        if s == e:
            labels.append(-100)
            continue
        tag = "O"
        for (es, ee, etype) in span_map:
            if s >= es and e <= ee:
                tag = ("B-" if s == es else "I-") + etype
                break
            if s < ee and e > es:
                tag = "I-" + etype
                break
        labels.append(NER2ID[tag])
    return labels

class NERDataset(Dataset):
    def __init__(self, path, max_len=256):
        self.items = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                enc = tokenizer(rec["text"], return_offsets_mapping=True,
                                truncation=True, max_length=max_len,
                                padding="max_length")
                labels = chars_to_ner_labels(rec["text"], rec["entities"],
                                             enc["offset_mapping"])
                self.items.append({
                    "input_ids": torch.tensor(enc["input_ids"]),
                    "attention_mask": torch.tensor(enc["attention_mask"]),
                    "labels": torch.tensor(labels),
                })
    def __len__(self): return len(self.items)
    def __getitem__(self, i): return self.items[i]

class ClauseDataset(Dataset):
    def __init__(self, path, max_len=256):
        self.items = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                enc = tokenizer(rec["text"], truncation=True,
                                max_length=max_len, padding="max_length")
                self.items.append({
                    "input_ids": torch.tensor(enc["input_ids"]),
                    "attention_mask": torch.tensor(enc["attention_mask"]),
                    "labels": torch.tensor(CLAUSE2ID[rec["clause"]]),
                })
    def __len__(self): return len(self.items)
    def __getitem__(self, i): return self.items[i]
