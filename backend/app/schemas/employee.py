from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmployeeCreateRequest(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=100
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=100
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    joining_date: date

    department_id: int

    designation_id: int

    manager_id: Optional[int] = None

    employment_type: str = Field(
        default="FULL_TIME",
        max_length=30
    )


class EmployeeUpdateRequest(BaseModel):

    first_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=100
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20
    )

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    joining_date: Optional[date] = None

    department_id: Optional[int] = None

    designation_id: Optional[int] = None

    manager_id: Optional[int] = None

    employment_type: Optional[str] = Field(
        default=None,
        max_length=30
    )

    status: Optional[str] = Field(
        default=None,
        max_length=30
    )


class EmployeeResponse(BaseModel):

    id: int

    employee_code: str

    user_id: int

    first_name: str

    last_name: Optional[str]

    email: EmailStr

    phone: Optional[str]

    date_of_birth: Optional[date]

    gender: Optional[str]

    joining_date: date

    department_id: Optional[int]

    department_name: Optional[str]

    designation_id: Optional[int]

    designation_name: Optional[str]

    manager_id: Optional[int]

    manager_name: Optional[str]

    employment_type: str

    status: str


class EmployeeCreateRequest(BaseModel):

    first_name: str

    last_name: str | None = None

    email: EmailStr

    phone: str | None = None

    date_of_birth: date | None = None

    gender: str | None = None

    joining_date: date

    department_id: int

    designation_id: int

    manager_id: int | None = None

    employment_type: str