"""
FastAPI-приложение «Учёт читателей библиотеки» (вариант 1 ЛР №1).

Эндпоинты:
  GET    /readers                       — список всех читателей
  GET    /readers/{id}                  — карточка одного
  POST   /readers                       — добавить нового
  PUT    /readers/{id}                  — редактировать информацию
  DELETE /readers/{id}                  — удалить запись из БД
  POST   /readers/{id}/revoke-ticket    — изъять читательский билет
  POST   /readers/{id}/issue-book       — выдать книгу на руки
  POST   /readers/{id}/return-book      — вернуть книгу
  GET    /report                        — сводный отчёт

Документация Swagger доступна по адресу /docs (генерируется автоматически).
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import ReaderCreate, ReaderUpdate, ReaderOut, ReaderReport, BookIssue
from crud import (
    get_all, get_by_id, create, update, delete,
    revoke_ticket, issue_book, return_book, report,
)

app = FastAPI(
    title="Учёт читателей библиотеки",
    description="Лабораторная работа №1 по дисциплине НИиСПО. Вариант 1.",
    version="1.0.0",
)


@app.get("/", tags=["System"])
def root():
    """Служебный эндпоинт — точка входа и подсказка про /docs."""
    return {"service": "reader-api", "docs": "/docs"}


# ---------------------------------------------------------------------------
#  CRUD
# ---------------------------------------------------------------------------

@app.get("/readers", response_model=list[ReaderOut], tags=["CRUD"])
def list_readers(db: Session = Depends(get_db)):
    """Вернуть список всех читателей."""
    return get_all(db)


@app.get("/readers/{reader_id}", response_model=ReaderOut, tags=["CRUD"])
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    """Вернуть одного читателя по id."""
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return r


@app.post("/readers", response_model=ReaderOut,
          status_code=status.HTTP_201_CREATED, tags=["CRUD"])
def create_reader(data: ReaderCreate, db: Session = Depends(get_db)):
    """Добавить нового читателя. Билет сразу активен."""
    return create(db, data)


@app.put("/readers/{reader_id}", response_model=ReaderOut, tags=["CRUD"])
def update_reader(reader_id: int, data: ReaderUpdate,
                  db: Session = Depends(get_db)):
    """Редактировать информацию о читателе (частичное обновление)."""
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return update(db, r, data)


@app.delete("/readers/{reader_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["CRUD"])
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    """
    Удалить запись из БД полностью.
    Для «правильного» изъятия билета используйте POST /readers/{id}/revoke-ticket.
    """
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    delete(db, r)


# ---------------------------------------------------------------------------
#  Специфичные операции
# ---------------------------------------------------------------------------

@app.post("/readers/{reader_id}/revoke-ticket", response_model=ReaderOut,
          tags=["Operations"])
def revoke(reader_id: int, db: Session = Depends(get_db)):
    """
    Изъять читательский билет. Повторный вызов вернёт 400.
    """
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if not r.has_ticket:
        raise HTTPException(status_code=400, detail="Билет уже изъят")
    return revoke_ticket(db, r)


@app.post("/readers/{reader_id}/issue-book", response_model=ReaderOut,
          tags=["Operations"])
def issue(reader_id: int, data: BookIssue, db: Session = Depends(get_db)):
    """
    Выдать книгу на руки. Требует активного билета и отсутствия книги.
    """
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if not r.has_ticket:
        raise HTTPException(status_code=400, detail="Билет изъят — выдача невозможна")
    if r.book_title is not None:
        raise HTTPException(status_code=400, detail="У читателя уже есть книга на руках")
    return issue_book(db, r, data.book_title)


@app.post("/readers/{reader_id}/return-book", response_model=ReaderOut,
          tags=["Operations"])
def return_b(reader_id: int, db: Session = Depends(get_db)):
    """Вернуть книгу в библиотеку. Ошибка, если книги нет."""
    r = get_by_id(db, reader_id)
    if not r:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if r.book_title is None:
        raise HTTPException(status_code=400, detail="У читателя нет книги на руках")
    return return_book(db, r)


@app.get("/report", response_model=ReaderReport, tags=["Operations"])
def get_report(db: Session = Depends(get_db)):
    """
    Отчёт: сколько всего читателей и сколько держат книгу на руках.
    """
    return report(db)