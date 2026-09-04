from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.leave import AdminLeaveResponse, LeaveRejectRequest
from app.services import leave_service

router = APIRouter(
    prefix="/admin/leaves",
    tags=["Admin Leaves"]
)


@router.get(
    "",
    dependencies=[
        Depends(require_permission("leave:read"))
    ]
)
def get_all_leaves_api(
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    
):
    return leave_service.get_all_leaves(
        status_filter=status_filter
    )

@router.get(
    "/{leave_id}",
    response_model=AdminLeaveResponse,
    dependencies=[
        Depends(
            require_permission(
                "leave:read_all"
            )
        )
    ]
)
def get_leave(
    leave_id: int
):
    return leave_service.get_admin_leave(
        leave_id
    )

@router.post(
    "/{leave_id}/approve",
    response_model=AdminLeaveResponse,
    dependencies=[
        Depends(
            require_permission(
                "leave:approve"
            )
        )
    ]
)
def approve_leave(
    leave_id: int,
    current_user=Depends(
        get_current_user
    )
):
    return leave_service.approve_leave(
        leave_id=leave_id,
        reviewer_id=current_user["user_id"]
    )

@router.post(
    "/{leave_id}/reject",
    response_model=AdminLeaveResponse,
    dependencies=[
        Depends(
            require_permission(
                "leave:reject"
            )
        )
    ]
)
def reject_leave(
    leave_id: int,
    request: LeaveRejectRequest,
    current_user=Depends(
        get_current_user
    )
):
    return leave_service.reject_leave(
        leave_id=leave_id,
        reviewer_id=current_user["user_id"],
        admin_remarks=request.admin_remarks
    )