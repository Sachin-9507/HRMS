from app.database.db import get_cursor


def get_role_by_id(role_id: int):

    query = """
        SELECT
            id,
            name,
            description,
            is_active
        FROM roles
        WHERE id = %s
        LIMIT 1;
    """ 

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (role_id,)
        )

        return cursor.fetchone()


def get_user_permissions(user_id: int):

    query = """
        SELECT DISTINCT
            p.name
        FROM users u
        JOIN roles r
            ON r.id = u.role_id
        JOIN role_permissions rp
            ON rp.role_id = r.id
        JOIN permissions p
            ON p.id = rp.permission_id
        WHERE u.id = %s
            AND u.is_active = TRUE
            AND r.is_active = TRUE
        ORDER BY p.name;
    """

    with get_cursor() as cursor:
        cursor.execute(
            query,
            (user_id,)
        )

        rows = cursor.fetchall()

    return [
        row[0]
        for row in rows
    ]