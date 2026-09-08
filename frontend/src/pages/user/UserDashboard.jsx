import { Link } from "react-router-dom";

import Layout from "../../components/layout/Layout";
import StatCard from "../../components/dashboard/StatCard";

function UserDashboard() {
  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>My Dashboard</h1>
          <p>
            Welcome to your HRMS dashboard
          </p>
        </div>
      </div>

      <div className="stats-grid">

        <StatCard
          title="Today's Attendance"
          value="Not Checked"
          description="Today's attendance status"
        />

        <StatCard
          title="Leave Balance"
          value="0"
          description="Available leave days"
        />

        <StatCard
          title="Pending Leaves"
          value="0"
          description="Leave requests awaiting review"
        />

        <StatCard
          title="Approved Leaves"
          value="0"
          description="Approved leave requests"
        />

      </div>

      <section className="dashboard-section">
        <h2>Quick Actions</h2>

        <div className="admin-quick-links">

          <Link to="/user/attendance/today">
            Attendance
          </Link>

          <Link to="/user/attendance/history">
            Attendance History
          </Link>

          <Link to="/user/leaves/apply">
            Apply Leave
          </Link>

          <Link to="/user/leaves/balance">
            Leave Balance
          </Link>

          <Link to="/user/leaves">
            My Leave Requests
          </Link>

          <Link to="/user/profile">
            My Profile
          </Link>

        </div>
      </section>
    </Layout>
  );
}

export default UserDashboard;