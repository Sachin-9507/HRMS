from datetime import datetime

from pydantic import BaseModel, Field


class RoleCreateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class RoleUpdateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class RoleStatusUpdateRequest(BaseModel):

    is_active: bool


class RoleResponse(BaseModel):

    id: int

    name: str

    description: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime

class RolePermissionRequest(BaseModel):

    permission_ids: list[int]

class RolePermissionResponse(BaseModel):

    role_id: int

    permissions: list[dict]