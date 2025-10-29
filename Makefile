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

.PHONY: rag-files rag-files-q

rag-files:
	@python scripts/rag_fetch_files.py --root data/raw --glob "**/*.*" --exts "csv,xlsx,edf" \
	| python scripts/rag_select.py "analyse des canaux et fréquences d'échantillonnage" \
	| python scripts/rag_ask.py "Résume les canaux et points notables (5-7 puces)"

rag-files-q:
	@python scripts/rag_fetch_files.py --root data/raw --glob "**/*.*" --exts "csv,xlsx,edf" \
	| python scripts/rag_select.py "$(Q)" \
	| python scripts/rag_ask.py "$(Q)"
rag-files-heavy:
	@python scripts/rag_fetch_files.py --root data/raw --exts "csv,xlsx,edf" \
	| python scripts/rag_select.py "analyse détaillée" --k 12 --chunk-lines 400 --overlap 80 \
	| NUM_CTX=65536 OLLAMA_MODEL="llama3.1:8b" python scripts/rag_ask.py "Analyse détaillée (10 puces)"

python scripts/rag_fetch_files.py --max-rows-per-file 100



