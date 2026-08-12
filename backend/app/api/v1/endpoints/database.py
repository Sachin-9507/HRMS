from fastapi import APIRouter

from backend.app.database.db import get_cursor

router = APIRouter()

@router.get("/database-test")
def database_test():
    with get_cursor() as cursor:
        cursor.execute("SELECT version();")

        version = cursor.fetchone()
        return {
            "database": "connected",
            "version": version[0]
        }