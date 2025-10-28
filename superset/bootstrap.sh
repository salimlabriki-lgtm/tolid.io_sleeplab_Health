#!/usr/bin/env bash
set -euo pipefail

# Attendre Postgres (superset et ta DB L2)
echo "Waiting for Postgres at ${DB_HOST:-postgres}:5432 ..."
for i in {1..60}; do
  (</dev/tcp/${DB_HOST:-postgres}/5432) && break || sleep 2
done

# Init base interne de Superset
superset db upgrade

# Créer l'admin (idempotent)
superset fab create-admin \
  --username ${SUPERSET_ADMIN:-admin} \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \
  --password ${SUPERSET_PASSWORD:-admin} || true

# Démarrage minimal
superset init

# Sanity check
curl -fsS http://localhost:8088/health || true

# Lancer le serveur
exec gunicorn \
  -w 3 \
  -k gevent \
  --timeout 300 \
  -b 0.0.0.0:8088 \
  "superset.app:create_app()"
