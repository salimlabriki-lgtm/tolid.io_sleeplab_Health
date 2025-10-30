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

.PHONY: rag-files rag-files-q rag-files-heavy rag-files-light

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

rag-files-light:
	@python scripts/rag_fetch_files.py --root data/raw --exts "csv,xlsx,edf" --max-rows-per-file 150 \
	| python scripts/rag_select.py "metadata extraction" --k 3 --chunk-lines 200 --overlap 40 \
	| python scripts/rag_ask.py "Output ONLY the Markdown table (no preface, no notes)."
rag-metadata:
	@python scripts/rag_fetch_files.py --root data/raw --exts "csv,xlsx,edf" --max-rows-per-file $${MAX_ROWS:-200} \
	| python scripts/rag_select.py "metadata catalog extraction" --k $${K:-8} --chunk-lines $${CHUNK:-300} --overlap $${OVL:-60} \
	| OLLAMA_MODEL="$${OLLAMA_MODEL:-qwen2.5:0.5b}" NUM_CTX=$${NUM_CTX:-16384} REQUEST_TIMEOUT=$${REQUEST_TIMEOUT:-900} NUM_PREDICT=$${NUM_PREDICT:-2048} \
	  python scripts/rag_ask.py "Build ONLY the required Markdown table (no other text)."
rag-metadata-per-file:
	@mkdir -p outputs
	@OLLAMA_MODEL="$${OLLAMA_MODEL:-qwen2.5:0.5b}" NUM_CTX=$${NUM_CTX:-16384} REQUEST_TIMEOUT=$${REQUEST_TIMEOUT:-900} NUM_PREDICT=$${NUM_PREDICT:-2048} \
	  python scripts/rag_metadata_per_file.py data/raw outputs/metadata_catalog.md 300
rag-metadata-each:
	@mkdir -p outputs
	@OLLAMA_MODEL="$${OLLAMA_MODEL:-qwen2.5:0.5b}" NUM_CTX=$${NUM_CTX:-16384} NUM_PREDICT=$${NUM_PREDICT:-1500} REQUEST_TIMEOUT=$${REQUEST_TIMEOUT:-900} \
	  python scripts/rag_metadata_per_file.py data/raw outputs 200

