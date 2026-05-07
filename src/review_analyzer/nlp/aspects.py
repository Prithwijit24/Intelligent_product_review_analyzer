from __future__ import annotations

import re
from collections import defaultdict
from typing import TYPE_CHECKING

from review_analyzer.nlp.lexicons import ASPECT_KEYWORDS, NEGATIVE_WORDS, POSITIVE_WORDS

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
WINDOW_SIZE = 5


class AspectExtractor:
    """Extract known product aspects and nearby opinion terms."""

    def __init__(self, nlp: Language | None = None) -> None:
        self.nlp = nlp

    def extract(self, text: str) -> dict[str, list[str]]:
        tokens = [token.lower() for token in WORD_RE.findall(text)]
        matches: dict[str, set[str]] = defaultdict(set)

        for index, token in enumerate(tokens):
            for aspect, keywords in ASPECT_KEYWORDS.items():
                if token not in keywords:
                    continue

                start = max(index - WINDOW_SIZE, 0)
                end = min(index + WINDOW_SIZE + 1, len(tokens))
                context = tokens[start:end]
                opinion_terms = [
                    item for item in context if item in POSITIVE_WORDS or item in NEGATIVE_WORDS
                ]
                if opinion_terms:
                    matches[aspect].update(opinion_terms)
                else:
                    matches[aspect].add(token)

        return {aspect: sorted(words) for aspect, words in matches.items()}


def extract_aspects(text: str, nlp: Language | None = None) -> dict[str, list[str]]:
    return AspectExtractor(nlp=nlp).extract(text)
