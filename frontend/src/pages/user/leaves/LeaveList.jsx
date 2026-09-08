import { Link } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function LeaveList() {
  const leaves = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "leave_type_name",
      label: "Leave Type",
    },
    {
      key: "start_date",
      label: "Start Date",
    },
    {
      key: "end_date",
      label: "End Date",
    },
    {
      key: "total_days",
      label: "Days",
    },
    {
      key: "status",
      label: "Status",
      render: (row) => (
        <Badge status={row.status} />
      ),
    },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <Link
          to={`/user/leaves/${row.id}`}
          className="table-action"
        >
          View
        </Link>
      ),
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>My Leave Requests</h1>
          <p>
            View your leave applications
          </p>
        </div>

        <Link
          to="/user/leaves/apply"
          className="btn btn-primary"
        >
          Apply Leave
        </Link>
      </div>

      <Table
        columns={columns}
        data={leaves}
        emptyMessage="No leave requests found"
      />
    </Layout>
  );
}

export default LeaveList;