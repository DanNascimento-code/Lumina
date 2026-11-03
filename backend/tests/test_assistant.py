import pytest
from pydantic import SecretStr

from backend.app.core.config import Settings
from backend.app.rag.knowledge_base import LocalKnowledgeBase
from backend.app.rag.retriever import HybridRetriever
from backend.app.schemas.chat import ChatHistoryItem, ChatRequest
from backend.app.services.assistant import AssistantService


def local_assistant() -> AssistantService:
    settings = Settings(openai_api_key=SecretStr(""))
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
