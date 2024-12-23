DOCKER_COMPOSE = docker-compose
DJANGO_MANAGE = python manage.py
PROJECT_NAME = post-flow

.PHONY: help dev prod create-admin populate-db reset-db

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  dev          - Run Django in development mode (with auto-reload)"
	@echo "  prod         - Run Django in production mode (with Gunicorn)"
	@echo "  create-admin - Create a superuser admin"
	@echo "  populate-db  - Populate the database with initial data"
	@echo "  reset-db     - Reset the database"

dev:
	@echo "Running Django in development mode..."
	$(DOCKER_COMPOSE) up

prod:
	@echo "Coming soon..."

create-admin:
	@echo "Creating admin user..."
	$(DOCKER_COMPOSE) exec web $(DJANGO_MANAGE) shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

populate-db:
	@echo "Populating the database with initial data..."
	$(DOCKER_COMPOSE) exec web $(DJANGO_MANAGE) loaddata initial_data.json

reset-db:
	@echo "Resetting the database..."
	$(DOCKER_COMPOSE) exec web $(DJANGO_MANAGE) flush --noinput

