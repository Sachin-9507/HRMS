def get_today_attendance_cursor(
    cursor,
    user_id: int
):

    query = """
        SELECT
            a.id,
            a.employee_id,
            a.attendance_date,
            a.check_in,
            a.check_out,
            a.status,
            a.working_minutes,
            a.remarks,
            a.created_at,
            a.updated_at

        FROM attendance a

        JOIN employees e
            ON e.id = a.employee_id

        JOIN users u
            ON u.id = e.user_id

        WHERE
            u.id = %s
            AND a.attendance_date = CURRENT_DATE

        LIMIT 1
    """

    cursor.execute(
        query,
        (user_id,)
    )

    return cursor.fetchone()


def create_check_in_cursor(
    cursor,
    user_id: int
):

    query = """
        INSERT INTO attendance (
            employee_id,
            attendance_date,
            check_in,
            status
        )

        SELECT
            e.id,
            CURRENT_DATE,
            CURRENT_TIMESTAMP,
            'PRESENT'

        FROM employees e

        JOIN users u
            ON u.id = e.user_id

        WHERE u.id = %s

        RETURNING
            id,
            employee_id,
            attendance_date,
            check_in,
            check_out,
            status,
            working_minutes,
            remarks,
            created_at,
            updated_at
    """

    cursor.execute(
        query,
        (user_id,)
    )

    return cursor.fetchone()


def checkout_cursor(
    cursor,
    user_id: int
):

    query = """
        UPDATE attendance a

        SET
            check_out = CURRENT_TIMESTAMP,

            working_minutes =
                EXTRACT(
                    EPOCH FROM (
                        CURRENT_TIMESTAMP - a.check_in
                    )
                ) / 60,

            updated_at = CURRENT_TIMESTAMP

        FROM employees e

        JOIN users u
            ON u.id = e.user_id

        WHERE
            u.id = %s
            AND a.employee_id = e.id
            AND a.attendance_date = CURRENT_DATE
            AND a.check_in IS NOT NULL
            AND a.check_out IS NULL

        RETURNING
            a.id,
            a.employee_id,
            a.attendance_date,
            a.check_in,
            a.check_out,
            a.status,
            a.working_minutes,
            a.remarks,
            a.created_at,
            a.updated_at
    """

    cursor.execute(
        query,
        (user_id,)
    )

    return cursor.fetchone()


def get_my_attendance_cursor(
    cursor,
    user_id: int,
    limit: int,
    offset: int
):

    query = """
        SELECT
            a.id,
            a.employee_id,
            a.attendance_date,
            a.check_in,
            a.check_out,
            a.status,
            a.working_minutes,
            a.remarks,
            a.created_at,
            a.updated_at

        FROM attendance a

        JOIN employees e
            ON e.id = a.employee_id

        JOIN users u
            ON u.id = e.user_id

        WHERE u.id = %s

        ORDER BY
            a.attendance_date DESC

        LIMIT %s
        OFFSET %s
    """

    cursor.execute(
        query,
        (
            user_id,
            limit,
            offset
        )
    )

    return cursor.fetchall()

def get_admin_attendance_cursor(
    cursor,
    attendance_date=None,
    employee_id=None,
    status=None,
    limit=50,
    offset=0
):

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
            a.remarks,
            a.created_at,
            a.updated_at

        FROM attendance a

        JOIN employees e
            ON e.id = a.employee_id

        WHERE 1 = 1
    """

    params = []

    if attendance_date is not None:

        query += """
            AND a.attendance_date = %s
        """

        params.append(
            attendance_date
        )

    if employee_id is not None:

        query += """
            AND a.employee_id = %s
        """

        params.append(
            employee_id
        )

    if status is not None:

        query += """
            AND a.status = %s
        """

        params.append(
            status
        )

    query += """
        ORDER BY
            a.attendance_date DESC,
            a.id DESC

        LIMIT %s
        OFFSET %s
    """

    params.extend([
        limit,
        offset
    ])

    cursor.execute(
        query,
        params
    )

    return cursor.fetchall()

def get_admin_attendance_by_id_cursor(
    cursor,
    attendance_id: int
):

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
            a.remarks,
            a.created_at,
            a.updated_at

        FROM attendance a

        JOIN employees e
            ON e.id = a.employee_id

        WHERE a.id = %s

        LIMIT 1
    """

    cursor.execute(
        query,
        (attendance_id,)
    )

    return cursor.fetchone()


def update_admin_attendance_cursor(
    cursor,
    attendance_id: int,
    data: dict
):

    allowed_fields = {
        "check_in",
        "check_out",
        "status",
        "remarks"
    }

    fields = []
    values = []

    for field, value in data.items():

        if field not in allowed_fields:
            continue

        fields.append(
            f"{field} = %s"
        )

        values.append(value)

    if not fields:
        return None

    fields.append(
        """
        working_minutes =
            CASE
                WHEN check_in IS NOT NULL
                AND check_out IS NOT NULL
                THEN EXTRACT(
                    EPOCH FROM (
                        check_out - check_in
                    )
                ) / 60
                ELSE 0
            END
        """
    )

    fields.append(
        "updated_at = CURRENT_TIMESTAMP"
    )

    query = f"""
        UPDATE attendance

        SET
            {", ".join(fields)}

        WHERE id = %s

        RETURNING id
    """

    values.append(
        attendance_id
    )

    cursor.execute(
        query,
        values
    )

    return cursor.fetchone()