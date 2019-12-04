up:
	@docker-compose -f docker-compose.yml up --build

down:
	@docker-compose -f docker-compose.yml down

test:
	@docker-compose -f docker-compose.yml build
	@docker-compose -f docker-compose.yml run --rm app sh entrypoints/test.sh
	@docker-compose -f docker-compose.yml down

build:
	@if [ -z ${VERSION} ]; then echo Usage: make build VERSION=0.0.0 && exit 1; fi;

	@echo "Building dev image"
	@docker-compose -f docker-compose.yml build

.PHONY: up down test build
