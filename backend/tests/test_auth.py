import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import dependencies


class FakeCursor:
    def __init__(self, user):
        self.user = user

    def execute(self, query, params):
        self.query = query
        self.params = params

    def fetchone(self):
        return self.user


class FakeCursorContext:
    def __init__(self, user):
        self.user = user

    def __enter__(self):
        return FakeCursor(self.user)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_get_current_user(monkeypatch):

    fake_user = {
        "id": 1,
        "email": "admin@example.com",
        "role_id": 1,
        "role_name": "Admin",
        "employee_id": 10,
    }

    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {"sub": "1"},
    )

    monkeypatch.setattr(
        dependencies,
        "get_cursor",
        lambda: FakeCursorContext(fake_user),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="fake-token",
    )

    result = dependencies.get_current_user(credentials)

    assert result["id"] == 1
    assert result["user_id"] == 1
    assert result["email"] == "admin@example.com"
    assert result["role_id"] == 1
    assert result["role_name"] == "Admin"
    assert result["employee_id"] == 10


def test_get_current_user_invalid_token(monkeypatch):

    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {},
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="fake-token",
    )

    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user(credentials)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid access token"


def test_get_current_user_not_found(monkeypatch):

    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {"sub": "999"},
    )

    monkeypatch.setattr(
        dependencies,
        "get_cursor",
        lambda: FakeCursorContext(None),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="fake-token",
    )

    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user(credentials)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid authentication credentials"


def test_get_current_user_inactive(monkeypatch):

    monkeypatch.setattr(
        dependencies,
        "decode_access_token",
        lambda token: {"sub": "1"},
    )

    # The SQL query contains:
    # AND u.is_active = TRUE
    # Therefore an inactive user should not be returned.
    monkeypatch.setattr(
        dependencies,
        "get_cursor",
        lambda: FakeCursorContext(None),
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="fake-token",
    )

    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user(credentials)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid authentication credentials"