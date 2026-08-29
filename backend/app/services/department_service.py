from fastapi import HTTPException

from app.database.transaction import transaction

from app.repositories.department_repository import (
    create_department as repository_create_department,
    get_departments as repository_get_departments,
    get_department_by_id as repository_get_department_by_id,
    update_department as repository_update_department,
    deactivate_department as repository_deactivate_department,
    list_departments_cursor,
    update_department_status_cursor,
)


def department_to_dict(department):

    if not department:
        return None

    return {
        "id": department[0],
        "name": department[1],
        "code": department[2],
        "description": department[3],
        "is_active": department[4],
        "created_at": department[5],
        "updated_at": department[6]
    }


def create_department(
    name: str,
    code: str,
    description: str | None = None
):

    existing_departments = repository_get_departments(
        include_inactive=True
    )

    for department in existing_departments:

        if (
            department[1]
            and department[1].strip().lower()
            == name.strip().lower()
        ):
            raise ValueError(
                "Department name already exists"
            )

        if (
            department[2]
            and department[2].strip().lower()
            == code.strip().lower()
        ):
            raise ValueError(
                "Department code already exists"
            )

    department = repository_create_department(
        name=name,
        code=code.upper(),
        description=description
    )

    return department_to_dict(department)


def get_departments(
    include_inactive=False
):

    departments = repository_get_departments(
        include_inactive
    )

    return [
        department_to_dict(department)
        for department in departments
    ]


def get_department(
    department_id: int
):

    department = (
        repository_get_department_by_id(
            department_id
        )
    )

    if not department:
        raise ValueError(
            "Department not found"
        )

    return department_to_dict(department)


def update_department(
    department_id: int,
    data
):

    department = get_department(
        department_id
    )

    existing_departments = repository_get_departments(
        include_inactive=True
    )

    for existing in existing_departments:

        # Skip the department currently being updated
        if existing[0] == department_id:
            continue

        if (
            data.name
            and existing[1]
            and existing[1].strip().lower()
            == data.name.strip().lower()
        ):
            raise ValueError(
                "Department name already exists"
            )

        if (
            data.code
            and existing[2]
            and existing[2].strip().lower()
            == data.code.strip().lower()
        ):
            raise ValueError(
                "Department code already exists"
            )

    updated_department = repository_update_department(
        department_id=department_id,
        name=data.name,
        code=(
            data.code.upper()
            if data.code
            else None
        ),
        description=data.description,
        is_active=data.is_active
    )

    return department_to_dict(updated_department)

def update_department_status(
    department_id: int,
    is_active: bool
):

    with transaction() as cursor:

        department = (
            repository_get_department_by_id(
                department_id
            )
        )

        if not department:

            raise ValueError(
                "Department not found"
            )

        row = (
            update_department_status_cursor(
                cursor,
                department_id,
                is_active
            )
        )

    return {
        "id": row[0],
        "name": row[1],
        "is_active": row[2],
        "updated_at": row[3]
    }


def list_departments(
    include_inactive: bool = False
):

    with transaction() as cursor:

        rows = list_departments_cursor(
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