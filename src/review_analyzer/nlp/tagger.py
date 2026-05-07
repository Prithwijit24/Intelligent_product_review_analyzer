from __future__ import annotations

import re

from review_analyzer.nlp.lexicons import NEGATIVE_WORDS, POSITIVE_WORDS

SUGGESTION_RE = re.compile(r"\b(should|could|please|wish|suggest|improve|add|make it)\b", re.I)
QUESTION_RE = re.compile(r"\?")
COMPLAINT_RE = re.compile(
    r"\b(refund|return|replace|complaint|issue|problem|defect|damaged)\b",
    re.I,
)


def tag_review(text: str) -> list[str]:
    tokens = {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z'-]*", text)}
    tags: list[str] = []

    if tokens & NEGATIVE_WORDS or COMPLAINT_RE.search(text):
        tags.append("complaint")
    if tokens & POSITIVE_WORDS:
        tags.append("praise")
    if SUGGESTION_RE.search(text):
        tags.append("suggestion")
    if QUESTION_RE.search(text):
        tags.append("question")

    return tags or ["neutral"]


def tag(text: str) -> list[str]:
    return tag_review(text)
