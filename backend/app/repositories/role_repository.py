def get_role_by_name_cursor(
    cursor,
    name: str
):

    query = """
        SELECT
            id,
            name
        FROM roles
        WHERE LOWER(name) = LOWER(%s)
        LIMIT 1
    """

    cursor.execute(
        query,
        (name,)
    )

    return cursor.fetchone()


def assign_role_cursor(
    cursor,
    user_id: int,
    role_id: int
):

    query = """
        INSERT INTO user_roles (
            user_id,
            role_id
        )
        VALUES (
            %s,
            %s
        )
        ON CONFLICT DO NOTHING
        RETURNING
            user_id,
            role_id
    """

    cursor.execute(
        query,
        (
            user_id,
            role_id
        )
    )

    return cursor.fetchone()

def get_role_by_id_cursor(
    cursor,
    role_id: int
):

    query = """
        SELECT
            id,
            name,
            description,
            is_active,
            created_at,
            updated_at
        FROM roles
        WHERE id = %s
        LIMIT 1
    """

    cursor.execute(
        query,
        (role_id,)
    )

    return cursor.fetchone()

def create_role_cursor(
    cursor,
    name: str,
    description: str | None
):

    query = """
        INSERT INTO roles (
            name,
            description
        )
        VALUES (%s, %s)

        RETURNING
            id,
            name,
            description,
            is_active,
            created_at,
            updated_at
    """

    cursor.execute(
        query,
        (
            name,
            description
        )
    )

    return cursor.fetchone()

def list_roles_cursor(
    cursor,
    include_inactive: bool = False
):

    if include_inactive:

        query = """
            SELECT
                id,
                name,
                description,
                is_active,
                created_at,
                updated_at
            FROM roles
            ORDER BY name ASC
        """

    else:

        query = """
            SELECT
                id,
                name,
                description,
                is_active,
                created_at,
                updated_at
            FROM roles
            WHERE is_active = TRUE
            ORDER BY name ASC
        """

    cursor.execute(query)

    return cursor.fetchall()

def update_role_cursor(
    cursor,
    role_id: int,
    name: str,
    description: str | None
):

    query = """
        UPDATE roles
        SET
            name = %s,
            description = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            name,
            description,
            is_active,
            created_at,
            updated_at
    """

    cursor.execute(
        query,
        (
            name,
            description,
            role_id
        )
    )

    return cursor.fetchone()


def update_role_status_cursor(
    cursor,
    role_id: int,
    is_active: bool
):

    query = """
        UPDATE roles
        SET
            is_active = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s

        RETURNING
            id,
            name,
            is_active,
            updated_at
    """

    cursor.execute(
        query,
        (
            is_active,
            role_id
        )
    )

    return cursor.fetchone()

def get_role_permissions_cursor(
    cursor,
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
        ORDER BY p.name ASC
    """

    cursor.execute(
        query,
        (role_id,)
    )

    return cursor.fetchall()

def replace_role_permissions_cursor(
    cursor,
    role_id: int,
    permission_ids: list[int]
):

    delete_query = """
        DELETE FROM role_permissions
        WHERE role_id = %s
    """

    cursor.execute(
        delete_query,
        (role_id,)
    )

    if not permission_ids:
        return

    insert_query = """
        INSERT INTO role_permissions (
            role_id,
            permission_id
        )
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """

    for permission_id in permission_ids:

        cursor.execute(
            insert_query,
            (
                role_id,
                permission_id
            )
        )

def get_existing_permission_ids_cursor(
    cursor,
    permission_ids: list[int]
):

    if not permission_ids:
        return set()

    query = """
        SELECT id
        FROM permissions
        WHERE id = ANY(%s)
    """

    cursor.execute(
        query,
        (permission_ids,)
    )

    return {
        row[0]
        for row in cursor.fetchall()
    }

