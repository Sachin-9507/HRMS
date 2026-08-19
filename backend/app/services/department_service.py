from app.repositories.department_repository import (
    create_department as repository_create_department,
    get_departments as repository_get_departments,
    get_department_by_id as repository_get_department_by_id,
    update_department as repository_update_department,
    deactivate_department as repository_deactivate_department
)


def create_department(
    name: str,
    code: str,
    description: str | None = None
):

    existing_departments = (
        repository_get_departments(
            include_inactive=False
        )
    )

    for department in existing_departments:

        if (
            department[1]
            and department[1].lower() == name.lower()
        ):
            raise ValueError(
                "Department name already exists"
            )

        if (
            department[2]
            and department[2].lower() == code.lower()
        ):
            raise ValueError(
                "Department code already exists"
            )

    return repository_create_department(
        name=name,
        code=code.upper(),
        description=description
    )


def get_departments(
    include_inactive=False
):

    return repository_get_departments(
        include_inactive
    )


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

    return department


def update_department(
    department_id: int,
    data
):

    department = get_department(
        department_id
    )

    return repository_update_department(
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


def deactivate_department(
    department_id: int
):

    department = get_department(
        department_id
    )

    return repository_deactivate_department(
        department_id
    )

