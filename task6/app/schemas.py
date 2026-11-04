"""
Pydantic-схемы для валидации запросов и ответов API.
Разделены по назначению: Create (POST), Update (PUT),
Out (ответы), Report (сводка).
"""
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# -------- Базовые поля --------
class ReaderBase(BaseModel):
    full_name:     str = Field(..., min_length=1, max_length=255, description="ФИО")
    ticket_number: str = Field(..., min_length=1, max_length=50,  description="Номер читательского билета")


# -------- Создание (POST) --------
class ReaderCreate(ReaderBase):
    """Поля при добавлении читателя. Билет сразу есть, книг нет."""
    pass


# -------- Обновление (PUT) --------
class ReaderUpdate(BaseModel):
    """Все поля опциональные — можно обновлять частично."""
    full_name:     str | None = Field(None, min_length=1, max_length=255)
    ticket_number: str | None = Field(None, min_length=1, max_length=50)


# -------- Выдача книги --------
class BookIssue(BaseModel):
    """Тело запроса при выдаче книги."""
    book_title: str = Field(..., min_length=1, max_length=255, description="Название книги")


# -------- Ответ (GET) --------
class ReaderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:             int
    full_name:      str
    ticket_number:  str
    has_ticket:     bool
    book_title:     str | None
    book_issued_at: date | None
    created_at:     datetime


# -------- Отчёт --------
class ReaderReport(BaseModel):
    total:      int = Field(..., description="Всего читателей")
    with_books: int = Field(..., description="С книгой на руках")