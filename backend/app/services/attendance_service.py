from app.database.transaction import transaction

from app.repositories.attendance_repository import (
    get_today_attendance_cursor,
    create_check_in_cursor,
    checkout_cursor,
    get_my_attendance_cursor,
    get_admin_attendance_cursor,
    get_admin_attendance_by_id_cursor,
    update_admin_attendance_cursor
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


def get_admin_attendance(
    attendance_date=None,
    employee_id=None,
    status=None,
    limit=50,
    offset=0
):

    with transaction() as cursor:

        rows = get_admin_attendance_cursor(
            cursor,
            attendance_date,
            employee_id,
            status,
            limit,
            offset
        )

    return [
        {
            "id": row[0],
            "employee_id": row[1],
            "employee_code": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "attendance_date": row[5],
            "check_in": row[6],
            "check_out": row[7],
            "status": row[8],
            "working_minutes": row[9],
            "remarks": row[10],
            "created_at": row[11],
            "updated_at": row[12]
        }
        for row in rows
    ]

def get_admin_attendance_by_id(
    attendance_id: int
):

    with transaction() as cursor:

        row = get_admin_attendance_by_id_cursor(
            cursor,
            attendance_id
        )

    if not row:

        raise ValueError(
            "Attendance record not found"
        )

    return {
        "id": row[0],
        "employee_id": row[1],
        "employee_code": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "attendance_date": row[5],
        "check_in": row[6],
        "check_out": row[7],
        "status": row[8],
        "working_minutes": row[9],
        "remarks": row[10],
        "created_at": row[11],
        "updated_at": row[12]
    }

def update_admin_attendance(
    attendance_id: int,
    check_in=None,
    check_out=None,
    status=None,
    remarks=None
):

    update_data = {}

    if check_in is not None:
        update_data["check_in"] = check_in

    if check_out is not None:
        update_data["check_out"] = check_out

    if status is not None:
        update_data["status"] = status

    if remarks is not None:
        update_data["remarks"] = remarks

    if not update_data:
        raise ValueError(
            "No fields provided for update"
        )

    with transaction() as cursor:

        existing = get_admin_attendance_by_id_cursor(
            cursor,
            attendance_id
        )

        if not existing:
            raise ValueError(
                "Attendance record not found"
            )

        updated = update_admin_attendance_cursor(
            cursor,
            attendance_id,
            update_data
        )

        if not updated:
            raise ValueError(
                "Attendance update failed"
            )

        row = get_admin_attendance_by_id_cursor(
            cursor,
            attendance_id
        )

    return {
        "id": row[0],
        "employee_id": row[1],
        "employee_code": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "attendance_date": row[5],
        "check_in": row[6],
        "check_out": row[7],
        "status": row[8],
        "working_minutes": row[9],
        "remarks": row[10],
        "created_at": row[11],
        "updated_at": row[12]
    }