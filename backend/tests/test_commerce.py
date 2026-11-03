from decimal import Decimal

from backend.app.schemas.commerce import AddressIn, CheckoutIn, OrderItemIn
from backend.app.services.catalog import list_products
from backend.app.services.orders import OrderService


def test_catalog_filter() -> None:
    assert len(list_products()) == 12
    assert len(list_products(category="Audio")) == 3
    assert {product.category for product in list_products()} == {
        "Audio",
        "Wearables",
        "Smart home",
        "Workspace",
        "Accessories",
        "Mobile",
        "Gaming",
    }


async def test_checkout_has_free_shipping_above_threshold() -> None:
    payload = CheckoutIn(
        customer_name="Test Customer",
        customer_email="customer@example.com",
        items=[OrderItemIn(product_id="aurora-headphones", quantity=1)],
        address=AddressIn(
            postal_code="01310-100",
            street="Avenida Paulista",
            number="1000",
            city="São Paulo",
            state="SP",
        ),
        payment_method="pix",
    )
    result = await OrderService().checkout(payload)
    assert result.status == "paid"
    assert result.total == Decimal("1299.90")
