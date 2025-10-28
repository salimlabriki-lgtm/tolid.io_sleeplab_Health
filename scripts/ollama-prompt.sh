#!/usr/bin/env bash
# Envoyer un prompt au modèle via l'API Ollama.
# USAGE:
#   ./scripts/ollama_prompt.sh "Dis bonjour en 5 mots"
#
# 🔧 Bare-metal localhost :
#   OLLAMA_MODEL=tinyllama ./scripts/ollama_prompt.sh "Hello"
#
# 🐳 Depuis un conteneur (ou Gitpod/CI si tu veux appeler le service Docker) :
#   OLLAMA_HOST=ollama OLLAMA_MODEL=tinyllama ./scripts/ollama_prompt.sh "Hello"

set -euo pipefail
HOST="${OLLAMA_HOST:-localhost}"
PORT="${OLLAMA_PORT:-11434}"
MODEL="${OLLAMA_MODEL:-tinyllama}"
PROMPT="${1:-Say hi in three words}"

payload=$(cat <<EOF
{"model":"${MODEL}","prompt":"${PROMPT}","stream":false}
EOF
)

echo "🗣️  Prompting '${MODEL}' at http://${HOST}:${PORT} ..."
curl -fsS -X POST "http://${HOST}:${PORT}/api/generate" \
  -H "Content-Type: application/json" \
  -d "${payload}"
echo
