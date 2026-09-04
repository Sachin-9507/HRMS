from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.dashboard import UserDashboardResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/my",
    response_model=UserDashboardResponse,
)
def get_my_dashboard(
    current_user=Depends(get_current_user),
    _=Depends(
        require_permission("dashboard.read_own")
    ),
):
    employee_id = current_user.get("employee_id")

    if not employee_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Employee profile is not linked "
                "to this user"
            ),
        )

    return DashboardService.get_user_dashboard(
        employee_id
    )