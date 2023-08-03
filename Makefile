default: help;

SVC_BACKEND=backend

# Hidden commands, to be used as deps
_env: ## Build .env with needed info for docker compose
	echo "USER_UID=$$(id -u)" > .env
	echo "USER_GID=$$(id -g)" >> .env
	echo "USERNAME=$$(id -un)" >> .env
	echo "HOME_DIR=$${HOME}" >> .env
.PHONY: _env

_build: _env ## Pull & build the services
	docker compose build --pull
.PHONY: _build

# Usable commands
up: ## Start all the containers
	docker compose up -d
	docker compose logs -f
.PHONY: up

stop: ## Stop and remove all the containers
	docker compose down
.PHONY: stop

backend: _build ## Open a bash inside the backend container
	docker compose run --rm ${SVC_BACKEND} poetry shell
.PHONY: bash_backend

setup: _build ## Build and install the dependencies
	docker compose run --rm ${SVC_BACKEND} poetry install --sync
.PHONY: setup

test: ## Launch unit tests
	docker compose run --rm ${SVC_BACKEND} poetry run pytest
.PHONY: test

format: ## Format all files inside backend with black & isort
	docker compose run --rm ${SVC_BACKEND} poetry run black .
	docker compose run --rm ${SVC_BACKEND} poetry run isort .
.PHONY: format

check_format: ## Format all files inside backend with black & isort
	docker compose run --rm ${SVC_BACKEND} poetry run black --check .
	docker compose run --rm ${SVC_BACKEND} poetry run isort -c .
.PHONY: check_format

check_linting: ## Verify code with lint tools, like pylint
	docker compose run --rm ${SVC_BACKEND} poetry run pylint ./src/backend
.PHONY: check_format

help: ## Display commands help
	@grep -E '^[a-zA-Z][a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
