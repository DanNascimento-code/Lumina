import time
import uuid
from collections import defaultdict, deque

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["X-Request-ID"] = getattr(request.state, "request_id", "")
        return response


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[:80]
        return await call_next(request)


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    """Development guard. Replace with Redis-backed limiting for multi-instance production."""

    def __init__(self, app, limit: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if not request.url.path.endswith("/chat"):
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        bucket = self.hits[client]
        while bucket and bucket[0] < now - self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many messages in a short period. Try again in one minute."},
                headers={"Retry-After": "60"},
            )
        bucket.append(now)
        return await call_next(request)
