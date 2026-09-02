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