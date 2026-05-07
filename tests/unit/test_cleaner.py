import pytest

from review_analyzer.core.exceptions import EmptyReviewError
from review_analyzer.nlp.cleaner import clean_text


def test_clean_text_removes_html_urls_and_extra_spaces() -> None:
    text = "<p>Great product!!!</p> Visit https://example.com now"

    assert clean_text(text) == "Great product!!! Visit now"


def test_clean_text_rejects_empty_review() -> None:
    with pytest.raises(EmptyReviewError):
        clean_text("<br />")
