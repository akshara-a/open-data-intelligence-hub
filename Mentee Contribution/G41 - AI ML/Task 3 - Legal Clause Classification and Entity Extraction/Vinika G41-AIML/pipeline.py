"""
pipeline.py - the complete NLP pipeline in one function: analyze_contract()

Contract text
  -> split into clauses (blocks separated by blank lines)
  -> preprocessing (cleaned COPY)
  -> BERT subword tokenization
  -> BERT embeddings
  -> BiLSTM classification (label + confidence)
  -> (only for flagged clauses) spaCy NER on the ORIGINAL clause text
  -> structured output (a Python dictionary that can be saved as JSON)

A clause is flagged only if the predicted class is one of the 3 risk classes
AND the confidence is at least CONFIDENCE_THRESHOLD.

Entity positions (start/end) are measured in the FULL original contract text.
"""
import os
import re
import torch
import spacy

from common import OUTPUT_DIR, SPACY_MODEL, CONFIDENCE_THRESHOLD, class_names, wanted_labels, clean_text
from model_tools import load_bert, get_embeddings, predict_probs, BiLSTMClassifier


def load_models():
    """Load BERT, the trained BiLSTM (from step 4) and spaCy. Call this once."""
    model_path = os.path.join(OUTPUT_DIR, "bilstm_model.pt")
    if not os.path.exists(model_path):
        print("Trained model not found. Please run 04_train_and_evaluate.py first.")
        raise SystemExit

    tokenizer, bert_model, device = load_bert()

    clf_model = BiLSTMClassifier()
    clf_model.load_state_dict(torch.load(model_path, map_location=device))
    clf_model.to(device)
    clf_model.eval()

    try:
        nlp = spacy.load(SPACY_MODEL)
    except OSError:
        print("The spaCy model is not installed. Run:  python -m spacy download", SPACY_MODEL)
        raise SystemExit

    return {"tokenizer": tokenizer, "bert_model": bert_model, "device": device,
            "clf_model": clf_model, "nlp": nlp}


def analyze_contract(contract_text, contract_id, models):
    """Take contract text and return the flagged clauses with their entities."""
    flagged_clauses = []
    clause_count = 0

    # Step 1: split the contract into clauses (blocks separated by blank lines).
    # re.finditer gives us the position of every clause inside the full contract.
    for match in re.finditer(r"\S[\s\S]*?(?=\n\s*\n|\Z)", contract_text):
        clause_original = match.group().rstrip()
        clause_start = match.start()
        clause_end = clause_start + len(clause_original)
        clause_count += 1

        # Step 2: preprocessing (a cleaned copy, the original stays unchanged)
        clause_clean = clean_text(clause_original)

        # Steps 3 and 4: tokenization + BERT embeddings
        emb, mask = get_embeddings([clause_clean], models["tokenizer"], models["bert_model"], models["device"])

        # Step 5: classification with the trained BiLSTM
        probs = predict_probs(models["clf_model"], emb, mask, models["device"])[0]
        best_id = int(probs.argmax())
        label = class_names[best_id]
        confidence = float(probs[best_id])      # comes from the trained model (softmax probability)

        # skip "Other" clauses and clauses the model is not sure about
        if label == "Other" or confidence < CONFIDENCE_THRESHOLD:
            continue

        # Step 6: NER on the ORIGINAL clause text, then shift the positions to the full contract
        clause_doc = models["nlp"](clause_original)
        entities = []
        for ent in clause_doc.ents:
            if ent.label_ in wanted_labels:
                start = clause_start + ent.start_char
                end = clause_start + ent.end_char
                # validation: only keep the entity if it is an exact substring of the contract
                if contract_text[start:end] == ent.text:
                    entities.append({"text": ent.text, "label": ent.label_, "start": start, "end": end})

        flagged_clauses.append({
            "text": clause_original,
            "start": clause_start,
            "end": clause_end,
            "classification": label,
            "confidence": round(confidence, 4),
            "entities": entities,
        })

    # Step 7: structured output
    return {"contract_id": contract_id, "clauses_checked": clause_count, "clauses": flagged_clauses}
