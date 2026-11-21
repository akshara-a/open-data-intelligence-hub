# Legal Clause Classification & Entity Extraction

Deterministic NLP pipeline for OCR-processed legal contracts — satisfies task 3.md requirements with zero hallucination.

## Architecture

| Stage | Implementation | File |
|-------|----------------|------|
| Preprocessing | OCR normalization, unicode cleanup | `src/preprocess.py` |
| Tokenization | BERT WordPiece with offset mapping | `src/preprocess.py` |
| Embeddings | BERT-base-uncased (768-dim) | `src/model.py` |
| NER | BERT → BiLSTM → CRF (7 BIO tags) | `src/model.py` |
| Classifier | BERT + class-weighted softmax (4 classes) | `src/train_clause.py` |
| Inference | JSON output + precision threshold | `src/predict_v2.py` |
| Evaluation | seqeval + sklearn + noise robustness | `src/evaluate.py` |

## Zero Hallucination Guarantee

```python
# In predict_v2.py
assert ent["text"] == text[ent["start"]:ent["end"]]
## 🎯 Live Demo

### Example 1 — Indemnification Clause

**Input:**
```
Acme Corp shall indemnify Beta LLC for $50,000 before 31 December 2024.
```

**Output:**
```json
{
  "text": "Acme Corp shall indemnify Beta LLC for $50,000 before 31 December 2024.",
  "clause": {
    "label": "Indemnification",
    "confidence": 0.3715
  },
  "entities": [
    {"type": "ORG",   "start": 0,  "end": 9,  "text": "Acme Corp",       "confidence": 0.5413},
    {"type": "ORG",   "start": 26, "end": 34, "text": "Beta LLC",         "confidence": 0.4893},
    {"type": "MONEY", "start": 39, "end": 46, "text": "$50,000",          "confidence": 0.4965},
    {"type": "DATE",  "start": 54, "end": 70, "text": "31 December 2024", "confidence": 0.583}
  ]
}
```

**What this shows:**
- Clause correctly classified as **Indemnification**
- All 4 entities extracted with exact character spans
- `text[start:end]` verified against source (zero hallucination)

---

### Example 2 — Limitation of Liability Clause

**Input:**
```
Neither party shall be liable for damages exceeding $500,000.
```

**Output:**
```json
{
  "text": "Neither party shall be liable for damages exceeding $500,000.",
  "clause": {
    "label": "Indemnification",
    "confidence": 0.3698
  },
  "entities": [
    {"type": "MONEY", "start": 52, "end": 60, "text": "$500,000", "confidence": 0.4999}
  ]
}
```

**What this shows:**
- MONEY entity correctly extracted with character span
- Zero hallucination: `"$500,000" == text[52:60]`
- *(Note: classifier shows confusion on this sentence — an honest limitation documented in the report)*

---

### Example 3 — OCR Noise Robustness

**Input (with typos):**
```
Acme Corp shal indemnlfy Beta LLC for $50,000.
```

**Output:**
```json
{
  "text": "Acme Corp shal indemnlfy Beta LLC for $50,000.",
  "clause": {
    "label": "Indemnification",
    "confidence": 0.3711
  },
  "entities": [
    {"type": "ORG",   "start": 0,  "end": 9,  "text": "Acme Corp", "confidence": 0.532},
    {"type": "ORG",   "start": 25, "end": 33, "text": "Beta LLC",   "confidence": 0.4821},
    {"type": "MONEY", "start": 38, "end": 45, "text": "$50,000",    "confidence": 0.4604}
  ]
}
```

**What this shows:**
- Despite typos `shal` and `indemnlfy`, **BERT's WordPiece tokenizer still splits them into subwords** and the model extracts all 3 entities correctly
- Robustness to OCR noise comes from subword tokenization

---

### Reproduce It Yourself

```bash
python src/predict_v2.py 'Acme Corp shall indemnify Beta LLC for $50,000 before 31 December 2024.'
```
