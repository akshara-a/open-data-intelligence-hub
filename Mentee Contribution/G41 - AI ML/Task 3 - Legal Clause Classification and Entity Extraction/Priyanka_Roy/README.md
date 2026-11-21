# Legal Clause Classification and Entity Extraction

**Student:** Priyanka Roy | **Batch:** G41 AI/ML | **Task:** Task 3 - Legal Clause Classification and Entity Extraction

## Objective
A deterministic (non-generative) NLP pipeline for OCR'd contracts: it classifies clauses (Indemnification, Limitation of Liability, Force Majeure, Other) and extracts ORG / DATE / MONEY entities as exact character spans in JSON.

Pipeline: BPE tokenizer -> Word2Vec embeddings -> BiLSTM -> CRF head (NER) + softmax head (clause class).

## Files
- `solution.ipynb` - full pipeline: data prep, training, inference, evaluation, threshold sweep
- `model.pt`, `tok.json` - trained weights and BPE tokenizer
- `sample_contract.txt` - OCR-noisy sample input
- `sample_contract.json` - JSON output (clause labels, spans, entities)
- `requirements.txt` - Python packages

## How to run
1. Open `solution.ipynb` in Kaggle and attach the dataset `bahushruth/legalclausedataset` (paths in the notebook start with `/kaggle/input/...`).
2. Run all cells top to bottom (training takes about 3 minutes on CPU).
3. The CRF layer is implemented inside the notebook, so `pytorch-crf` is not needed.

## Results (held-out test set, unseen company names)
- DATE and MONEY: about 0.99 precision and recall on clean and light OCR text; under heavy OCR noise, DATE recall is 0.984 and MONEY recall 0.975, versus 0.747 and 0.831 for a regex-only baseline.
- Clause classification: risk-class precision 0.96-1.00 on Force Majeure and Limitation of Liability and 0.86-0.93 on Indemnification (threshold 0.9).
- Precision over recall: raising the confidence threshold from 0.5 to 0.99 raises risk-class precision from 0.891 to 0.983 (light OCR) while the model abstains on uncertain clauses.
- Zero hallucination: every entity is sliced from the source text using offsets, checked by an assertion.
- ORG: 0.869 

## Limitations
- NER labels are rule-generated (silver) plus injected entities, not human-annotated.
- ORG extraction on unseen company names is weak (precision about 0.30 before the suffix validator).
- Limitation of Liability recall is low (0.55 clean, 0.38 heavy OCR); the model abstains instead of guessing.
