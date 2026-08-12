CREATE TABLE IF NOT EXISTS role_permissions (
    role_id BIGINT NOT NULL,

    permission_id BIGINT NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (role_id, permission_id),

    CONSTRAINT fk_role_permissions_permission
        FOREIGN KEY (permission_id)
         REFERENCES permissions (id)
          ON DELETE CASCADE,

);         