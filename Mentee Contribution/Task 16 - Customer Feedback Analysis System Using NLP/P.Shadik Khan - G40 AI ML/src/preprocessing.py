import re
import string


def clean_text(text):
    """
    Clean customer feedback text.

    Steps:
    1. Convert text to lowercase
    2. Remove URLs
    3. Remove numbers
    4. Remove punctuation
    5. Remove extra spaces

    Parameters:
        text (str): Customer feedback

    Returns:
        str: Cleaned feedback
    """

    # Convert to string and lowercase
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    sample_feedback = (
        "The application is VERY slow!!! "
        "Please visit https://example.com 123."
    )

    cleaned_feedback = clean_text(sample_feedback)

    print("Original:")
    print(sample_feedback)

    print("\nCleaned:")
    print(cleaned_feedback)