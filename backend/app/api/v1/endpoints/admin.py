from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user

from app.repositories.admin_repository import (
    get_all_users,
    get_user_details,
    set_user_active,
    change_user_role as change_user_role_repository,
)

router = APIRouter(
    tags=["Administration"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/users")
def fetch_all_users():
    users = get_all_users()

    return {
        "message": "Users fetched successfully",
        "users": users,
    }



@router.get("/users/{user_id}")
def get_single_user(user_id: int):
    user = get_user_details(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User details fetched successfully",
        "user": user,
    }



@router.patch("/users/{user_id}/status")
def change_user_status(
    user_id: int,
    status: bool,
):
    result = set_user_active(
        user_id=user_id,
        status=status,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User status updated successfully",
        "user": result,
    }


@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role_id: int,
):
    result = change_user_role_repository(
        user_id=user_id,
        role_id=role_id,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User role updated successfully",
        "user": result,
    }