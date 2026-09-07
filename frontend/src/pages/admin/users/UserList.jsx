import { Link } from "react-router-dom";

import Layout from "../../../components/layout/Layout";
import Table from "../../../components/common/Table";
import Badge from "../../../components/common/Badge";

function UserList() {
  const users = [];

  const columns = [
    {
      key: "id",
      label: "ID",
    },
    {
      key: "email",
      label: "Email",
    },
    {
      key: "role",
      label: "Role",
    },
    {
      key: "is_active",
      label: "Status",
      render: (row) => (
        <Badge
          status={
            row.is_active
              ? "ACTIVE"
              : "INACTIVE"
          }
        />
      ),
    },
    {
      key: "actions",
      label: "Actions",
      render: (row) => (
        <Link
          to={`/admin/users/${row.id}/edit`}
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
          <h1>Users</h1>
          <p>Manage HRMS user accounts</p>
        </div>

        <Link
          to="/admin/users/create"
          className="btn btn-primary"
        >
          Add User
        </Link>
      </div>

      <Table
        columns={columns}
        data={users}
        emptyMessage="No users found"
      />
    </Layout>
  );
}

export default UserList;