from app.database.db import get_cursor


def get_all_users():
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                u.phone_number,
                u.role_id,
                u.is_active,
                u.is_email_verified,
                u.is_2fa_enabled,
                u.failed_login_attempts,
                u.locked_until,
                u.last_login,
                u.created_at,
                u.updated_at
            FROM public.users u
            ORDER BY u.id;
        """)

        return cursor.fetchall()

def get_user_details(
    user_id: int
):

     query = """
        SELECT
            u.id,
            u.email,
            u.first_name,
            u.last_name,
            u.phone_number,
            u.role_id,
            r.name AS role, 
            u.is_active,
            u.is_email_verified,
            u.is_2fa_enabled,
            u.created_at,
            u.last_login_at
        FROM users u
        JOIN roles r
            ON r.id = u.role_id
        WHERE u.id = %s
        LIMIT 1;
    """

     with get_cursor() as cursor:

        cursor.execute(
            query,
            (user_id,)
        )

        return cursor.fetchone()

def set_user_active(
    user_id: int,
    is_active: bool
):

     query = """
        UPDATE users
        SET is_active = %s
        WHERE id = %s
        RETURNING
            id,
            email,
            is_active;
    """

     with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                is_active,
                user_id
            )
        )

     return cursor.fetchone()

def change_user_role(
    user_id: int,
    role_id: int
):

     query = """
        UPDATE users
        SET role_id = %s
        WHERE id = %s
        RETURNING
            id,
            email,
            role_id;
    """

     with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                role_id,
                user_id
            )
        )
        result = cursor.fetchone()
     return cursor.fetchone()

    