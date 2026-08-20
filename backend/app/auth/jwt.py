from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone


from jose import jwt ,JWTError
  

from core.config import settings

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def create_access_token(
    data: dict,
    expires_minutes: int = 30,
) -> str:

    payload = data.copy()

    payload["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    payload["type"] = "access"

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            raise JWTError("Invalid access token")

        return payload

    except JWTError:
        raise JWTError("Invalid access token")

  
def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

def create_refresh_token(
    data: dict,
    expires_days: int = 7,
) -> str:

    payload = data.copy()

    payload["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(days=expires_days)
    )

    payload["type"] = "refresh"

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )





def get_refresh_token_expiry(
    expires_days: int = 7,
) -> datetime:
 return (
        datetime.now(timezone.utc)
        + timedelta(days=expires_days)
    )