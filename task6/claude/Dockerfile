# =============================================================================
#  Образ для Claude Code CLI.
#
#  Собирает контейнер, внутри которого живёт официальный CLI-агент Claude Code
#  от Anthropic, направленный на локальную Ollama (Anthropic Messages API).
#
#  Claude Code CLI — это Node.js-приложение, поэтому базой берём официальный
#  образ Node.js. Slim-версия — чтобы образ был меньше.
#
#  Сам по себе контейнер при старте ничего не делает — он ждёт, когда вы
#  подключитесь к нему через `docker exec -it` и запустите Claude Code
#  в интерактивном режиме.
# =============================================================================
FROM node:22-slim

# Базовые утилиты, которые Claude Code использует в работе:
#   git   — для контроля версий и diff-ов
#   curl  — для сетевых запросов
#   ripgrep — быстрый поиск по коду (Claude Code предпочитает rg)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
        ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Claude Code CLI глобально через npm.
# Пакет @anthropic-ai/claude-code. Для лабораторного стенда берём latest;
# бинарник сразу переименовываем: в PATH должен оказаться wrapper, не CLI.
RUN npm install -g @anthropic-ai/claude-code@latest \
    && mv /usr/local/bin/claude /usr/local/bin/claude-real

# Обёртка подменяет `claude`: режет список инструментов до Bash/Read/…
# (см. claude-wrapper.sh). sed снимает Windows-CRLF, иначе /bin/sh падает.
# settings.json — модель claude-local и обычный режим разрешений (не bypass).
COPY claude-wrapper.sh /usr/local/bin/claude
COPY settings.json /tmp/claude-settings.json
RUN sed -i 's/\r$//' /usr/local/bin/claude \
    && chmod 755 /usr/local/bin/claude

# Создаём непривилегированного пользователя app — от него будем запускать
# CLI. Работа от root внутри контейнера считается плохой практикой.
RUN groupadd --system app \
    && useradd --system --create-home --gid app app

# Создаём директорию .claude заранее с правильным владельцем.
# Без этого при монтировании тома Docker создаст его от root, и Claude
# Code (работающий как app) не сможет писать внутрь — отсюда EACCES.
RUN mkdir -p /home/app/.claude \
    && cp /tmp/claude-settings.json /home/app/.claude/settings.json \
    && chown -R app:app /home/app/.claude
	
# Каталог проекта, в котором Claude Code будет работать.
# Сюда мы смонтируем папку с кодом из хоста.
WORKDIR /workspace
RUN chown -R app:app /workspace

USER app

# По умолчанию контейнер «спит» — ждём, пока пользователь подключится
# через `docker exec -it`. Это стандартный паттерн для интерактивных
# dev-контейнеров.
CMD ["sleep", "infinity"]