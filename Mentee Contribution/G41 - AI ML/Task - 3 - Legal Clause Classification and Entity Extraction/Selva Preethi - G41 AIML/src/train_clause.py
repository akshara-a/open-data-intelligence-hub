import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from dataset import ClauseDataset, CLAUSE_LABELS
from model import build_clause_model


def train(data_path, epochs=3, batch_size=8, lr=2e-5):
    ds = ClauseDataset(data_path)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=True)
    model = build_clause_model(len(CLAUSE_LABELS))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    opt = AdamW(model.parameters(), lr=lr)

    # Class weights (order: Indemnification, Limitation of Liability,
    #                        Force Majeure, Other)
    # Higher weight = model pays more attention to that class
    class_weights = torch.tensor([1.5, 1.0, 1.5, 3.0], dtype=torch.float).to(device)

    for ep in range(epochs):
        model.train()
        total = 0
        for batch in dl:
            batch = {k: v.to(device) for k, v in batch.items()}
            out = model(input_ids=batch["input_ids"],
                        attention_mask=batch["attention_mask"])
            loss = torch.nn.functional.cross_entropy(
                out.logits, batch["labels"], weight=class_weights
            )
            loss.backward()
            opt.step()
            opt.zero_grad()
            total += loss.item()
        print(f"Epoch {ep+1} loss = {total/len(dl):.4f}")

    model.save_pretrained("clause_model")
    print("Saved clause_model/")


if __name__ == "__main__":
    train("data/annotated/train.jsonl")