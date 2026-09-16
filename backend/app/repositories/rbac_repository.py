from app.database.db import get_cursor


def get_user_permissions(user_id):
    query = """
        SELECT DISTINCT
            p.name AS permission_key
        FROM users u
        JOIN roles r
            ON r.id = u.role_id
        JOIN role_permissions rp
            ON rp.role_id = r.id
        JOIN permissions p
            ON p.id = rp.permission_id
        WHERE u.id = %s
          AND u.is_active = TRUE
    """

    with get_cursor() as cursor:
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        return [row["permission_key"] for row in rows]