from __future__ import annotations

import re

from review_analyzer.nlp.lexicons import ASPECT_KEYWORDS, NEGATIONS, NEGATIVE_WORDS, POSITIVE_WORDS

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
WINDOW_SIZE = 6


class RuleBasedSentimentAnalyzer:
    """Small deterministic sentiment scorer for baseline production use."""

    def score_tokens(self, tokens: list[str]) -> int:
        score = 0
        for index, token in enumerate(tokens):
            value = 0
            if token in POSITIVE_WORDS:
                value = 1
            elif token in NEGATIVE_WORDS:
                value = -1

            if value and any(item in NEGATIONS for item in tokens[max(0, index - 3) : index]):
                value *= -1
            score += value
        return score

    def label_from_score(self, score: int) -> str:
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    def overall(self, text: str) -> str:
        tokens = [token.lower() for token in WORD_RE.findall(text)]
        score = self.score_tokens(tokens)
        positive_seen = any(token in POSITIVE_WORDS for token in tokens)
        negative_seen = any(token in NEGATIVE_WORDS for token in tokens)
        if positive_seen and negative_seen:
            return "mixed"
        return self.label_from_score(score)

    def aspect_sentiments(self, text: str) -> dict[str, str]:
        tokens = [token.lower() for token in WORD_RE.findall(text)]
        sentiments: dict[str, str] = {}

        for aspect, keywords in ASPECT_KEYWORDS.items():
            aspect_scores: list[int] = []
            for index, token in enumerate(tokens):
                if token not in keywords:
                    continue

                candidates: list[tuple[int, int]] = []
                start = max(0, index - WINDOW_SIZE)
                end = min(len(tokens), index + WINDOW_SIZE + 1)
                for candidate_index in range(start, end):
                    candidate = tokens[candidate_index]
                    value = 0
                    if candidate in POSITIVE_WORDS:
                        value = 1
                    elif candidate in NEGATIVE_WORDS:
                        value = -1

                    if value:
                        boundary = tokens[
                            min(index, candidate_index) + 1 : max(index, candidate_index)
                        ]
                        if "but" in boundary:
                            continue
                        distance = abs(candidate_index - index)
                        candidates.append((distance, value))

                if candidates:
                    nearest_distance = min(distance for distance, _ in candidates)
                    aspect_scores.extend(
                        value for distance, value in candidates if distance == nearest_distance
                    )

            if aspect_scores:
                sentiments[aspect] = self.label_from_score(sum(aspect_scores))

        return sentiments
