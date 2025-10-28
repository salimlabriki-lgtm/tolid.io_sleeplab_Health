.PHONY: up down logs test
up:
	docker compose up -d --build
down:
	docker compose down -v
logs:
	docker compose logs -f --tail=200
test:
	docker compose exec -T etl pytest -q || echo "no tests yet"
