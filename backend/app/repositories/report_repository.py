from app.database.connection import get_connection


class ReportRepository:

    @staticmethod
    def attendance_report(
        employee_id=None,
        start_date=None,
        end_date=None,
        status=None,
    ):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    a.id,
                    a.employee_id,
                    e.employee_code,
                    e.first_name,
                    e.last_name,
                    a.attendance_date,
                    a.check_in,
                    a.check_out,
                    a.status,
                    a.working_minutes,
                    a.remarks
                FROM attendance a
                INNER JOIN employees e
                    ON e.id = a.employee_id
                WHERE 1 = 1
            """

            params = []

            if employee_id is not None:
                query += """
                    AND a.employee_id = %s
                """
                params.append(employee_id)

            if start_date is not None:
                query += """
                    AND a.attendance_date >= %s
                """
                params.append(start_date)

            if end_date is not None:
                query += """
                    AND a.attendance_date <= %s
                """
                params.append(end_date)

            if status is not None:
                query += """
                    AND a.status = %s
                """
                params.append(status)

            query += """
                ORDER BY
                    a.attendance_date DESC,
                    a.employee_id
            """

            cursor.execute(
                query,
                tuple(params),
            )

            return cursor.fetchall()

        finally:
            conn.close()

    @staticmethod
    def leave_report(
        employee_id=None,
        leave_type_id=None,
        status=None,
        start_date=None,
        end_date=None,
    ):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    lr.id,
                    lr.employee_id,
                    e.employee_code,
                    e.first_name,
                    e.last_name,
                    lr.leave_type_id,
                    lt.code,
                    lt.name,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status,
                    lr.admin_remarks,
                    lr.reviewed_by,
                    lr.reviewed_at,
                    lr.created_at
                FROM leave_requests lr
                INNER JOIN employees e
                    ON e.id = lr.employee_id
                INNER JOIN leave_types lt
                    ON lt.id = lr.leave_type_id
                WHERE 1 = 1
            """

            params = []

            if employee_id is not None:
                query += """
                    AND lr.employee_id = %s
                """
                params.append(employee_id)

            if leave_type_id is not None:
                query += """
                    AND lr.leave_type_id = %s
                """
                params.append(leave_type_id)

            if status is not None:
                query += """
                    AND lr.status = %s
                """
                params.append(status)

            if start_date is not None:
                query += """
                    AND lr.start_date >= %s
                """
                params.append(start_date)

            if end_date is not None:
                query += """
                    AND lr.end_date <= %s
                """
                params.append(end_date)

            query += """
                ORDER BY lr.created_at DESC
            """

            cursor.execute(
                query,
                tuple(params),
            )

            return cursor.fetchall()

        finally:
            conn.close()