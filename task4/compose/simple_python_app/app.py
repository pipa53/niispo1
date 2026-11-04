"""
Задание 4. Минимальное FastAPI-приложение за Nginx.

Два эндпоинта:
  GET /            — Hello World + версия PostgreSQL
  GET /hello/{name} — приветствие по имени

Подключение к БД берётся из переменных API_DB_* (задаёт compose.yaml).
"""
from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# --- параметры соединения: внутри Compose хост = имя сервиса «db» ---
DATABASE_HOST = os.getenv("API_DB_HOST", "localhost")
DATABASE_PORT = os.getenv("API_DB_PORT", "5432")
DATABASE_NAME = os.getenv("API_DB_NAME", "api")
DATABASE_USER = os.getenv("API_DB_USER", "apiuser")
DATABASE_PASS = os.getenv("API_DB_PASS", "apipass")

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Соединение открывается при старте процесса uvicorn (учебный пример, не пул).
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


@app.get("/")
async def root():
    """Проверка связи с Postgres через Nginx: в ответе версия сервера."""
    cursor.execute("SELECT version();")
    item = cursor.fetchone()
    return {"message": "Hello World", "postgres_version": item[0]}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Простой эндпоинт без БД — удобно проверить цепочку Nginx → FastAPI."""
    return {"message": f"Hello {name}"}
