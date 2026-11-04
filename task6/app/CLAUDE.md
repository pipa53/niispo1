\# Проект: «Учёт читателей библиотеки»



Это FastAPI-приложение. Рабочая директория — `/workspace`.



\## Структура



\- `main.py`     — HTTP-эндпоинты (/readers, /report, /health, /docs)

\- `crud.py`     — функции работы с БД (get\_all, create, update, delete,

&#x20;                  revoke\_ticket, issue\_book, return\_book, report)

\- `schemas.py`  — Pydantic-схемы (ReaderCreate, ReaderUpdate, ReaderOut,

&#x20;                  ReaderReport, BookIssue)

\- `models.py`   — ORM-таблица reader

\- `database.py` — подключение SQLAlchemy к PostgreSQL

\- `cache.py`    — Redis-кэш для GET /report (опциональный)



\## Бизнес-логика



\- Читатель имеет билет (`has\_ticket`) — иначе брать книги нельзя.

\- Книгу можно выдать только при активном билете и отсутствии книги на руках.

\- `revoke-ticket` сбрасывает книгу, если она была.

\- `return-book` — отдельная операция возврата.

\- Отчёт `/report` возвращает `{total, with\_books}`.

