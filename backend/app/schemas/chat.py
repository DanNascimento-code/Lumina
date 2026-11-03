from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


class CartContextItem(BaseModel):
    product_id: str
    name: str
    quantity: int = Field(ge=1, le=10)
    price: float = Field(gt=0)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    locale: Literal["en-US", "pt-BR", "es-419"] = "en-US"
    session_id: str = Field(default="anonymous", max_length=100)
    history: list[ChatHistoryItem] = Field(default_factory=list, max_length=12)
    cart: list[CartContextItem] = Field(default_factory=list, max_length=20)

    @field_validator("message")
    @classmethod
    def normalize_message(cls, value: str) -> str:
        return " ".join(value.strip().split())


class Citation(BaseModel):
    id: str
    title: str
    source: str
    excerpt: str


class ProductAction(BaseModel):
    type: Literal["view_product", "add_to_cart", "open_cart", "track_order"]
    label: str
    product_id: str | None = None
    product_name: str | None = None


class ChatResponse(BaseModel):
    message: str
    intent: str
    confidence: float = Field(ge=0, le=1)
    grounded: bool
    mode: Literal["live-rag", "live-conversation", "local-rag", "safe-refusal"]
    citations: list[Citation] = []
    suggestions: list[str] = []
    actions: list[ProductAction] = []
    safety_notice: str | None = None


class LLMAnswer(BaseModel):
    answer: str = Field(description="A concise, human answer grounded in the provided context")
    cited_source_ids: list[str] = Field(
        default_factory=list, description="Only source IDs supplied in the context"
    )
    follow_up_questions: list[str] = Field(default_factory=list, max_length=3)
    answerable: bool = Field(description="Whether the context contains enough evidence to answer")
    confidence: float = Field(ge=0, le=1)
