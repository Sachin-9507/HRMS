from datetime import date

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.dashboard import (
    AttendanceReportResponse,
    LeaveReportResponse,
)
from app.services.report_service import ReportService


router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"],
)


@router.get(
    "/attendance",
    response_model=list[AttendanceReportResponse],
)
def attendance_report(
    employee_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    status: str | None = None,
    current_user=Depends(get_current_user),
    _=Depends(
        require_permission("reports.attendance")
    ),
):
    return ReportService.attendance_report(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )


@router.get(
    "/leave",
    response_model=list[LeaveReportResponse],
)
def leave_report(
    employee_id: int | None = None,
    leave_type_id: int | None = None,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    current_user=Depends(get_current_user),
    _=Depends(
        require_permission("reports.leave")
    ),
):
    return ReportService.leave_report(
        employee_id=employee_id,
        leave_type_id=leave_type_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )