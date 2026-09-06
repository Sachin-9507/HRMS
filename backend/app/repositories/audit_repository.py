from app.database.connection import get_connection


class AuditRepository:

    @staticmethod
    def create(
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
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO audit_logs (
                    user_id,
                    action,
                    module,
                    entity_type,
                    entity_id,
                    description,
                    old_data,
                    new_data,
                    ip_address,
                    user_agent,
                    status,
                    error_message
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s::jsonb,
                    %s::jsonb,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id
                """,
                (
                    user_id,
                    action,
                    module,
                    entity_type,
                    entity_id,
                    description,
                    (
                        None
                        if old_data is None
                        else __import__("json").dumps(old_data)
                    ),
                    (
                        None
                        if new_data is None
                        else __import__("json").dumps(new_data)
                    ),
                    ip_address,
                    user_agent,
                    status,
                    error_message,
                ),
            )

            audit_id = cursor.fetchone()[0]

            conn.commit()

            return audit_id

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

import json


class AuditRepository:

    @staticmethod
    def create_with_cursor(
        cursor,
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
        cursor.execute(
            """
            INSERT INTO audit_logs (
                user_id,
                action,
                module,
                entity_type,
                entity_id,
                description,
                old_data,
                new_data,
                ip_address,
                user_agent,
                status,
                error_message
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s::jsonb,
                %s::jsonb,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING id
            """,
            (
                user_id,
                action,
                module,
                entity_type,
                entity_id,
                description,
                None if old_data is None else json.dumps(old_data),
                None if new_data is None else json.dumps(new_data),
                ip_address,
                user_agent,
                status,
                error_message,
            ),
        )

        return cursor.fetchone()[0]