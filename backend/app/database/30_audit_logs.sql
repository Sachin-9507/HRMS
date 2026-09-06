CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT,

    action VARCHAR(100) NOT NULL,

    module VARCHAR(100) NOT NULL,

    entity_type VARCHAR(100),

    entity_id BIGINT,

    description VARCHAR(1000),

    old_data JSONB,

    new_data JSONB,

    ip_address INET,

    user_agent VARCHAR(1000),

    status VARCHAR(30) NOT NULL DEFAULT 'SUCCESS',

    error_message VARCHAR(1000),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_log_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_audit_log_status
        CHECK (
            status IN ('SUCCESS', 'FAILED')
        )
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user
ON audit_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action
ON audit_logs(action);

CREATE INDEX IF NOT EXISTS idx_audit_logs_module
ON audit_logs(module);

CREATE INDEX IF NOT EXISTS idx_audit_logs_entity
ON audit_logs(entity_type, entity_id);

CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at
ON audit_logs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_audit_logs_status
ON audit_logs(status);