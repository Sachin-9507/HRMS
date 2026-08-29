from app.database.db import get_cursor


def create_department(
    name: str,
    code: str,
    description: str | None
):

    query = """
        INSERT INTO departments (
            name,
            code,
            description
        )
        VALUES (
            %s,
            %s,
            %s
        )
        RETURNING
            id,
            name,
            code,
            description,
            is_active,
            created_at,
            updated_at;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                name,
                code,
                description
            )
        )

        return cursor.fetchone()

def get_departments(
    include_inactive: bool = False
):

    query = """
        SELECT
            id,
            name,
            code,
            description,
            is_active,
            created_at,
            updated_at
        FROM departments
    """

    if not include_inactive:

        query += """
            WHERE is_active = TRUE
        """

    query += """
        ORDER BY name ASC;
    """

    with get_cursor() as cursor:

        cursor.execute(query)

        return cursor.fetchall()

def get_department_by_id(
    department_id: int
):

    query = """
        SELECT
            id,
            name,
            code,
            description,
            is_active,
            created_at,
            updated_at
        FROM departments
        WHERE id = %s;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (department_id,)
        )

        return cursor.fetchone()

def update_department(
    department_id: int,
    name: str,
    code: str,
    description: str | None,
    is_active: bool | None
):

    query = """
        UPDATE departments

        SET
            name = COALESCE(%s, name),
            code = COALESCE(%s, code),
            description = COALESCE(
                %s,
                description
            ),
            is_active = COALESCE(
                %s,
                is_active
            ),
            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s

        RETURNING
            id,
            name,
            code,
            description,
            is_active,
            created_at,
            updated_at;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (
                name,
                code,
                description,
                is_active,
                department_id
            )
        )

        return cursor.fetchone()

def deactivate_department(
    department_id: int
):

    query = """
        UPDATE departments

        SET
            is_active = FALSE,
            updated_at = CURRENT_TIMESTAMP

        WHERE id = %s

        RETURNING
            id,
            name,
            code,
            is_active;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (department_id,)
        )

        return cursor.fetchone()


def get_department_by_id_cursor(
    cursor,
    department_id: int
):
    query = """
        SELECT
            id,
            name
        FROM departments
        WHERE id = %s
        LIMIT 1
    """

    cursor.execute(
        query,
        (department_id,)
    )

    return cursor.fetchone()


def get_department_by_name_cursor(cursor, name: str):
    cursor.execute(
        """
        SELECT id, name, code, description, is_active,
               created_at, updated_at
        FROM departments
        WHERE TRIM(LOWER(name)) = TRIM(LOWER(%s))
        LIMIT 1
        """,
        (name,)
    )
    return cursor.fetchone()

def list_departments_cursor(
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
            FROM departments
            ORDER BY name ASC
        """

        cursor.execute(query)

    else:

        query = """
            SELECT
                id,
                name,
                description,
                is_active,
                created_at,
                updated_at
            FROM departments
            WHERE is_active = TRUE
            ORDER BY name ASC
        """

        cursor.execute(query)

    return cursor.fetchall()


def update_department_status_cursor(
    cursor,
    department_id: int,
    is_active: bool
):

    query = """
        UPDATE departments

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
            department_id
        )
    )

    return cursor.fetchone()