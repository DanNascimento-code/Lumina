"""Embedding providers used by Lumina retrieval and ingestion."""

import asyncio
import hashlib
import math
import re
import unicodedata

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from backend.app.core.config import Settings

SEMANTIC_ALIASES: dict[str, tuple[str, ...]] = {
    "returns": ("return", "returns", "devolucao", "devolver", "devolucion", "cambio", "troca"),
    "refund": ("refund", "reembolso", "estorno", "reintegro"),
    "shipping": ("shipping", "delivery", "frete", "entrega", "envio"),
    "tracking": ("tracking", "track order", "rastreio", "rastrear", "seguimiento"),
    "warranty": ("warranty", "garantia", "garantia contractual"),
    "repair": ("repair", "technical support", "conserto", "reparo", "assistencia tecnica", "soporte tecnico"),
    "payment": ("payment", "pagamento", "pago"),
    "installments": ("installment", "installments", "parcelamento", "parcelas", "cuotas"),
    "battery": ("battery", "battery life", "bateria", "autonomia"),
    "headphones": ("headphones", "headset", "fone", "fones", "audifonos", "auriculares"),
    "travel": ("travel", "trip", "viagem", "viajar", "viaje"),
    "work": ("work", "office", "trabalho", "escritorio", "oficina"),
}


class LocalHashEmbeddings(Embeddings):
    """Deterministic, zero-cost embeddings for compact commerce knowledge bases.

    The representation combines normalized words, word bigrams and character
    n-grams. It is intentionally provider-independent and keeps pgvector usable
    when no paid embedding API is configured.
    """

    def __init__(self, dimensions: int = 1536) -> None:
        self.dimensions = dimensions

    @staticmethod
    def _normalize(text: str) -> str:
        decomposed = unicodedata.normalize("NFKD", text.casefold())
        return "".join(char for char in decomposed if not unicodedata.combining(char))

    def _features(self, text: str) -> list[tuple[str, float]]:
        normalized = self._normalize(text)
        words = re.findall(r"[a-z0-9]+", normalized)
        features: list[tuple[str, float]] = [(f"w:{word}", 1.0) for word in words]
        for concept, aliases in SEMANTIC_ALIASES.items():
            if any(re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", normalized) for alias in aliases):
                features.append((f"semantic:{concept}", 2.0))
        features.extend(
            (f"b:{left}_{right}", 0.75) for left, right in zip(words, words[1:], strict=False)
        )
        compact = "_".join(words)
        for size, weight in ((3, 0.18), (4, 0.24), (5, 0.3)):
            features.extend(
                (f"c{size}:{compact[index:index + size]}", weight)
                for index in range(max(0, len(compact) - size + 1))
            )
        return features

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for feature, weight in self._features(text):
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            value = int.from_bytes(digest, "big")
            index = value % self.dimensions
            vector[index] += weight if value & 1 else -weight
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self.embed_documents, texts)

    async def aembed_query(self, text: str) -> list[float]:
        return await asyncio.to_thread(self.embed_query, text)


def build_embeddings(settings: Settings) -> Embeddings | None:
    if settings.embedding_provider == "local":
        return LocalHashEmbeddings(settings.embedding_dimensions)
    if not settings.has_embeddings:
        return None
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
        api_key=settings.openai_api_key,
        max_retries=1,
    )
