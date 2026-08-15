from fastapi import APIRouter, Depends, HTTPException

from app.auth.rbac import require_permission

from app.repositories.employee_repository import (
    get_all_employee,
    get_employee_by_id,
    deactivate_employee
)

from app.services.employee_service import (
    create_new_employee
)


router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

@router.get(
    "",
    dependencies=[
        Depends(
            require_permission(
                "employee.read"
            )
        )
    ]
)
def list_employee():

    employees = get_all_employee()

    result = []

    for employee in employees:

        result.append({
            "id": employee[0],
            "employee_code": employee[1],
            "user_id": employee[2],
            "first_name": employee[3],
            "last_name": employee[4],
            "email": employee[5],
            "phone": employee[6],
            "joining_date": employee[7],
            "employment_type": employee[8],
            "department": employee[9],
            "designation": employee[10],
            "manager_id": employee[11],
            "salary": employee[12],
            "employment_status": employee[13],
            "created_at": employee[14]
        })

    return {
        "employee": result
    } 

@router.get(
    "/{employee_id}",
    dependencies=[
        Depends(
            require_permission(
                "employee.read"
            )
        )
    ]
)
def get_employee(
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
        "employment_status": employee[22],
        "emergency_contact_name": employee[23],
        "emergency_contact_phone": employee[24],
        "created_at": employee[25],
        "updated_at": employee[26]
    }

@router.patch(
    "/{employee_id}/deactivate",
    dependencies=[
        Depends(
            require_permission(
                "employee.update"
            )
        )
    ]
)
def deactivate_employee_api(
    employee_id: int
):

    employee = deactivate_employee(
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
            "employment_status": employee[2]
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
def create_employee_api(
    employee_code: str,
    first_name: str,
    last_name: str,
    email: str,
    joining_date: str,
    employment_type: str,
    phone: str | None = None,
    department_id: int | None = None,
    designation_id: int | None = None,
    manager_id: int | None = None,
    salary: float | None = None
):

    employee = create_new_employee(
        employee_code=employee_code,
        user_id=None,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        date_of_birth=None,
        gender=None,
        address=None,
        city=None,
        state=None,
        country=None,
        postal_code=None,
        joining_date=joining_date,
        employment_type=employment_type.upper(),
        department_id=department_id,
        designation_id=designation_id,
        manager_id=manager_id,
        salary=salary,
        emergency_contact_name=None,
        emergency_contact_phone=None
    )

    return { 
        "message": "Employee created successfully",
        "employee": employee
    }