from app.database.db import get_cursor


def get_role_permissions(role_id: int):

    query = """
        SELECT
            p.id,
            p.name,
            p.resource,
            p.action,
            p.description
        FROM role_permissions rp
        JOIN permissions p
            ON p.id = rp.permission_id
        WHERE rp.role_id = %s
        ORDER BY p.name;
    """

    with get_cursor() as cursor:
        cursor.execute(query, (role_id,))
        return cursor.fetchall()


def get_permission_by_id_cursor(
    cursor,
    permission_id: int
):

    query = """
        SELECT
            id,
            name,
            resource,
            action,
            description,
            created_at
        FROM permissions
        WHERE id = %s
        LIMIT 1
    """

    cursor.execute(query, (permission_id,))

    return cursor.fetchone()


def get_permission_by_name_cursor(
    cursor,
    name: str
):

    query = """
        SELECT
            id,
            name,
            resource,
            action,
            description,
            created_at
        FROM permissions
        WHERE LOWER(name) = LOWER(%s)
        LIMIT 1
    """

    cursor.execute(query, (name,))

    return cursor.fetchone()


def create_permission_cursor(
    cursor,
    name: str,
    resource: str,
    action: str,
    description: str | None
):

    query = """
        INSERT INTO permissions (
            name,
            resource,
            action,
            description
        )
        VALUES (%s, %s, %s, %s)

        RETURNING
            id,
            name,
            resource,
            action,
            description,
            created_at
    """

    cursor.execute(
        query,
        (
            name,
            resource,
            action,
            description
        )
    )

    return cursor.fetchone()


def list_permissions_cursor(cursor):

    query = """
        SELECT
            id,
            name,
            resource,
            action,
            description,
            created_at
        FROM permissions
        ORDER BY name ASC
    """

    cursor.execute(query)

    return cursor.fetchall()