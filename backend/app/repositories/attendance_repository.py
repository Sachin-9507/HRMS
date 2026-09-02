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