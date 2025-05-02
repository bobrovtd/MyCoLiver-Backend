.PHONY: help setup dev test lint format migrate docker-up docker-down docker-build

# Default target executed when no arguments are given to make.
help:
	@echo "Available commands:"
	@echo "  setup         Install dependencies"
	@echo "  dev           Run development server"
	@echo "  test          Run tests"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code"
	@echo "  migrate       Run database migrations"
	@echo "  docker-up     Start Docker containers"
	@echo "  docker-down   Stop Docker containers"
	@echo "  docker-build  Build Docker images"

# Install dependencies
setup:
	pip install -r requirements.txt

# Run development server
dev:
	uvicorn app.app:app --reload

# Run tests
test:
	pytest

# Run linting
lint:
	flake8 app tests

# Format code
format:
	black app tests

# Run database migrations
migrate:
	alembic upgrade head

# Generate migration
migration:
	alembic revision --autogenerate -m "$(m)"

# Start Docker containers
docker-up:
	docker-compose up -d

# Stop Docker containers
docker-down:
	docker-compose down

# Build Docker images
docker-build:
	docker-compose build
