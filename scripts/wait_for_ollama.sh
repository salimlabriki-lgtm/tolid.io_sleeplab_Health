#!/usr/bin/env bash
# Attendre que l'API Ollama réponde.
# 🔧 Par défaut on cible l'hôte 'localhost' (utile en bare-metal).
# 🐳 Si tu appelles ce script DEPUIS UN CONTENEUR, utilise le nom du service Docker:
#     OLLAMA_HOST=ollama ./scripts/wait_for_ollama.sh
# 🌐 Si tu es sur une autre machine que l'hôte, remplace par l'IP/hostname du serveur:
#     OLLAMA_HOST=192.168.1.50 ./scripts/wait_for_ollama.sh

set -euo pipefail
HOST="${OLLAMA_HOST:-localhost}"
PORT="${OLLAMA_PORT:-11434}"
URL="http://$HOST:$PORT/api/tags"

echo "⏳ Waiting for Ollama at $URL ..."
for i in {1..60}; do
  if curl -fsS "$URL" >/dev/null; then
    echo "✅ Ollama is up ($URL)"
    exit 0
  fi
  sleep 2
done
echo "❌ Ollama not reachable ($URL)"
exit 1
