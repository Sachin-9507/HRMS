from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class LeaveApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    leave_type_id: int
    start_date: date
    end_date: date

    reason: str = Field(
        min_length=1,
        max_length=1000
    )


class LeaveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int

    leave_type_id: int
    leave_type_code: str
    leave_type_name: str

    start_date: date
    end_date: date
    total_days: Decimal

    reason: str
    status: str

    admin_remarks: str | None

    reviewed_by: int | None
    reviewed_at: datetime | None

    created_at: datetime
    updated_at: datetime


class LeaveBalanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int

    leave_type_id: int
    leave_type_code: str
    leave_type_name: str

    leave_year: int

    allocated_days: Decimal
    used_days: Decimal
    remaining_days: Decimal

class AdminLeaveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    employee_id: int
    employee_code: str
    first_name: str
    last_name: str

    leave_type_id: int
    leave_type_code: str
    leave_type_name: str

    start_date: date
    end_date: date
    total_days: Decimal

    reason: str
    status: str

    admin_remarks: str | None

    reviewed_by: int | None
    reviewed_at: datetime | None

    created_at: datetime
    updated_at: datetime


class LeaveRejectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    admin_remarks: str = Field(
        min_length=1,
        max_length=1000
    )