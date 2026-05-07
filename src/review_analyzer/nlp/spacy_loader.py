import logging
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
else:
    Language = object

logger = logging.getLogger(__name__)


@lru_cache
def load_spacy_model(model_name: str) -> Language:
    """Load the configured spaCy model, falling back to a blank English pipeline."""

    import spacy

    try:
        return spacy.load(model_name)
    except OSError:
        logger.warning(
            "spaCy model '%s' is not installed; using blank English pipeline",
            model_name,
        )
        return spacy.blank("en")
