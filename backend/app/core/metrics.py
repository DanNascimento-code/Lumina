from prometheus_client import Counter, Histogram

CHAT_REQUESTS = Counter("lumina_chat_requests_total", "Chat requests", ["mode", "intent"])
CHAT_LATENCY = Histogram("lumina_chat_latency_seconds", "Chat endpoint latency")
SAFETY_BLOCKS = Counter("lumina_safety_blocks_total", "Blocked unsafe prompts")
CHECKOUTS = Counter("lumina_checkouts_total", "Successful simulated checkouts", ["payment_method"])
