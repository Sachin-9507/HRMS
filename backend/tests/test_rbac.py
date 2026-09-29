import pytest
from fastapi import HTTPException

from app.auth import rbac


def test_require_permission_allowed(monkeypatch):

    current_user = {
        "id": 1,
        "user_id": 1,
        "email": "admin@example.com",
        "role_id": 1,
        "employee_id": 10,
    }

    monkeypatch.setattr(
        rbac,
        "get_user_permissions",
        lambda user_id: {
            "employee:read",
            "employee:create",
            "leave:approve",
            "attendance.read_all",
        },
    )

    checker = rbac.require_permission("employee:read")

    result = checker(current_user)

    assert result == current_user


def test_require_permission_denied(monkeypatch):

    current_user = {
        "id": 2,
        "user_id": 2,
        "email": "employee@example.com",
        "role_id": 2,
        "employee_id": 20,
    }

    monkeypatch.setattr(
        rbac,
        "get_user_permissions",
        lambda user_id: {
            "profile.read",
            "leave.apply",
        },
    )

    checker = rbac.require_permission("employee:create")

    with pytest.raises(HTTPException) as exc:
        checker(current_user)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Permission denied"