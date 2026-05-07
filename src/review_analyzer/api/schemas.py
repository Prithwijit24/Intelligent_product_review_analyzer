from pydantic import BaseModel, Field

from review_analyzer.pipeline.schemas import AnalysisResult

AnalyzeResponse = AnalysisResult


class AnalyzeRequest(BaseModel):
    review_text: str = Field(..., min_length=1, max_length=10_000)
    product_id: str | None = Field(default=None, max_length=128)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str
