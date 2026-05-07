from __future__ import annotations

from typing import TYPE_CHECKING

from review_analyzer.nlp.aspects import AspectExtractor
from review_analyzer.nlp.cleaner import clean_text
from review_analyzer.nlp.entities import extract_entities
from review_analyzer.nlp.normalizer import normalize
from review_analyzer.nlp.sentiment import RuleBasedSentimentAnalyzer
from review_analyzer.nlp.tagger import tag_review
from review_analyzer.nlp.tokenizer import tokenize
from review_analyzer.pipeline.schemas import AnalysisResult

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object


class ReviewAnalyzer:
    """End-to-end product review analysis pipeline."""

    def __init__(self, nlp: Language | None = None) -> None:
        self.nlp = nlp
        self.aspect_extractor = AspectExtractor(nlp=nlp)
        self.sentiment_analyzer = RuleBasedSentimentAnalyzer()

    def analyze(self, review_text: str, product_id: str | None = None) -> AnalysisResult:
        cleaned = clean_text(review_text)
        tokens = tokenize(cleaned)
        normalized_tokens = normalize(cleaned, self.nlp)
        aspect_terms = self.aspect_extractor.extract(cleaned)
        aspects = self.sentiment_analyzer.aspect_sentiments(cleaned)

        for aspect in aspect_terms:
            aspects.setdefault(aspect, "neutral")

        return AnalysisResult(
            product_id=product_id,
            review_text=review_text,
            cleaned_text=cleaned,
            overall_sentiment=self.sentiment_analyzer.overall(cleaned),
            aspects=aspects,
            aspect_terms=aspect_terms,
            tags=tag_review(cleaned),
            entities=extract_entities(cleaned, self.nlp),
            tokens=tokens,
            normalized_tokens=normalized_tokens,
        )
