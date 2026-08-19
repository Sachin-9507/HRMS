from fastapi import HTTPException

from app.repositories.designation_repository import (
    create_designation as repository_create_designation,
    get_designations as repository_get_designations,
    get_designation_by_id as repository_get_designation_by_id,
    update_designation as repository_update_designation,
    deactivate_designation as repository_deactivate_designation
)

from app.repositories.department_repository import (
    get_department_by_id
)


def create_designation(
    name: str,
    code: str,
    description: str | None = None,
    department_id: int | None = None
):

    # Check department
    if department_id:

        department = get_department_by_id(
            department_id
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    # Check duplicate designation
    existing_designations = (
        repository_get_designations(
            include_inactive=True
        )
    )

    for designation in existing_designations:

        # Check duplicate name
        if designation[1] is not None:

            if designation[1].lower() == name.lower():

                raise HTTPException(
                    status_code=400,
                    detail="Designation name already exists"
                )

        # Check duplicate code
        if designation[2] is not None and code is not None:

            if designation[2].lower() == code.lower():

                raise HTTPException(
                    status_code=400,
                    detail="Designation code already exists"
                )

    # Create designation
    return repository_create_designation(
        name=name,
        code=code,
        description=description,
        department_id=department_id
    )


def get_designations(include_inactive: bool = False):

    return repository_get_designations(
        include_inactive=include_inactive
    )


def get_designation(designation_id: int):

    designation = repository_get_designation_by_id(
        designation_id
    )

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return designation


def update_designation(
    designation_id: int,
    name: str | None = None,
    code: str | None = None,
    description: str | None = None,
    department_id: int | None = None
):

    designation = repository_get_designation_by_id(
        designation_id
    )

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    if department_id:

        department = get_department_by_id(department_id)

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    return repository_update_designation(
        designation_id=designation_id,
        name=name,
        code=code,
        description=description,
        department_id=department_id
    )


def deactivate_designation(designation_id: int):

    designation = repository_get_designation_by_id(
        designation_id
    )

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return repository_deactivate_designation(
        designation_id
    )