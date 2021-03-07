# XO Makefile

POSTGRESQL_URL 	?= postgresql://test:test@127.0.0.1/test
APP_PORT       	?= 8080
POSTGRESQL_PORT ?= 5432
POSTGRESQL_HOST ?= 127.0.0.1

pipenv:
	pipenv update -d

start:
	docker-compose up -d --build

stop:
	docker-compose down -v --remove-orphans

postgresql: stop
	docker-compose run -d -p $(POSTGRESQL_PORT):$(POSTGRESQL_PORT) postgresql
	DB_PORT=$(POSTGRESQL_PORT) DB_HOST=$(POSTGRESQL_HOST) scripts/wait-services.sh
	sleep 2

postgresql-migration: postgresql migration

migration:
	POSTGRESQL_URL=$(POSTGRESQL_URL) pipenv run alembic upgrade head

test-local: postgresql-migration
	POSTGRESQL_URL=$(POSTGRESQL_URL) pipenv run pytest -v

test-docker: stop
	scripts/docker-compose-test.sh

run-local: postgresql-migration
	POSTGRESQL_URL=$(POSTGRESQL_URL) pipenv run python main.py

run-docker: start

lint:
	pipenv run bash -c 'flake8 && mypy .'

.PHONY: pipenv lint start stop postgresql test-local test-docker run-local run-docker migration postgresql-migration
