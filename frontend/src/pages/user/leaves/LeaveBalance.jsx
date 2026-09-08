import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";

function LeaveBalance() {
  const balances = [];

  const columns = [
    {
      key: "leave_type_code",
      label: "Code",
    },
    {
      key: "leave_type_name",
      label: "Leave Type",
    },
    {
      key: "leave_year",
      label: "Year",
    },
    {
      key: "allocated_days",
      label: "Allocated",
    },
    {
      key: "used_days",
      label: "Used",
    },
    {
      key: "remaining_days",
      label: "Remaining",
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Leave Balance</h1>
          <p>
            View your available leave balance
          </p>
        </div>
      </div>

      <Table
        columns={columns}
        data={balances}
        emptyMessage="No leave balances found"
      />
    </Layout>
  );
}

export default LeaveBalance;