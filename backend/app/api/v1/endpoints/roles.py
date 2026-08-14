from fastapi import APIRouter, Depends

from app.auth.rbac import require_permission
from app.repositories.role_permission_repository import get_role_permissions


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get(
    "/{role_id}/permissions",
    dependencies=[
        Depends(require_permission("role.read"))
    ]
)
def role_permissions(role_id: int):

    permissions = get_role_permissions(
        role_id=role_id
    )

    return {
        "role_id": role_id,
        "permissions": [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2]
            }
            for row in permissions
        ]
    }