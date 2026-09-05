# Transformers in NLP

In NLP, a **Transformer** is a neural-network architecture designed to understand relationships between words in a sentence using a mechanism called **attention**.

It is the architecture behind models such as **BERT, GPT, T5, Llama**, and many modern LLMs.

---

## Simple Example

Consider:

> **"The cat sat on the mat because it was tired."**

To understand the word **"it"**, the model needs to determine what `"it"` refers to.

A Transformer can pay attention to different words:

```text
The cat sat on the mat because it was tired
    ↑                            ↑
    └──────── strong relation ──┘
```

The model may learn that `"it"` is strongly related to `"cat"`.

This ability comes mainly from **self-attention**.

---

# Transformer Flow

Suppose the input is:

```text
"The cat is sleeping"
```

The processing roughly looks like:

```text
Sentence
   │
   ▼
Tokenization
   │
   ▼
["The", "cat", "is", "sleeping"]
   │
   ▼
Token IDs
   │
   ▼
[464, 3797, 318, 15105]
   │
   ▼
Embeddings
   │
   ▼
Numerical vectors
   │
   +
Positional Information
   │
   ▼
Self-Attention
   │
   ▼
Feed-Forward Neural Network
   │
   ▼
Transformer Layers
   │
   ▼
Context-aware representations
   │
   ▼
Prediction / Classification / Generation
```

---

## 1. Tokenization

The sentence is broken into tokens.

```text
"I love machine learning"

↓
["I", "love", "machine", "learning"]
```

Sometimes words are broken further:

```text
"unbelievable"

↓
["un", "believ", "able"]
```

---

## 2. Token IDs

Each token is converted into an ID.

```text
["I", "love", "machine", "learning"]

↓

[40, 1842, 3024, 4673]
```

These numbers are just **vocabulary indexes**.

`4673` does not mathematically mean "learning".

---

## 3. Embeddings

Token IDs are converted into vectors.

For illustration:

```text
cat
↓
[0.21, -0.42, 0.81, 0.13]

dog
↓
[0.24, -0.39, 0.78, 0.17]
```

Because **cat** and **dog** have related meanings, their learned vectors may be relatively close in the embedding space.

---

## 4. Positional Encoding

Transformers process tokens largely in parallel, so they need additional information about **word position**.

Compare:

```text
Dog bites man
```

with:

```text
Man bites dog
```

The same words appear, but the meaning is completely different.

Therefore the Transformer combines:

```text
Word embedding
+
Position information
```

Conceptually:

```text
"dog"

Embedding:
[0.2, 0.7, 0.4]

Position 1:
[0.1, 0.2, 0.1]

Combined:
[0.3, 0.9, 0.5]
```

Real Transformers use much larger vectors.

---

# 5. Self-Attention — The Key Idea

Self-attention asks:

> **For this word, which other words should I pay attention to?**

Take:

```text
The animal didn't cross the street because it was tired.
```

When processing:

```text
"it"
```

the model may assign attention roughly like:

```text
The       5%
animal   60%
didn't    2%
cross     3%
street   10%
because   5%
it        -
was       5%
tired    10%
```

So the model understands that:

```text
it → animal
```

This allows Transformers to understand **context**.

---

# Query, Key and Value

Inside self-attention, every token gets three representations:

```text
Query (Q)
Key   (K)
Value (V)
```

A useful analogy is a search engine.

Imagine the word:

```text
"it"
```

is trying to find what it refers to.

```text
Query
"What word am I related to?"
```

Other words provide **Keys**:

```text
animal → possible match
street → possible match
tired  → possible match
```

The Transformer compares:

```text
Query × Keys
```

to calculate attention scores.

Then it retrieves information from the corresponding **Values**.

Conceptually:

```text
             Query
               │
               ▼
        Compare with Keys
               │
      ┌────────┼─────────┐
      ▼        ▼         ▼
   animal    street    tired
    0.70      0.10      0.20
      │        │         │
      └────────┼─────────┘
               ▼
       Weighted Values
               │
               ▼
     Contextual representation
```

Mathematically, attention is commonly written as:

```text
Attention(Q,K,V)
=
softmax(QKᵀ / √dₖ)V
```

As a beginner, the important idea is simply:

```text
Compare words
      ↓
Find important relationships
      ↓
Give relevant words more importance
```

---

# Multi-Head Attention

Transformers don't perform attention only once.

They use several **attention heads**.

Different heads can learn different relationships.

For example:

```text
"The young boy who lives next door plays football."
```

One head might learn:

```text
boy → young
```

