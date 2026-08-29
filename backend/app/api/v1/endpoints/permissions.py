from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.rbac import require_permission

from app.schemas.permission import (
    PermissionCreateRequest
)

from app.services.permission_service import (
    create_permission,
    list_permissions
)


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

@router.post(
    "",
    dependencies=[
        Depends(
            require_permission(
                "permission.create"
            )
        )
    ]
)
def create_permission_endpoint(
    data: PermissionCreateRequest
):

    try:

        return create_permission(data)

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get(
    "",
    dependencies=[
        Depends(
            require_permission(
                "permission.read"
            )
        )
    ]
)
def get_permissions():

    return list_permissions()

