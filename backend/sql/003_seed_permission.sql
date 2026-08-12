INSERT INTO permissions
     (name, resource, action, description)
VALUES
--user
('user:create', 'user', 'create', 'Create user'),
('user:read', 'user', 'read', 'View user '),
('user:update', 'user', 'update', 'Update user '),
('user:delete', 'user', 'delete', 'Delete user '),

--Employee
('employee:create', 'employee', 'create', 'Create employees'),
('employee:read', 'employee', 'read', 'View employees '),
('employee:update', 'employee', 'update', 'Update employees '),
('employee:delete', 'employee', 'delete', 'Delete employee '),

--Attendance
('attendance:create', 'attendance', 'create', 'Create attendance'),
('attendance:read', 'attendance', 'read', 'View attendance '),
('attendance:update', 'attendance', 'update', 'Update attendance '),
('attendance:delete', 'attendance', 'delete', 'Delete attendance ');

--Leave
('leave:create', 'leave', 'create', 'Create leave'),
('leave:read', 'leave', 'read', 'View leave '),
('leave:update', 'leave', 'update', 'Update leave '),
('leave:delete', 'leave', 'delete', 'Delete leave ');
('leave:approve', 'leave', 'approve', 'Approve leave ');
('leave:reject', 'leave', 'reject', 'Reject leave ');

--Payroll
('payroll:create', 'payroll', 'create', 'Create payroll'),
('payroll:read', 'payroll', 'read', 'View payroll '),
('payroll:update', 'payroll', 'update', 'Update payroll '),
('payroll:delete', 'payroll', 'delete', 'Delete payroll ');

--Report
('report:read', 'report', 'read', 'View report '),

--Settings
('settings:read', 'settings', 'read', 'View settings '),
('settings:update', 'settings', 'update', 'Update settings ');

ON CONFLICT (name) DO NOTHING;
