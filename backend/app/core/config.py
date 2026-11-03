from functools import lru_cache
from typing import Literal
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

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
    database_url_unpooled: str | None = None
    llm_provider: Literal["groq", "openai"] = "groq"
    groq_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    llm_model: str | None = None
    embedding_provider: Literal["local", "openai"] = "local"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    llm_temperature: float = Field(default=0.2, ge=0, le=1)

    rag_vector_candidates: int = Field(default=24, ge=4, le=100)
    rag_lexical_candidates: int = Field(default=24, ge=4, le=100)
    rag_rerank_top_k: int = Field(default=6, ge=2, le=12)
    rag_min_relevance: float = Field(default=0.18, ge=0, le=1)
    max_user_message_chars: int = Field(default=4000, ge=200, le=12000)
    enable_ragas: bool = False

    @property
    def has_llm(self) -> bool:
        return bool(self.active_llm_api_key)

    @property
    def active_llm_api_key(self) -> SecretStr | None:
        key = self.groq_api_key if self.llm_provider == "groq" else self.openai_api_key
        if key and key.get_secret_value().strip():
            return key
        return None

    @property
    def active_llm_model(self) -> str:
        if self.llm_model:
            return self.llm_model
        return "openai/gpt-oss-120b" if self.llm_provider == "groq" else "gpt-4.1-mini"

    @property
    def llm_base_url(self) -> str | None:
        return "https://api.groq.com/openai/v1" if self.llm_provider == "groq" else None

    @property
    def has_embeddings(self) -> bool:
        if self.embedding_provider == "local":
            return True
        return bool(self.openai_api_key and self.openai_api_key.get_secret_value().strip())

    @property
    def effective_database_url(self) -> str:
        url = self.database_url_unpooled or self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        parts = urlsplit(url)
        query: list[tuple[str, str]] = []
        for key, value in parse_qsl(parts.query, keep_blank_values=True):
            if key == "sslmode":
                query.append(("ssl", value))
            elif key != "channel_binding":
                query.append((key, value))
        return urlunsplit(parts._replace(query=urlencode(query)))


@lru_cache
def get_settings() -> Settings:
    return Settings()
