CREATE TABLE IF NOT EXISTS roles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (name, description) VALUES
    ('Super Admin', 'Full system access'),
    ('HR Admin', 'HR administrator access'),
    ('HR Executive', 'Employee and HR operations access'),
    ('Manager', 'Team management and approval access'),
    ('Employee', 'Employee self-service access')
ON CONFLICT (name) DO NOTHING;