from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object

DEFAULT_STOPWORDS = frozenset({
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
})


def normalize(text: str, nlp: Language | None = None) -> list[str]:
    """Return lowercased lemmas/tokens with common stopwords removed."""

    if nlp is not None:
        doc = nlp(text)
        normalized: list[str] = []
        for token in doc:
            value = token.lemma_.lower().strip() if token.lemma_ else token.text.lower().strip()
            if value and not token.is_punct and not token.is_space and not token.is_stop:
                normalized.append(value)
        if normalized:
            return normalized

    return [
        token.lower()
        for token in text.split()
        if token.lower() not in DEFAULT_STOPWORDS and any(char.isalnum() for char in token)
    ]
