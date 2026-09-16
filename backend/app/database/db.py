from contextlib import contextmanager
from psycopg.rows import dict_row

from app.database.connection import get_connection


@contextmanager
def get_cursor():
    connection = get_connection()

    try:
        with connection.cursor(row_factory=dict_row) as cursor:
            yield cursor
            connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()