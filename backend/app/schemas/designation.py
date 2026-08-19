from typing import Optional

from pydantic import BaseModel, Field


class DesignationCreateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    code: str = Field(
        min_length=2,
        max_length=50
    )

    description: Optional[str] = None

    department_id: Optional[int] = None


class DesignationUpdateRequest(BaseModel):

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

    department_id: Optional[int] = None

    is_active: Optional[bool] = None