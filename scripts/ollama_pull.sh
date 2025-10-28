#!/usr/bin/env bash
# Télécharger (pull) le modèle indiqué par OLLAMA_MODEL.
# 🔧 Par défaut on parle à http://localhost:11434 (bare-metal).
# 🐳 Depuis un conteneur, vise le service: OLLAMA_HOST=ollama
#     OLLAMA_HOST=ollama OLLAMA_MODEL=tinyllama ./scripts/ollama_pull.sh

set -euo pipefail
HOST="${OLLAMA_HOST:-localhost}"
PORT="${OLLAMA_PORT:-11434}"
MODEL="${OLLAMA_MODEL:-tinyllama}"

echo "⬇️  Pulling model '$MODEL' from http://$HOST:$PORT ..."
curl -fsS -X POST "http://$HOST:$PORT/api/pull" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"${MODEL}\"}"
echo
echo "✅ Model '$MODEL' pulled."
