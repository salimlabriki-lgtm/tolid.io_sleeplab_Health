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

rag-files:
	@python scripts/rag_fetch_files.py --root data/raw --glob "**/*.{csv,xlsx,edf}" --max-rows-per-file 800 \
	| python scripts/rag_select.py "analyse des canaux et fréquences d'échantillonnage" \
	| python scripts/rag_ask.py "Résume les canaux et points notables (5-7 puces)"

	@{ \
	  python scripts/rag_fetch_files.py --root data/raw --glob "**/*.csv" --max-rows-per-file 800; \
	  python scripts/rag_fetch_files.py --root data/raw --glob "**/*.xlsx" --max-rows-per-file 800; \
	  python scripts/rag_fetch_files.py --root data/raw --glob "**/*.edf" --max-rows-per-file 800; \
	} \
	| python scripts/rag_select.py "..." \
	| python scripts/rag_ask.py "..."



