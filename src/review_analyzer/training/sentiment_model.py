from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline(**tfidf_kwargs: object) -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(**tfidf_kwargs)),
            ("classifier", LogisticRegression(max_iter=1_000)),
        ]
    )


class SentimentClassifier:
    """Trainable sentiment classifier for future labeled datasets."""

    def __init__(self, **tfidf_kwargs: object) -> None:
        self.pipeline = build_pipeline(**tfidf_kwargs)

    def train(self, texts: list[str], labels: list[str]) -> None:
        self.pipeline.fit(texts, labels)

    def predict(self, texts: list[str]) -> list[str]:
        return list(self.pipeline.predict(texts))

    def save(self, path: str | Path) -> None:
        joblib.dump(self.pipeline, path)

    @classmethod
    def load(cls, path: str | Path) -> SentimentClassifier:
        instance = cls()
        instance.pipeline = joblib.load(path)
        return instance
