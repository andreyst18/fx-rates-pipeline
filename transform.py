import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def run_transform():
    with open("sql/transform.sql", "r") as f:
        sql = f.read()

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
            print("Витрина mart_fx_daily создана/обновлена")


if __name__ == "__main__":
    run_transform()