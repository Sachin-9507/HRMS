from app.database.transaction import transaction

from app.repositories.permission_repository import (
    get_permission_by_id_cursor,
    get_permission_by_name_cursor,
    create_permission_cursor,
    list_permissions_cursor
)

def create_permission(data):

    name = data.name.strip().lower()

    with transaction() as cursor:

        existing = get_permission_by_name_cursor(
            cursor,
            name
        )

        if existing:
            raise ValueError(
                "Permission already exists"
            )

        row = create_permission_cursor(
            cursor,
            name,
            data.resource,
            data.action,
            data.description
        )

    return {
        "id": row[0],
        "name": row[1],
        "resource": row[2],
        "action": row[3],
        "description": row[4],
        "created_at": row[5]
    }


def list_permissions():

    with transaction() as cursor:

        rows = list_permissions_cursor(
            cursor
        )

    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

