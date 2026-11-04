"""
ORM-модель таблицы reader.
Имя таблицы (__tablename__) должно совпадать с тем, что создаёт Liquibase
в миграции 01-create-reader-table.sql.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func
from database import Base


class Reader(Base):
    """Строка таблицы reader: схема задаётся Liquibase, здесь только маппинг."""
    __tablename__ = "reader"

    id             = Column(Integer, primary_key=True, index=True)   # SERIAL
    full_name      = Column(String(255), nullable=False)              # ФИО
    ticket_number  = Column(String(50), nullable=False, unique=True)  # номер билета
    has_ticket     = Column(Boolean, nullable=False, default=True)    # True = билет активен
    book_title     = Column(String(255), nullable=True)               # книга на руках
    book_issued_at = Column(Date, nullable=True)                      # дата выдачи
    created_at     = Column(DateTime, server_default=func.now(), nullable=False)