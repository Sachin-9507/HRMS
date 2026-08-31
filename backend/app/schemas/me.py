from datetime import datetime

from pydantic import BaseModel, Field


class MyProfileResponse(BaseModel):

    user_id: int
    email: str
    role_id: int
    role_name: str
    is_active: bool


class MyProfileUpdateRequest(BaseModel):

    email: str | None = Field(
        default=None,
        min_length=5,
        max_length=255
    )


class MyEmployeeResponse(BaseModel):

    employee_id: int
    employee_code: str

    first_name: str
    last_name: str

    email: str | None
    phone: str | None

    department_id: int | None
    department_name: str | None

    designation_id: int | None
    designation_name: str | None

    is_active: bool

    created_at: datetime
    updated_at: datetime