from collections import defaultdict

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import Settings
from backend.app.rag.embeddings import build_embeddings
from backend.app.rag.knowledge_base import LocalKnowledgeBase, tokenize
from backend.app.rag.types import RetrievedChunk

log = structlog.get_logger()


class HybridRetriever:
    """Postgres FTS + pgvector candidates, fused with RRF and deterministically reranked."""

    def __init__(self, settings: Settings, local_kb: LocalKnowledgeBase) -> None:
        self.settings = settings
        self.local_kb = local_kb
        self.embeddings = build_embeddings(settings)

    async def retrieve(self, query: str, session: AsyncSession | None) -> list[RetrievedChunk]:
        if session is None or self.embeddings is None:
            return self.local_kb.search(query, self.settings.rag_rerank_top_k)
        try:
            # Do not spend an embeddings request when the production database is unavailable.
            await session.execute(text("SELECT 1"))
            vector = await self.embeddings.aembed_query(query)
            vector_rows = await self._vector_search(session, vector)
            lexical_rows = await self._lexical_search(session, query)
            return self._fuse_and_rerank(query, vector_rows, lexical_rows)
        except Exception as exc:  # database/provider outage must degrade gracefully
            log.warning("rag_retrieval_fallback", error=type(exc).__name__)
            return self.local_kb.search(query, self.settings.rag_rerank_top_k)

    async def _vector_search(self, session: AsyncSession, vector: list[float]) -> list[dict]:
        await session.execute(text("SET LOCAL hnsw.iterative_scan = 'relaxed_order'"))
        result = await session.execute(
            text(
                """
                SELECT id::text, title, content, source, doc_type, metadata,
                       1 - (embedding <=> CAST(:embedding AS vector)) AS score
                FROM document_chunks
                WHERE tenant_id = 'lumina' AND is_active = true AND embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :candidate_limit
                """
            ),
            {"embedding": str(vector), "candidate_limit": self.settings.rag_vector_candidates},
        )
        return [dict(row) for row in result.mappings()]

    async def _lexical_search(self, session: AsyncSession, query: str) -> list[dict]:
        result = await session.execute(
            text(
                """
                SELECT id::text, title, content, source, doc_type, metadata,
                       ts_rank_cd(
                         to_tsvector('portuguese', coalesce(title, '') || ' ' || content),
                         websearch_to_tsquery('portuguese', :query)
                       ) AS score
                FROM document_chunks
                WHERE tenant_id = 'lumina' AND is_active = true
                  AND to_tsvector('portuguese', coalesce(title, '') || ' ' || content)
                      @@ websearch_to_tsquery('portuguese', :query)
                ORDER BY score DESC
                LIMIT :candidate_limit
                """
            ),
            {"query": query, "candidate_limit": self.settings.rag_lexical_candidates},
        )
        return [dict(row) for row in result.mappings()]

    def _fuse_and_rerank(
        self, query: str, vector_rows: list[dict], lexical_rows: list[dict]
    ) -> list[RetrievedChunk]:
        rrf_scores: dict[str, float] = defaultdict(float)
        rows_by_id: dict[str, dict] = {}
        for rows in (vector_rows, lexical_rows):
            for rank, row in enumerate(rows, start=1):
                row_id = row["id"]
                rrf_scores[row_id] += 1 / (60 + rank)
                rows_by_id[row_id] = row

        query_tokens = tokenize(query)
        chunks: list[RetrievedChunk] = []
        max_rrf = max(rrf_scores.values(), default=1)
        for row_id, rrf in rrf_scores.items():
            row = rows_by_id[row_id]
            content_tokens = tokenize(f"{row['title']} {row['content']}")
            coverage = len(query_tokens & content_tokens) / max(len(query_tokens), 1)
            normalized_rrf = rrf / max_rrf
            score = min(0.99, normalized_rrf * 0.68 + coverage * 0.32)
            chunks.append(
                RetrievedChunk(
                    id=row_id,
                    title=row["title"],
                    content=row["content"],
                    source=row["source"],
                    doc_type=row["doc_type"],
                    score=score,
                    metadata=row.get("metadata") or {},
                )
            )
        return sorted(chunks, key=lambda chunk: chunk.score, reverse=True)[
            : self.settings.rag_rerank_top_k
        ]
