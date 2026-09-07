import { Link } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function AttendanceList() {
  const attendance = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "employee_code",
      label: "Employee",
    },
    {
      key: "attendance_date",
      label: "Date",
    },
    {
      key: "check_in",
      label: "Check In",
    },
    {
      key: "check_out",
      label: "Check Out",
    },
    {
      key: "working_minutes",
      label: "Minutes",
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
          to={`/admin/attendance/${row.id}/edit`}
          className="table-action"
        >
          Edit
        </Link>
      ),
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Attendance</h1>
          <p>Manage employee attendance</p>
        </div>
      </div>

      <Table
        columns={columns}
        data={attendance}
        emptyMessage="No attendance records found"
      />
    </Layout>
  );
}

export default AttendanceList;