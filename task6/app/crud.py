"""
Слой работы с базой данных (CRUD-операции над таблицей reader).
Кэш Redis здесь не трогается — за него отвечает main.py после
успешного изменения данных.
"""
from datetime import date
from sqlalchemy.orm import Session

from models import Reader
from schemas import ReaderCreate, ReaderUpdate


def get_all(db: Session) -> list[Reader]:
    """Вернуть всех читателей, отсортированных по id."""
    return db.query(Reader).order_by(Reader.id).all()


def get_by_id(db: Session, reader_id: int) -> Reader | None:
    """Найти читателя по id. None, если не найден."""
    return db.query(Reader).filter(Reader.id == reader_id).first()


def create(db: Session, data: ReaderCreate) -> Reader:
    """
    Добавить нового читателя.
    Билет сразу активен, книг на руках нет.
    """
    reader = Reader(
        full_name=data.full_name,
        ticket_number=data.ticket_number,
        has_ticket=True,
        book_title=None,
        book_issued_at=None,
    )
    db.add(reader)
    db.commit()
    # refresh(): подтянуть id и created_at, сгенерированные в СУБД.
    db.refresh(reader)
    return reader


def update(db: Session, reader: Reader, data: ReaderUpdate) -> Reader:
    """
    Частичное обновление: model_dump(exclude_unset=True) возвращает только
    присланные клиентом поля — остальные не трогаем.
    """
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader


def delete(db: Session, reader: Reader) -> None:
    """Удалить запись из БД (жёсткое удаление)."""
    db.delete(reader)
    db.commit()


def revoke_ticket(db: Session, reader: Reader) -> Reader:
    """
    Изъять читательский билет: has_ticket = False.
    Если книга на руках — тоже обнуляем (человек больше не читатель).
    """
    reader.has_ticket = False
    reader.book_title = None
    reader.book_issued_at = None
    db.commit()
    db.refresh(reader)
    return reader


def issue_book(db: Session, reader: Reader, book_title: str) -> Reader:
    """
    Выдать книгу на руки: сохранить название и дату выдачи = сегодня.
    Проверки «билет активен» и «книги ещё нет» — в main.py.
    """
    reader.book_title = book_title
    reader.book_issued_at = date.today()
    db.commit()
    db.refresh(reader)
    return reader


def return_book(db: Session, reader: Reader) -> Reader:
    """Вернуть книгу: сбросить название и дату."""
    reader.book_title = None
    reader.book_issued_at = None
    db.commit()
    db.refresh(reader)
    return reader


def report(db: Session) -> dict:
    """
    Сводный отчёт: всего читателей / с книгой на руках.
    Считаем в Python — при небольшом объёме проще и читаемее.
    """
    all_readers = db.query(Reader).all()
    total = len(all_readers)
    with_books = sum(1 for r in all_readers if r.book_title is not None)
    return {"total": total, "with_books": with_books}