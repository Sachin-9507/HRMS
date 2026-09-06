from app.repositories.report_repository import (
    ReportRepository,
)


class ReportService:

    @staticmethod
    def attendance_report(
        employee_id=None,
        start_date=None,
        end_date=None,
        status=None,
    ):
        return ReportRepository.attendance_report(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

    @staticmethod
    def leave_report(
        employee_id=None,
        leave_type_id=None,
        status=None,
        start_date=None,
        end_date=None,
    ):
        return ReportRepository.leave_report(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )