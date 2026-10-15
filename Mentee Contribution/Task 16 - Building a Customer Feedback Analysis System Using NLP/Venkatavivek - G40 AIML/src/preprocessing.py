import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)



STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()



def clean_text(text):
    """
    Convert raw feedback into clean lowercase text.
    """

    text = str(text)

    text = text.lower()

    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_text(text):
    """
    Split text into individual words.
    """

    return word_tokenize(text)



def remove_stopwords(tokens):
    """
    Remove common English words such as:
    the, is, a, an, and, of, etc.
    """

    return [
        word
        for word in tokens
        if word== "not" or word not in STOP_WORDS  
    ]



def lemmatize_tokens(tokens):
    """
    Convert words to their base/dictionary form.
    """

    return [
        LEMMATIZER.lemmatize(word)
        for word in tokens
    ]



def preprocess_text(text):
    """
    Perform complete preprocessing:

    Raw text
        ↓
    Cleaning
        ↓
    Tokenization
        ↓
    Stopword removal
        ↓
    Lemmatization
        ↓
    Final processed text
    """

    # Step 1: Cleaning
    text = clean_text(text)

    # Step 2: Tokenization
    tokens = tokenize_text(text)

    # Step 3: Stopword removal
    tokens = remove_stopwords(tokens)

    # Step 4: Lemmatization
    tokens = lemmatize_tokens(tokens)

    # Step 5: Convert tokens back to text
    processed_text = " ".join(tokens)

    return processed_text


if __name__ == "__main__":

    sample_feedback = (
        "The payment page is not working! "
        "I tried it twice."
    )

    result = preprocess_text(sample_feedback)

    print("Original:")
    print(sample_feedback)

    print("\nProcessed:")
    print(result)