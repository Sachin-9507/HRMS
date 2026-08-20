from app.repositories.department_repository import (
    create_department as repository_create_department,
    get_departments as repository_get_departments,
    get_department_by_id as repository_get_department_by_id,
    update_department as repository_update_department,
    deactivate_department as repository_deactivate_department
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


def deactivate_department(
    department_id: int
):

    department = get_department(
        department_id
    )

    deactivated_department = (
        repository_deactivate_department(
            department_id
        )
    )

    if not deactivated_department:
        raise ValueError(
            "Department not found"
        )

    return {
        "id": deactivated_department[0],
        "name": deactivated_department[1],
        "code": deactivated_department[2],
        "is_active": deactivated_department[3]
    }