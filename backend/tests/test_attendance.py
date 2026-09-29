from datetime import date, datetime

from app.api.v1.endpoints import admin_attendance


def test_admin_attendance_list(monkeypatch):
    expected = [
        {
            "id": 1,
            "employee_id": 10,
            "attendance_date": date(2026, 9, 21),
            "check_in": None,
            "check_out": None,
            "status": "PRESENT",
            "remarks": None,
        }
    ]

    def fake_get_admin_attendance(
        attendance_date,
        employee_id,
        status,
        limit,
        offset,
    ):
        assert attendance_date == date(2026, 9, 21)
        assert employee_id == 10
        assert status == "PRESENT"
        assert limit == 50
        assert offset == 0

        return expected

    monkeypatch.setattr(
        admin_attendance,
        "get_admin_attendance",
        fake_get_admin_attendance,
    )

    result = admin_attendance.admin_attendance_list(
        attendance_date=date(2026, 9, 21),
        employee_id=10,
        status="PRESENT",
        limit=50,
        offset=0,
        current_user={"id": 1},
    )

    assert result == expected


def test_admin_attendance_detail(monkeypatch):
    expected = {
        "id": 1,
        "employee_id": 10,
        "attendance_date": date(2026, 9, 21),
        "check_in": None,
        "check_out": None,
        "status": "PRESENT",
        "remarks": None,
    }

    monkeypatch.setattr(
        admin_attendance,
        "get_admin_attendance_by_id",
        lambda attendance_id: expected,
    )

    result = admin_attendance.admin_attendance_detail(
        attendance_id=1,
        current_user={"id": 1},
    )

    assert result == expected


def test_admin_attendance_detail_not_found(monkeypatch):
    def fake_get_admin_attendance_by_id(attendance_id):
        raise ValueError("Attendance record not found")

    monkeypatch.setattr(
        admin_attendance,
        "get_admin_attendance_by_id",
        fake_get_admin_attendance_by_id,
    )

    try:
        admin_attendance.admin_attendance_detail(
            attendance_id=999,
            current_user={"id": 1},
        )

        assert False, "Expected HTTPException"

    except Exception as error:
        assert error.status_code == 404
        assert error.detail == "Attendance record not found"


def test_admin_attendance_update(monkeypatch):
    expected = {
        "id": 1,
        "employee_id": 10,
        "attendance_date": date(2026, 9, 21),
        "check_in": datetime(2026, 9, 21, 9, 0),
        "check_out": datetime(2026, 9, 21, 18, 0),
        "status": "PRESENT",
        "remarks": "Updated by admin",
    }

    def fake_update_admin_attendance(
        attendance_id,
        check_in,
        check_out,
        status,
        remarks,
    ):
        assert attendance_id == 1
        assert check_in == datetime(2026, 9, 21, 9, 0)
        assert check_out == datetime(2026, 9, 21, 18, 0)
        assert status == "PRESENT"
        assert remarks == "Updated by admin"

        return expected

    monkeypatch.setattr(
        admin_attendance,
        "update_admin_attendance",
        fake_update_admin_attendance,
    )

    result = admin_attendance.admin_attendance_update(
        attendance_id=1,
        check_in=datetime(2026, 9, 21, 9, 0),
        check_out=datetime(2026, 9, 21, 18, 0),
        status="PRESENT",
        remarks="Updated by admin",
        current_user={"id": 1},
    )

    assert result == expected


def test_admin_attendance_update_error(monkeypatch):
    def fake_update_admin_attendance(
        attendance_id,
        check_in,
        check_out,
        status,
        remarks,
    ):
        raise ValueError("Invalid attendance update")

    monkeypatch.setattr(
        admin_attendance,
        "update_admin_attendance",
        fake_update_admin_attendance,
    )

    try:
        admin_attendance.admin_attendance_update(
            attendance_id=1,
            check_in=None,
            check_out=None,
            status="INVALID",
            remarks=None,
            current_user={"id": 1},
        )

        assert False, "Expected HTTPException"

    except Exception as error:
        assert error.status_code == 400
        assert error.detail == "Invalid attendance update"