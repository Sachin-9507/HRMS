from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.rbac import require_permission

from app.repositories.employee_repository import (
    get_all_employee,
    get_employee_by_id,
    deactivate_employee as repository_deactivate_employee
)

from app.services.employee_service import (
    create_employee_account
)


from app.auth.jwt import (
    get_current_user
)

from app.schemas.employee import (
    EmployeeCreateRequest,
  )



router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)



@router.get(
    "",
    dependencies=[
        Depends(
            require_permission(
                "employee:read"
            )
        )
    ]
)
def list_employee_api(
    search: str | None = None,

    department_id: int | None = None,

    designation_id: int | None = None,

    status: str | None = None,

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=20,
        ge=1,
        le=100
    )
):

    return get_all_employee(
        search=search,
        department_id=department_id,
        designation_id=designation_id,
        status=status,
        page=page,
        page_size=page_size
    )

@router.get(
    "/{employee_id}",
    dependencies=[
        Depends(
            require_permission(
                "employee:read"
            )
        )
    ]
)
def get_employee_api(
    employee_id: int
):

    employee = get_employee_by_id(
        employee_id
    )

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
        "state": employee[11],
        "country": employee[12],
        "postal_code": employee[13],
        "joining_date": employee[14],
        "employment_type": employee[15],
        "department_id": employee[16],
        "department": employee[17],
        "designation_id": employee[18],
        "designation": employee[19],
        "manager_id": employee[20],
        "salary": employee[21],
        "status": employee[22],
        "created_at": employee[25],
        "updated_at": employee[26]
    }


@router.patch(
    "/{employee_id}/deactivate",
    dependencies=[
        Depends(
            require_permission(
                "employee:update"
            )
        )
    ]
)
def deactivate_employee(
    employee_id: int
):

    employee = repository_deactivate_employee(
        employee_id
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deactivated",
        "employee": {
            "id": employee[0],
            "employee_code": employee[1],
            "status": employee[2]
        }
    }


@router.post(
    "",
    dependencies=[
        Depends(
            require_permission(
                "employee:create"
            )
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

    return create_employee_account(
        employee_data
    )


@router.get(
    "/me"
)
def get_my_employee_profile(
    current_user=Depends(
        get_current_user
    )
):

    try:

        user_id = current_user["user_id"]

        employee = (
            get_employee_by_id(
                user_id
            )
        )

        return {
            "employee":
                employee
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


