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

            rows = cursor.fetchall()

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
                }
                for row in rows
            ]

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

            rows = cursor.fetchall()

            return [
                {
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
                }
                for row in rows
            ]

        finally:
            conn.close()