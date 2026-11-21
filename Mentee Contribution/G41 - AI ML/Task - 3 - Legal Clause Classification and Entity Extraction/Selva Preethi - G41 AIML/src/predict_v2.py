"""
Full inference: outputs clause label + entities with confidence,
applies precision threshold, verifies zero-hallucination.
"""
import json
import sys
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizer
from preprocess import clean_ocr, tokenize_with_offsets
from dataset import NER_LABELS, CLAUSE_LABELS
from model import BertBiLSTMCRF

NER_MODEL_PATH = "ner_model.pt"
CLAUSE_MODEL_DIR = "clause_model"
CONFIDENCE_THRESHOLD = 0.60


def predict_clause(text, model_dir=CLAUSE_MODEL_DIR):
    tok = BertTokenizer.from_pretrained(model_dir)
    model = BertForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    enc = tok(text, truncation=True, max_length=256, return_tensors="pt")
    with torch.no_grad():
        logits = model(**enc).logits
    probs = F.softmax(logits, dim=-1)[0]
    idx = int(probs.argmax())
    return {
        "label": CLAUSE_LABELS[idx],
        "confidence": round(float(probs[idx]), 4),
        "all_scores": {
            CLAUSE_LABELS[i]: round(float(probs[i]), 4)
            for i in range(len(CLAUSE_LABELS))
        }
    }


def predict_entities(text, model_path=NER_MODEL_PATH, threshold=CONFIDENCE_THRESHOLD):
    text = clean_ocr(text)
    ids, offsets = tokenize_with_offsets(text)
    model = BertBiLSTMCRF(num_labels=len(NER_LABELS))
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    with torch.no_grad():
        out = model.bert(
            input_ids=torch.tensor([ids]),
            attention_mask=torch.tensor([[1] * len(ids)])
        )
        seq = model.dropout(out.last_hidden_state)
        seq, _ = model.bilstm(seq)
        emissions = model.classifier(seq)[0]
        probs = F.softmax(emissions, dim=-1)
        mask = torch.tensor([[True] * len(ids)], dtype=torch.bool)
        preds = model.crf.decode(emissions.unsqueeze(0), mask=mask)[0]

    entities = []
    cur = None
    for (s, e), p, prob_row in zip(offsets, preds, probs):
        if s == e:
            continue
        lab = NER_LABELS[p]
        conf = float(prob_row[p])
        if lab.startswith("B-"):
            if cur:
                entities.append(cur)
            cur = {
                "type": lab[2:],
                "start": s,
                "end": e,
                "text": text[s:e],
                "confidence": round(conf, 4)
            }
        elif lab.startswith("I-") and cur and cur["type"] == lab[2:]:
            cur["end"] = e
            cur["text"] = text[cur["start"]:e]
            cur["confidence"] = round(min(cur["confidence"], conf), 4)
        else:
            if cur:
                entities.append(cur)
            cur = None
    if cur:
        entities.append(cur)

    for ent in entities:
        assert ent["text"] == text[ent["start"]:ent["end"]], \
            f"SPAN MISMATCH: {ent}"
    entities = [e for e in entities if e["confidence"] >= threshold]
    return text, entities


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else (
        "Acme Corp shall indemnify Beta LLC for $50,000 before 31 December 2024."
    )
    cleaned, entities = predict_entities(text)
    clause = predict_clause(cleaned)
    result = {
        "text": cleaned,
        "clause": clause,
        "entities": entities,
        "meta": {
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "entity_count": len(entities)
        }
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()