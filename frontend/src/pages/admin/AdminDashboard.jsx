import Layout from "../../components/layout/Layout";
import StatCard from "../../components/dashboard/StatCard";

function AdminDashboard() {
  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Admin Dashboard</h1>
          <p>HRMS administration overview</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Employees"
          value="0"
          description="Registered employees"
        />

        <StatCard
          title="Active Employees"
          value="0"
          description="Currently active"
        />

        <StatCard
          title="Today's Attendance"
          value="0"
          description="Attendance records"
        />

        <StatCard
          title="Pending Leaves"
          value="0"
          description="Awaiting review"
        />

        <StatCard
          title="Approved Leaves"
          value="0"
          description="Approved requests"
        />

        <StatCard
          title="Audit Logs"
          value="0"
          description="Recorded activities"
        />
      </div>

      <section className="dashboard-section">
        <h2>Administration</h2>

        <div className="admin-quick-links">
          <a href="/admin/employees">
            Manage Employees
          </a>

          <a href="/admin/users">
            Manage Users
          </a>

          <a href="/admin/attendance">
            Attendance
          </a>

          <a href="/admin/leaves">
            Leave Requests
          </a>

          <a href="/admin/audit-logs">
            Audit Logs
          </a>
        </div>
      </section>
    </Layout>
  );
}

export default AdminDashboard;