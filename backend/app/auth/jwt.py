import os
import secrets

import jwt

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7"
    )
)


if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured"
    )




def create_access_token(
    user_id: int,
    email: str,
    role_id: int
) -> str:

    now = datetime.now(timezone.utc)

    expires_at = (
        now +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role_id": role_id,
        "type": "access",
        "iat": now,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def create_refresh_token() -> tuple[str, str]:

    token = secrets.token_urlsafe(64)

    token_hash = hash_refresh_token(token)

    return token, token_hash


import hashlib


def hash_refresh_token(token: str) -> str:

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest() 



def get_refresh_token_expiry():

    return (
        datetime.now(timezone.utc)
        +
        timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )



def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            return None

        return payload

    except jwt.ExpiredSignatureError:

        return None

    except jwt.InvalidTokenError:

        return None


    