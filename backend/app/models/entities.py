import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from backend.app.core.config import get_settings


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(180))
    short_description: Mapped[str] = mapped_column(String(280))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    old_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    rating: Mapped[Decimal] = mapped_column(Numeric(2, 1), default=Decimal("4.8"))
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String(500))
    accent: Mapped[str] = mapped_column(String(30), default="#9d7bff")
    specs: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(160))
    customer_email: Mapped[str] = mapped_column(String(254), index=True)
    status: Mapped[str] = mapped_column(String(40), default="paid")
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    shipping_address: Mapped[dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    items: Mapped[list["OrderItem"]] = relationship(cascade="all, delete-orphan", lazy="selectin")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("products.id"), nullable=True)
    product_name: Mapped[str] = mapped_column(String(180))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[str] = mapped_column(String(80), default="lumina", index=True)
    document_id: Mapped[str] = mapped_column(String(160), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(240))
    content: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(500))
    doc_type: Mapped[str] = mapped_column(String(80), index=True)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    content_tsv: Mapped[Any] = mapped_column(
        Text, nullable=True, deferred=True
    )  # The migration SQL creates the tsvector expression.
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(get_settings().embedding_dimensions), nullable=True
    )
    checksum: Mapped[str] = mapped_column(String(64), index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("uq_document_chunk", "tenant_id", "document_id", "chunk_index", unique=True),
        Index(
            "ix_document_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            postgresql_with={"m": 16, "ef_construction": 64},
        ),
    )
