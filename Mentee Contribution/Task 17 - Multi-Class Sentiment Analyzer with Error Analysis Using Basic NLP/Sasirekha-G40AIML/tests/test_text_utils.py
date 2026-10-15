from src.text_utils import clean_text

def test_clean_text():
    value = clean_text("I REALLY loved this movie!!! https://example.com @user #Amazing")
    assert value == "i really loved this movie amazing"
