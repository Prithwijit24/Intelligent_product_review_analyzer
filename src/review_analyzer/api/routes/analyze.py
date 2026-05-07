from fastapi import APIRouter, Depends, HTTPException

from review_analyzer.api.dependencies import get_analyzer
from review_analyzer.api.schemas import AnalyzeRequest, AnalyzeResponse
from review_analyzer.core.exceptions import ReviewAnalyzerError
from review_analyzer.pipeline.analyzer import ReviewAnalyzer

router = APIRouter(prefix="/analyze", tags=["analysis"])
AnalyzerDependency = Depends(get_analyzer)


@router.post("", response_model=AnalyzeResponse)
async def analyze_review(
    payload: AnalyzeRequest,
    analyzer: ReviewAnalyzer = AnalyzerDependency,
) -> AnalyzeResponse:
    try:
        return analyzer.analyze(payload.review_text, payload.product_id)
    except ReviewAnalyzerError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
