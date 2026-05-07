from review_analyzer.pipeline.analyzer import ReviewAnalyzer


def test_analyzer_returns_structured_review_insights() -> None:
    analyzer = ReviewAnalyzer()

    result = analyzer.analyze(
        "The product quality is great but delivery was very slow.",
        product_id="B001234",
    )

    assert result.product_id == "B001234"
    assert result.overall_sentiment == "mixed"
    assert result.aspects["quality"] == "positive"
    assert result.aspects["delivery"] == "negative"
    assert "praise" in result.tags
    assert "complaint" in result.tags


def test_analyzer_returns_structured_named_entities() -> None:
    analyzer = ReviewAnalyzer()

    result = analyzer.analyze("The red large backpack from PackCo feels durable.")

    assert result.entities == ["PackCo", "large", "red"]
    assert {entity.label for entity in result.named_entities} == {"BRAND", "COLOR", "SIZE"}
