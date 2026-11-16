import json, torch, sys
from preprocess import clean_ocr, tokenize_with_offsets
from dataset import NER_LABELS
from model import BertBiLSTMCRF

def predict_entities(text, ner_model_path="ner_model.pt"):
    text = clean_ocr(text)
    ids, offsets = tokenize_with_offsets(text)
    model = BertBiLSTMCRF(num_labels=len(NER_LABELS))
    model.load_state_dict(torch.load(ner_model_path, map_location="cpu"))
    model.eval()
    with torch.no_grad():
        preds = model(input_ids=torch.tensor([ids]),
                      attention_mask=torch.tensor([[1]*len(ids)]))[0]
    entities, cur = [], None
    for (s, e), p in zip(offsets, preds):
        if s == e: continue
        lab = NER_LABELS[p]
        if lab.startswith("B-"):
            if cur: entities.append(cur)
            cur = {"type": lab[2:], "start": s, "end": e, "text": text[s:e]}
        elif lab.startswith("I-") and cur and cur["type"] == lab[2:]:
            cur["end"] = e; cur["text"] = text[cur["start"]:e]
        else:
            if cur: entities.append(cur)
            cur = None
    if cur: entities.append(cur)
    for ent in entities:
        assert ent["text"] == text[ent["start"]:ent["end"]], "span mismatch!"
    return entities

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Acme Corp shall indemnify Beta LLC."
    print(json.dumps({"text": text, "entities": predict_entities(text)},
                     indent=2, ensure_ascii=False))
