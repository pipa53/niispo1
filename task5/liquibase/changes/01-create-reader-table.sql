--liquibase formatted sql

--changeset belsky:1
--comment Создание таблицы читателей библиотеки
CREATE TABLE reader (
    id             SERIAL PRIMARY KEY,          -- суррогатный ключ
    full_name      VARCHAR(255) NOT NULL,       -- ФИО
    ticket_number  VARCHAR(50)  NOT NULL UNIQUE,-- номер читательского билета
    has_ticket     BOOLEAN      NOT NULL DEFAULT TRUE,  -- TRUE = билет активен
    book_title     VARCHAR(255),                -- книга на руках (NULL = нет)
    book_issued_at DATE,                        -- дата выдачи книги
    created_at     TIMESTAMP    NOT NULL DEFAULT NOW()
);
--rollback DROP TABLE reader;