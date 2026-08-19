from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.schemas.department import (
    DepartmentCreateRequest,
    DepartmentUpdateRequest
)

from app.services import department_service

from app.auth.rbac import (
    require_permission
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    dependencies=[
        Depends(
            require_permission("department.create")
        )
    ]
)
def create_department(
    name: str,
    code: str,
    description: str | None = None
):
    try:
        department = department_service.create_department(
            name=name,
            code=code,
            description=description
        )

        return {
            "message": "Department created successfully",
            "department": department
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "",
    dependencies=[
        Depends(
            require_permission("department.read")
        )
    ]
)
def list_departments(
    include_inactive: bool = False
):
    departments = department_service.get_departments(
        include_inactive
    )

    return {
        "departments": departments
    }


@router.get(
    "/{department_id}",
    dependencies=[
        Depends(
            require_permission("department.read")
        )
    ]
)
def get_department_by_id(
    department_id: int
):
    try:
        department = department_service.get_department(
            department_id
        )

        return {
            "department": department
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put(
    "/{department_id}",
    dependencies=[
        Depends(
            require_permission("department.update")
        )
    ]
)
def update_department_by_id(
    department_id: int,
    data: DepartmentUpdateRequest
):
    try:
        department = department_service.update_department(
            department_id,
            data
        )

        return {
            "message": "Department updated successfully",
            "department": department
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.delete(
    "/{department_id}",
    dependencies=[
        Depends(
            require_permission("department.delete")
        )
    ]
)
def delete_department(
    department_id: int
):
    try:
        department = department_service.deactivate_department(
            department_id
        )

        return {
            "message": "Department deactivated successfully",
            "department": department
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )