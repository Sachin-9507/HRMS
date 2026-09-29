from app.database.connection import get_connection


class AuditQueryRepository:

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
        conn = get_connection()

        try:
            cursor = conn.cursor()

            query = """
                SELECT
                    id,
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
                    error_message,
                    created_at
                FROM audit_logs
                WHERE 1 = 1
            """

            params = []

            if user_id is not None:
                query += """
                    AND user_id = %s
                """
                params.append(user_id)

            if action is not None:
                query += """
                    AND action = %s
                """
                params.append(action)

            if module is not None:
                query += """
                    AND module = %s
                """
                params.append(module)

            if entity_type is not None:
                query += """
                    AND entity_type = %s
                """
                params.append(entity_type)

            if status is not None:
                query += """
                    AND status = %s
                """
                params.append(status)

            if start_date is not None:
                query += """
                    AND created_at >= %s
                """
                params.append(start_date)

            if end_date is not None:
                query += """
                    AND created_at < (%s + INTERVAL '1 day')
                """
                params.append(end_date)

            query += """
                ORDER BY created_at DESC
            """

            cursor.execute(
                query,
                tuple(params),
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "action": row[2],
                    "module": row[3],
                    "entity_type": row[4],
                    "entity_id": row[5],
                    "description": row[6],
                    "old_data": row[7],
                    "new_data": row[8],
                    "ip_address": row[9],
                    "user_agent": row[10],
                    "status": row[11],
                    "error_message": row[12],
                    "created_at": row[13],
                }
                for row in rows
            ]

        finally:
            conn.close()