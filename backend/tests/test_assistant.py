import pytest
from pydantic import SecretStr

from backend.app.core.config import Settings
from backend.app.rag.knowledge_base import LocalKnowledgeBase
from backend.app.rag.retriever import HybridRetriever
from backend.app.schemas.chat import ChatHistoryItem, ChatRequest
from backend.app.services.assistant import AssistantService
from backend.app.services.catalog import PRODUCTS


def local_assistant() -> AssistantService:
    settings = Settings(groq_api_key=SecretStr(""), openai_api_key=SecretStr(""))
    knowledge = LocalKnowledgeBase()
    return AssistantService(settings, HybridRetriever(settings, knowledge))


@pytest.mark.asyncio
async def test_local_assistant_answers_with_specific_catalog_facts() -> None:
    response = await local_assistant().answer(
        ChatRequest(message="Qual é a bateria do Flow Keys Pro?", locale="pt-BR"),
        session=None,
    )

    assert response.mode == "local-rag"
    assert response.grounded is True
    assert "120h" in response.message
    assert response.citations


@pytest.mark.asyncio
async def test_local_assistant_uses_history_for_follow_up() -> None:
    assistant = local_assistant()
    first_question = "Quero escrever bastante e alternar entre notebook e tablet. O que recomenda?"
    first = await assistant.answer(
        ChatRequest(message=first_question, locale="pt-BR"),
        session=None,
    )
    second = await assistant.answer(
        ChatRequest(
            message="E quanto dura a bateria dele?",
            locale="pt-BR",
            history=[
                ChatHistoryItem(role="user", content=first_question),
                ChatHistoryItem(role="assistant", content=first.message),
            ],
        ),
        session=None,
    )

    assert second.grounded is True
    assert second.message != first.message
    assert "bateria" in second.message.casefold()
    assert "Flow Keys Pro" in second.message
    assert "Slate Tab 11" in second.message
    assert "Vertex Controller" not in second.message


@pytest.mark.asyncio
async def test_policy_question_does_not_abstain_when_local_rag_has_evidence() -> None:
    response = await local_assistant().answer(
        ChatRequest(message="Como funcionam as devoluções?", locale="pt-BR"),
        session=None,
    )

    assert response.grounded is True
    assert response.confidence > 0.2
    assert response.citations


@pytest.mark.asyncio
async def test_payment_question_does_not_match_arc_product_by_substring() -> None:
    response = await local_assistant().answer(
        ChatRequest(message="Como funciona o parcelamento?", locale="pt-BR"),
        session=None,
    )

    assert "10 vezes" in response.message
    assert "Arc Charger" not in response.message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("locale", "question", "return_phrase", "refund_phrase"),
    [
        (
            "pt-BR",
            "Posso devolver uma compra online? Explique também o prazo de estorno no Pix.",
            "7 dias corridos",
            "2 dias úteis",
        ),
        (
            "en-US",
            "Can I return an online purchase, and when will my Pix refund arrive?",
            "7 calendar days",
            "2 business days",
        ),
        (
            "es-419",
            "¿Puedo devolver una compra en línea y cuándo llega el reembolso por Pix?",
            "7 días calendario",
            "2 días hábiles",
        ),
    ],
)
async def test_compound_return_questions_cover_every_part(
    locale: str,
    question: str,
    return_phrase: str,
    refund_phrase: str,
) -> None:
    response = await local_assistant().answer(
        ChatRequest(message=question, locale=locale),
        session=None,
    )

    assert response.grounded is True
    assert return_phrase in response.message
    assert refund_phrase in response.message
    assert response.citations


def test_compound_question_is_decomposed_into_retrieval_parts() -> None:
    assistant = local_assistant()
    request = ChatRequest(
        message="Posso devolver uma compra online? Explique também o prazo do estorno no Pix.",
        locale="pt-BR",
    )

    queries = assistant._retrieval_queries(request, "returns")

    assert len(queries) >= 3
    assert any("devolver" in query.casefold() for query in queries)
    assert any("estorno" in query.casefold() for query in queries)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1,000", 1000.0),
        ("1.000", 1000.0),
        ("999.90", 999.9),
        ("999,90", 999.9),
        ("1,299.90", 1299.9),
        ("1.299,90", 1299.9),
    ],
)
def test_localized_budget_parser(raw: str, expected: float) -> None:
    assert local_assistant()._parse_localized_number(raw) == expected


@pytest.mark.asyncio
async def test_local_recommendation_respects_english_thousands_separator() -> None:
    response = await local_assistant().answer(
        ChatRequest(
            message="I need headphones for travel and calls under R$1,000. What do you recommend?",
            locale="en-US",
        ),
        session=None,
    )

    assert "Aero Buds Pro" in response.message
    assert "Aurora Headphones" not in response.message
    assert "Vertex Controller" not in response.message
    assert "Nimbus Speaker" not in response.message
    assert all(float(item.price) <= 1000 for item in local_assistant()._recommend_products(
        ChatRequest(message="Headphones under R$1,000", locale="en-US")
    ))


@pytest.mark.asyncio
async def test_english_recommendation_converts_usd_budget_and_price() -> None:
    assistant = local_assistant()
    response = await assistant.answer(
        ChatRequest(
            message="I need headphones for travel and calls under $150. What do you recommend?",
            locale="en-US",
        ),
        session=None,
    )

    assert "Aero Buds Pro" in response.message
    assert "$125.98" in response.message
    assert "R$" not in response.message


@pytest.mark.asyncio
async def test_spanish_recommendation_uses_usd_price() -> None:
    response = await local_assistant().answer(
        ChatRequest(
            message=(
                "Necesito audífonos para viajes y llamadas por menos de US$150. "
                "¿Qué recomiendas?"
            ),
            locale="es-419",
        ),
        session=None,
    )

    assert "Aero Buds Pro" in response.message
    assert "$125.98" in response.message
    assert "R$" not in response.message


def test_product_price_uses_currency_for_locale() -> None:
    product = next(item for item in PRODUCTS if item.id == "aero-earbuds")

    assert local_assistant()._format_price(product, "pt-BR") == "R$ 699,90"
    assert local_assistant()._format_price(product, "en-US") == "$125.98"
    assert local_assistant()._format_price(product, "es-419") == "$125.98"
