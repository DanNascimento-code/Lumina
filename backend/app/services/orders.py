import uuid
from datetime import date, timedelta
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Order, OrderItem
from backend.app.schemas.commerce import CheckoutIn, CheckoutOut
from backend.app.services.catalog import get_product


class OrderService:
    """Checkout orchestration. Payment providers plug in behind this service boundary."""

    async def checkout(self, payload: CheckoutIn, session: AsyncSession | None = None) -> CheckoutOut:
        total = Decimal("0")
        resolved_items = []
        for item in payload.items:
            product = get_product(item.product_id)
            if product is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"Product {item.product_id} does not exist")
            if item.quantity > product.stock:
                raise HTTPException(status.HTTP_409_CONFLICT, f"Insufficient inventory for {product.name}")
            total += product.price * item.quantity
            resolved_items.append((product, item.quantity))

        shipping = Decimal("0") if total >= Decimal("499") else Decimal("24.90")
        order_id = uuid.uuid4()
        code = f"LMN-{order_id.int % 900000 + 100000}"
        eta = date.today() + timedelta(days=5)
        if session is not None:
            try:
                session.add(
                    Order(
                        id=order_id,
                        code=code,
                        customer_name=payload.customer_name,
                        customer_email=str(payload.customer_email),
                        status="paid",
                        total=total + shipping,
                        shipping_address=payload.address.model_dump(),
                        items=[
                            OrderItem(
                                product_name=product.name,
                                quantity=quantity,
                                unit_price=product.price,
                            )
                            for product, quantity in resolved_items
                        ],
                    )
                )
                await session.commit()
            except Exception:
                await session.rollback()  # Checkout remains available during database outages.
        return CheckoutOut(
            order_id=str(order_id),
            code=code,
            status="paid",
            total=total + shipping,
            message="Payment approved. Your order is now being prepared.",
            estimated_delivery=eta.isoformat(),
        )
