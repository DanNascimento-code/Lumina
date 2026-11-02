# Technical architecture

## Assistant request lifecycle

| Stage | Responsibility | Safe failure behavior |
|---|---|---|
| Input guard | Normalize Unicode and inspect direct injection, role tags, invisible characters and encoded payloads | Refuse without sending the message to the LLM |
| Contextual query | Use a bounded recent history window | Prevent unbounded context growth |
| Retrieval | Search vector and lexical indexes with 24 candidates per channel | Use the versioned local knowledge layer during provider outages |
| Fusion | Apply Reciprocal Rank Fusion with `k=60` | Avoid direct comparison of incompatible scores |
| Reranking | Combine fused rank with query-term coverage | Send only the top six chunks to generation |
| Answerability | Require a minimum relevance score of `0.32` | Return an explicit abstention |
| Generation | Use temperature `0.1`, strict source boundaries and structured output | Fall back to deterministic grounded responses on timeout |
| Validation | Allow only retrieved source IDs and require at least one valid citation | Convert unsupported output to abstention |
| Actions | Return UI suggestions only | Transactional APIs validate every state change |

## Scaling model

- Async FastAPI endpoints and a SQLAlchemy/asyncpg pool configured for 10 base connections and 20 overflow connections.
- HNSW indexes with `m=16`, `ef_construction=64` and `iterative_scan=relaxed_order` for filtered retrieval.
- GIN index over `to_tsvector` for lexical retrieval.
- Idempotent ingestion keyed by tenant, document, chunk index and checksum.
- `tenant_id` on every chunk. Large installations should partition by tenant or use partial indexes to prevent HNSW post-filter recall loss.
- Stateless assistant service. Durable conversation state can be stored in Redis or PostgreSQL with bounded summaries.

## Threat model

- **Direct prompt injection:** heuristic inspection, a constrained model role and no privileged tools.
- **Indirect injection and RAG poisoning:** ingestion inspection, versioned sources and content boundaries.
- **Data exfiltration:** secrets never enter model context; sensitive values are excluded from logs.
- **Hallucination:** hybrid retrieval, evidence thresholds, validated citations, structured output and abstention.
- **Unauthorized actions:** the model suggests actions but never creates orders or payments directly.
- **Abuse and cost:** message limits, rate limiting, provider timeouts and bounded retrieval.

Prompt engineering is not the security boundary. Least privilege, deterministic authorization and output validation remain mandatory even when a model response appears trustworthy.

## Observability and evaluation

Prometheus exposes chat volume, latency, response modes, intent distribution, safety blocks and checkout completion. Structured JSON logs include request IDs. The golden dataset covers policy questions, product comparisons, privacy and medical-boundary questions. RAGAS measures Faithfulness, Answer Relevancy and Context Precision.
