INSERT INTO permissions (name, resource, action, description)
VALUES
    ('user:create', 'user', 'create', 'Create user'),
    ('user:read', 'user', 'read', 'View users'),
    ('user:update', 'user', 'update', 'Update users'),
    ('user:delete', 'user', 'delete', 'Delete users'),

    ('employee:create', 'employee', 'create', 'Create employees'),
    ('employee:read', 'employee', 'read', 'View employees'),
    ('employee:update', 'employee', 'update', 'Update employees'),
    ('employee:delete', 'employee', 'delete', 'Delete employees'),

    ('attendance:create', 'attendance', 'create', 'Create attendance'),
    ('attendance:read', 'attendance', 'read', 'View attendance'),
    ('attendance:update', 'attendance', 'update', 'Update attendance'),
    ('attendance:delete', 'attendance', 'delete', 'Delete attendance'),

    ('leave:create', 'leave', 'create', 'Create leave'),
    ('leave:apply', 'leave', 'apply', 'Apply for leave'),
    ('leave:read', 'leave', 'read', 'View leave'),
    ('leave:read_own', 'leave', 'read_own', 'View own leave'),
    ('leave:update', 'leave', 'update', 'Update leave'),
    ('leave:delete', 'leave', 'delete', 'Delete leave'),
    ('leave:approve', 'leave', 'approve', 'Approve leave'),
    ('leave:reject', 'leave', 'reject', 'Reject leave'),

    ('payroll:create', 'payroll', 'create', 'Create payroll'),
    ('payroll:read', 'payroll', 'read', 'View payroll'),
    ('payroll:update', 'payroll', 'update', 'Update payroll'),
    ('payroll:delete', 'payroll', 'delete', 'Delete payroll'),

    ('report:read', 'report', 'read', 'View reports'),
    ('settings:read', 'settings', 'read', 'View settings'),
    ('settings:update', 'settings', 'update', 'Update settings'),

    ('role:read', 'role', 'read', 'View roles'),
    ('role:create', 'role', 'create', 'Create roles'),
    ('role:update', 'role', 'update', 'Update roles'),
    ('role:delete', 'role', 'delete', 'Delete roles'),
    ('role.permission.read', 'role', 'permission.read', 'View role permissions'),
    ('role.permission.update', 'role', 'permission.update', 'Update role permissions')
ON CONFLICT (name) DO NOTHING;