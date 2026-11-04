# Рабочий Dockerfile задания 3 (= v6): multi-stage slim + non-root.
# ============ STAGE 1: builder ============
FROM python:3.12.1 AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
    pip wheel --no-cache-dir --no-deps -r /app/requirements.txt --wheel-dir /app/wheels

# ============ STAGE 2: финальный образ ============
FROM python:3.12.1-slim

COPY --from=builder /app/wheels /wheels

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir /wheels/*

# Копирование кода приложения
COPY app.py /app/

# Создание непривилегированного пользователя и назначение его владельцем /app
RUN addgroup --system app \
    && adduser --system --group app \
    && chown -R app:app /app/

# Переключение на пользователя app
USER app

WORKDIR /app

# 0.0.0.0 — слушать все интерфейсы контейнера, иначе порт с хоста не достучится
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
