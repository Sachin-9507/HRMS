from datetime import date
from decimal import Decimal

from app.database.connection import get_connection


def get_leave_type(leave_type_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    code,
                    name,
                    description,
                    default_days,
                    is_active
                FROM leave_types
                WHERE id = %s
                """,
                (leave_type_id,)
            )

            return cursor.fetchone()

    finally:
        connection.close()


def has_overlapping_leave(
    employee_id: int,
    start_date: date,
    end_date: date
) -> bool:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM leave_requests
                    WHERE employee_id = %s
                      AND status IN ('PENDING', 'APPROVED')
                      AND start_date <= %s
                      AND end_date >= %s
                )
                """,
                (
                    employee_id,
                    end_date,
                    start_date
                )
            )

            row = cursor.fetchone()

            return bool(row[0])

    finally:
        connection.close()


def create_leave_request(
    employee_id: int,
    leave_type_id: int,
    start_date: date,
    end_date: date,
    total_days: Decimal,
    reason: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO leave_requests (
                    employee_id,
                    leave_type_id,
                    start_date,
                    end_date,
                    total_days,
                    reason,
                    status
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    'PENDING'
                )
                RETURNING id
                """,
                (
                    employee_id,
                    leave_type_id,
                    start_date,
                    end_date,
                    total_days,
                    reason
                )
            )

            leave_id = cursor.fetchone()[0]

        connection.commit()

        return leave_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_leave_request(
    leave_id: int,
    employee_id: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    lr.id,
                    lr.employee_id,

                    lr.leave_type_id,
                    lt.code AS leave_type_code,
                    lt.name AS leave_type_name,

                    lr.start_date,
                    lr.end_date,
                    lr.total_days,

                    lr.reason,
                    lr.status,
                    lr.admin_remarks,

                    lr.reviewed_by,
                    lr.reviewed_at,

                    lr.created_at,
                    lr.updated_at

                FROM leave_requests lr

                JOIN leave_types lt
                    ON lt.id = lr.leave_type_id

                WHERE lr.id = %s
                  AND lr.employee_id = %s
                """,
                (
                    leave_id,
                    employee_id
                )
            )

            row = cursor.fetchone()

            if not row:
                return None

            return {
                "id": row[0],
                "employee_id": row[1],
                "leave_type_id": row[2],
                "leave_type_code": row[3],
                "leave_type_name": row[4],
                "start_date": row[5],
                "end_date": row[6],
                "total_days": row[7],
                "reason": row[8],
                "status": row[9],
                "admin_remarks": row[10],
                "reviewed_by": row[11],
                "reviewed_at": row[12],
                "created_at": row[13],
                "updated_at": row[14]
            }

    finally:
        connection.close()

