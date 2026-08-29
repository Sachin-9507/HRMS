from datetime import datetime

from pydantic import BaseModel, Field


class PermissionCreateRequest(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class PermissionResponse(BaseModel):

    id: int

    name: str

    created_at: datetime