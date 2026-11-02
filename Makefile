.PHONY: dev api web test lint ingest eval up down

dev:
	@echo "Run 'make api' and 'make web' in separate terminals."
api:
	uv run uvicorn backend.app.main:app --reload --port 8000
web:
	cd frontend && npm run dev
test:
	uv run pytest
lint:
	uv run ruff check backend
	cd frontend && npm run lint
ingest:
	uv run python -m backend.app.rag.ingest
eval:
	uv run --extra eval python -m backend.evals.run_ragas
up:
	docker compose up --build
down:
	docker compose down
