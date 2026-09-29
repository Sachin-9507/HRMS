from datetime import date

from fastapi import HTTPException

from app.api.v1.endpoints import leaves


def test_apply_leave(monkeypatch):
    expected = {
        "id": 1,
        "employee_id": 10,
        "leave_type_id": 2,
        "start_date": date(2026, 9, 25),
        "end_date": date(2026, 9, 26),
        "reason": "Personal work",
        "status": "PENDING",
    }

    def fake_apply_leave(
        employee_id,
        leave_type_id,
        start_date,
        end_date,
        reason,
    ):
        assert employee_id == 10
        assert leave_type_id == 2
        assert start_date == date(2026, 9, 25)
        assert end_date == date(2026, 9, 26)
        assert reason == "Personal work"

        return 1

    def fake_get_my_leave(employee_id, leave_id):
        assert employee_id == 10
        assert leave_id == 1
        return expected

    monkeypatch.setattr(
        leaves.leave_service,
        "apply_leave",
        fake_apply_leave,
    )

    monkeypatch.setattr(
        leaves.leave_service,
        "get_my_leave",
        fake_get_my_leave,
    )

    result = leaves.apply_leave(
        leave_type_id=2,
        start_date=date(2026, 9, 25),
        end_date=date(2026, 9, 26),
        reason="Personal work",
        current_user={
            "id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected


def test_get_my_leaves(monkeypatch):
    expected = [
        {
            "id": 1,
            "employee_id": 10,
            "leave_type_id": 2,
            "status": "PENDING",
        }
    ]

    def fake_get_my_leaves(employee_id, status_filter):
        assert employee_id == 10
        assert status_filter == "PENDING"
        return expected

    monkeypatch.setattr(
        leaves.leave_service,
        "get_my_leaves",
        fake_get_my_leaves,
    )

    result = leaves.get_my_leaves(
        status_filter="PENDING",
        current_user={
            "id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected


def test_get_my_leave(monkeypatch):
    expected = {
        "id": 5,
        "employee_id": 10,
        "leave_type_id": 2,
        "status": "APPROVED",
    }

    def fake_get_my_leave(employee_id, leave_id):
        assert employee_id == 10
        assert leave_id == 5
        return expected

    monkeypatch.setattr(
        leaves.leave_service,
        "get_my_leave",
        fake_get_my_leave,
    )

    result = leaves.get_my_leave(
        leave_id=5,
        current_user={
            "id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected


def test_cancel_my_leave(monkeypatch):
    called = {}

    def fake_cancel_leave(employee_id, leave_id):
        called["employee_id"] = employee_id
        called["leave_id"] = leave_id

    monkeypatch.setattr(
        leaves.leave_service,
        "cancel_leave",
        fake_cancel_leave,
    )

    result = leaves.cancel_my_leave(
        leave_id=5,
        current_user={
            "id": 1,
            "employee_id": 10,
        },
    )

    assert result is None
    assert called["employee_id"] == 10
    assert called["leave_id"] == 5


def test_get_my_leave_balances(monkeypatch):
    expected = [
        {
            "leave_type_id": 1,
            "leave_type": "CASUAL",
            "total": 12,
            "used": 2,
            "remaining": 10,
        }
    ]

    def fake_get_my_balances(employee_id, leave_year):
        assert employee_id == 10
        assert leave_year == 2026
        return expected

    monkeypatch.setattr(
        leaves.leave_service,
        "get_my_balances",
        fake_get_my_balances,
    )

    result = leaves.get_my_leave_balances(
        year=2026,
        current_user={
            "id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected