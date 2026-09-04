from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.leave import (
    LeaveApplyRequest,
    LeaveBalanceResponse,
    LeaveResponse
)
from app.services import leave_service


router = APIRouter(
    prefix="/leaves",
    tags=["Leaves"]
)

@router.post(
    "",
    response_model=LeaveResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permission("leave.apply"))
    ]
)
def apply_leave(
    leave_type_id: int = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    reason: str = Query(..., min_length=1, max_length=1000),
    current_user=Depends(get_current_user)
):
    leave_id = leave_service.apply_leave(
        employee_id=current_user["employee_id"],
        leave_type_id=leave_type_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason
    )

    return leave_service.get_my_leave(
        employee_id=current_user["employee_id"],
        leave_id=leave_id
    )

@router.get(
    "/my",
    response_model=list[LeaveResponse],
    dependencies=[
        Depends(require_permission("leave.read_own"))
    ]
)
def get_my_leaves(
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    current_user=Depends(get_current_user)
):
    return leave_service.get_my_leaves(
        employee_id=current_user["employee_id"],
        status_filter=status_filter
    )

@router.get(
    "/my/{leave_id}",
    response_model=LeaveResponse,
    dependencies=[
        Depends(require_permission("leave.read_own"))
    ]
)
def get_my_leave(
    leave_id: int,
    current_user=Depends(get_current_user)
):
    return leave_service.get_my_leave(
        employee_id=current_user["employee_id"],
        leave_id=leave_id
    )

@router.post(
    "/my/{leave_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("leave.cancel_own"))
    ]
)
def cancel_my_leave(
    leave_id: int,
    current_user=Depends(get_current_user)
):
    leave_service.cancel_leave(
        employee_id=current_user["employee_id"],
        leave_id=leave_id
    )

    return None

@router.get(
    "/balances",
    response_model=list[LeaveBalanceResponse],
    dependencies=[
        Depends(require_permission("leave.read_own"))
    ]
)
def get_my_leave_balances(
    year: int | None = None,
    current_user=Depends(get_current_user)
):
    print("CURRENT USER:", current_user)
    print("CURRENT USER KEYS:", current_user.keys())

    leave_year = year or date.today().year

    return leave_service.get_my_balances(
        employee_id=current_user["employee_id"],
        leave_year=leave_year
    )
