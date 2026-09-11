import { NavLink } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";



function Sidebar() {
  const {
  user,
} = useAuth();

  const isAdmin =
  user?.role_name === "ADMIN";

  const {
  logout,
} = useAuth();

function handleLogout() {
  logout();

  navigate(
    "/login",
    { replace: true }
  );
}
  
  {isAdmin && (
  <div className="sidebar-section">

    <div className="sidebar-section-title">
      Administration
    </div>

    {/* Admin navigation items */}

  </div>
)}

  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        HRMS
      </div>

      <nav className="sidebar-nav">

        <div className="sidebar-section">
          <div className="sidebar-section-title">
            My HRMS
          </div>

          <NavLink
            to="/user/dashboard"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Dashboard
          </NavLink>

          <NavLink
            to="/user/profile"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            My Profile
          </NavLink>

          <NavLink
            to="/user/attendance/today"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Today's Attendance
          </NavLink>

          <NavLink
            to="/user/attendance/history"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Attendance History
          </NavLink>

          <NavLink
            to="/user/leaves/balance"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Leave Balance
          </NavLink>

          <NavLink
            to="/user/leaves"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            My Leaves
          </NavLink>

          <NavLink
            to="/user/leaves/apply"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Apply Leave
          </NavLink>
        </div>

        <div className="sidebar-section">
          <div className="sidebar-section-title">
            Administration
          </div>

          <NavLink
            to="/admin/dashboard"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Admin Dashboard
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
        </div>

      </nav>
    </aside>
  );
}

export default Sidebar;