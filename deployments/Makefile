.PHONY: up check-logs down check-volume

up:
	docker compose --verbose up -d

check-logs:
	docker compose logs -f -t

down:
	docker compose down --remove-orphans -v

check-volume:
	docker system df -v
