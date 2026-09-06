from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
    action: str
    module: str
    entity_type: str | None
    entity_id: int | None
    description: str | None
    old_data: dict[str, Any] | None
    new_data: dict[str, Any] | None
    ip_address: str | None
    user_agent: str | None
    status: str
    error_message: str | None
    created_at: datetime