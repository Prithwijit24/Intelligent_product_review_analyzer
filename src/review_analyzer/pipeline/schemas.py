from pydantic import BaseModel, Field


class NamedEntity(BaseModel):
    text: str
    label: str
    start_char: int
    end_char: int
    source: str


class AnalysisResult(BaseModel):
    product_id: str | None = None
    review_text: str
    cleaned_text: str
    overall_sentiment: str
    aspects: dict[str, str] = Field(default_factory=dict)
    aspect_terms: dict[str, list[str]] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    named_entities: list[NamedEntity] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)
    normalized_tokens: list[str] = Field(default_factory=list)
