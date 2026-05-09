from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    product_id: str | None = None
    review_text: str
    cleaned_text: str
    overall_sentiment: str
    aspects: dict[str, str] = Field(default_factory=dict)
    aspect_terms: dict[str, list[str]] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    normalized_tokens: list[str] = Field(default_factory=list)
