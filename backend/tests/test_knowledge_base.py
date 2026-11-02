from backend.app.rag.knowledge_base import LocalKnowledgeBase


def test_retrieves_returns_policy() -> None:
    results = LocalKnowledgeBase().search("Can I return my purchase within seven days?", limit=3)
    assert results
    assert any("Returns" in result.title for result in results)


def test_retrieves_product_comparison() -> None:
    results = LocalKnowledgeBase().search("Aurora Nimbus travel battery", limit=3)
    assert results[0].source.endswith("product_catalog.md")
