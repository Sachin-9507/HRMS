from app.database.transaction import transaction

from app.repositories.role_repository import (
    get_role_by_id_cursor,
    get_role_by_name_cursor,
    create_role_cursor,
    list_roles_cursor,
    update_role_cursor,
    update_role_status_cursor,
    get_role_permissions_cursor,
    replace_role_permissions_cursor,
    get_existing_permission_ids_cursor
)

def create_role(data):

    name = data.name.strip().upper()

    with transaction() as cursor:

        existing = get_role_by_name_cursor(
            cursor,
            name
        )

        if existing:

            raise ValueError(
                "Role already exists"
            )

        row = create_role_cursor(
            cursor,
            name,
            data.description
        )

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "is_active": row[3],
        "created_at": row[4],
        "updated_at": row[5]
    }

def list_roles(
    include_inactive: bool = False
):

    with transaction() as cursor:

        rows = list_roles_cursor(
            cursor,
            include_inactive
        )

    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "is_active": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        }
        for row in rows
    ]

def get_role(role_id: int):

    with transaction() as cursor:

        row = get_role_by_id_cursor(
            cursor,
            role_id
        )

    if not row:

        raise ValueError(
            "Role not found"
        )

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "is_active": row[3],
        "created_at": row[4],
        "updated_at": row[5]
    }

def update_role(
    role_id: int,
    data
):

    name = data.name.strip().upper()

    with transaction() as cursor:

        role = get_role_by_id_cursor(
            cursor,
            role_id
        )

        if not role:

            raise ValueError(
                "Role not found"
            )

        existing = get_role_by_name_cursor(
            cursor,
            name
        )

        if (
            existing
            and existing[0] != role_id
        ):

            raise ValueError(
                "Role already exists"
            )

        row = update_role_cursor(
            cursor,
            role_id,
            name,
            data.description
        )

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "is_active": row[3],
        "created_at": row[4],
        "updated_at": row[5]
    }

def update_role_status(
    role_id: int,
    is_active: bool
):

    with transaction() as cursor:

        role = get_role_by_id_cursor(
            cursor,
            role_id
        )

        if not role:

            raise ValueError(
                "Role not found"
            )

        if role[1] == "ADMIN" and not is_active:

            raise ValueError(
                "ADMIN role cannot be deactivated"
            )

        row = update_role_status_cursor(
            cursor,
            role_id,
            is_active
        )

    return {
        "id": row[0],
        "name": row[1],
        "is_active": row[2],
        "updated_at": row[3]
    }

def replace_role_permissions(
    role_id: int,
    permission_ids: list[int]
):

    permission_ids = list(
        set(permission_ids)
    )

    with transaction() as cursor:

        role = get_role_by_id_cursor(
            cursor,
            role_id
        )

        if not role:

            raise ValueError(
                "Role not found"
            )

        existing_ids = (
            get_existing_permission_ids_cursor(
                cursor,
                permission_ids
            )
        )

        missing_ids = (
            set(permission_ids)
            - existing_ids
        )

        if missing_ids:

            raise ValueError(
                "One or more permissions do not exist"
            )

        replace_role_permissions_cursor(
            cursor,
            role_id,
            permission_ids
        )

        permissions = (
            get_role_permissions_cursor(
                cursor,
                role_id
            )
        )

    return {
        "role_id": role_id,
        "permissions": [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
            for row in permissions
        ]
    }

def get_role_permissions(
    role_id: int
):

    with transaction() as cursor:

        role = get_role_by_id_cursor(
            cursor,
            role_id
        )

        if not role:

            raise ValueError(
                "Role not found"
            )

        permissions = (
            get_role_permissions_cursor(
                cursor,
                role_id
            )
        )

    return {
        "role_id": role_id,
        "permissions": [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
            for row in permissions
        ]
    }

