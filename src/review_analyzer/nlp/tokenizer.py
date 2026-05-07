from __future__ import annotations

import re

TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?|[!?.,;:%$]")


def tokenize(text: str) -> list[str]:
    """Tokenize review text without requiring external NLTK data downloads."""

    try:
        from nltk.tokenize import wordpunct_tokenize

        return [token for token in wordpunct_tokenize(text) if token.strip()]
    except Exception:
        return TOKEN_RE.findall(text)
