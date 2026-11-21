import torch.nn as nn
from transformers import BertModel, BertForSequenceClassification
from torchcrf import CRF

class BertBiLSTMCRF(nn.Module):
    def __init__(self, num_labels, lstm_hidden=256, dropout=0.3):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        hidden = self.bert.config.hidden_size
        self.bilstm = nn.LSTM(hidden, lstm_hidden // 2, num_layers=1,
                              bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(lstm_hidden, num_labels)
        self.crf = CRF(num_labels, batch_first=True)

    def forward(self, input_ids, attention_mask, labels=None):
        out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        seq = self.dropout(out.last_hidden_state)
        seq, _ = self.bilstm(seq)
        emissions = self.classifier(seq)
        if labels is not None:
            mask = attention_mask.bool()
            clean = labels.clone()
            clean[clean == -100] = 0
            loss = -self.crf(emissions, clean, mask=mask, reduction="mean")
            return loss
        return self.crf.decode(emissions, mask=attention_mask.bool())

def build_clause_model(num_labels):
    return BertForSequenceClassification.from_pretrained(
        "bert-base-uncased", num_labels=num_labels)
