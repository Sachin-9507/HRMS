from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.schemas.department import (
    DepartmentUpdateRequest,
    DepartmentStatusUpdateRequest,
    DepartmentResponse
)

from app.services.department_service import (
    create_department as create_department_service,
    list_departments as list_departments_service,
    get_department as get_department_service,
    update_department as update_department_service,
    update_department_status as update_department_status_service
)

from app.auth.rbac import require_permission


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# =========================
# CREATE DEPARTMENT
# =========================

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
        department = create_department_service(
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


# =========================
# LIST DEPARTMENTS
# =========================

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
    departments = list_departments_service(
        include_inactive
    )

    return {
        "departments": departments
    }


# =========================
# GET DEPARTMENT BY ID
# =========================

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
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
        return get_department_service(
            department_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# =========================
# UPDATE DEPARTMENT
# =========================

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
    name: str,
    code: str,
    description: str | None = None,
    is_active: bool = True
):
    try:

        # Create the schema object manually
        data = DepartmentUpdateRequest(
            name=name,
            code=code,
            description=description,
            is_active=is_active
        )

        department = update_department_service(
            department_id,
            data
        )

        return {
            "message": "Department updated successfully",
            "department": department
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# =========================
# DELETE / DEACTIVATE
# =========================

@router.delete(
    "/{department_id}",
    include_in_schema=False,
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

        department = update_department_status_service(
            department_id,
            DepartmentStatusUpdateRequest(
                is_active=False
            )
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


# =========================
# CHANGE STATUS
# =========================

@router.patch(
    "/{department_id}/status",
    dependencies=[
        Depends(
            require_permission("department.update")
        )
    ]
)
def change_department_status(
    department_id: int,
    is_active: bool
):
    try:
        return update_department_status_service(
            department_id,
            is_active
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )