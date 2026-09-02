from app.database.transaction import transaction

from app.repositories.attendance_repository import (
    get_today_attendance_cursor,
    create_check_in_cursor,
    checkout_cursor,
    get_my_attendance_cursor
)

def get_today_attendance(
    user_id: int
):

    with transaction() as cursor:

        row = get_today_attendance_cursor(
            cursor,
            user_id
        )

    if not row:

        return None

    return {
        "id": row[0],
        "employee_id": row[1],
        "attendance_date": row[2],
        "check_in": row[3],
        "check_out": row[4],
        "status": row[5],
        "working_minutes": row[6],
        "remarks": row[7],
        "created_at": row[8],
        "updated_at": row[9]
    }

def check_in(
    user_id: int
):

    with transaction() as cursor:

        existing = get_today_attendance_cursor(
            cursor,
            user_id
        )

        if existing:

            raise ValueError(
                "Attendance already exists for today"
            )

        row = create_check_in_cursor(
            cursor,
            user_id
        )

    if not row:

        raise ValueError(
            "Employee account is not linked"
        )

    return {
        "id": row[0],
        "employee_id": row[1],
        "attendance_date": row[2],
        "check_in": row[3],
        "check_out": row[4],
        "status": row[5],
        "working_minutes": row[6],
        "remarks": row[7],
        "created_at": row[8],
        "updated_at": row[9]
    }

def check_out(
    user_id: int
):

    with transaction() as cursor:

        existing = get_today_attendance_cursor(
            cursor,
            user_id
        )

        if not existing:

            raise ValueError(
                "You have not checked in today"
            )

        if existing[4] is not None:

            raise ValueError(
                "You have already checked out"
            )

        row = checkout_cursor(
            cursor,
            user_id
        )

    if not row:

        raise ValueError(
            "Unable to check out"
        )

    return {
        "id": row[0],
        "employee_id": row[1],
        "attendance_date": row[2],
        "check_in": row[3],
        "check_out": row[4],
        "status": row[5],
        "working_minutes": row[6],
        "remarks": row[7],
        "created_at": row[8],
        "updated_at": row[9]
    }

def get_my_attendance(
    user_id: int,
    limit: int = 30,
    offset: int = 0
):

    with transaction() as cursor:

        rows = get_my_attendance_cursor(
            cursor,
            user_id,
            limit,
            offset
        )

    return [
        {
            "id": row[0],
            "employee_id": row[1],
            "attendance_date": row[2],
            "check_in": row[3],
            "check_out": row[4],
            "status": row[5],
            "working_minutes": row[6],
            "remarks": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        }
        for row in rows
    ]

