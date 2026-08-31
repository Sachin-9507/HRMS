def get_my_profile_cursor(
    cursor,
    user_id: int
):

    query = """
        SELECT
            u.id,
            u.email,
            u.role_id,
            r.name,
            u.is_active
        FROM users u

        JOIN roles r
            ON r.id = u.role_id

        WHERE u.id = %s

        LIMIT 1
    """

    cursor.execute(
        query,
        (user_id,)
    )

    return cursor.fetchone()

def get_my_employee_cursor(
    cursor,
    user_id: int
):

    query = """
        SELECT
            e.id,
            e.employee_code,

            e.first_name,
            e.last_name,

            e.email,
            e.phone,

            e.department_id,
            d.name,

            e.designation_id,
            des.name,

            u.is_active,

            e.created_at,
            e.updated_at

        FROM users u

        JOIN employees e
            ON e.user_id = u.id

        LEFT JOIN departments d
            ON d.id = e.department_id

        LEFT JOIN designations des
            ON des.id = e.designation_id

        WHERE u.id = %s

        LIMIT 1
    """

    cursor.execute(
        query,
        (user_id,)
    )

    return cursor.fetchone()

def update_my_email_cursor(
    cursor,
    user_id: int,
    email: str
):

    query = """
        UPDATE users

        SET
            email = %s,
            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s

        RETURNING
            id,
            email,
            role_id,
            is_active
    """

    cursor.execute(
        query,
        (
            email,
            user_id
        )
    )

    return cursor.fetchone()

def get_user_by_email_cursor(
    cursor,
    email: str
):

    query = """
        SELECT
            id,
            email
        FROM users
        WHERE LOWER(email) = LOWER(%s)
        LIMIT 1
    """

    cursor.execute(
        query,
        (email,)
    )

    return cursor.fetchone()