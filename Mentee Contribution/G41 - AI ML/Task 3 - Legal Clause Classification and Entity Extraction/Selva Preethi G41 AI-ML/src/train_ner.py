import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from dataset import NERDataset, NER_LABELS
from model import BertBiLSTMCRF

def train(data_path, epochs=5, batch_size=8, lr=2e-5):
    ds = NERDataset(data_path)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=True)
    model = BertBiLSTMCRF(num_labels=len(NER_LABELS))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    opt = AdamW(model.parameters(), lr=lr)
    for ep in range(epochs):
        model.train()
        total = 0
        for batch in dl:
            batch = {k: v.to(device) for k, v in batch.items()}
            loss = model(**batch)
            opt.zero_grad(); loss.backward(); opt.step()
            total += loss.item()
        print(f"Epoch {ep+1} loss = {total/len(dl):.4f}")
    torch.save(model.state_dict(), "ner_model.pt")
    print("Saved ner_model.pt")

if __name__ == "__main__":
    train("data/annotated/train.jsonl")
