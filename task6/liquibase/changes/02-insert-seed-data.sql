--liquibase formatted sql

--changeset belsky:2
--comment Начальные данные читателей (5 строк: 2 с книгой, 2 без, 1 без билета)
INSERT INTO reader (full_name, ticket_number, has_ticket, book_title, book_issued_at) VALUES
    ('Бельский Тимофей Дмитриевич',   'AB-1001', TRUE,  'Война и мир',        '2024-09-15'),
    ('Иванов Иван Иванович',          'AB-1002', TRUE,  'Преступление и наказание', '2024-10-01'),
    ('Петрова Анна Сергеевна',        'AB-1003', TRUE,  NULL,                 NULL),
    ('Сидоров Пётр Алексеевич',       'AB-1004', TRUE,  NULL,                 NULL),
    ('Кузнецова Мария Владимировна',  'AB-1005', FALSE, NULL,                 NULL);