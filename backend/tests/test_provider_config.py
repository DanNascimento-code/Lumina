from pydantic import SecretStr

from backend.app.core.config import Settings
from backend.app.rag.embeddings import LocalHashEmbeddings, build_embeddings


def test_groq_is_default_and_requires_its_own_key() -> None:
    settings = Settings(openai_api_key=SecretStr("openai-key"), llm_model=None)

    assert settings.llm_provider == "groq"
    assert settings.has_llm is False
    assert settings.active_llm_model == "openai/gpt-oss-120b"
    assert settings.llm_base_url == "https://api.groq.com/openai/v1"


def test_openai_provider_remains_supported() -> None:
    settings = Settings(
        llm_provider="openai", openai_api_key=SecretStr("openai-key"), llm_model=None
    )

    assert settings.has_llm is True
    assert settings.active_llm_model == "gpt-4.1-mini"
    assert settings.llm_base_url is None


def test_neon_database_url_is_normalized_for_asyncpg() -> None:
    settings = Settings(
        database_url="postgresql://pooled.example/lumina",
        database_url_unpooled="postgresql://direct.example/lumina?sslmode=require",
    )

    assert settings.effective_database_url.startswith(
        "postgresql+asyncpg://direct.example/lumina"
    )
    assert "ssl=require" in settings.effective_database_url
    assert "sslmode" not in settings.effective_database_url


def test_local_embeddings_are_deterministic_and_normalized() -> None:
    embeddings = LocalHashEmbeddings(dimensions=128)
    first = embeddings.embed_query("Aurora headphones with adaptive noise cancellation")
    second = embeddings.embed_query("Aurora headphones with adaptive noise cancellation")

    assert first == second
    assert len(first) == 128
    assert abs(sum(value * value for value in first) - 1.0) < 1e-9


def test_local_embedding_provider_needs_no_api_key() -> None:
    settings = Settings(embedding_provider="local", embedding_dimensions=64)

    embeddings = build_embeddings(settings)
    assert isinstance(embeddings, LocalHashEmbeddings)
    assert len(embeddings.embed_query("shipping policy")) == 64
