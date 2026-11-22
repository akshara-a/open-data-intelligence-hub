# LexExtract – Legal Clause Classification & Entity Extraction (CUAD)

Deterministic, extraction-only NLP pipeline (no text generation) with a Flask backend and a web frontend.

## Run in VS Code (trained models are included)
Python 3.10+ required.

**Windows:** double-click `run.bat` (or run it in the VS Code terminal)  
**macOS/Linux:** `./run.sh`

Manual:
```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cd backend && python app.py     # open http://127.0.0.1:5000
```

## Retrain (optional)
Put the CUAD zip contents in `data/` so `data/CUAD_v1/CUAD_v1.json` exists, then:
```bash
cd backend
python train.py --cuad ../data/CUAD_v1/CUAD_v1.json --ner-sents 20000     # ~10 min on CPU
```
This rewrites `backend/models/` (BPE, Word2Vec, CRF, classifier, metrics.json).

## Architecture
| Stage | Implementation |
|---|---|
| Tokenisation | Offset-preserving regex tokens (`nlp/common.py`) – spans always index the original OCR text |
| Subwords | Byte-Pair Encoding (HuggingFace `tokenizers`, 6k vocab) trained on CUAD |
| Embeddings | Word2Vec (gensim, 24-d) trained over BPE pieces on clean + OCR-noised text; word vector = mean of piece vectors |
| NER | Linear-chain **CRF** (`sklearn-crfsuite`) → `ORG`, `DATE`, `MONEY`; spans kept only if marginal probability ≥ threshold |
| Clause classification | BPE TF-IDF (1–2 grams) + mean embedding → logistic regression; low-confidence → suppressed |
| Zero hallucination | Output = offsets + label only; server asserts `text[start:end] == span` on every response |
| Robustness | Training data augmented with simulated OCR noise (missing punctuation, 0/O, l/1, rn/m, split/merged words, dropped/swapped chars) |

## API
- `POST /api/analyze` – JSON `{text, ocr_noise?, ner_tau?, clause_tau?}` or multipart `file` (.txt/.csv)
- `GET /api/metrics`, `GET /api/samples`, `GET /api/health`

Response excerpt:
```json
{"entities":[{"start":104,"end":125,"text":"Northwind Logistics Inc","label":"ORG","confidence":0.97}],
 "clauses":[{"start":410,"end":690,"label":"Indemnification","confidence":0.98,"text":"...","entities":[]}]}
```

## Important, honest notes
1. **Labels.** CUAD has no *Indemnification* or *Force Majeure* annotation. These two are weakly labelled by keyword triggers in `train.py`; so their scores are optimistic (the model partly learns the keyword). Other classes (Limitation of Liability = CUAD *Cap/Uncapped Liability*, Liquidated Damages, Insurance, Warranty, Governing Law, Anti-Assignment, Change of Control, Non-Compete, Exclusivity, Audit Rights, Termination for Convenience, Covenant Not to Sue) use gold CUAD spans.
2. **NER ground truth.** CUAD has no ORG/DATE/MONEY tags. Training/eval labels are CUAD party names plus rule-based silver labels, so NER metrics measure agreement with those labels, not human annotation. For production, hand-annotate a few hundred spans and retrain.
3. **Model choice.** A CRF (explicitly allowed by the brief) is used instead of a BiLSTM, so everything runs on CPU, trains in minutes and is fully deterministic. The clause classifier is not a sequence model.
4. **Precision-first.** Default thresholds (entity 0.85, clause 0.70) trade recall for precision; tune with the UI sliders and see the *Model performance* tab for the trade-off at each noise level.
5. Decision support only – a lawyer must review outputs. CUAD is CC BY 4.0 (The Atticus Project); sample excerpts come from CUAD contracts.
