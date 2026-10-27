# FX Rates Pipeline

ETL-пайплайн для загрузки курсов валют из [Frankfurter API](https://frankfurter.dev/) в PostgreSQL с построением аналитической витрины.

## Проблема

Аналитикам и BI-системам нужны актуальные курсы валют с аналитикой изменений (дневное изменение, скользящие средние). Писать сложные SQL-запросы каждый раз долго и дорого. Нужна готовая витрина, которая обновляется регулярно.

## Решение

Пайплайн из трёх слоёв:

1. **Extract** - загрузка исторических курсов из Frankfurter API (v2).
2. **Load** - загрузка в staging-таблицу `raw_fx_rates` с идемпотентным `ON CONFLICT DO NOTHING`.
3. **Transform** - построение витрины `mart_fx_daily` с оконными функциями:
   - `daily_change` - абсолютное изменение курса за день (`LAG`)
   - `daily_change_pct` - изменение в процентах
   - `ma_7d` - скользящее среднее за 7 дней (`AVG OVER`)
   - `ma_30d` - скользящее среднее за 30 дней

## Стек

- **Python 3.14** (requests, psycopg3, python-dotenv)
- **PostgreSQL 18** (NUMERIC для курсов, составной PRIMARY KEY)
- **SQL** (оконные функции `LAG`, `AVG OVER`, CTE, `CASE`)
- **pytest** (тесты подключения, схемы, Data Quality)
- **Git**, **Linux (WSL)**


## Как запустить

1. Клонировать репозиторий:
   ```
   git clone git@github.com:andreyst18/fx-rates-pipeline.git
   cd fx-rates-pipeline

2. Создать venv и установить зависимости:
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Создать .env по шаблону .env.example:

    ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=fx_db
    DB_USER=your_user
    DB_PASSWORD=your_password

4. Создать базу и таблицы:

    ```
    psql -h localhost -U <user_name> -d fx_db -f sql/01_create_tables.sql

5. Запустить пайплайн:

    ```
    python load.py

6. Построить витрину:

    ```
    psql -h localhost -U <user_name> -d fx_db -f sql/transform.sql
