from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Intelligent Product Review Analyzer"
    environment: str = Field(default="local", validation_alias="ENVIRONMENT")
    spacy_model: str = Field(default="en_core_web_sm", validation_alias="SPACY_MODEL")
    api_url: str = Field(default="http://localhost:8000", validation_alias="API_URL")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
