from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from review_analyzer import __version__
from review_analyzer.api.routes import analyze, health
from review_analyzer.core.config import get_settings
from review_analyzer.core.logging import configure_logging
from review_analyzer.nlp.spacy_loader import load_spacy_model
from review_analyzer.pipeline.analyzer import ReviewAnalyzer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Warm the NLP pipeline during application startup."""

    settings = get_settings()
    app.state.analyzer = ReviewAnalyzer(nlp=load_spacy_model(settings.spacy_model))
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Aspect-level sentiment and tagging API for product reviews.",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(analyze.router)
    return app


app = create_app()
