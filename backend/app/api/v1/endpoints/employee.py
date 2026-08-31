from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.rbac import require_permission
from app.auth.dependencies import get_current_user

from app.repositories.employee_repository import (
    get_employee_by_id,
    get_employee_by_user_id,
    update_employee_status
)

from app.services.employee_service import (
    create_employee_account,
    list_employees,
    update_employee
)

from app.services.me_service import get_my_employee

from app.schemas.employee import (
    EmployeeCreateRequest,
    EmployeeListResponse,
    EmployeeUpdateRequest
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)



@router.post(
    "",
    dependencies=[
        Depends(
            require_permission("employee:create")
        )
    ]
)
def create_employee(
    employee_code: str,
    first_name: str,
    last_name: str,
    email: str,
    joining_date: str,
    employment_type: str,
    phone: str | None = None,
    date_of_birth: str | None = None,
    gender: str | None = None,
    address: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    postal_code: str | None = None,
    department_id: int | None = None,
    designation_id: int | None = None,
    manager_id: int | None = None,
    salary: float | None = None
):

    employee_data = EmployeeCreateRequest(
        employee_code=employee_code,
        first_name=first_name,
        last_name=last_name,
        email=email,
        joining_date=joining_date,
        employment_type=employment_type,
        phone=phone,
        date_of_birth=date_of_birth,
        gender=gender,
        address=address,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
        department_id=department_id,
        designation_id=designation_id,
        manager_id=manager_id,
        salary=salary
    )

    return create_employee_account(employee_data)


@router.get("/me")
def get_my_employee_profile(
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="User ID not found in token"
            )

        employee = get_my_employee(user_id)

        return employee

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get(
    "/{employee_id}",
    summary="Get Employee Details",
    dependencies=[
        Depends(
            require_permission("employee:read")
        )
    ]
)
def get_employee_details(employee_id: int):

    employee = get_employee_by_id(employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "id": employee[0],
        "employee_code": employee[1],
        "user_id": employee[2],
        "first_name": employee[3],
        "last_name": employee[4],
        "email": employee[5],
        "phone": employee[6],
        "date_of_birth": employee[7],
        "gender": employee[8],
        "address": employee[9],
        "city": employee[10],
        "country": employee[11],
        "postal_code": employee[12],
        "joining_date": employee[13],
        "employment_type": employee[14],
        "department_id": employee[15],
        "department": employee[16],
        "designation_id": employee[17],
        "designation": employee[18],
        "manager_id": employee[19],
        "salary": employee[20],
        "status": employee[21],
        "created_at": employee[22],
        "updated_at": employee[23]
    }




@router.put("/{employee_id}")
def update_employee(
    employee_id: int,

    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    date_of_birth: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    joining_date: Optional[str] = Query(None),
    department_id: Optional[int] = Query(None),
    designation_id: Optional[int] = Query(None),
    manager_id: Optional[int] = Query(None),
    employment_type: Optional[str] = Query(None),

    current_user=Depends(get_current_user)
):

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "joining_date": joining_date,
        "department_id": department_id,
        "designation_id": designation_id,
        "manager_id": manager_id,
        "employment_type": employment_type,
    }

    data = {
        key: value
        for key, value in data.items()
        if value is not None
    }

    if not data:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required for update"
        )

    try:
        updated_employee = update_employee(
            employee_id,
            data
        )

        if not updated_employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "message": "Employee updated successfully",
            "employee_id": employee_id,
            "updated_fields": data
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
   

@router.patch(
    "/{employee_id}/status",
    dependencies=[
        Depends(
            require_permission("employee:update")
        )
    ]
)
def update_employee_status_api(
    employee_id: int,
    status: str = Query(...)
):

    try:

        return update_employee_status(
            employee_id,
            status
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


