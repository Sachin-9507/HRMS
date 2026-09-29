import pytest
from jose import JWTError

from app.auth.jwt import (
    create_access_token,
    decode_access_token,
    create_refresh_token,
    get_refresh_token_expiry,
)


def test_create_and_decode_access_token():
    token = create_access_token(
        {"user_id": 1, "email": "admin@example.com"}
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "1"
    assert payload["user_id"] == 1
    assert payload["email"] == "admin@example.com"
    assert payload["type"] == "access"
    assert "exp" in payload


def test_decode_invalid_token():
    with pytest.raises(JWTError):
        decode_access_token("invalid-token")


def test_refresh_token():
    token = create_refresh_token(
        {"user_id": 1}
    )

    assert isinstance(token, str)
    assert len(token) > 0


def test_refresh_token_expiry():
    expiry = get_refresh_token_expiry()

    assert expiry is not None
    assert expiry.tzinfo is not None