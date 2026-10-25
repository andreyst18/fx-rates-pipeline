import os
import psycopg
from dotenv import load_dotenv

from extract import get_fx_rates

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}


def load_fx_rates(rates):

    if not rates:
        print('Нет данных для загрузки.')
        return

    rows = [
        (r['date'], r['base'], r['quote'], r['rate'])
        for r in rates
    ]

    sql = """
        INSERT INTO raw_fx_rates (date, base, quote, rate)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (date, base, quote) DO NOTHING;
    """

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
            conn.commit()
            print(f'Обработано записей: {len(rows)}')
            print(f'Добавлено строк: {cur.rowcount}')


def main():
    print('Extract...')
    rates = get_fx_rates(base='USD', quote='EUR', days_back=30)

    print('Load...')
    load_fx_rates(rates)

    print('Check...')
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as curr:
            curr.execute('SELECT COUNT(*) FROM raw_fx_rates;')
            count = curr.fetchone()[0]
            print(f'Всего записей в таблице: {count}')

            curr.execute("""
                SELECT date, base, quote, rate
                FROM raw_fx_rates
                ORDER BY date DESC
                LIMIT 5;
            """)

            print('\nПоследние 5 записей:')
            for row in curr.fetchall():
                print(row)


if __name__ == '__main__':
    main()

    
