import { Link } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function EmployeeList() {
  const employees = [];

  const columns = [
    {
      key: "employee_code",
      label: "Employee Code",
    },
    {
      key: "first_name",
      label: "First Name",
    },
    {
      key: "last_name",
      label: "Last Name",
    },
    {
      key: "email",
      label: "Email",
    },
    {
      key: "department",
      label: "Department",
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
          to={`/admin/employees/${row.id}/edit`}
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
          <h1>Employees</h1>
          <p>Manage HRMS employees</p>
        </div>

        <Link
          to="/admin/employees/create"
          className="btn btn-primary"
        >
          Add Employee
        </Link>
      </div>

      <Table
        columns={columns}
        data={employees}
        emptyMessage="No employees found"
      />
    </Layout>
  );
}

export default EmployeeList;