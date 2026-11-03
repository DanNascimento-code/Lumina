"""Offline RAGAS evaluation using the configured live LLM provider."""

import asyncio
import json
from pathlib import Path

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy, ContextPrecision, Faithfulness

from backend.app.core.config import get_settings
from backend.app.rag.knowledge_base import LocalKnowledgeBase


async def main() -> None:
    settings = get_settings()
    if not settings.has_llm:
        raise RuntimeError("Configure the selected LLM provider key for the RAGAS judge.")
    dataset = json.loads(
        (Path(__file__).parent / "golden_dataset.json").read_text(encoding="utf-8")
    )
    kb = LocalKnowledgeBase()
    client_options = {"api_key": settings.active_llm_api_key.get_secret_value()}
    if settings.llm_base_url:
        client_options["base_url"] = settings.llm_base_url
    judge = llm_factory(
        settings.active_llm_model,
        client=AsyncOpenAI(**client_options),
    )
    faithfulness = Faithfulness(llm=judge)
    answer_relevancy = AnswerRelevancy(llm=judge)
    context_precision = ContextPrecision(llm=judge)
    scores: list[dict] = []

    for sample in dataset:
        contexts = [chunk.content for chunk in kb.search(sample["user_input"], limit=6)]
        response = sample["reference"]  # retriever-focused baseline; CI can replace with API response
        result = {"question": sample["user_input"]}
        metric_results = {
            "Faithfulness": await faithfulness.ascore(
                user_input=sample["user_input"], response=response, retrieved_contexts=contexts
            ),
            "AnswerRelevancy": await answer_relevancy.ascore(
                user_input=sample["user_input"], response=response
            ),
            "ContextPrecision": await context_precision.ascore(
                user_input=sample["user_input"],
                reference=sample["reference"],
                retrieved_contexts=contexts,
            ),
        }
        for name, score in metric_results.items():
            result[name] = round(float(score.value), 4)
        scores.append(result)
    print(json.dumps(scores, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
