from app.database.db import get_cursor

def get_role_permissions(
    role_id: int
):

    query = """
        SELECT
            p.id,
            p.name,
            p.description
        FROM role_permissions rp
        JOIN permissions p
            ON p.id = rp.permission_id
        WHERE rp.role_id = %s
        ORDER BY p.name;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (role_id,)
        )

        return cursor.fetchall()