"""
model_tools.py - BERT loading, embedding generation and the small BiLSTM model.

These are shared by the training script (04) and the pipeline (pipeline.py).
"""
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

from common import BERT_NAME, MAX_LEN, class_names


def get_device():
    # use the GPU if there is one, otherwise the CPU
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_bert():
    """Load the pretrained BERT tokenizer and BERT model (downloaded the first time, about 440 MB)."""
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(BERT_NAME)
    bert_model = AutoModel.from_pretrained(BERT_NAME).to(device)
    bert_model.eval()   # we only use BERT to read text, we do not train it
    return tokenizer, bert_model, device


def get_embeddings(text_list, tokenizer, bert_model, device, batch_size=16, show_progress=False):
    """Turn a LIST of texts into BERT embeddings.

    Returns:
      embeddings: tensor [number of texts, MAX_LEN, 768]
      masks:      tensor [number of texts, MAX_LEN]  (1 = real token, 0 = padding)
    """
    bert_model.eval()
    emb_parts = []
    mask_parts = []
    total_batches = (len(text_list) + batch_size - 1) // batch_size

    for b in range(total_batches):
        batch = text_list[b * batch_size:(b + 1) * batch_size]
        # tokenizer: text -> subword tokens -> ids (padded / cut to MAX_LEN)
        enc = tokenizer(batch, padding="max_length", truncation=True,
                        max_length=MAX_LEN, return_tensors="pt")
        with torch.no_grad():
            output = bert_model(input_ids=enc["input_ids"].to(device),
                                attention_mask=enc["attention_mask"].to(device))
        emb_parts.append(output.last_hidden_state.cpu())
        mask_parts.append(enc["attention_mask"])
        if show_progress and (b + 1) % 10 == 0:
            print("   embedded", min((b + 1) * batch_size, len(text_list)), "of", len(text_list))

    return torch.cat(emb_parts), torch.cat(mask_parts)


class BiLSTMClassifier(nn.Module):
    """BERT embeddings -> BiLSTM -> max pooling -> dropout -> linear layer -> class scores."""

    def __init__(self, input_size=768, hidden_size=64, num_classes=len(class_names)):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x, mask):
        lstm_out, _ = self.lstm(x)                         # [batch, tokens, 128]
        mask = mask.unsqueeze(-1)                          # [batch, tokens, 1]
        lstm_out = lstm_out.masked_fill(mask == 0, -1e9)   # padding tokens are ignored in pooling
        pooled = lstm_out.max(dim=1).values                # [batch, 128] strongest signal over tokens
        pooled = self.dropout(pooled)
        return self.fc(pooled)                             # [batch, number of classes]


def predict_probs(model, emb, mask, device):
    """Return class probabilities (numpy array) for a batch of embeddings."""
    model.eval()
    parts = []
    with torch.no_grad():
        for i in range(0, len(emb), 64):
            logits = model(emb[i:i + 64].to(device), mask[i:i + 64].to(device))
            parts.append(torch.softmax(logits, dim=1).cpu())   # softmax -> probabilities that add up to 1
    return torch.cat(parts).numpy()
