from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user

from app.schemas.me import (
    MyProfileResponse,
    MyProfileUpdateRequest,
    MyEmployeeResponse,
    MyEmployeeUpdateRequest,
)

from app.services.me_service import (
    get_my_profile,
    get_my_employee,
    update_my_email,
)


router = APIRouter(
    prefix="/me",
    tags=["My Profile"]
)


# =========================================================
# GET MY PROFILE
# =========================================================

@router.get(
    "",
    response_model=MyProfileResponse
)
def my_profile(
    current_user=Depends(get_current_user)
):
    try:
        return get_my_profile(
            current_user["id"]
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# =========================================================
# GET MY EMPLOYEE PROFILE
# =========================================================

@router.get(
    "/employee",
    response_model=MyEmployeeResponse
)
def my_employee(
    current_user=Depends(get_current_user)
):
    try:
        return get_my_employee(
            current_user["id"]
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# =========================================================
# UPDATE MY PROFILE
# =========================================================

@router.put(
    "",
    response_model=MyProfileResponse
)
def update_my_profile(
    data: MyProfileUpdateRequest,
    current_user=Depends(get_current_user)
):

    if data.email is None:
        return get_my_profile(
            current_user["id"]
        )

    try:
        return update_my_email(
            current_user["id"],
            data.email
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )