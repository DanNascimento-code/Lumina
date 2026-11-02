"""Idempotent ingestion of the fictional Lumina knowledge base into pgvector."""

import asyncio
import hashlib
import re
from pathlib import Path

import structlog
from langchain_openai import OpenAIEmbeddings
from sqlalchemy import delete, text

from backend.app.core.config import get_settings
from backend.app.db.session import SessionLocal, engine
from backend.app.models import Base, DocumentChunk
from backend.app.rag.guardrails import PromptInjectionGuard

log = structlog.get_logger()
settings = get_settings()
knowledge_dir = Path(__file__).resolve().parents[2] / "knowledge"


def split_markdown(markdown: str, max_chars: int = 1800, overlap: int = 180) -> list[str]:
    """Heading-aware chunker with bounded overlap for policy documents."""
    sections = re.split(r"\n(?=##? )", markdown.strip())
    chunks: list[str] = []
    current = ""
    for section in sections:
        if len(current) + len(section) + 2 <= max_chars:
            current = f"{current}\n\n{section}".strip()
            continue
        if current:
            chunks.append(current)
        if len(section) <= max_chars:
            current = section
            continue
        start = 0
        while start < len(section):
            end = min(start + max_chars, len(section))
            chunks.append(section[start:end])
            start = max(end - overlap, start + 1)
        current = ""
    if current:
        chunks.append(current)
    return chunks


async def ingest() -> None:
    if not settings.has_llm:
        raise RuntimeError("Set OPENAI_API_KEY to generate embeddings and run ingestion.")
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
        api_key=settings.openai_api_key,
    )
    guard = PromptInjectionGuard()
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await connection.run_sync(Base.metadata.create_all)
        await connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_document_chunks_fts ON document_chunks "
                "USING gin (to_tsvector('portuguese', coalesce(title, '') || ' ' || content))"
            )
        )

    async with SessionLocal() as session:
        for path in sorted(knowledge_dir.glob("*.md")):
            markdown = path.read_text(encoding="utf-8")
            safety = guard.inspect_document(markdown)
            if not safety.allowed:
                log.error("document_quarantined", document=path.name, reason=safety.reason)
                continue
            title = markdown.splitlines()[0].removeprefix("# ").strip()
            document_id = path.stem
            chunks = split_markdown(markdown)
            vectors = await embeddings.aembed_documents(chunks)
            await session.execute(
                delete(DocumentChunk).where(
                    DocumentChunk.tenant_id == "lumina",
                    DocumentChunk.document_id == document_id,
                )
            )
            for index, (content, vector) in enumerate(zip(chunks, vectors, strict=True)):
                session.add(
                    DocumentChunk(
                        tenant_id="lumina",
                        document_id=document_id,
                        chunk_index=index,
                        title=title,
                        content=content,
                        source=f"knowledge/{path.name}",
                        doc_type=path.stem.split("_")[0],
                        metadata_={"versioned": True, "language": "pt-BR"},
                        embedding=vector,
                        checksum=hashlib.sha256(content.encode()).hexdigest(),
                    )
                )
            log.info("document_ingested", document=path.name, chunks=len(chunks))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(ingest())
