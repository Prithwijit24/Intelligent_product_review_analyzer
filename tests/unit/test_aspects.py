from review_analyzer.nlp.aspects import extract_aspects


def test_extract_aspects_maps_known_aspects_to_nearby_terms() -> None:
    aspects = extract_aspects("Quality is excellent but delivery was slow and packaging damaged.")

    assert aspects["quality"] == ["excellent"]
    assert "slow" in aspects["delivery"]
    assert "damaged" in aspects["packaging"]
