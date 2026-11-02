from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievedChunk:
    id: str
    title: str
    content: str
    source: str
    doc_type: str
    score: float
    metadata: dict = field(default_factory=dict)
