from app.database.connection import get_connection


class DashboardRepository:

    @staticmethod
    def get_today_attendance(employee_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    attendance_date,
                    check_in,
                    check_out,
                    status,
                    working_minutes,
                    remarks
                FROM attendance
                WHERE employee_id = %s
                  AND attendance_date = CURRENT_DATE
                LIMIT 1
                """,
                (employee_id,),
            )

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_leave_summary(employee_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(allocated_days), 0),
                    COALESCE(SUM(used_days), 0),
                    COALESCE(
                        SUM(allocated_days - used_days),
                        0
                    )
                FROM leave_balances
                WHERE employee_id = %s
                  AND leave_year = EXTRACT(
                      YEAR FROM CURRENT_DATE
                  )
                """,
                (employee_id,),
            )

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_recent_leaves(employee_id, limit=5):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    lr.id,
                    lt.code,
                    lt.name,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.status
                FROM leave_requests lr
                INNER JOIN leave_types lt
                    ON lt.id = lr.leave_type_id
                WHERE lr.employee_id = %s
                ORDER BY lr.created_at DESC
                LIMIT %s
                """,
                (
                    employee_id,
                    limit,
                ),
            )

            return cursor.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_employee_statistics():
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    COUNT(*) FILTER (
                        WHERE status = 'ACTIVE'
                    ),
                    COUNT(*) FILTER (
                        WHERE status <> 'ACTIVE'
                    )
                FROM employees
                """
            )

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_attendance_statistics():
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (
                        WHERE status = 'PRESENT'
                    ),
                    COUNT(*) FILTER (
                        WHERE check_in IS NOT NULL
                    ),
                    COUNT(*) FILTER (
                        WHERE check_out IS NOT NULL
                    ),
                    COUNT(*) FILTER (
                        WHERE check_in IS NULL
                    )
                FROM attendance
                WHERE attendance_date = CURRENT_DATE
                """
            )

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_leave_statistics():
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) FILTER (
                        WHERE status = 'PENDING'
                    ),
                    COUNT(*) FILTER (
                        WHERE status = 'APPROVED'
                    ),
                    COUNT(*) FILTER (
                        WHERE status = 'REJECTED'
                    ),
                    COUNT(*) FILTER (
                        WHERE status = 'CANCELLED'
                    )
                FROM leave_requests
                """
            )

            return cursor.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_recent_leave_requests(limit=10):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    lr.id,
                    e.id,
                    e.employee_code,
                    e.first_name,
                    e.last_name,
                    lt.code,
                    lt.name,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.status
                FROM leave_requests lr
                INNER JOIN employees e
                    ON e.id = lr.employee_id
                INNER JOIN leave_types lt
                    ON lt.id = lr.leave_type_id
                ORDER BY lr.created_at DESC
                LIMIT %s
                """,
                (limit,),
            )

            return cursor.fetchall()

        finally:
            conn.close()