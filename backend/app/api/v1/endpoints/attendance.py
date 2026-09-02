from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.schemas.attendance import (
    AttendanceResponse
)

from app.services.attendance_service import (
    check_in,
    check_out,
    get_my_attendance,
    get_today_attendance
)



from app.auth.dependencies import (
    get_current_user
)

from app.auth.rbac import (
    require_permission
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.post(
    "/check-in",
    response_model=AttendanceResponse,
    dependencies=[
        Depends(
            require_permission(
                "attendance:check_in"
            )
        )
    ]
)
def attendance_check_in(
    current_user=Depends(
        get_current_user
    )
):

    try:

        return check_in(
            current_user["id"]
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post(
    "/check-out",
    response_model=AttendanceResponse,
    dependencies=[
        Depends(
            require_permission(
                "attendance:check_out"
            )
        )
    ]
)
def attendance_check_out(
    current_user=Depends(
        get_current_user
    )
):

    try:

        return check_out(
            current_user["id"]
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get(
    "/today",
    response_model=AttendanceResponse | None,
    dependencies=[
        Depends(
            require_permission(
                "attendance:read"
            )
        )
    ]
)
def attendance_today(
    current_user=Depends(
        get_current_user
    )
):

    return get_today_attendance(
        current_user["id"]
    )

@router.get(
    "/my",
    response_model=list[AttendanceResponse],
    dependencies=[
        Depends(
            require_permission(
                "attendance:read"
            )
        )
    ]
)
def my_attendance(
    limit: int = 30,
    offset: int = 0,
    current_user=Depends(
        get_current_user
    )
):

    if limit > 100:
        limit = 100

    return get_my_attendance(
        current_user["id"],
        limit,
        offset
    )