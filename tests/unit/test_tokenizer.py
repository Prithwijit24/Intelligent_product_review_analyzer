from review_analyzer.nlp.tokenizer import tokenize


def test_tokenize_returns_word_and_punctuation_tokens() -> None:
    tokens = tokenize("Great quality, slow delivery!")

    assert "Great" in tokens
    assert "quality" in tokens
    assert "delivery" in tokens
