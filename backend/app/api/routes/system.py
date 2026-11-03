from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text

from backend.app.core.config import get_settings
from backend.app.db.session import SessionLocal

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict:
    database = "connected"
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception:
        database = "fallback"
    settings = get_settings()
    return {
        "status": "ok",
        "database": database,
        "assistant_mode": "live-rag-configured" if settings.has_llm else "local-rag",
        "assistant_provider_check": "per-request",
        "version": "1.0.0",
    }


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
