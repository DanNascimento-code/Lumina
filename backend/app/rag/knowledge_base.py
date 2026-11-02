import math
import re
from pathlib import Path

from backend.app.rag.types import RetrievedChunk

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "knowledge"


def tokenize(text: str) -> set[str]:
    stop = {"a", "o", "e", "de", "da", "do", "das", "dos", "um", "uma", "para", "por", "com"}
    return {word for word in re.findall(r"[\wÀ-ÿ-]+", text.lower()) if len(word) > 2 and word not in stop}


class LocalKnowledgeBase:
    """Deterministic local knowledge layer used during provider outages and development."""

    def __init__(self) -> None:
        self._documents = self._load_documents()

    @staticmethod
    def _load_documents() -> list[RetrievedChunk]:
        documents: list[RetrievedChunk] = []
        for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = text.splitlines()[0].removeprefix("# ").strip()
            sections = re.split(r"\n(?=## )", text)
            for index, section in enumerate(sections):
                documents.append(
                    RetrievedChunk(
                        id=f"{path.stem}-{index}",
                        title=title,
                        content=section.strip(),
                        source=f"knowledge/{path.name}",
                        doc_type=path.stem.split("_")[0],
                        score=0,
                    )
                )
        return documents

    def search(self, query: str, limit: int = 8) -> list[RetrievedChunk]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        ranked: list[RetrievedChunk] = []
        for document in self._documents:
            doc_tokens = tokenize(f"{document.title} {document.content}")
            overlap = len(query_tokens & doc_tokens)
            union = len(query_tokens | doc_tokens) or 1
            phrase_bonus = 0.12 if query.lower() in document.content.lower() else 0
            coverage = overlap / max(len(query_tokens), 1)
            jaccard = overlap / union
            score = min(0.98, coverage * 0.72 + math.sqrt(jaccard) * 0.28 + phrase_bonus)
            if score > 0.05:
                ranked.append(
                    RetrievedChunk(
                        id=document.id,
                        title=document.title,
                        content=document.content,
                        source=document.source,
                        doc_type=document.doc_type,
                        score=score,
                        metadata=document.metadata,
                    )
                )
        return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
