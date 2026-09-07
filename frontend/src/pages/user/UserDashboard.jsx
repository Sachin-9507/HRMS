import Layout from "../../components/layout/Layout";
import StatCard from "../../components/dashboard/StatCard";

function UserDashboard() {
  return (
    <Layout>
      <div className="page-header">
        <h1>User Dashboard</h1>

        <p>
          Welcome to your HRMS dashboard.
        </p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Attendance"
          value="--"
          description="Current attendance"
        />

        <StatCard
          title="Leave Balance"
          value="--"
          description="Available leave"
        />

        <StatCard
          title="Pending Leaves"
          value="--"
          description="Leave requests"
        />
      </div>

      <div className="dashboard-section">
        <h2>Quick Information</h2>

        <p>
          Attendance, leave balances and leave requests
          will be loaded from the FastAPI backend in
          later parts.
        </p>
      </div>
    </Layout>
  );
}

export default UserDashboard;