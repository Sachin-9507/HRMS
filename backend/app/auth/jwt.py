from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from core.config import settings


def create_access_token(
    data: dict,
    expires_minutes: int | None = None,
) -> str:
    payload = data.copy()

    if "user_id" in payload and "sub" not in payload:
        payload["sub"] = str(payload["user_id"])

    if "sub" in payload:
        payload["sub"] = str(payload["sub"])

    expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else settings.access_token_expire_minutes
    )

    now = datetime.now(timezone.utc)

    payload["iat"] = now
    payload["exp"] = now + timedelta(
        minutes=expire_minutes
    )
    payload["type"] = "access"

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        if payload.get("type") != "access":
            raise JWTError("Invalid token type")

        if not payload.get("sub"):
            raise JWTError("Missing subject")

        return payload

    except JWTError as exc:
        raise JWTError("Invalid or expired access token") from exc

def create_refresh_token(
    data: dict,
    expires_days: int = 7,
) -> str:
    payload = data.copy()

    if "user_id" in payload and "sub" not in payload:
        payload["sub"] = str(payload["user_id"])

    if "sub" in payload:
        payload["sub"] = str(payload["sub"])

    now = datetime.now(timezone.utc)

    payload["iat"] = now
    payload["exp"] = now + timedelta(days=expires_days)
    payload["type"] = "refresh"

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

def get_refresh_token_expiry(
    expires_days: int = 7,
) -> datetime:
    return datetime.now(timezone.utc) + timedelta(
        days=expires_days
    )