def list_my_leave_requests(
    employee_id: int,
    status: str | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT
                    lr.id,
                    lr.employee_id,

                    lr.leave_type_id,
                    lt.code AS leave_type_code,
                    lt.name AS leave_type_name,

                    lr.start_date,
                    lr.end_date,
                    lr.total_days,

                    lr.reason,
                    lr.status,
                    lr.admin_remarks,

                    lr.reviewed_by,
                    lr.reviewed_at,

                    lr.created_at,
                    lr.updated_at

                FROM leave_requests lr

                JOIN leave_types lt
                    ON lt.id = lr.leave_type_id

                WHERE lr.employee_id = %s
            """

            params = [employee_id]

            if status:
                query += """
                    AND lr.status = %s
                """

                params.append(status)

            query += """
                ORDER BY lr.created_at DESC
            """

            cursor.execute(query, tuple(params))

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "employee_id": row[1],
                    "leave_type_id": row[2],
                    "leave_type_code": row[3],
                    "leave_type_name": row[4],
                    "start_date": row[5],
                    "end_date": row[6],
                    "total_days": row[7],
                    "reason": row[8],
                    "status": row[9],
                    "admin_remarks": row[10],
                    "reviewed_by": row[11],
                    "reviewed_at": row[12],
                    "created_at": row[13],
                    "updated_at": row[14]
                }
                for row in rows
            ]

    finally:
        connection.close()



def cancel_leave_request(
    leave_id: int,
    employee_id: int
) -> bool:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE leave_requests
                SET
                    status = 'CANCELLED',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND employee_id = %s
                  AND status = 'PENDING'
                """,
                (
                    leave_id,
                    employee_id
                )
            )

            updated = cursor.rowcount > 0

        connection.commit()

        return updated

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def list_leave_balances(
    employee_id: int,
    leave_year: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    lb.id,
                    lb.employee_id,
                    lb.leave_type_id,
                    lt.code AS leave_type_code,
                    lt.name AS leave_type_name,
                    lb.leave_year,
                    lb.allocated_days,
                    lb.used_days,
                    (
                        lb.allocated_days - lb.used_days
                    ) AS remaining_days
                FROM leave_balances lb
                JOIN leave_types lt
                    ON lt.id = lb.leave_type_id
                WHERE lb.employee_id = %s
                  AND lb.leave_year = %s
                ORDER BY lt.name
                """,
                (
                    employee_id,
                    leave_year
                )
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "employee_id": row[1],
                    "leave_type_id": row[2],
                    "leave_type_code": row[3],
                    "leave_type_name": row[4],
                    "leave_year": row[5],
                    "allocated_days": row[6],
                    "used_days": row[7],
                    "remaining_days": row[8]
                }
                for row in rows
            ]

    finally:
        connection.close()

def list_all_leave_requests(
    status_filter: str | None = None,
    employee_id: int | None = None,
    leave_type_id: int | None = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT
                    lr.id,

                    lr.employee_id,
                    e.employee_code,
                    e.first_name,
                    e.last_name,

                    lr.leave_type_id,
                    lt.code AS leave_type_code,
                    lt.name AS leave_type_name,

                    lr.start_date,
                    lr.end_date,
                    lr.total_days,

                    lr.reason,
                    lr.status,

                    lr.admin_remarks,

                    lr.reviewed_by,
                    lr.reviewed_at,

                    lr.created_at,
                    lr.updated_at

                FROM leave_requests lr

                JOIN employees e
                    ON e.id = lr.employee_id

                JOIN leave_types lt
                    ON lt.id = lr.leave_type_id

                WHERE 1 = 1
            """

            params = []

            if status_filter:
                query += """
                    AND lr.status = %s
                """
                params.append(status_filter)

            if employee_id:
                query += """
                    AND lr.employee_id = %s
                """
                params.append(employee_id)

            if leave_type_id:
                query += """
                    AND lr.leave_type_id = %s
                """
                params.append(leave_type_id)

            query += """
                ORDER BY lr.created_at DESC
            """

            cursor.execute(
                query,
                tuple(params)
            )

            return cursor.fetchall()

    finally:
        connection.close()

def get_admin_leave_request(
    leave_id: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    lr.id,

                    lr.employee_id,
                    e.employee_code,
                    e.first_name,
                    e.last_name,

                    lr.leave_type_id,
                    lt.code AS leave_type_code,
                    lt.name AS leave_type_name,

                    lr.start_date,
                    lr.end_date,
                    lr.total_days,

                    lr.reason,
                    lr.status,

                    lr.admin_remarks,

                    lr.reviewed_by,
                    lr.reviewed_at,

                    lr.created_at,
                    lr.updated_at

                FROM leave_requests lr

                JOIN employees e
                    ON e.id = lr.employee_id

                JOIN leave_types lt
                    ON lt.id = lr.leave_type_id

                WHERE lr.id = %s
                """,
                (leave_id,)
            )

            row = cursor.fetchone()

            if not row:
                return None

            return {
                "id": row[0],
                "employee_id": row[1],
                "employee_code": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "leave_type_id": row[5],
                "leave_type_code": row[6],
                "leave_type_name": row[7],
                "start_date": row[8],
                "end_date": row[9],
                "total_days": row[10],
                "reason": row[11],
                "status": row[12],
                "admin_remarks": row[13],
                "reviewed_by": row[14],
                "reviewed_at": row[15],
                "created_at": row[16],
                "updated_at": row[17]
            }

    finally:
        connection.close()

def approve_leave_request(
    leave_id: int,
    reviewer_id: int
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # 1. Lock leave request
            cursor.execute(
                """
                SELECT
                    id,
                    employee_id,
                    leave_type_id,
                    start_date,
                    total_days,
                    status
                FROM leave_requests
                WHERE id = %s
                FOR UPDATE
                """,
                (leave_id,)
            )

            leave = cursor.fetchone()

            if not leave:
                raise ValueError(
                    "Leave request not found"
                )

            (
                request_id,
                employee_id,
                leave_type_id,
                start_date,
                total_days,
                leave_status
            ) = leave

            if leave_status != "PENDING":
                raise ValueError(
                    "Only pending leave requests can be approved"
                )

            # 2. Lock leave balance
            cursor.execute(
                """
                SELECT
                    id,
                    allocated_days,
                    used_days
                FROM leave_balances
                WHERE employee_id = %s
                  AND leave_type_id = %s
                  AND leave_year = EXTRACT(
                      YEAR FROM %s
                  )::INTEGER
                FOR UPDATE
                """,
                (
                    employee_id,
                    leave_type_id,
                    start_date
                )
            )

            balance = cursor.fetchone()

            if not balance:
                raise ValueError(
                    "Leave balance not found for employee"
                )

            balance_id, allocated_days, used_days = balance

            remaining_days = (
                allocated_days - used_days
            )

            if remaining_days < total_days:
                raise ValueError(
                    "Insufficient leave balance"
                )

            # 3. Deduct balance
            cursor.execute(
                """
                UPDATE leave_balances
                SET
                    used_days = used_days + %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    total_days,
                    balance_id
                )
            )

            # 4. Approve leave
            cursor.execute(
                """
                UPDATE leave_requests
                SET
                    status = 'APPROVED',
                    reviewed_by = %s,
                    reviewed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    reviewer_id,
                    leave_id
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def reject_leave_request(
    leave_id: int,
    reviewer_id: int,
    admin_remarks: str
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT status
                FROM leave_requests
                WHERE id = %s
                FOR UPDATE
                """,
                (leave_id,)
            )

            leave = cursor.fetchone()

            if not leave:
                raise ValueError(
                    "Leave request not found"
                )

            if leave[0] != "PENDING":
                raise ValueError(
                    "Only pending leave requests can be rejected"
                )

            cursor.execute(
                """
                UPDATE leave_requests
                SET
                    status = 'REJECTED',
                    admin_remarks = %s,
                    reviewed_by = %s,
                    reviewed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    admin_remarks,
                    reviewer_id,
                    leave_id
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()