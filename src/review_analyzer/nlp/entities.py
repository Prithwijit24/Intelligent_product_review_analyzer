from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object

COLOR_RE = re.compile(
    r"\b(black|blue|brown|gold|green|grey|gray|pink|red|silver|white|yellow)\b",
    re.I,
)
SIZE_RE = re.compile(
    r"\b(xs|s|m|l|xl|xxl|small|medium|large|\d+\s?(gb|tb|ml|kg|inch|inches))\b",
    re.I,
)
BRAND_HINT_RE = re.compile(r"\b(?:brand|by|from)\s+([A-Z][A-Za-z0-9&.-]+)\b")


def extract_entities(text: str, nlp: Language | None = None) -> list[str]:
    entities: set[str] = set()

    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"ORG", "PRODUCT", "GPE", "NORP"}:
                entities.add(ent.text.strip())

    for match in COLOR_RE.finditer(text):
        entities.add(match.group(0).lower())
    for match in SIZE_RE.finditer(text):
        entities.add(match.group(0).lower())
    for match in BRAND_HINT_RE.finditer(text):
        entities.add(match.group(1))

    return sorted(item for item in entities if item)
