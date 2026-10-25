import os
import psycopg
import pytest
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

@pytest.fixture(scope='module')
def db_connection():
    conn = psycopg.connect(**DB_CONFIG)
    yield conn
    conn.close()

def test_db_connection(db_connection):
    assert db_connection is not None
    assert db_connection.closed is False

def test_simple_query(db_connection):
    with db_connection.cursor() as cur:
        cur.execute('SELECT NOW();')
        result = cur.fetchone()
        assert result is not None
        assert len(result) == 1
        assert result[0] is not None
        print(f'Результат теста - {result[0]}')


