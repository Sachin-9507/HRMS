from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.repositories.rbac_repository import (
    get_user_permissions
)


def require_permission(permission: str):

    def permission_checker(
        current_user=Depends(
            get_current_user
        )
    ):

        user_id = int(
            current_user["id"]
        )

        permissions = get_user_permissions(
            user_id
        )

        if permission not in permissions:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return permission_checker