# =============================================================================
#  Образ для Liquibase.
#  Задача контейнера — один раз применить миграции к БД и завершиться.
#  В базовом образе liquibase/liquibase уже есть JDBC-драйвер PostgreSQL.
# =============================================================================
FROM liquibase/liquibase:4.27

# Рабочая директория: Liquibase автоматически читает liquibase.properties
# из текущей директории, а changelog.xml — по пути из changeLogFile.
WORKDIR /liquibase/changelog

# Файл с настройками подключения к БД
COPY liquibase.properties .

# Корневой changelog и все SQL-миграции
COPY changelog.xml .
COPY changes ./changes