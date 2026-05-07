from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object


SPACY_NER_LABELS = {"ORG", "PRODUCT", "GPE", "NORP"}
PRODUCT_ENTITY_LABELS = {"BRAND", "COLOR", "SIZE"}

COLOR_RE = re.compile(
    r"\b(black|blue|brown|gold|green|grey|gray|pink|red|silver|white|yellow)\b",
    re.I,
)
SIZE_RE = re.compile(
    r"\b(xs|s|m|l|xl|xxl|small|medium|large|\d+\s?(gb|tb|ml|kg|inch|inches))\b",
    re.I,
)
BRAND_HINT_RE = re.compile(r"\b(?:brand|by|from)\s+([A-Z][A-Za-z0-9&.-]+)\b")


@dataclass(frozen=True)
class EntityMention:
    """Structured NER mention used by the analysis pipeline."""

    text: str
    label: str
    start_char: int
    end_char: int
    source: str


class ProductEntityRecognizer:
    """Product-review NER scaffold.

    This class combines spaCy NER with lightweight review-specific rules. It is
    intentionally small so a trained product NER model can later replace or
    extend the rule layer without changing the pipeline contract.
    """

    def __init__(self, nlp: Language | None = None) -> None:
        self.nlp = nlp

    def extract(self, text: str) -> list[EntityMention]:
        mentions = [
            *self._extract_spacy_entities(text),
            *self._extract_rule_entities(text),
        ]
        return sorted(
            self._deduplicate(mentions),
            key=lambda entity: (entity.start_char, entity.end_char, entity.label),
        )

    def _extract_spacy_entities(self, text: str) -> list[EntityMention]:
        if self.nlp is None:
            return []

        doc = self.nlp(text)
        return [
            EntityMention(
                text=ent.text.strip(),
                label=ent.label_,
                start_char=ent.start_char,
                end_char=ent.end_char,
                source="spacy",
            )
            for ent in doc.ents
            if ent.label_ in SPACY_NER_LABELS and ent.text.strip()
        ]

    def _extract_rule_entities(self, text: str) -> list[EntityMention]:
        mentions: list[EntityMention] = []

        mentions.extend(_mentions_from_matches(COLOR_RE.finditer(text), "COLOR"))
        mentions.extend(_mentions_from_matches(SIZE_RE.finditer(text), "SIZE"))

        for match in BRAND_HINT_RE.finditer(text):
            mentions.append(
                EntityMention(
                    text=match.group(1).strip(),
                    label="BRAND",
                    start_char=match.start(1),
                    end_char=match.end(1),
                    source="rule",
                )
            )

        return mentions

    @staticmethod
    def _deduplicate(mentions: Iterable[EntityMention]) -> list[EntityMention]:
        unique: dict[tuple[str, str, int, int], EntityMention] = {}
        for mention in mentions:
            key = (
                mention.text.casefold(),
                mention.label,
                mention.start_char,
                mention.end_char,
            )
            unique.setdefault(key, mention)
        return list(unique.values())


def _mentions_from_matches(matches: Iterable[re.Match[str]], label: str) -> list[EntityMention]:
    return [
        EntityMention(
            text=match.group(0).strip().lower(),
            label=label,
            start_char=match.start(),
            end_char=match.end(),
            source="rule",
        )
        for match in matches
        if match.group(0).strip()
    ]


def extract_named_entities(text: str, nlp: Language | None = None) -> list[EntityMention]:
    """Extract structured named entities from review text."""
    return ProductEntityRecognizer(nlp=nlp).extract(text)


def extract_entities(text: str, nlp: Language | None = None) -> list[str]:
    """Backward-compatible entity text list used by earlier API responses."""
    entities = {entity.text for entity in extract_named_entities(text, nlp)}
    return sorted(item for item in entities if item)
