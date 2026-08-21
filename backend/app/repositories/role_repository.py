def get_role_by_name_cursor(
    cursor,
    role_name: str
):

    query = """
        SELECT
            id,
            name
        FROM roles
        WHERE name = %s
        LIMIT 1
    """

    cursor.execute(
        query,
        (role_name,)
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