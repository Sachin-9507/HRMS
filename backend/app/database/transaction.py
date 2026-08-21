from contextlib import contextmanager

from app.database.connection import get_connection


@contextmanager
def transaction():

    connection = None
    cursor = None

    try:
        # Create a fresh database connection
        connection = get_connection()

        # Make sure the connection is open
        if connection.closed:
            raise RuntimeError("Database connection is already closed")

        cursor = connection.cursor()

        yield cursor

        # Commit only after all operations succeed
        connection.commit()

    except Exception:
        if connection is not None and not connection.closed:
            connection.rollback()

        raise

    finally:
        if cursor is not None and not cursor.closed:
            cursor.close()

        if connection is not None and not connection.closed:
            connection.close()