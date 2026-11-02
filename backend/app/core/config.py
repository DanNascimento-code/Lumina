from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    app_name: str = "Lumina Commerce AI"
    app_env: str = "development"
    app_secret_key: SecretStr = SecretStr("dev-only-change-this-secret-before-production")
    api_prefix: str = "/api/v1"
    frontend_origin: str = "http://localhost:5173"

    database_url: str = "postgresql+asyncpg://lumina:lumina@localhost:5432/lumina"
    openai_api_key: SecretStr | None = None
    llm_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    llm_temperature: float = Field(default=0.1, ge=0, le=1)

    rag_vector_candidates: int = Field(default=24, ge=4, le=100)
    rag_lexical_candidates: int = Field(default=24, ge=4, le=100)
    rag_rerank_top_k: int = Field(default=6, ge=2, le=12)
    rag_min_relevance: float = Field(default=0.32, ge=0, le=1)
    max_user_message_chars: int = Field(default=4000, ge=200, le=12000)
    enable_ragas: bool = False

    @property
    def has_llm(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.get_secret_value().strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
