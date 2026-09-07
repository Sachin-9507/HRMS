import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        Admin Panel
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/admin/dashboard"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/admin/employees"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Employees
        </NavLink>

        <NavLink
          to="/admin/users"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Users
        </NavLink>

        <NavLink
          to="/admin/roles"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Roles
        </NavLink>

        <NavLink
          to="/admin/permissions"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Permissions
        </NavLink>

        <NavLink
          to="/admin/attendance"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Attendance
        </NavLink>

        <NavLink
          to="/admin/leaves"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Leave Management
        </NavLink>

        <NavLink
          to="/admin/audit-logs"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Audit Logs
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;