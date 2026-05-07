from review_analyzer.nlp.entities import (
    ProductEntityRecognizer,
    extract_entities,
    extract_named_entities,
)


def test_product_entity_recognizer_extracts_rule_based_product_entities() -> None:
    recognizer = ProductEntityRecognizer()

    entities = recognizer.extract("I bought the black 128gb phone from PixelCo.")

    assert entities == [
        entity
        for entity in entities
        if entity.start_char < entity.end_char and entity.source == "rule"
    ]
    assert {entity.label for entity in entities} == {"BRAND", "COLOR", "SIZE"}
    assert {entity.text for entity in entities} == {"PixelCo", "black", "128gb"}


def test_extract_named_entities_keeps_offsets_and_labels() -> None:
    entities = extract_named_entities("The red large hoodie by ClothCo is soft.")

    assert ("red", "COLOR", 4, 7) in {
        (entity.text, entity.label, entity.start_char, entity.end_char) for entity in entities
    }
    assert ("large", "SIZE", 8, 13) in {
        (entity.text, entity.label, entity.start_char, entity.end_char) for entity in entities
    }
    assert ("ClothCo", "BRAND", 24, 31) in {
        (entity.text, entity.label, entity.start_char, entity.end_char) for entity in entities
    }


def test_extract_entities_preserves_legacy_text_list() -> None:
    assert extract_entities("The blue medium jacket from NorthPeak fits well.") == [
        "NorthPeak",
        "blue",
        "medium",
    ]
