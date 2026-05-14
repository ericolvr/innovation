COLOR_RESET=\033[0m
COLOR_GREEN=\033[32m
COLOR_YELLOW=\033[33m
COLOR_RED=\033[31m

.PHONY: help install run migrate createsuperuser build users

help:
	@echo ""
	@echo "  $(COLOR_YELLOW)Available targets:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)install$(COLOR_RESET)         - Install dependencies"
	@echo "  $(COLOR_GREEN)run$(COLOR_RESET)             - Run development server"
	@echo "  $(COLOR_GREEN)migrate$(COLOR_RESET)         - Run migrations"
	@echo "  $(COLOR_GREEN)createsuperuser$(COLOR_RESET) - Create admin user"
	@echo "  $(COLOR_GREEN)build$(COLOR_RESET)           - Build React + collectstatic"
	@echo ""

install:
	@echo "$(COLOR_YELLOW)Installing dependencies...$(COLOR_RESET)"
	pip install -r requirements.txt
	@echo "$(COLOR_GREEN)Done$(COLOR_RESET)"

run:
	@if [ ! -f .env ]; then cp .env-sample .env; fi
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate
	@echo "$(COLOR_GREEN)Migrations applied$(COLOR_RESET)"

createsuperuser:
	python manage.py createsuperuser

build:
	@echo "$(COLOR_YELLOW)Building React...$(COLOR_RESET)"
	cd ../frontend && npm run build
	@echo "$(COLOR_YELLOW)Copying to static/...$(COLOR_RESET)"
	rm -rf static
	cp -r ../frontend/dist static
	@echo "$(COLOR_YELLOW)Running collectstatic...$(COLOR_RESET)"
	python manage.py collectstatic --noinput
	@echo "$(COLOR_GREEN)Build complete$(COLOR_RESET)"

users:
	@cat users.txt 2>/dev/null || echo "no users.txt found"
