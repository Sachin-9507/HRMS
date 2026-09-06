from app.repositories.audit_query_repository import (
    AuditQueryRepository,
)


class AuditQueryService:

    @staticmethod
    def list_logs(
        user_id=None,
        action=None,
        module=None,
        entity_type=None,
        status=None,
        start_date=None,
        end_date=None,
    ):
        return AuditQueryRepository.list_logs(
            user_id=user_id,
            action=action,
            module=module,
            entity_type=entity_type,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )