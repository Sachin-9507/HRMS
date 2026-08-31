from datetime import datetime, timedelta, timezone
from jose import jwt ,JWTError

from core.config import settings

ALGORITHM = "HS256"


def create_access_token(
    data: dict,
    expires_minutes: int = 30,
) -> str:

    payload = data.copy()

    # Make sure JWT contains "sub"
    if "user_id" in payload and "sub" not in payload:
        payload["sub"] = str(payload["user_id"])

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