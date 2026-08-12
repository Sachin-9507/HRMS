CREATE TABLE IF NOT EXISTS ROLES (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255) ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO ROLES (name, description) VALUES
('Super Admin', ' full System access'),
('HR Admin', 'HR administrator  access '),
('HR Executive', 'Employee and HR Operations access'),
('Manager', 'Team management and approval access'),
('Employee', 'Employee self-service access');
ON CONFLICT (name) DO NOTHING;
