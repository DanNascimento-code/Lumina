from functools import lru_cache

from fastapi import APIRouter

from backend.app.core.config import get_settings
from backend.app.core.metrics import CHAT_LATENCY, CHAT_REQUESTS, SAFETY_BLOCKS
from backend.app.db.session import SessionLocal
from backend.app.rag.knowledge_base import LocalKnowledgeBase
from backend.app.rag.retriever import HybridRetriever
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.assistant import AssistantService

router = APIRouter(prefix="/assistant", tags=["assistant"])


@lru_cache
def get_assistant() -> AssistantService:
    settings = get_settings()
    knowledge_base = LocalKnowledgeBase()
    return AssistantService(settings, HybridRetriever(settings, knowledge_base))


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    with CHAT_LATENCY.time():
        async with SessionLocal() as session:
            response = await get_assistant().answer(payload, session)
    CHAT_REQUESTS.labels(mode=response.mode, intent=response.intent).inc()
    if response.mode == "safe-refusal":
        SAFETY_BLOCKS.inc()
    return response


@router.get("/starters")
async def starters() -> list[dict[str, str]]:
    return [
        {"icon": "sparkles", "label": "Find my product", "prompt": "Help me choose the right product"},
        {"icon": "compare", "label": "Compare for me", "prompt": "Compare Aurora and Nimbus for my needs"},
        {"icon": "truck", "label": "Shipping and delivery", "prompt": "How do shipping and delivery times work?"},
        {"icon": "shield", "label": "Returns and warranty", "prompt": "Explain the returns and warranty policies"},
    ]
