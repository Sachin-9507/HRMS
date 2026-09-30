from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.auth.jwt import decode_access_token
from app.database.db import get_cursor


security = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

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
                (user_id,),
            )

            user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if isinstance(user, dict):
            return {
                "id": user["id"],
                "user_id": user["id"],
                "role_id": user["role_id"],
                "role_name": user["role_name"],
                "employee_id": user["employee_id"],
            }

        return {
            "id": user[0],
            "user_id": user[0],
            "role_id": user[1],
            "role_name": user[2],
            "employee_id": user[3],
        }

    except HTTPException:
        raise

    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )