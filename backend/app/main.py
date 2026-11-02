from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from backend.app.api.routes import chat, orders, products, system
from backend.app.core.config import get_settings
from backend.app.core.logging import configure_logging
from backend.app.core.middleware import (
    InMemoryRateLimitMiddleware,
    RequestContextMiddleware,
    SecurityHeadersMiddleware,
)
from backend.app.db.session import engine
from backend.app.models import Base

configure_logging()
log = structlog.get_logger()
settings = get_settings()
frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        async with engine.begin() as connection:
            await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await connection.run_sync(Base.metadata.create_all)
        log.info("database_ready")
    except Exception as exc:
        log.warning("database_unavailable_local_fallback", error=type(exc).__name__)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Commerce API with a secure, hybrid, source-grounded RAG assistant.",
    lifespan=lifespan,
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Request-ID"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(InMemoryRateLimitMiddleware)
app.add_middleware(RequestContextMiddleware)

app.include_router(system.router)
app.include_router(products.router, prefix=settings.api_prefix)
app.include_router(orders.router, prefix=settings.api_prefix)
app.include_router(chat.router, prefix=settings.api_prefix)


if frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="storefront")
else:

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {"name": settings.app_name, "docs": "/docs", "health": "/health"}
