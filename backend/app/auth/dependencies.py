from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt import decode_access_token
from app.database.db import get_cursor


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        print("JWT PAYLOAD:", payload)
        print("USER ID:", user_id)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

        user_id = int(user_id)

        with get_cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    u.id,
                    u.role_id,
                    r.name AS role_name,
                    e.id AS employee_id
                FROM users u

                JOIN roles r
                    ON r.id = u.role_id

                LEFT JOIN employees e
                    ON e.user_id = u.id

                WHERE u.id = %s
                  AND u.is_active = TRUE

                LIMIT 1
                """,
                (user_id,)
            )

            user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        if isinstance(user, dict):
            return {
                "id": user["id"],
                "user_id": user["id"],
                "role_id": user["role_id"],
                "role_name": user["role_name"],
                "employee_id": user["employee_id"]
            }

        return {
            "id": user[0],
            "user_id": user[0],
            "role_id": user[1],
            "role_name": user[2],
            "employee_id": user[3]
        }
    except HTTPException:
        raise

    except Exception as e:
        print("get_current_user error:", e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )