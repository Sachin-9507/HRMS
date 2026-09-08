import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function AttendanceHistory() {
  const attendance = [];

  const columns = [
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
      label: "Working Minutes",
    },
    {
      key: "status",
      label: "Status",
      render: (row) => (
        <Badge status={row.status} />
      ),
    },
    {
      key: "remarks",
      label: "Remarks",
    },
  ];

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>Attendance History</h1>
          <p>
            View your previous attendance records
          </p>
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

export default AttendanceHistory;