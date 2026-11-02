from decimal import Decimal
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class ProductOut(BaseModel):
    id: str
    slug: str
    name: str
    short_description: str
    description: str
    category: str
    price: Decimal
    old_price: Decimal | None = None
    rating: float
    review_count: int
    stock: int
    image_url: str
    accent: str
    badges: list[str] = []
    specs: dict[str, Any] = {}


class OrderItemIn(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, le=10)


class AddressIn(BaseModel):
    postal_code: str = Field(min_length=8, max_length=10)
    street: str = Field(min_length=3, max_length=160)
    number: str = Field(min_length=1, max_length=20)
    complement: str = Field(default="", max_length=80)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=2)


class CheckoutIn(BaseModel):
    customer_name: str = Field(min_length=3, max_length=160)
    customer_email: EmailStr
    items: list[OrderItemIn] = Field(min_length=1, max_length=30)
    address: AddressIn
    payment_method: str = Field(pattern="^(credit_card|pix)$")


class CheckoutOut(BaseModel):
    order_id: str
    code: str
    status: str
    total: Decimal
    message: str
    estimated_delivery: str
