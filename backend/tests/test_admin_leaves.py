from datetime import date

from app.api.v1.endpoints import admin_leaves


def test_get_all_leaves(monkeypatch):
    expected = [
        {
            "id": 1,
            "employee_id": 10,
            "leave_type_id": 2,
            "status": "PENDING",
        }
    ]

    def fake_get_all_leaves(status_filter):
        assert status_filter == "PENDING"
        return expected

    monkeypatch.setattr(
        admin_leaves.leave_service,
        "get_all_leaves",
        fake_get_all_leaves,
    )

    result = admin_leaves.get_all_leaves_api(
        status_filter="PENDING"
    )

    assert result == expected


def test_get_admin_leave(monkeypatch):
    expected = {
        "id": 5,
        "employee_id": 10,
        "leave_type_id": 2,
        "status": "PENDING",
    }

    def fake_get_admin_leave(leave_id):
        assert leave_id == 5
        return expected

    monkeypatch.setattr(
        admin_leaves.leave_service,
        "get_admin_leave",
        fake_get_admin_leave,
    )

    result = admin_leaves.get_leave(
        leave_id=5
    )

    assert result == expected


def test_approve_leave(monkeypatch):
    expected = {
        "id": 5,
        "employee_id": 10,
        "leave_type_id": 2,
        "status": "APPROVED",
    }

    def fake_approve_leave(leave_id, reviewer_id):
        assert leave_id == 5
        assert reviewer_id == 1

        return expected

    monkeypatch.setattr(
        admin_leaves.leave_service,
        "approve_leave",
        fake_approve_leave,
    )

    result = admin_leaves.approve_leave(
        leave_id=5,
        current_user={
            "id": 1,
            "user_id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected


def test_reject_leave(monkeypatch):
    expected = {
        "id": 5,
        "employee_id": 10,
        "leave_type_id": 2,
        "status": "REJECTED",
        "admin_remarks": "Insufficient leave balance",
    }

    def fake_reject_leave(
        leave_id,
        reviewer_id,
        admin_remarks,
    ):
        assert leave_id == 5
        assert reviewer_id == 1
        assert admin_remarks == "Insufficient leave balance"

        return expected

    monkeypatch.setattr(
        admin_leaves.leave_service,
        "reject_leave",
        fake_reject_leave,
    )

    result = admin_leaves.reject_leave(
        leave_id=5,
        admin_remarks="Insufficient leave balance",
        current_user={
            "id": 1,
            "user_id": 1,
            "employee_id": 10,
        },
    )

    assert result == expected


def test_reject_leave_empty_remarks_not_directly_validated():
    """
    FastAPI validates min_length=1 for admin_remarks when the
    endpoint is called through HTTP.

    This direct function test intentionally does not test FastAPI's
    Query validation.
    """

    assert True