from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AttendanceResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    employee_id: int

    attendance_date: date

    check_in: datetime | None
    check_out: datetime | None

    status: str

    working_minutes: int

    remarks: str | None

    created_at: datetime
    updated_at: datetime

class AttendanceAdminUpdateRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    check_in: datetime | None = None

    check_out: datetime | None = None

    status: str | None = Field(
        default=None,
        max_length=30
    )

    remarks: str | None = Field(
        default=None,
        max_length=500
    )

   
class AdminAttendanceResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    employee_id: int
    employee_code: str

    first_name: str
    last_name: str

    attendance_date: date

    check_in: datetime | None
    check_out: datetime | None

    status: str

    working_minutes: int

    remarks: str | None

    created_at: datetime
    updated_at: datetime


class AttendanceFilterRequest(BaseModel):

    attendance_date: date | None = None

    employee_id: int | None = None

    status: str | None = None

    limit: int = Field(
        default=50,
        ge=1,
        le=100
    )

    offset: int = Field(
        default=0,
        ge=0
    )