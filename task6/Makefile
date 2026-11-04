# =============================================================================
#  Makefile — локальный LLM-стек (п.9) и dev/prod (п.10).
#
#  Локально всё в Docker: make up
#  Dev/prod: Postgres, Redis, Nginx на хосте, в Docker только приложение:
#    make dev-up    /  make prod-up
#
#  На Windows удобнее запускать из Git Bash. Нужен GNU Make.
# =============================================================================

COMPOSE       := docker compose
COMPOSE_DEV   := docker compose -f compose.dev.yaml
COMPOSE_PROD  := docker compose -f compose.prod.yaml
COMPOSE_CLAUDE := docker compose -f docker-compose-claude.yml

.PHONY: help up down restart logs ps pull \
	model-pull model-setup \
	claude-up claude-down claude \
	aider \
	dev-up dev-down dev-logs \
	prod-up prod-down prod-logs \
	app-rebuild

help:
	@echo "=== локальное окружение (п.9, всё в Docker) ==="
	@echo "  make up            поднять library + ollama + litellm + webui + searxng + redis"
	@echo "  make down          остановить локальный стек (тома НЕ удаляются)"
	@echo "  make logs          логи локального стека"
	@echo "  make ps            статус контейнеров"
	@echo "  make pull          docker compose pull"
	@echo "  make model-pull    скачать базовую модель в Ollama"
	@echo "  make model-setup   создать overlay claude-local (num_ctx=4096)"
	@echo "  make claude-up     контейнер Claude Code CLI"
	@echo "  make claude        интерактивный Claude Code (нужен TTY)"
	@echo "  make aider         Aider: редактирование кода через LiteLLM"
	@echo ""
	@echo "=== dev / prod (п.10, в Docker только app) ==="
	@echo "  make dev-up        приложение с --reload, БД/Redis/Nginx на хосте"
	@echo "  make dev-down      остановить dev-контейнеры"
	@echo "  make prod-up       приложение без bind-mount"
	@echo "  make prod-down     остановить prod-контейнеры"
	@echo ""
	@echo "Open WebUI:  http://127.0.0.1:3000"
	@echo "API (local): http://127.0.0.1:8080"
	@echo "LiteLLM:     http://127.0.0.1:4000"
	@echo "SearXNG:     http://127.0.0.1:8085"

# ----- п.9: локальная инфраструктура -----
# down без -v: volume ollama-data (десятки ГБ моделей) не трогаем.

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down
	$(COMPOSE_CLAUDE) down

restart: down up

logs:
	$(COMPOSE) logs -f --tail=100

ps:
	$(COMPOSE) ps -a
	$(COMPOSE_CLAUDE) ps -a

pull:
	$(COMPOSE) pull

# База для claude-local. Переопределение: make model-pull OLLAMA_MODEL=…
model-pull:
	docker exec ollama ollama pull $(or $(OLLAMA_MODEL),mistral-nemo:12b)

# Overlay не качает веса повторно — только параметры из claude/Modelfile.
model-setup: model-pull
	docker cp claude/Modelfile ollama:/tmp/Modelfile
	docker exec ollama ollama create claude-local -f /tmp/Modelfile

claude-up:
	$(COMPOSE_CLAUDE) up -d --build

claude-down:
	$(COMPOSE_CLAUDE) down

# Нужен TTY (Git Bash / Windows Terminal). Из Make в cmd.exe -it часто ломается.
claude: claude-up
	docker exec -it claude-code claude

# Профиль tools: aider не стартует вместе с make up.
aider:
	$(COMPOSE) --profile tools run --rm aider

app-rebuild:
	$(COMPOSE) up -d --build app

# ----- п.10: dev (системные postgres/redis/nginx) -----

dev-up:
	$(COMPOSE_DEV) up -d --build

dev-down:
	$(COMPOSE_DEV) down

dev-logs:
	$(COMPOSE_DEV) logs -f --tail=100

# ----- п.10: prod -----

prod-up:
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f --tail=100