Another:

```text
boy → plays
```

Another:

```text
lives → next door
```

So:

```text
                 Sentence
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
       Head 1     Head 2     Head 3
      grammar    meaning    position
         │          │          │
         └──────────┼──────────┘
                    ▼
              Combined output
```

This is called **Multi-Head Attention**.

---

# Transformer Layer

A simplified Transformer layer looks like:

```text
Input embeddings
       │
       ▼
Multi-Head Self-Attention
       │
       ▼
Add + Normalization
       │
       ▼
Feed-Forward Network
       │
       ▼
Add + Normalization
       │
       ▼
Output
```

Modern models stack many such layers:

```text
Input

 ↓

Transformer Layer 1

 ↓

Transformer Layer 2

 ↓

Transformer Layer 3

 ↓
...

Transformer Layer 30+

 ↓

Output
```

Large models may have dozens or even hundreds of layers.

---

# Encoder vs Decoder

The original Transformer architecture has two major sections:

```text
Input
  │
  ▼
Encoder
  │
  ▼
Context representation
  │
  ▼
Decoder
  │
  ▼
Output
```

---

## Encoder

Main purpose:

> Understand the input.

Example:

```text
Input:
"The movie was fantastic."

Encoder understands:

sentiment → positive
subject   → movie
description → fantastic
```

**BERT** is primarily encoder-based.

Good for:

- Text classification
- Sentiment analysis
- Named entity recognition
- Question understanding
- Embeddings

---

## Decoder

Main purpose:

> Generate text.

Example:

```text
Input:

"The capital of France is"

↓

Paris
```

Then:

```text
"The capital of France is Paris"
```

GPT-style models are primarily **decoder-only Transformers**.

Good for:

- Text generation
- Chatbots
- Code generation
- Writing
- Question answering

---

## Encoder-Decoder

Models such as T5 use both.

```text
Input:
Translate English to French:
"How are you?"

      │
      ▼
   Encoder
      │
      ▼
   Decoder
      │
      ▼

"Comment allez-vous?"
```

Good for tasks such as:

- Translation
- Summarization
- Text transformation

---

# Why Transformers Replaced Older NLP Approaches

Earlier NLP architectures commonly used:

- RNN
- LSTM
- GRU

They typically processed text more sequentially:

```text
Word1 → Word2 → Word3 → Word4 → Word5
```

This makes long sequences harder to parallelize and can make long-distance relationships difficult to learn.

Transformers can examine many token relationships at once:

```text
        Word1
      ↙   ↓   ↘
   Word2 Word3 Word4
      ↘   ↓   ↙
        Word5
```

Therefore they offer major advantages:

- Better understanding of long-range relationships
- Highly parallelizable training
- Strong contextual representations
- Scalable to very large datasets and models

---

# Traditional NLP vs Transformer NLP

For sentiment analysis, older systems might look like:

```text
Sentence
   ↓
Tokenization
   ↓
TF-IDF
   ↓
Logistic Regression
   ↓
Positive / Negative
```

Transformer approach:

```text
Sentence
   ↓
Tokenizer
   ↓
Embeddings
   ↓
Transformer
   ↓
Contextual understanding
   ↓
Positive / Negative
```

The major difference is **context**.

Consider:

```text
"I went to the bank to deposit money."
```

and:

```text
"I sat on the river bank."
```

Traditional representations such as Bag of Words may treat `"bank"` almost identically.

A Transformer creates different contextual representations:

```text
bank
↓
financial institution
```

versus

```text
bank
↓
side of a river
```

That contextual understanding is one of the biggest reasons Transformers became so important in NLP.

---

# Overall NLP Learning Chain

A useful sequence to remember is:

```text
Raw Text
   ↓
Tokenization
   ↓
Token IDs
   ↓
Embeddings
   ↓
Positional Information
   ↓
Self-Attention
   ↓
Multi-Head Attention
   ↓
Feed-Forward Network
   ↓
Multiple Transformer Layers
   ↓
Contextual Representation
   ↓
NLP Task
```

And ultimately:

```text
NLP
 │
 ├── Traditional NLP
 │     ├── Bag of Words
 │     ├── TF-IDF
 │     └── ML algorithms
 │
 └── Modern NLP
       ├── Embeddings
       ├── Attention
       ├── Transformers
       │
       ├── BERT
       ├── GPT
       └── LLMs
```

---

# Simple Definition

> **A Transformer is a neural-network architecture that uses attention to understand how tokens relate to one another in context, making it highly effective for understanding and generating language.**
