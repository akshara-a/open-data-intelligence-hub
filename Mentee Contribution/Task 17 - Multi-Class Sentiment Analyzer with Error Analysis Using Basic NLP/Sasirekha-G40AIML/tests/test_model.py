from src.model import build_pipeline

def test_pipeline_can_fit():
    model = build_pipeline()
    model.fit(
        ["I love this", "I hate this", "it is okay"],
        ["positive", "negative", "neutral"],
    )
    assert model.predict(["I love this"])[0] == "positive"
