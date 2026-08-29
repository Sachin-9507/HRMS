from fastapi import APIRouter, Depends, HTTPException,Query

from app.auth.rbac import require_permission
from app.repositories.permission_repository import (
    get_role_permissions as repository_get_role_permissions
)

from app.schemas.role import (
    RoleCreateRequest,
    RoleUpdateRequest,
    RoleStatusUpdateRequest,
    RolePermissionRequest
)

from app.services.role_service import (
    create_role,
    list_roles,
    get_role,
    update_role,
    update_role_status,
    replace_role_permissions,
    get_role_permissions
)


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.get(
    "/{role_id}/permissions",
    dependencies=[
        Depends(
            require_permission(
                "role.permission.read"
            )
        )
    ]
)
def get_permissions_for_role(
    role_id: int
):

    try:

        return get_role_permissions(
            role_id=role_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    
@router.post(
    "",
    dependencies=[
        Depends(
            require_permission(
                "role.create"
            )
        )
    ]
)
def create_role_endpoint(
    name: str = Query(...),
    description: str = Query(None)
):

    try:

        data = RoleCreateRequest(
            name=name,
            description=description
        )

        return create_role(data)

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
                "role.read"
            )
        )
    ]
)
def get_roles(
    include_inactive: bool = Query(
        default=False
    )
):

    return list_roles(
        include_inactive
    )

@router.get(
    "/{role_id}",
    dependencies=[
        Depends(
            require_permission(
                "role.read"
            )
        )
    ]
)
def get_role_endpoint(
    role_id: int
):

    try:

        return get_role(role_id)

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.put(
    "/{role_id}",
    dependencies=[
        Depends(
            require_permission(
                "role.update"
            )
        )
    ]
)
def update_role_endpoint(
    role_id: int,
    data: RoleUpdateRequest
):

    try:

        return update_role(
            role_id,
            data
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.patch(
    "/{role_id}/status",
    dependencies=[
        Depends(
            require_permission(
                "role.update"
            )
        )
    ]
)
def change_role_status(
    role_id: int,
    data: RoleStatusUpdateRequest
):

    try:

        return update_role_status(
            role_id,
            data.is_active
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.put(
    "/{role_id}/permissions",
    dependencies=[
        Depends(
            require_permission(
                "role.permission.update"
            )
        )
    ]
)
def update_role_permissions(
    role_id: int,
    permission_ids: list[int] = Query(...)
):

    try:

        return replace_role_permissions(
            role_id,
            permission_ids
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )