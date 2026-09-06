import logging

from app.repositories.audit_repository import (
    AuditRepository,
)


logger = logging.getLogger(__name__)


class AuditService:

    @staticmethod
    def log(
        user_id=None,
        action=None,
        module=None,
        entity_type=None,
        entity_id=None,
        description=None,
        old_data=None,
        new_data=None,
        ip_address=None,
        user_agent=None,
        status="SUCCESS",
        error_message=None,
    ):
        try:
            return AuditRepository.create(
                user_id=user_id,
                action=action,
                module=module,
                entity_type=entity_type,
                entity_id=entity_id,
                description=description,
                old_data=old_data,
                new_data=new_data,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                error_message=error_message,
            )

        except Exception:
            logger.exception(
                "Failed to create audit log"
            )

            return None