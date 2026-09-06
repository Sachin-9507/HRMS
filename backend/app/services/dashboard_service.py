from app.repositories.dashboard_repository import (
    DashboardRepository,
)


class DashboardService:

    @staticmethod
    def get_user_dashboard(employee_id):

        # -------------------------
        # Today's attendance
        # -------------------------
        attendance_row = (
            DashboardRepository.get_today_attendance(
                employee_id
            )
        )

        attendance = None

        if attendance_row:
            attendance = {
                "attendance_date": attendance_row[0],
                "check_in": attendance_row[1],
                "check_out": attendance_row[2],
                "status": attendance_row[3],
                "working_minutes": attendance_row[4],
                "remarks": attendance_row[5],
            }

        # -------------------------
        # Leave summary
        # -------------------------
        leave_summary_row = (
            DashboardRepository.get_leave_summary(
                employee_id
            )
        )

        leave_summary = {
            "total_allocated": leave_summary_row[0],
            "total_used": leave_summary_row[1],
            "total_remaining": leave_summary_row[2],
        }

        # -------------------------
        # Recent leaves
        # -------------------------
        recent_leave_rows = (
            DashboardRepository.get_recent_leaves(
                employee_id
            )
        )

        recent_leaves = [
            {
                "id": row[0],
                "leave_type_code": row[1],
                "leave_type_name": row[2],
                "start_date": row[3],
                "end_date": row[4],
                "total_days": row[5],
                "status": row[6],
            }
            for row in recent_leave_rows
        ]

        return {
            "attendance": attendance,
            "leave_summary": leave_summary,
            "recent_leaves": recent_leaves,
        }

    @staticmethod
    def get_admin_dashboard():

        # -------------------------
        # Employee statistics
        # -------------------------
        employee_statistics_row = (
            DashboardRepository.get_employee_statistics()
        )

        employee_statistics = {
            "total_employees": employee_statistics_row[0],
            "active_employees": employee_statistics_row[1],
            "inactive_employees": employee_statistics_row[2],
        }

        # -------------------------
        # Attendance statistics
        # -------------------------
        attendance_statistics_row = (
            DashboardRepository.get_attendance_statistics()
        )

        attendance_statistics = {
            "present_today": attendance_statistics_row[0],
            "checked_in_today": attendance_statistics_row[1],
            "checked_out_today": attendance_statistics_row[2],
            "not_checked_in_today": attendance_statistics_row[3],
        }

        # -------------------------
        # Leave statistics
        # -------------------------
        leave_statistics_row = (
            DashboardRepository.get_leave_statistics()
        )

        leave_statistics = {
            "pending": leave_statistics_row[0],
            "approved": leave_statistics_row[1],
            "rejected": leave_statistics_row[2],
            "cancelled": leave_statistics_row[3],
        }

        # -------------------------
        # Recent leave requests
        # -------------------------
        recent_leave_rows = (
            DashboardRepository.get_recent_leave_requests()
        )

        recent_leave_requests = [
            {
                "id": row[0],
                "employee_id": row[1],
                "employee_code": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "leave_type_code": row[5],
                "leave_type_name": row[6],
                "start_date": row[7],
                "end_date": row[8],
                "total_days": row[9],
                "status": row[10],
            }
            for row in recent_leave_rows
        ]

        return {
            "employee_statistics": employee_statistics,
            "attendance_statistics": attendance_statistics,
            "leave_statistics": leave_statistics,
            "recent_leave_requests": recent_leave_requests,
        }