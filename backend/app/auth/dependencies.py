from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt import decode_access_token
from app.database.db import get_cursor

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    with get_cursor() as cursor:

        cursor.execute(
            """
            SELECT
                u.id,
                u.email,
                u.role_id,
                u.is_active,
                e.id AS employee_id
            FROM users u
            LEFT JOIN employees e
                ON e.user_id = u.id
            WHERE u.id = %s
            LIMIT 1
            """,
            (int(user_id),)
        )

        user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )

    return {
        "id": user["id"],
        "user_id": user["id"],
        "email": user["email"],
        "role_id": user["role_id"],
        "employee_id": user["employee_id"]
    }