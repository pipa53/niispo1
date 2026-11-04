\# Overview

Отчёт по лабораторной работе №1 «Управление многоконтейнерными системами».



Дисциплина: «Непрерывное интегрирование и сборка программного обеспечения».

БГУ, ФПМИ, кафедра технологий программирования, 2026.



\# Usage

To check, please, preview report by \[docs/report.md](docs/report.md) and source files in `task1/` — `task6/`.



Проверка результатов:

\- \*\*Отчёт:\*\* \[docs/report.md](docs/report.md) — 6 заданий, ответы на 32 контрольных вопроса, список источников.

\- \*\*Скриншоты:\*\* \[docs/screenshots/](docs/screenshots/) — 83 шт., сгруппированы по заданиям (`task1-01-…` … `task6-26-…`).

\- \*\*Исходники:\*\* папки `task1/` … `task6/`.



\# Structure

\- `task1/` — основы Docker: запуск nginx-контейнеров, `exec`, `stop/rm`, bind mount

\- `task2/` — сборка собственного образа по Dockerfile и публикация в Docker Hub

\- `task3/` — эволюция Dockerfile v1→v6, оптимизация размера (441 MB → 29 MB), non-root

\- `task4/` — Docker Compose: nginx + FastAPI + PostgreSQL, две сети, healthcheck

\- `task5/` — CRUD-приложение «Учёт читателей библиотеки» (вариант 1): FastAPI + SQLAlchemy + Liquibase + Swagger

\- `task6/` — локальная LLM-инфраструктура (Ollama + LiteLLM + Open WebUI + SearXNG), Claude Code CLI, dev/prod-окружения, Makefile

\- `docs/report.md` — общий отчёт

\- `docs/screenshots/` — скриншоты (83 шт.)

\- `README.md` — этот файл

\- `.gitignore` — исключения секретов, кешей, IDE-файлов



\# Author

\*\*Бельский Тимофей Дмитриевич\*\*, группа \*\*11а\*\*

GitHub: \[@pipa53](https://github.com/pipa53)



\# Docker Hub

Образ из задания 2: \[timofeos/mynginx-lab1](https://hub.docker.com/r/timofeos/mynginx-lab1) (тег `v1`).



```bash

docker pull timofeos/mynginx-lab1:v1

docker run --name mynginx-lab1 -p 8083:80 -d timofeos/mynginx-lab1:v1

```



\# Технологии

| Компонент | Версия / назначение |

| --- | --- |

| Docker Desktop | Engine \*\*29.8.0\*\*, API 1.55 |

| Docker Compose | v5.5.1 (плагин CLI) |

| Buildx | v0.37.0-desktop.1 |

| WSL2 | ядро 6.18.33.2-microsoft-standard-WSL2 |

| Python (локально) | 3.13 в venv, 3.12.1 в Docker-образах |

| Node.js | 22 (`node:22-slim` для Claude Code CLI) |

| FastAPI | 0.110.2 + Uvicorn 0.29.0 |

| SQLAlchemy | 2.0.29 |

| PostgreSQL | 16.2-alpine |

| Redis | 7.2-alpine |

| Liquibase | 4.27 |

| Nginx | alpine |

| Ollama | локальный инференс LLM на GPU NVIDIA RTX 4070 Laptop (8 ГБ VRAM) |

| LiteLLM | OpenAI/Anthropic-совместимый роутер |

| Open WebUI | чат-интерфейс в браузере |

| GNU Make | автоматизация стенда (`task6/Makefile`) |



\# Запуск проектов

Каждое задание самодостаточно и запускается из своей папки.



\*\*Задание 4\*\* (nginx + FastAPI + PostgreSQL):

```bash

cd task4/compose

docker compose up -d

curl http://localhost:8080/

docker compose down -v

```



\*\*Задание 5\*\* (учёт читателей с миграциями):

```bash

cd task5

docker compose up -d

curl http://localhost:8080/readers

curl http://localhost:8080/report

\# Swagger: http://localhost:8080/docs

docker compose down -v

```



\*\*Задание 6\*\* (LLM-стек + Claude Code):

```bash

cd task6

make up           # поднять local-стек

make model-setup  # pull mistral-nemo:12b + создание claude-local

make claude-up    # контейнер Claude Code CLI

docker exec -it claude-code claude

```



Подробности по каждому заданию — в \[docs/report.md](docs/report.md).



\# Additional Notes

Лабораторная работа №1 по дисциплине «Непрерывное интегрирование и сборка программного обеспечения».

БГУ, ФПМИ, кафедра технологий программирования, 2026.



\*\*Ключевые результаты:\*\*

\- Опубликованный образ на Docker Hub: `timofeos/mynginx-lab1:v1`.

\- Оптимизация Python-образа от 441 MB (v1) до 29 MB (v5-alpine) — экономия \~93%.

\- Стек из 3 сервисов (nginx + FastAPI + PostgreSQL) через Docker Compose.

\- CRUD-приложение с миграциями Liquibase и Swagger UI.

\- Локальная LLM (mistral-nemo:12b) на GPU, подключённая к Claude Code CLI через нативный Anthropic API Ollama.



\*\*Заметки по безопасности:\*\*

\- Секреты (`.env`) \*\*не коммитятся\*\* — см. `.gitignore`.

\- Пароли в `task4`/`task5` (`apipass`) — учебные, для локального стенда.

\- В задании 6 контейнеры LLM изолированы в internal-сетях, наружу выходят только published-порты на `127.0.0.1`.
