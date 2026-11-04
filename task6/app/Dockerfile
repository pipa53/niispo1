# =============================================================================
#  Многостадийная сборка: тяжёлые build-зависимости (gcc) остаются в builder-
#  стадии и не попадают в финальный образ. База — slim, чтобы размер был
#  минимальным при сохранении совместимости с glibc.
# =============================================================================

# -------- STAGE 1: builder --------
FROM python:3.12.1 AS builder

# Системные зависимости, нужные только на этапе сборки psycopg2:
#   gcc           — C-компилятор
#   libpq-dev     — заголовки клиента PostgreSQL (pg_config)
# После установки apt-кэш удаляется, чтобы не раздувать промежуточный слой.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем только файл зависимостей, чтобы слой кешировался,
# пока не изменится сам requirements.txt.
COPY requirements.txt /app/requirements.txt

# Собираем wheel-пакеты всех зависимостей в /app/wheels.
# --no-deps: не тянуть транзитивные зависимости повторно (они уже в requirements).
RUN pip wheel --no-cache-dir --no-deps \
        -r /app/requirements.txt \
        --wheel-dir /app/wheels

# -------- STAGE 2: финальный образ --------
FROM python:3.12.1-slim

# Копируем заранее собранные wheel-пакеты из builder.
COPY --from=builder /app/wheels /wheels

# Рантайм-зависимость: libpq — клиентская библиотека PostgreSQL.
# Нужна psycopg2 в момент выполнения. dev-заголовки не нужны.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости из локальных wheel-файлов — без обращения в PyPI
# и без повторной сборки C-расширений.
RUN pip install --no-cache-dir /wheels/*

# Копируем исходники приложения.
COPY . /app/

# Создаём непривилегированного пользователя app и назначаем его владельцем
# каталога /app — чтобы процесс не работал от root (best practice безопасности).
RUN addgroup --system app \
    && adduser --system --group app \
    && chown -R app:app /app/
USER app

WORKDIR /app

# ENTRYPOINT — неизменяемая часть команды запуска,
# CMD — аргументы по умолчанию (можно переопределить в docker run/compose).
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]