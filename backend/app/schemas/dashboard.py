from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AttendanceDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attendance_date: date
    check_in: datetime | None
    check_out: datetime | None
    status: str
    working_minutes: int
    remarks: str | None


class LeaveSummaryResponse(BaseModel):
    total_allocated: Decimal
    total_used: Decimal
    total_remaining: Decimal


class LeaveDashboardItem(BaseModel):
    id: int
    leave_type_code: str
    leave_type_name: str
    start_date: date
    end_date: date
    total_days: Decimal
    status: str


class UserDashboardResponse(BaseModel):
    attendance: AttendanceDashboardResponse | None
    leave_summary: LeaveSummaryResponse
    recent_leaves: list[LeaveDashboardItem]


class EmployeeStatisticsResponse(BaseModel):
    total_employees: int
    active_employees: int
    inactive_employees: int


class AttendanceStatisticsResponse(BaseModel):
    present_today: int
    checked_in_today: int
    checked_out_today: int
    not_checked_in_today: int


class LeaveStatisticsResponse(BaseModel):
    pending: int
    approved: int
    rejected: int
    cancelled: int


class RecentLeaveRequest(BaseModel):
    id: int
    employee_id: int
    employee_code: str
    first_name: str
    last_name: str
    leave_type_code: str
    leave_type_name: str
    start_date: date
    end_date: date
    total_days: Decimal
    status: str


class AdminDashboardResponse(BaseModel):
    employee_statistics: EmployeeStatisticsResponse
    attendance_statistics: AttendanceStatisticsResponse
    leave_statistics: LeaveStatisticsResponse
    recent_leave_requests: list[RecentLeaveRequest]