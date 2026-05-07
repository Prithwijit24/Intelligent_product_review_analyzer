from fastapi import Request

from review_analyzer.pipeline.analyzer import ReviewAnalyzer


async def get_analyzer(request: Request) -> ReviewAnalyzer:
    """Return the analyzer warmed by the FastAPI lifespan handler."""

    return request.app.state.analyzer
