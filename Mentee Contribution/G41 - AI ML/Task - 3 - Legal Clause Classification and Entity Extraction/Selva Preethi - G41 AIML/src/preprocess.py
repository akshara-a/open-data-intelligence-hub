import re
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def clean_ocr(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    return text.strip()

def tokenize_with_offsets(text: str, max_len: int = 512):
    enc = tokenizer(
        text, return_offsets_mapping=True, truncation=True,
        max_length=max_len, padding=False,
    )
    return enc["input_ids"], enc["offset_mapping"]
