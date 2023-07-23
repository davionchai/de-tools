.PHONY: start worker up down check-logs

start:
	dask scheduler

worker:
	dask worker tcp://localhost:8786

up:
	docker compose --verbose up -d --build

down:
	docker compose down --remove-orphans -v

check-logs:
	docker compose logs -f -t
