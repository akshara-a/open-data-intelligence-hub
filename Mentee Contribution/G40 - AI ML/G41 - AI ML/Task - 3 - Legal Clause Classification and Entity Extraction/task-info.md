# Problem Statement: Legal Clause Classification and Entity Extraction

## 1. Background
A legal consultancy processes thousands of legacy, text-based contracts daily. To streamline legal review and risk assessment, the firm requires an automated system capable of analyzing these documents, identifying specific risk-related clauses, and extracting critical entities. Since this pertains to legal compliance, the system cannot generate new text (zero hallucination); it must deterministically extract and classify existing text.

## 2. The Challenge
The raw data consists of unstructured, variable-length text obtained via OCR (Optical Character Recognition) from scanned contracts. The text is often noisy and lacks standard formatting. The goal is to build a traditional NLP pipeline that accurately categorizes specific liability and indemnification clauses while extracting key entities such as dates, monetary values, and organization names.

## 3. Technical Requirements

### 3.1 Inputs
*   Unstructured text files (TXT/CSV format) generated from OCR-processed legal contracts.

### 3.2 System Architecture
The solution must implement a deterministic NLP pipeline including, but not limited to, the following stages:
1.  **Preprocessing & Tokenization:** Apply robust subword tokenization (e.g., Byte Pair Encoding or WordPiece) to handle out-of-vocabulary legal jargon and OCR errors.
2.  **Vectorization:** Generate dense word embeddings (e.g., Word2Vec, GloVe, or non-generative contextual embeddings like BERT).
3.  **Modeling:** 
    *   Route the embeddings through a sequence model such as a Bidirectional LSTM (BiLSTM) or a Conditional Random Field (CRF).
    *   Perform multi-class sequence classification for clause categorization.
    *   Perform Named Entity Recognition (NER) to isolate target variables.

### 3.3 Outputs
*   A structured JSON object mapping exact text spans (start and end indices) to predefined entity labels (e.g., `ORG`, `DATE`, `MONEY`).
*   A classification label for the extracted clause mapping to specific legal risk categories (e.g., `Indemnification`, `Limitation of Liability`, `Force Majeure`).

## 4. Success Criteria
*   **Precision over Recall:** In legal contexts, false positives are costly. The model must prioritize high precision.
*   **Zero Hallucination:** The system must strictly extract spans from the source text and must not synthesize or summarize information.
*   **Robustness:** The model must maintain baseline performance despite common OCR artifacts (e.g., missing punctuation, misspelled words).
