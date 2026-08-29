from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DepartmentCreateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    code: str = Field(
        min_length=2,
        max_length=50
    )

    description: Optional[str] = None


class DepartmentUpdateRequest(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None

class DepartmentStatusUpdateRequest(BaseModel):

    is_active: bool


class DepartmentResponse(BaseModel):

    id: int

    name: str

    description: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime