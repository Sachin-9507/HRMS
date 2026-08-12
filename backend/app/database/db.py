from contextlib import contextmanager

from app.database.connection import connection


@contextmanager
def get_cursor():
   
   try:
      cursor = connection.cursor()
      yield cursor
      connection.commit()

   except Exception:
        connection.rollback()
        raise
   finally:
        cursor.close()