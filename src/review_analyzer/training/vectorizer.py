from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf(**kwargs: object) -> TfidfVectorizer:
    """Build a configurable TF-IDF vectorizer for training scripts."""

    return TfidfVectorizer(**kwargs)


def save_artifact(obj: object, path: str | Path) -> None:
    joblib.dump(obj, path)


def load_artifact(path: str | Path) -> object:
    return joblib.load(path)
