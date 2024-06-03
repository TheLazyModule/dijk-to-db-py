include .env
export

up:
	docker compose up -d

down:
	docker compose down -v


postgres:
	 docker run --name $(PG_CONTAINER_NAME) -p $(PG_PORT_MAPPING) -e POSTGRES_PASSWORD=$(PGPASSWORD) -e POSTGRES_USER=$(PGUSER) -d $(IMAGE)

createdb:
	 docker exec -it $(PG_CONTAINER_NAME) createdb --username=$(PGUSER) --owner=$(PGUSER) $(PGDATABASE)

dropdb:
	 docker exec -it $(PG_CONTAINER_NAME) dropdb $(PGDATABASE) -f --username=$(PGUSER)

run:
	@echo "Running in development mode..."
	@MODE=development python3 main.py

run-prod:
	@echo "Running in production mode..."
	@MODE=production python3 main.py


migrate_up:
	migrate -path ./database/migrations -database "$(DATABASE_URL)" -verbose up

migrate_down:
	migrate -path ./database/migrations -database "$(DATABASE_URL)" -verbose down

restart_db:
	$(MAKE) migrate_down
	$(MAKE) migrate_up



shuv:
	git add .
	git commit -a
	git push

generate:
	sqlc generate


.PHONY: down, up, up-prod, run, createdb, dropdb, migrate_up, migrate_down, restart_db, server-container
