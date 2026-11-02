from fastapi import APIRouter

from backend.app.core.metrics import CHECKOUTS
from backend.app.db.session import SessionLocal
from backend.app.schemas.commerce import CheckoutIn, CheckoutOut
from backend.app.services.orders import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])
service = OrderService()


@router.post("/checkout", response_model=CheckoutOut, status_code=201)
async def checkout(payload: CheckoutIn) -> CheckoutOut:
    async with SessionLocal() as session:
        result = await service.checkout(payload, session)
    CHECKOUTS.labels(payment_method=payload.payment_method).inc()
    return result
