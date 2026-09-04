from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.dashboard import AdminDashboardResponse
from app.services.dashboard_service import (
    DashboardService,
)


router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin Dashboard"],
)


@router.get(
    "",
    response_model=AdminDashboardResponse,
)
def get_admin_dashboard(
    current_user=Depends(get_current_user),
    _=Depends(
        require_permission("dashboard.read_all")
    ),
):
    return DashboardService.get_admin_dashboard()