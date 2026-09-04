from app.repositories.dashboard_repository import (
    DashboardRepository,
)


class DashboardService:

    @staticmethod
    def get_user_dashboard(employee_id):

        attendance = (
            DashboardRepository.get_today_attendance(
                employee_id
            )
        )

        leave_summary = (
            DashboardRepository.get_leave_summary(
                employee_id
            )
        )

        recent_leaves = (
            DashboardRepository.get_recent_leaves(
                employee_id
            )
        )

        return {
            "attendance": attendance,
            "leave_summary": leave_summary,
            "recent_leaves": recent_leaves,
        }

    @staticmethod
    def get_admin_dashboard():

        employee_statistics = (
            DashboardRepository.get_employee_statistics()
        )

        attendance_statistics = (
            DashboardRepository.get_attendance_statistics()
        )

        leave_statistics = (
            DashboardRepository.get_leave_statistics()
        )

        recent_leave_requests = (
            DashboardRepository.get_recent_leave_requests()
        )

        return {
            "employee_statistics": employee_statistics,
            "attendance_statistics": attendance_statistics,
            "leave_statistics": leave_statistics,
            "recent_leave_requests": recent_leave_requests,
        }