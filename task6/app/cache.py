"""
Необязательный кэш Redis. Если API_REDIS_HOST не задан или Redis недоступен,
приложение продолжает работать только с PostgreSQL.

Используется для GET /report: считать total/with_books по всей таблице
на каждый запрос незачем. После create/update/delete/issue-book/revoke-ticket
ключ сбрасывается (см. main.py), чтобы отчёт не устаревал.
"""
import json
import os

_client = None
_failed = False

REDIS_HOST = os.getenv("API_REDIS_HOST")
REDIS_PORT = int(os.getenv("API_REDIS_PORT", "6379"))
REPORT_KEY = "reader:report"
# TTL короткий: если инвалидация ключа по какой-то причине не сработала,
# через полминуты отчёт всё равно пересчитается из БД.
REPORT_TTL = 30


def get_redis():
    """
    Ленивое подключение. Один неудачный ping — дальше не долбим Redis
    (_failed=True), чтобы /health и /report не висели на таймаутах.
    """
    global _client, _failed
    if _failed or not REDIS_HOST:
        return None
    if _client is not None:
        return _client
    try:
        import redis
        _client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
        _client.ping()
        return _client
    except Exception:
        _failed = True
        _client = None
        return None


def ping() -> str:
    """Статус для GET /health: ok / down / disabled (хост не задан)."""
    r = get_redis()
    if r is None:
        return "disabled" if not REDIS_HOST else "down"
    try:
        r.ping()
        return "ok"
    except Exception:
        return "down"


def get_json(key: str):
    """Прочитать JSON из Redis. None — промаха кэша или Redis недоступен."""
    r = get_redis()
    if r is None:
        return None
    try:
        raw = r.get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None


def set_json(key: str, value, ttl: int = REPORT_TTL) -> None:
    """Записать JSON с TTL. Ошибки глотаем: кэш не должен ронять API."""
    r = get_redis()
    if r is None:
        return
    try:
        r.setex(key, ttl, json.dumps(value))
    except Exception:
        return


def delete_key(key: str) -> None:
    """Сбросить ключ после изменения данных читателей."""
    r = get_redis()
    if r is None:
        return
    try:
        r.delete(key)
    except Exception:
        return