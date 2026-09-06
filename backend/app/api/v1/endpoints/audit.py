from datetime import date

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_permission
from app.schemas.audit import AuditLogResponse
from app.services.audit_query_service import (
    AuditQueryService,
)


router = APIRouter(
    prefix="/admin/audit-logs",
    tags=["Admin Audit Logs"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def list_audit_logs(
    user_id: int | None = None,
    action: str | None = None,
    module: str | None = None,
    entity_type: str | None = None,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    current_user=Depends(get_current_user),
    _=Depends(
        require_permission("audit.read_all")
    ),
):
    return AuditQueryService.list_logs(
        user_id=user_id,
        action=action,
        module=module,
        entity_type=entity_type,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )