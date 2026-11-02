from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.commerce import ProductOut
from backend.app.services.catalog import get_product, list_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
async def products(
    category: str | None = Query(default=None, max_length=80),
    search: str | None = Query(default=None, max_length=120),
) -> list[ProductOut]:
    return list_products(category, search)


@router.get("/{product_id}", response_model=ProductOut)
async def product_detail(product_id: str) -> ProductOut:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product
