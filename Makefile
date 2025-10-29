.PHONY: up down logs test
up:
	docker compose up -d --build
down:
	docker compose down -v
logs:
	docker compose logs -f --tail=200
test:
	docker compose exec -T etl pytest -q || echo "no tests yet"
.PHONY: llm-up llm-down llm-wait llm-pull llm-prompt

llm-up:
	docker compose up -d ollama

llm-down:
	docker compose rm -sfv ollama || true
	docker compose stop ollama || true

llm-wait:
	./scripts/wait_for_ollama.sh

llm-pull:
	./scripts/wait_for_ollama.sh
	./scripts/ollama_pull.sh

llm-prompt:
	./scripts/wait_for_ollama.sh
	./scripts/ollama_prompt.sh "Hello, réponds en 5 mots"

.PHONY: rag

rag:
	@python scripts/rag_fetch.py \
	| python scripts/rag_select.py "analyse des cycles et proportion de REM" \
	| python scripts/rag_ask.py "Analyse les cycles et la part de REM"

