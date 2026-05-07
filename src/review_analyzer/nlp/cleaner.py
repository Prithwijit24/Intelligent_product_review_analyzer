from __future__ import annotations

import html
import re

from review_analyzer.core.exceptions import EmptyReviewError

HTML_TAG_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
NON_TEXT_RE = re.compile(r"[^A-Za-z0-9\s.,!?;:'\"/$%&()+-]")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalize noisy review text while preserving useful sentiment punctuation."""

    if text is None:
        raise EmptyReviewError("Review text is required")

    cleaned = html.unescape(str(text))
    cleaned = HTML_TAG_RE.sub(" ", cleaned)
    cleaned = URL_RE.sub(" ", cleaned)
    cleaned = EMAIL_RE.sub(" ", cleaned)
    cleaned = CONTROL_RE.sub(" ", cleaned)
    cleaned = NON_TEXT_RE.sub(" ", cleaned)
    cleaned = WHITESPACE_RE.sub(" ", cleaned).strip()

    if not cleaned:
        raise EmptyReviewError("Review text is empty after cleaning")

    return cleaned
