"""
Подключение к PostgreSQL через SQLAlchemy.
Параметры соединения берутся из переменных окружения (API_DB_*),
которые прокидываются через docker-compose.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_HOST = os.getenv("API_DB_HOST", "localhost")
DATABASE_PORT = os.getenv("API_DB_PORT", "5432")
DATABASE_NAME = os.getenv("API_DB_NAME", "api")
DATABASE_USER = os.getenv("API_DB_USER", "apiuser")
DATABASE_PASS = os.getenv("API_DB_PASS", "apipass")

DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASS}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# pool_pre_ping не включаем: для лабораторного стенда хватает простого engine.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: открывает сессию и закрывает её после запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_db() -> str:
    """Проверка PostgreSQL для GET /health. Не бросает исключение наружу."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "down"