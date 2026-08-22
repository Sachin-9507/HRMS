from app.database.db import get_cursor


def create_designation(
    name: str,
    code: str,
    description: str | None,
    department_id: int | None
):

    query = """
        INSERT INTO designations (
            name,
            code,
            description,
            department_id
        )
        VALUES (
            %s,
            %s,
            %s,
            %s
        )
        RETURNING
            id,
            name,
            code,
            description,
            department_id,
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
                department_id
            )
        )

        return cursor.fetchone()

def get_designations(
    department_id=None,
    include_inactive=False
):

    query = """
        SELECT
            d.id,
            d.name,
            d.code,
            d.description,
            d.department_id,
            dp.name AS department_name,
            d.is_active,
            d.created_at,
            d.updated_at
        FROM designations d

        LEFT JOIN departments dp
            ON dp.id = d.department_id

        WHERE 1 = 1
    """

    params = []

    if department_id is not None:

        query += """
            AND d.department_id = %s
        """

        params.append(
            department_id
        )

    if not include_inactive:

        query += """
            AND d.is_active = TRUE
        """

    query += """
        ORDER BY d.name ASC;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            tuple(params)
        )

        return cursor.fetchall()

def get_designation_by_id(
    designation_id: int
):

    query = """
        SELECT
            d.id,
            d.name,
            d.code,
            d.description,
            d.department_id,
            dp.name AS department_name,
            d.is_active,
            d.created_at,
            d.updated_at
        FROM designations d

        LEFT JOIN departments dp
            ON dp.id = d.department_id

        WHERE d.id = %s;
    """

    with get_cursor() as cursor:

        cursor.execute(
            query,
            (designation_id,)
        )

        return cursor.fetchone()

def update_designation(
    designation_id: int,
    name,
    code,
    description,
    department_id,
    is_active
):

    query = """
        UPDATE designations

        SET
            name = COALESCE(%s, name),
            code = COALESCE(%s, code),
            description = COALESCE(
                %s,
                description
            ),
            department_id = COALESCE(
                %s,
                department_id
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
            department_id,
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
                department_id,
                is_active,
                designation_id
            )
        )

        return cursor.fetchone()

def deactivate_designation(
    designation_id: int
):

    query = """
        UPDATE designations

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
            (designation_id,)
        )

        return cursor.fetchone()

def get_designation_by_id_cursor(
    cursor,
    designation_id: int
):
    query = """
        SELECT
            id,
            name
        FROM designations
        WHERE id = %s
        LIMIT 1
    """

    cursor.execute(
        query,
        (designation_id,)
    )

    return cursor.fetchone()