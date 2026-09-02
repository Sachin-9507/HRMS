from datetime import date, datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from app.auth.dependencies import (
    get_current_user
)

from app.auth.rbac import (
    require_permission
)

from app.schemas.attendance import (
    AdminAttendanceResponse,
    
)

from app.services.attendance_service import (
    get_admin_attendance,
    get_admin_attendance_by_id,
    update_admin_attendance
)

router = APIRouter(
    prefix="/admin/attendance",
    tags=["Admin Attendance"]
)

@router.get(
    "",
    response_model=list[
        AdminAttendanceResponse
    ],
    dependencies=[
        Depends(
            require_permission(
                "attendance.read_all"
            )
        )
    ]
)
def admin_attendance_list(
    attendance_date: date | None = Query(
        default=None
    ),

    employee_id: int | None = Query(
        default=None,
        gt=0
    ),

    status: str | None = Query(
        default=None
    ),

    limit: int = Query(
        default=50,
        ge=1,
        le=100
    ),

    offset: int = Query(
        default=0,
        ge=0
    ),

    current_user=Depends(
        get_current_user
    )
):

    return get_admin_attendance(
        attendance_date=attendance_date,
        employee_id=employee_id,
        status=status,
        limit=limit,
        offset=offset
    )

@router.get(
    "/{attendance_id}",
    response_model=AdminAttendanceResponse,
    dependencies=[
        Depends(
            require_permission(
                "attendance.read_all"
            )
        )
    ]
)
def admin_attendance_detail(
    attendance_id: int,
    current_user=Depends(
        get_current_user
    )
):

    try:

        return get_admin_attendance_by_id(
            attendance_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put(
    "/{attendance_id}",
    response_model=AdminAttendanceResponse,
    dependencies=[
        Depends(
            require_permission(
                "attendance.update"
            )
        )
    ]
)
def admin_attendance_update(
    attendance_id: int,

    check_in: datetime | None = Query(
        default=None
    ),

    check_out: datetime | None = Query(
        default=None
    ),

    status: str | None = Query(
        default=None
    ),

    remarks: str | None = Query(
        default=None
    ),

    current_user=Depends(
        get_current_user
    )
):

    try:

        return update_admin_attendance(
            attendance_id=attendance_id,
            check_in=check_in,
            check_out=check_out,
            status=status,
            remarks=remarks
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )